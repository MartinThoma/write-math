// Checks that the browser code (docs/js/raster.js + docs/js/nn.js) reproduces
// the Python preprocessing and the exported model's outputs.
// Run: node tests/parity.mjs
import { readFile } from "node:fs/promises";
import { Model } from "../docs/js/nn.js";
import { rasterize } from "../docs/js/raster.js";

const root = new URL("../", import.meta.url);
const spec = JSON.parse(await readFile(new URL("docs/model/model.json", root), "utf8"));
const weights = await readFile(new URL(`docs/model/${spec.weights}`, root));
const model = Model.fromBuffers(spec, weights.buffer.slice(weights.byteOffset, weights.byteOffset + weights.byteLength));
const fixtures = JSON.parse(await readFile(new URL("tests/fixtures.json", root), "utf8"));

let maxImg = 0, maxLogit = 0, argmaxMismatch = 0, correct = 0, ms = 0;
for (const fx of fixtures) {
  const img = rasterize(fx.strokes);
  for (let i = 0; i < img.length; i++) maxImg = Math.max(maxImg, Math.abs(img[i] - fx.image[i]));
  const t0 = performance.now();
  const logits = model.forward(img);
  ms += performance.now() - t0;
  let a = 0, b = 0;
  for (let i = 0; i < logits.length; i++) {
    maxLogit = Math.max(maxLogit, Math.abs(logits[i] - fx.logits[i]));
    if (logits[i] > logits[a]) a = i;
    if (fx.logits[i] > fx.logits[b]) b = i;
  }
  if (a !== b) argmaxMismatch++;
  if (spec.labels[a].latex === fx.latex) correct++;
}

console.log(`fixtures: ${fixtures.length}`);
console.log(`max |image diff|:  ${maxImg.toExponential(2)}`);
console.log(`max |logit diff|:  ${maxLogit.toExponential(2)}`);
console.log(`argmax mismatches: ${argmaxMismatch}`);
console.log(`top-1 correct:     ${correct}/${fixtures.length}`);
console.log(`avg forward pass:  ${(ms / fixtures.length).toFixed(1)} ms`);

const ok = maxImg < 1e-4 && maxLogit < 1e-2 && argmaxMismatch === 0;
console.log(ok ? "OK" : "FAILED");
process.exit(ok ? 0 : 1);
