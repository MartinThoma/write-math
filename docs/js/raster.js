// Port of training/raster.py. Keep both files in sync
// (tests/parity.mjs verifies that they produce the same bitmaps).

export const SIZE = 32;
const PAD = 2.0;
const PEN_RADIUS = 0.9;

/**
 * Rasterize strokes ([[{x, y}, ...], ...]) into a Float32Array of SIZE*SIZE
 * values in [0, 1], row-major, y pointing down.
 */
export function rasterize(strokes) {
  const out = new Float32Array(SIZE * SIZE);
  strokes = strokes.filter((s) => s.length > 0);
  if (strokes.length === 0) return out;

  let minX = Infinity, maxX = -Infinity, minY = Infinity, maxY = -Infinity;
  for (const s of strokes) {
    for (const p of s) {
      if (p.x < minX) minX = p.x;
      if (p.x > maxX) maxX = p.x;
      if (p.y < minY) minY = p.y;
      if (p.y > maxY) maxY = p.y;
    }
  }
  const w = maxX - minX, h = maxY - minY;
  const extent = Math.max(w, h);
  const scale = extent > 1e-9 ? (SIZE - 2 * PAD) / extent : 0;
  const offX = (SIZE - w * scale) / 2;
  const offY = (SIZE - h * scale) / 2;

  // Collect segments in the normalized pixel frame.
  const seg = [];
  for (const s of strokes) {
    const pts = s.map((p) => [(p.x - minX) * scale + offX, (p.y - minY) * scale + offY]);
    if (pts.length === 1) seg.push([pts[0][0], pts[0][1], pts[0][0], pts[0][1]]);
    for (let i = 1; i < pts.length; i++) {
      seg.push([pts[i - 1][0], pts[i - 1][1], pts[i][0], pts[i][1]]);
    }
  }

  const reach = PEN_RADIUS + 0.5;
  const img = new Float64Array(SIZE * SIZE);
  for (const [ax, ay, bx, by] of seg) {
    const dx = bx - ax, dy = by - ay;
    const len2 = dx * dx + dy * dy;
    // Only visit pixels whose centre can be within reach of the segment.
    const r0 = Math.max(0, Math.floor(Math.min(ay, by) - reach - 0.5));
    const r1 = Math.min(SIZE - 1, Math.ceil(Math.max(ay, by) + reach - 0.5));
    const c0 = Math.max(0, Math.floor(Math.min(ax, bx) - reach - 0.5));
    const c1 = Math.min(SIZE - 1, Math.ceil(Math.max(ax, bx) + reach - 0.5));
    for (let r = r0; r <= r1; r++) {
      const cy = r + 0.5;
      for (let c = c0; c <= c1; c++) {
        const cx = c + 0.5;
        let t = 0;
        if (len2 > 0) {
          t = ((cx - ax) * dx + (cy - ay) * dy) / len2;
          t = t < 0 ? 0 : t > 1 ? 1 : t;
        }
        const qx = ax + t * dx - cx, qy = ay + t * dy - cy;
        let v = reach - Math.sqrt(qx * qx + qy * qy);
        v = v < 0 ? 0 : v > 1 ? 1 : v;
        const k = r * SIZE + c;
        if (v > img[k]) img[k] = v;
      }
    }
  }
  out.set(img);
  return out;
}
