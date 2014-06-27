## 2-layer MLP
```bash
detl show < model.json
model: stack
  properties: {}
  [1] model: sigmoid
    properties:
      activation: sigmoid
      n_hidden: 400
      n_visible: 161
    parameters:
      W: (161, 400) min -0.414, max 0.414, avg 0.001, std 0.239
      b: (400,) min 0.000, max 0.000, avg 0.000, std 0.000
  [2] model: logreg
    properties:
      activation: softmax
      n_hidden: 1070
      n_visible: 400
      output: prediction
    parameters:
      W: (400, 1070) min 0.000, max 0.000, avg 0.000, std 0.000
      b: (1070,) min 0.000, max 0.000, avg 0.000, std 0.000
```

### 200 epochs
Train

```bash
$ time detl train --epochs 200 -v trndata-0.pfile < model.json > trained_model.json
[2014-06-26 21:03:24,537] >> Loading model
[2014-06-26 21:03:24,618] >> Loading datasets
[2014-06-26 21:03:24,952] >> Supervised training started with arguments:
{'adadelta': False,
 'adadelta_epsilon': '1e-6',
 'adadelta_rho': '0.95',
 'adagrad': False,
 'adagrad_decay': False,
 'batch_size': 256,
 'datasets': (DatasetContainer [PFileDataset@trndata-0.pfile,1],
              DatasetContainer [],
              DatasetContainer []),
 'epochs': 200,
 'fix_layers': [],
 'graph': False,
 'hooks': [],
 'l1_reg': '0.0',
 'l2_reg': '0.0',
 'layer_args': [],
 'learning_rate': '0.01',
 'minibatches': -1,
 'momentum': '',
 'newbob': False,
 'newbob_decay': 0.5,
 'newbob_threshold': [0.005, 0.001],
 'patience': -1,
 'patience_improve_threshold': 0.995,
 'patience_increase': 1.5,
 'pre_validate': False,
 'print_errors': False,
 'validation_interval': -1,
 'verbosity': 1,
 'warn': False}
[2014-06-26 21:03:24,953] >> Compiling theano graph
[2014-06-26 21:03:26,644] >> Training started
[2014-06-26 21:03:41,941] >  epoch 1/29, training cost 6.874600
[2014-06-26 21:03:57,317] >  epoch 2/58, training cost 6.655831
[...]
[2014-06-26 21:54:01,867] >  epoch 200/5800, training cost 3.739707
[2014-06-26 21:54:01,929] >> Training finished in 0:50:35.283719
detl train --epochs 200 -v trndata-0.pfile < model.json > trained_model.json  2994,28s user 7,47s system 98% cpu 50:38,29 total
```

Test

```bash
detl test tstdata-0.pfile < trained_model.json 
[2014-06-26 22:01:42,698] >> Loading model
[2014-06-26 22:01:42,775] >> Loading datasets
[2014-06-26 22:01:43,094] >> Testing started with arguments:
{'batch_size': 256,
 'datasets': [PFileDataset@tstdata-0.pfile,1],
 'verbosity': 0,
 'warn': False}
[2014-06-26 22:01:43,117] >> Compiling theano model
[2014-06-26 22:01:44,586] PFileDataset@tstdata-0.pfile,1: errors = 0.700521, cost = 3.805463
```