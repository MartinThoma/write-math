# Write Math — offline symbol recognizer

Draw a mathematical symbol, get its LaTeX command. A single static page with
no server and no third-party scripts. Once the page has loaded, it keeps
working offline: a service worker caches the app and the model, and you can
install it as a PWA.

The recognizer is a small convolutional network trained on the
[HWRT database of handwritten symbols](https://zenodo.org/records/50022)
(369 symbols, 151k training and 17k test recordings). Most of that data
comes from Daniel Kirsch's [detexify-data](https://github.com/kirel/detexify-data).

## Results

On the 17,074 HWRT test recordings, the shipped model (float16 weights, 1.8 MB)
reaches **86.1% top-1** and **98.4% top-3** accuracy. Most remaining top-1
errors are between symbols that look the same when drawn, such as `\bot`/`\perp`,
`\Omega`/`\ohm`, `\models`/`\vDash` and `\emptyset`/`\varnothing`. That is
why the app shows the top 10 candidates. Training took about 2¼ hours on a
4-core laptop CPU (20 epochs).

## Layout

```
docs/                    the static site (served as-is, e.g. via GitHub Pages "/docs")
  index.html, css/, js/  UI
  js/raster.js           stroke -> 32x32 bitmap (port of training/raster.py)
  js/nn.js               dependency-free CNN inference
  model/                 exported model (model.json + weights-<hash>.bin, float16)
  sw.js                  offline-first service worker
training/                Python pipeline that produces docs/model/
tests/parity.mjs         checks JS preprocessing + inference against Python
```

## Running the app

Any static file server works:

```sh
python3 -m http.server -d docs 8000
# open http://localhost:8000
```

Service workers need `https://` or `localhost`.

## Training the model

```sh
python3 -m venv .venv && . .venv/bin/activate
pip install -r training/requirements.txt   # CPU-only torch is enough
cd training
python download.py    # fetch + verify + extract the HWRT tar into training/data/
python prepare.py     # rasterize all recordings -> data/hwrt32.npz
python train.py       # ~20 epochs, writes data/model.pt
python export.py      # writes ../docs/model/ and ../tests/fixtures.json
cd .. && npm test           # node tests/parity.mjs
```

### How it works

1. **Preprocessing** (`training/raster.py`, mirrored by `docs/js/raster.js`):
   the strokes are scaled uniformly so that the longer side of their bounding
   box fills a 32×32 frame (with 2 px of padding), centred. Each line segment
   is then drawn with an anti-aliased pen of half-width 0.9 px. Because the
   bitmap is drawn from line segments rather than individual points, the
   sampling rate of the input device does not matter.
2. **Model** (`training/model.py`): three blocks of two 3×3 conv layers each
   (32/64/128 channels, BatchNorm, ReLU), each block followed by 2×2 max-pooling.
   After that comes a 256-unit dense layer with dropout, then the 369-way output.
   Training uses AdamW with a one-cycle schedule, label smoothing, and random
   affine augmentation.
3. **Export** (`training/export.py`): BatchNorm is folded into the convolutions
   and the weights are rounded to float16. The test accuracy stored in
   `model.json` is measured on exactly that exported model.
4. **Inference** (`docs/js/nn.js`): plain JavaScript loops over `Float32Array`s.
   One forward pass takes a few tens of milliseconds.

`tests/parity.mjs` rasterizes the stored test recordings in JS and runs the
JS model on them. It checks that bitmaps and logits match the Python
reference.

## License

The code is MIT licensed (see `LICENSE`). The model in `docs/model/` is
trained on the HWRT database, which is published under the
[Open Database License (ODbL)](https://opendatacommons.org/licenses/odbl/)
(DOI [10.5281/zenodo.50022](https://doi.org/10.5281/zenodo.50022)).
