// Runs the model off the main thread so drawing stays smooth.
import { Model } from "./nn.js";

const ready = Model.load(new URL("../model/", import.meta.url));

ready.then(
  (model) => postMessage({ type: "ready", labels: model.labels.length, metrics: model.spec.metrics }),
  (err) => postMessage({ type: "error", message: String(err) }),
);

onmessage = async ({ data }) => {
  const model = await ready;
  postMessage({ type: "result", id: data.id, top: model.predict(data.image, data.k) });
};
