// Minimal dependency-free CNN inference for the exported model.
// Model format (written by training/export.py):
//   model.json: { input: [C, H, W], dtype: "float16", layers: [...], labels: [...] }
//   weights.bin: concatenated little-endian float16 tensors referenced by
//                {offset, length} (in elements) from the layer specs.

function halfToFloat(h) {
  const s = (h & 0x8000) ? -1 : 1;
  const e = (h >> 10) & 0x1f;
  const f = h & 0x3ff;
  if (e === 0) return s * f * 2 ** -24;
  if (e === 31) return f ? NaN : s * Infinity;
  return s * (1 + f / 1024) * 2 ** (e - 15);
}

function decode(buffer, dtype) {
  if (dtype === "float32") return new Float32Array(buffer);
  if (dtype !== "float16") throw new Error(`unsupported dtype ${dtype}`);
  const half = new Uint16Array(buffer);
  const table = new Float32Array(65536);
  for (let i = 0; i < 65536; i++) table[i] = halfToFloat(i);
  const out = new Float32Array(half.length);
  for (let i = 0; i < half.length; i++) out[i] = table[half[i]];
  return out;
}

// Reorder conv weights from [O, C, K, K] to [C, K, K, O] so that the
// innermost loop of conv2d runs over contiguous output channels.
function transposeConv(w, O, C, K) {
  const q = C * K * K;
  const t = new Float32Array(q * O);
  for (let o = 0; o < O; o++) for (let i = 0; i < q; i++) t[i * O + o] = w[o * q + i];
  return t;
}

// 'same' 2D convolution, stride 1, odd square kernel.
// x: [C, H, W], wt: weights in [C, K, K, O] order (see transposeConv).
// Zero inputs (most of them, after ReLU / on blank canvas) are skipped.
function conv2d(x, C, H, W, wt, b, O, K, relu) {
  const p = (K - 1) >> 1;
  const Hp = H + 2 * p, Wp = W + 2 * p;
  const xp = new Float32Array(C * Hp * Wp);
  for (let c = 0; c < C; c++) {
    for (let i = 0; i < H; i++) {
      xp.set(x.subarray((c * H + i) * W, (c * H + i + 1) * W), (c * Hp + i + p) * Wp + p);
    }
  }
  const y = new Float32Array(O * H * W);
  const acc = new Float32Array(O);
  for (let i = 0; i < H; i++) {
    for (let j = 0; j < W; j++) {
      acc.set(b);
      let q = 0;
      for (let c = 0; c < C; c++) {
        for (let ky = 0; ky < K; ky++) {
          const r = (c * Hp + i + ky) * Wp + j;
          for (let kx = 0; kx < K; kx++, q++) {
            const v = xp[r + kx];
            if (v === 0) continue;
            const wo = q * O;
            for (let o = 0; o < O; o++) acc[o] += v * wt[wo + o];
          }
        }
      }
      const k = i * W + j;
      for (let o = 0; o < O; o++) {
        const v = acc[o];
        y[o * H * W + k] = relu && v < 0 ? 0 : v;
      }
    }
  }
  return y;
}

function maxpool2(x, C, H, W) {
  const h = H >> 1, w = W >> 1;
  const y = new Float32Array(C * h * w);
  for (let c = 0; c < C; c++) {
    for (let i = 0; i < h; i++) {
      for (let j = 0; j < w; j++) {
        const a = (c * H + 2 * i) * W + 2 * j;
        y[(c * h + i) * w + j] = Math.max(x[a], x[a + 1], x[a + W], x[a + W + 1]);
      }
    }
  }
  return y;
}

function globalAvgPool(x, C, H, W) {
  const y = new Float32Array(C);
  const n = H * W;
  for (let c = 0; c < C; c++) {
    let s = 0;
    for (let k = c * n; k < (c + 1) * n; k++) s += x[k];
    y[c] = s / n;
  }
  return y;
}

function dense(x, w, b, O, relu) {
  const N = x.length;
  const y = new Float32Array(O);
  for (let o = 0; o < O; o++) {
    let s = b[o];
    const row = o * N;
    for (let k = 0; k < N; k++) s += w[row + k] * x[k];
    y[o] = relu && s < 0 ? 0 : s;
  }
  return y;
}

export function softmax(z) {
  let m = -Infinity;
  for (const v of z) if (v > m) m = v;
  const e = z.map((v) => Math.exp(v - m));
  const s = e.reduce((a, b) => a + b, 0);
  return e.map((v) => v / s);
}

export class Model {
  constructor(spec, weights) {
    this.spec = spec;
    this.labels = spec.labels;
    const t = (ref) => weights.subarray(ref.offset, ref.offset + ref.length);
    this.layers = spec.layers.map((l) => {
      let w = l.weight && t(l.weight);
      if (l.type === "conv") w = transposeConv(w, l.out, l.in, l.kernel);
      return { ...l, w, b: l.bias && t(l.bias) };
    });
  }

  static async load(baseUrl, fetchImpl = fetch) {
    const spec = await (await fetchImpl(new URL("model.json", baseUrl))).json();
    const buf = await (await fetchImpl(new URL(spec.weights, baseUrl))).arrayBuffer();
    return new Model(spec, decode(buf, spec.dtype));
  }

  static fromBuffers(spec, buffer) {
    return new Model(spec, decode(buffer, spec.dtype));
  }

  /** Forward pass. input: Float32Array of size C*H*W. Returns logits. */
  forward(input) {
    let [C, H, W] = this.spec.input;
    let x = input;
    for (const l of this.layers) {
      switch (l.type) {
        case "conv":
          x = conv2d(x, C, H, W, l.w, l.b, l.out, l.kernel, l.relu);
          C = l.out;
          break;
        case "maxpool":
          x = maxpool2(x, C, H, W);
          H >>= 1; W >>= 1;
          break;
        case "gap":
          x = globalAvgPool(x, C, H, W);
          H = W = 1;
          break;
        case "dense":
          x = dense(x, l.w, l.b, l.out, l.relu);
          C = l.out; H = W = 1;
          break;
        default:
          throw new Error(`unknown layer ${l.type}`);
      }
    }
    return x;
  }

  /** Returns the top-k [{index, label, p}] for one input. */
  predict(input, k = 10) {
    const p = softmax(Array.from(this.forward(input)));
    return p
      .map((v, i) => ({ index: i, p: v, ...this.labels[i] }))
      .sort((a, b) => b.p - a.p)
      .slice(0, k);
  }
}
