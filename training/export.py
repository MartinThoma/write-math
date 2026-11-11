"""Export a trained SymbolNet for docs/js/nn.js.

* folds BatchNorm into the preceding convolution,
* stores all weights as little-endian float16 in model/weights-<hash>.bin,
* writes model/model.json (layer list, labels, test metrics of the exported,
  float16-rounded model),
* writes tests/fixtures.json with Python reference bitmaps and logits for the
  JS parity test.
"""

import argparse
import hashlib
import json
from pathlib import Path

import numpy as np
import torch
from torch import nn

from model import SymbolNet
from raster import SIZE, rasterize
from symbols import describe

ROOT = Path(__file__).resolve().parent.parent


def fold(conv, bn):
    w = conv.weight.detach().double()
    b = conv.bias.detach().double() if conv.bias is not None else torch.zeros(w.shape[0], dtype=torch.float64)
    scale = bn.weight.double() / torch.sqrt(bn.running_var.double() + bn.eps)
    w = w * scale[:, None, None, None]
    b = (b - bn.running_mean.double()) * scale + bn.bias.double()
    return w.float(), b.float()


def to_layers(model):
    """Return [(spec, weight, bias)] in inference order."""
    out = []
    mods = list(model.features)
    i = 0
    while i < len(mods):
        m = mods[i]
        if isinstance(m, nn.Conv2d):
            w, b = fold(m, mods[i + 1])
            assert isinstance(mods[i + 2], nn.ReLU)
            out.append(({"type": "conv", "in": m.in_channels, "out": m.out_channels,
                         "kernel": m.kernel_size[0], "relu": True}, w, b))
            i += 3
        elif isinstance(m, nn.MaxPool2d):
            out.append(({"type": "maxpool"}, None, None))
            i += 1
        else:
            raise TypeError(m)
    linears = [m for m in model.classifier if isinstance(m, nn.Linear)]
    for k, m in enumerate(linears):
        out.append(({"type": "dense", "in": m.in_features, "out": m.out_features,
                     "relu": k < len(linears) - 1}, m.weight.detach(), m.bias.detach()))
    return out


def fp16_round(t):
    return t.detach().half().float()


def reference_forward(layers, x):
    """Plain torch forward of the exported (folded, fp16-rounded) layers."""
    x = torch.as_tensor(x, dtype=torch.float32).reshape(-1, 1, SIZE, SIZE)
    for spec, w, b in layers:
        if spec["type"] == "conv":
            x = torch.nn.functional.conv2d(x, w, b, padding=spec["kernel"] // 2)
        elif spec["type"] == "maxpool":
            x = torch.nn.functional.max_pool2d(x, 2)
        elif spec["type"] == "dense":
            x = torch.nn.functional.linear(x.flatten(1), w, b)
        if spec.get("relu"):
            x = torch.relu(x)
    return x


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", type=Path, default=Path(__file__).parent / "data")
    parser.add_argument("--out", type=Path, default=ROOT / "docs" / "model")
    parser.add_argument("--fixtures-out", type=Path, default=ROOT / "tests" / "fixtures.json")
    parser.add_argument("--fixtures", type=int, default=20, help="number of parity fixtures to write")
    args = parser.parse_args()

    ckpt = torch.load(args.data / "model.pt", weights_only=False)
    cfg = ckpt["config"]
    model = SymbolNet(cfg["n_classes"], tuple(cfg["widths"]), cfg["hidden"], cfg["dropout"])
    model.load_state_dict(ckpt["state_dict"])
    model.eval()

    layers = [(s, w if w is None else fp16_round(w), b if b is None else fp16_round(b))
              for s, w, b in to_layers(model)]

    # Serialize.
    chunks, offset, specs = [], 0, []
    for spec, w, b in layers:
        spec = dict(spec)
        for name, t in (("weight", w), ("bias", b)):
            if t is None:
                continue
            arr = t.numpy().astype("<f2").ravel()
            spec[name] = {"offset": offset, "length": int(arr.size)}
            offset += arr.size
            chunks.append(arr.tobytes())
        specs.append(spec)
    blob = b"".join(chunks)
    digest = hashlib.sha256(blob).hexdigest()[:12]

    # Evaluate exactly what ships.
    d = np.load(args.data / "hwrt32.npz")
    X_test, y_test = d["X_test"], d["y_test"].astype(np.int64)
    top1 = top3 = 0
    with torch.no_grad():
        for i in range(0, len(X_test), 2048):
            logits = reference_forward(layers, X_test[i:i + 2048].astype(np.float32) / 255)
            t3 = logits.topk(3, 1).indices.numpy()
            yb = y_test[i:i + 2048]
            top1 += int((t3[:, 0] == yb).sum())
            top3 += int((t3 == yb[:, None]).any(1).sum())
    metrics = {"top1": top1 / len(X_test), "top3": top3 / len(X_test), "test_samples": len(X_test)}
    print(f"exported model: test top1 {metrics['top1']:.4f} top3 {metrics['top3']:.4f}")

    args.out.mkdir(parents=True, exist_ok=True)
    for old in args.out.glob("weights-*.bin"):
        old.unlink()
    weights_name = f"weights-{digest}.bin"
    (args.out / weights_name).write_bytes(blob)
    spec = {
        "format": 1,
        "input": [1, SIZE, SIZE],
        "dtype": "float16",
        "weights": weights_name,
        "layers": specs,
        "metrics": metrics,
        "labels": [describe(str(l)) for l in ckpt["labels"]],
    }
    (args.out / "model.json").write_text(json.dumps(spec, ensure_ascii=False, separators=(",", ":")))
    print(f"wrote {args.out / 'model.json'} and {weights_name} ({len(blob):,} bytes)")

    # Parity fixtures for tests/parity.mjs.
    fixtures = json.loads((args.data / "fixtures.json").read_text())[:args.fixtures]
    for fx in fixtures:
        img = rasterize([[(p["x"], p["y"]) for p in s] for s in fx["strokes"]])
        with torch.no_grad():
            logits = reference_forward(layers, img)[0]
        fx["image"] = [round(float(v), 5) for v in img.ravel()]
        fx["logits"] = [round(float(v), 5) for v in logits]
    args.fixtures_out.parent.mkdir(parents=True, exist_ok=True)
    args.fixtures_out.write_text(json.dumps(fixtures))
    print(f"wrote {args.fixtures_out} ({len(fixtures)} fixtures)")


if __name__ == "__main__":
    main()
