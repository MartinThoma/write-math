This model is based on `baseline-1`. Only another 500 hidden layer is added.

## How it was created

1. Copy `model-3.json` from `archive/models/baseline-2-pretraining` to this folder.
2. Manually remove the last layer from `model-3.json`.
3. `$ nntoolkit make mlp 500:500:369 > layer2.json`.
4. `$ nntoolkit stack model-3.json layer2.json > model-4.json`.
5. `$ rm layer2.json`