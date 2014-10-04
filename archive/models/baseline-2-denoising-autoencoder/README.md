This model is based on `baseline-1`. Only another 500 hidden layer is added.

## How it was created

1. Copy 'datrained.json' from baseline-1-denoising-autoencoder
2. `$ nntoolkit make da 500:500 > da2.json`
3. `$ nntoolkit stack datrained.json da2.json > da3.json`
4. `$ nntoolkit make mlp 500:369 > layer2.json`
5. `$ nntoolkit recontrain -v --loss mse --epochs 1000 --learning-rate 0.001 --corruption 0.3 --l2-reg=1e-4 ../../feature-files/baseline/traindata.pfile < da3.json > datrained-2layers.json`
6. `$ nntoolkit stack datrained-2layers.json layer2.json > model-1.json`
7. `$ rm da.json layer2.json datrained.json`