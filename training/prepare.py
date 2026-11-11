"""Rasterize the HWRT recordings into a compact .npz for training.

Output (in --data):
  hwrt32.npz     X_train/X_test uint8 [N, 32, 32], y_train/y_test int16,
                 u_train int32 (user ids), labels (LaTeX strings)
  fixtures.json  a few raw test recordings, used by tests/parity.mjs
"""

import argparse
import csv
import json
import random
import sys
from multiprocessing import Pool
from pathlib import Path

import numpy as np

from raster import rasterize

csv.field_size_limit(sys.maxsize)


def read_symbols(path):
    with open(path, newline="") as f:
        rows = list(csv.DictReader(f, delimiter=";", quotechar="'"))
    return [(int(r["symbol_id"]), r["latex"]) for r in rows]


def parse(data):
    """Recording JSON -> list of strokes of (x, y) tuples."""
    return [[(float(p["x"]), float(p["y"])) for p in stroke] for stroke in json.loads(data)]


def _work(row):
    symbol_id, user_id, data = row
    strokes = parse(data)
    img = rasterize(strokes)
    return symbol_id, user_id, np.round(img * 255).astype(np.uint8)


def read_rows(path):
    with open(path, newline="") as f:
        for r in csv.DictReader(f, delimiter=";", quotechar="'"):
            yield int(r["symbol_id"]), int(r["user_id"]), r["data"]


def rasterize_file(path, id2idx, workers):
    xs, ys, us = [], [], []
    with Pool(workers) as pool:
        for i, (sid, uid, img) in enumerate(pool.imap(_work, read_rows(path), chunksize=256)):
            xs.append(img)
            ys.append(id2idx[sid])
            us.append(uid)
            if i % 20000 == 0:
                print(f"  {path.name}: {i}", flush=True)
    return np.stack(xs), np.asarray(ys, np.int16), np.asarray(us, np.int32)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", type=Path, default=Path(__file__).parent / "data")
    parser.add_argument("--workers", type=int, default=None)
    parser.add_argument("--fixtures", type=int, default=40)
    args = parser.parse_args()

    symbols = read_symbols(args.data / "symbols.csv")
    id2idx = {sid: i for i, (sid, _) in enumerate(symbols)}
    labels = np.asarray([latex for _, latex in symbols])

    X_test, y_test, _ = rasterize_file(args.data / "test-data.csv", id2idx, args.workers)
    X_train, y_train, u_train = rasterize_file(args.data / "train-data.csv", id2idx, args.workers)
    print(f"train {X_train.shape}, test {X_test.shape}, classes {len(labels)}")
    np.savez_compressed(
        args.data / "hwrt32.npz",
        X_train=X_train, y_train=y_train, u_train=u_train,
        X_test=X_test, y_test=y_test, labels=labels,
    )

    rows = list(read_rows(args.data / "test-data.csv"))
    rng = random.Random(0)
    fixtures = []
    for sid, _, data in rng.sample(rows, args.fixtures):
        strokes = [[{"x": p["x"], "y": p["y"]} for p in s] for s in json.loads(data)]
        fixtures.append({"latex": symbols[id2idx[sid]][1], "strokes": strokes})
    (args.data / "fixtures.json").write_text(json.dumps(fixtures))


if __name__ == "__main__":
    main()
