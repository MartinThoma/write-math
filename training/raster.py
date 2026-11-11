"""Stroke rasterizer.

This is the single source of truth for preprocessing. `docs/js/raster.js`
is a line-by-line port of this file; if you change anything here, change it
there too (``tests/parity.mjs`` checks that both agree).

A recording is a list of strokes, each stroke a list of (x, y) points in
screen coordinates (y grows downwards). The recording is scaled uniformly so
that its longer side fits into ``SIZE - 2 * PAD`` pixels, centred, and every
line segment is drawn with an anti-aliased pen of half-width ``PEN_RADIUS``.
"""

import numpy as np

SIZE = 32
PAD = 2.0
PEN_RADIUS = 0.9


def normalize(strokes):
    """Return the strokes mapped into the SIZE x SIZE pixel frame."""
    xs = [p[0] for s in strokes for p in s]
    ys = [p[1] for s in strokes for p in s]
    min_x, max_x, min_y, max_y = min(xs), max(xs), min(ys), max(ys)
    w, h = max_x - min_x, max_y - min_y
    extent = max(w, h)
    scale = (SIZE - 2 * PAD) / extent if extent > 1e-9 else 0.0
    off_x = (SIZE - w * scale) / 2
    off_y = (SIZE - h * scale) / 2
    return [
        [((x - min_x) * scale + off_x, (y - min_y) * scale + off_y) for x, y in s]
        for s in strokes
    ]


def segments(strokes):
    """Return arrays ax, ay, bx, by of all line segments (dots -> zero length)."""
    a, b = [], []
    for s in strokes:
        if len(s) == 1:
            a.append(s[0])
            b.append(s[0])
        for p, q in zip(s, s[1:]):
            a.append(p)
            b.append(q)
    a = np.asarray(a, dtype=np.float64)
    b = np.asarray(b, dtype=np.float64)
    return a[:, 0], a[:, 1], b[:, 0], b[:, 1]


_centres = (np.arange(SIZE, dtype=np.float64) + 0.5)
_CY, _CX = np.meshgrid(_centres, _centres, indexing="ij")
_CX = _CX.reshape(-1, 1)
_CY = _CY.reshape(-1, 1)


def rasterize(strokes):
    """Rasterize a list of strokes [[(x, y), ...], ...] to a float32 SIZExSIZE image."""
    strokes = [s for s in strokes if len(s) > 0]
    if not strokes:
        return np.zeros((SIZE, SIZE), dtype=np.float32)
    ax, ay, bx, by = segments(normalize(strokes))
    out = np.zeros(SIZE * SIZE, dtype=np.float64)
    chunk = 512
    for i in range(0, len(ax), chunk):
        sl = slice(i, i + chunk)
        dx = bx[sl] - ax[sl]
        dy = by[sl] - ay[sl]
        len2 = dx * dx + dy * dy
        safe = np.where(len2 > 0, len2, 1.0)
        t = ((_CX - ax[sl]) * dx + (_CY - ay[sl]) * dy) / safe
        t = np.where(len2 > 0, np.clip(t, 0.0, 1.0), 0.0)
        qx = ax[sl] + t * dx - _CX
        qy = ay[sl] + t * dy - _CY
        d = np.sqrt(qx * qx + qy * qy)
        v = np.clip(PEN_RADIUS + 0.5 - d, 0.0, 1.0).max(axis=1)
        np.maximum(out, v, out=out)
    return out.reshape(SIZE, SIZE).astype(np.float32)
