This model is based on `baseline-1`. Only another 500 hidden layer is added.

## How it was created

1. `$ nntoolkit make da 160,tanh:500 > da.json`
2. `$ nntoolkit make mlp 500:369 > layer2.json`
3. `$ nntoolkit recontrain -v --loss mse --epochs 1000 --learning-rate 0.001 --corruption 0.3 --l2-reg=1e-4 ../../feature-files/baseline/traindata.pfile < da.json > datrained.json`
4. `$ nntoolkit stack datrained.json layer2.json > model-1.json`
5. `$ rm da.json layer2.json datrained.json`