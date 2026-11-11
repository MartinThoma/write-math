"""Train SymbolNet on the rasterized HWRT data produced by prepare.py."""

import argparse
import json
import math
import time
from pathlib import Path

import numpy as np
import torch
import torch.nn.functional as F

from model import SymbolNet


def augment(x, strength=1.0):
    """Random affine distortion (rotation, anisotropic scale, shear, shift)."""
    n = x.shape[0]
    rot = (torch.rand(n) * 2 - 1) * math.radians(10) * strength
    sx = 1 + (torch.rand(n) * 2 - 1) * 0.12 * strength
    sy = 1 + (torch.rand(n) * 2 - 1) * 0.12 * strength
    sh = (torch.rand(n) * 2 - 1) * 0.15 * strength
    tx = (torch.rand(n) * 2 - 1) * 0.05 * strength
    ty = (torch.rand(n) * 2 - 1) * 0.05 * strength
    c, s = torch.cos(rot), torch.sin(rot)
    # inverse mapping output->input; scale >1 here shrinks the symbol
    theta = torch.stack([
        torch.stack([c * sx, -s * sx + sh, tx], 1),
        torch.stack([s * sy, c * sy, ty], 1),
    ], 1)
    grid = F.affine_grid(theta, x.shape, align_corners=False)
    return F.grid_sample(x, grid, mode="bilinear", padding_mode="zeros", align_corners=False)


@torch.no_grad()
def evaluate(model, X, y, batch=2048):
    model.eval()
    top1 = top3 = 0
    for i in range(0, len(X), batch):
        xb = torch.from_numpy(X[i:i + batch]).float().unsqueeze(1) / 255
        logits = model(xb)
        t3 = logits.topk(3, 1).indices
        yb = torch.from_numpy(y[i:i + batch].astype(np.int64))
        top1 += (t3[:, 0] == yb).sum().item()
        top3 += (t3 == yb[:, None]).any(1).sum().item()
    return top1 / len(X), top3 / len(X)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", type=Path, default=Path(__file__).parent / "data")
    parser.add_argument("--epochs", type=int, default=20)
    parser.add_argument("--batch", type=int, default=256)
    parser.add_argument("--lr", type=float, default=3e-3)
    parser.add_argument("--val-fraction", type=float, default=0.03)
    parser.add_argument("--threads", type=int, default=None)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--widths", type=int, nargs=3, default=[32, 64, 128])
    parser.add_argument("--limit", type=int, default=None, help="use only N training samples (smoke tests)")
    args = parser.parse_args()

    if args.threads:
        torch.set_num_threads(args.threads)
    torch.manual_seed(args.seed)
    rng = np.random.default_rng(args.seed)

    d = np.load(args.data / "hwrt32.npz")
    X, y, labels = d["X_train"], d["y_train"], d["labels"]
    X_test, y_test = d["X_test"], d["y_test"]
    perm = rng.permutation(len(X))
    n_val = int(len(X) * args.val_fraction)
    val_idx, tr_idx = perm[:n_val], perm[n_val:][:args.limit]
    X_val, y_val = X[val_idx], y[val_idx]
    X_tr = torch.from_numpy(X[tr_idx])
    y_tr = torch.from_numpy(y[tr_idx].astype(np.int64))
    print(f"train {len(X_tr)}, val {n_val}, test {len(X_test)}, classes {len(labels)}")

    model = SymbolNet(len(labels), tuple(args.widths))
    print(f"parameters: {sum(p.numel() for p in model.parameters()):,}")
    opt = torch.optim.AdamW(model.parameters(), lr=args.lr, weight_decay=5e-4)
    steps = args.epochs * math.ceil(len(X_tr) / args.batch)
    sched = torch.optim.lr_scheduler.OneCycleLR(opt, max_lr=args.lr, total_steps=steps, pct_start=0.15)

    for epoch in range(args.epochs):
        model.train()
        t0 = time.time()
        order = torch.randperm(len(X_tr))
        total = 0.0
        # Fade augmentation out over the last epochs so the model also sees clean data.
        strength = 1.0 if epoch < args.epochs - 2 else 0.4
        for i in range(0, len(order), args.batch):
            idx = order[i:i + args.batch]
            xb = augment(X_tr[idx].float().unsqueeze(1) / 255, strength)
            loss = F.cross_entropy(model(xb), y_tr[idx], label_smoothing=0.1)
            opt.zero_grad(set_to_none=True)
            loss.backward()
            opt.step()
            sched.step()
            total += loss.item() * len(idx)
        v1, v3 = evaluate(model, X_val, y_val)
        print(f"epoch {epoch + 1:2d}/{args.epochs} loss {total / len(X_tr):.4f} "
              f"val top1 {v1:.4f} top3 {v3:.4f} ({time.time() - t0:.0f}s)", flush=True)

    t1, t3 = evaluate(model, X_test, y_test)
    print(f"test top1 {t1:.4f} top3 {t3:.4f}")
    torch.save({"config": model.config, "state_dict": model.state_dict(), "labels": list(labels)},
               args.data / "model.pt")
    (args.data / "metrics.json").write_text(json.dumps({"top1": t1, "top3": t3, "epochs": args.epochs}))


if __name__ == "__main__":
    main()
