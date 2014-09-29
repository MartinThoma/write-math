This model is based on `baseline-1`. Only another 500 hidden layer is added.

## How it was created

1. `$ nntoolkit make da 160:500 > da.json`
2. `$ nntoolkit make mlp 500:369 > layer2.json`
3. `$ nntoolkit recontrain --epochs 1000 --learning-rate 0.1 --momentum 0.1 -v ../../feature-files/baseline/traindata.pfile ../../feature-files/baseline/validdata.pfile ../../feature-files/baseline/testdata.pfile < model-2.json > model-3.json`
4. `$ nntoolkit stack model-3.json layer2.json > model-4.json`
5. `$ rm da.json layer2.json datrained.json`