The following datasets were created with a KIT internal toolkit for
neural nets.

## Dataset information
```
The following 184 symbols were evaluated:
! (51), + (47), - (46), / (56), 
0 (106), 1 (61), 2 (63), 3 (55), 4 (92), 5 (54), 6 (54), 7 (55), 8 (53), 9 (53), 
< (60), > (45), 
A (283), B (86), C (110), D (78), E (98), F (88), G (84), H (81), I (72), J (75), K (74), L (71), M (81), N (62), O (57), P (56), Q (57), R (63), S (35), T (40), U (36), V (32), W (40), X (35), Y (36), Z (41), 
[ (54), \$ (24), \% (10), \Delta (86), \Downarrow (14), \Frowny (11), \Gamma (78), \Lambda (39), \Omega (72), \Phi (28), \Pi (37), \Psi (27), \Rightarrow (25), \Sigma (76), \Theta (26), \Upsilon (26), \Xi (25), \alpha (105), \approx (22), \barwedge (54), \beta (92), \bigcap (53), \bigcup (55), \cap (58), \cdot (65), \celsius (31), \checkmark (11), \chi (26), \circ (13), \cong (29), \copyright (11), \cup (59), \dashv (59), \delta (39), \div (10), \dots (58), \dot{\cup} (53), \emptyset (58), \epsilon (29), \equiv (56), \eta (30), \exists (59), \frownie (16), \gamma (68), \geq (30), \hbar (57), \heartsuit (19), \in (57), \int (31), \iota (26), \kappa (29), \lambda (54), \leadsto (58), \leftarrow (57), \leq (35), \mathbb{H} (62), \mathbb{N} (26), \mathbb{Q} (26), \mathbb{R} (22), \mathbb{Z} (54), \mid (12), \mu (57), \nabla (31), \neq (57), \ni (59), \nu (25), \ohm (57), \oint (28), \omega (29), \parallel (61), \partial (49), \permil (16), \perp (60), \phi (26), \pi (103), \pm (60), \prec (26), \propto (49), \psi (28), \rceil (56), \rho (27), \rightarrow (71), \setminus (56), \sharp (43), \sigma (30), \sim (57), \sqrt{} (59), \subset (31), \subseteq (29), \succ (23), \succeq (26), \sum (31), \supset (65), \supseteq (27), \tau (43), \textasciitilde (30), \textbackslash (56), \theta (32), \times (73), \uplus (25), \upsilon (25), \varepsilon (83), \varkappa (27), \varphi (34), \varrho (25), \vdash (59), \vdots (57), \vee (55), \wedge (57), \xi (100), \zeta (36), \{ (24), \| (57), \} (22), ] (57), 
a (39), b (26), c (29), d (26), e (24), f (36), g (29), h (25), i (28), j (24), k (24), l (24), m (27), n (27), o (24), p (24), q (36), r (23), s (26), t (44), u (27), v (23), w (23), x (34), y (24), z (25), 
| (58), 
raw datasets: 8562
### Preprocessing Parameters ###
Epsilon: 10.00
Center: False
Squared quadratic: False
Flatten: False
Threshold: 20
Space evenly: True (20 points, cubic)
```


## 3-layer MLP
```bash
d show < model.json
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
$ time d train --epochs 200 -v trndata-0.pfile < model.json > trained_model.json
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
$ d train --epochs 200 -v trndata-0.pfile < model.json > trained_model.json  2994,28s user 7,47s system 98% cpu 50:38,29 total
```

Test

```bash
$ d test tstdata-0.pfile < trained_model.json 
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

### 2000 epochs

```bash
[2014-06-26 23:04:25,833] >  epoch 2000/58000, training cost 2.172440
[2014-06-26 23:04:25,841] >> Training finished in 0:19:10.198515
$ d train --epochs 2000 -v trndata-0.pfile < mlp2.json > trained_model.json  1150,12s user 0,77s system 99% cpu 19:12,11 total
```

Test

```bash
$ d test tstdata-0.pfile < trained_model.json
[2014-06-27 05:35:47,574] >> Loading model
[2014-06-27 05:35:47,593] >> Loading datasets
[2014-06-27 05:35:47,931] >> Testing started with arguments:
{'batch_size': 256,
 'datasets': [PFileDataset@tstdata-0.pfile,1],
 'verbosity': 0,
 'warn': False}
[2014-06-27 05:35:47,954] >> Compiling theano model
[2014-06-27 05:35:48,891] PFileDataset@tstdata-0.pfile,1: errors = 0.468750, cost = 2.322245
```

### 161:400:1070 (Repeated training)

```bash
$ d show < model.json
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
$ d train traindata-1.pfile validdata-1.pfile < model.json > trained_model.json
$ d train traindata-1.pfile validdata-1.pfile < trained_model.json > trained_model2.json
$ d train --epoch 200 traindata-1.pfile validdata-1.pfile < trained_model2.json > trained_model3.json
$ d train --epochs 10 --learning-rate 3 traindata-1.pfile validdata-1.pfile < trained_model3.json > trained_model4.json
$ d train --epochs 10 --learning-rate 3 --momentum 0.1 traindata-1.pfile validdata-1.pfile < trained_model4.json > trained_model5.json
$ d train --epochs 10 --learning-rate 3 --momentum 0.1 traindata-1.pfile validdata-1.pfile < trained_model5.json > trained_model6.json
$ d train --epochs 100 --learning-rate 3 --momentum 0.1 traindata-1.pfile validdata-1.pfile < trained_model6.json > trained_model7.json
$ d train --epochs 100 --learning-rate 30 --momentum 0.1 traindata-1.pfile validdata-1.pfile < trained_model7.json > trained_model8.json
$ d train --epochs 100 --learning-rate 1 --momentum 0.1 traindata-1.pfile validdata-1.pfile < trained_model7.json > trained_model8.json
$ d train --epochs 10 --learning-rate 0.1 --momentum 0.1 traindata-1.pfile validdata-1.pfile < trained_model8.json > trained_model9.json
$ d train --epochs 100 --learning-rate 0.1 --momentum 0.1 traindata-1.pfile validdata-1.pfile < trained_model9.json > trained_model10.json
$ d test testdata-1.pfile < trained_model10.json 
[2014-06-27 12:34:47,808] >> Loading model
[2014-06-27 12:34:47,885] >> Loading datasets
[2014-06-27 12:34:48,282] >> Testing started with arguments:
{'batch_size': 256,
 'datasets': [PFileDataset@testdata-1.pfile,1],
 'verbosity': 0,
 'warn': False}
[2014-06-27 12:34:48,307] >> Compiling theano model
[2014-06-27 12:34:49,877] PFileDataset@testdata-1.pfile,1: errors = 0.260417, cost = 1.318792
```

### 161:322:322 MLP
```bash
$ d make mlp 161:322:322 > mlp3.json
$ d train --epochs 300 --learning-rate 10 --momentum 0.1 traindata-0.pfile validdata-0.pfile < mlp3.json > mlp3-1.json
$ d test testdata-0.pfile < mlp3-1.json 
[2014-06-27 13:29:23,732] >> Loading model
[2014-06-27 13:29:23,765] >> Loading datasets
[2014-06-27 13:29:24,299] >> Testing started with arguments:
{'batch_size': 256,
 'datasets': [PFileDataset@testdata-0.pfile,1],
 'verbosity': 0,
 'warn': False}
[2014-06-27 13:29:24,319] >> Compiling theano model
[2014-06-27 13:29:25,455] PFileDataset@testdata-0.pfile,1: errors = 0.326823, cost = 1.554708
```

### 161:483:322 MLP
```bash
$ d make mlp 161:483:322 > mlp3.json
$ d train --epochs 300 --learning-rate 10 --momentum 0.1 traindata-0.pfile validdata-0.pfile < mlp3.json > mlp3-1.json
$ d test testdata-0.pfile < mlp3-1.json 
[2014-06-27 13:29:23,732] >> Loading model
[2014-06-27 13:29:23,765] >> Loading datasets
[2014-06-27 13:29:24,299] >> Testing started with arguments:
{'batch_size': 256,
 'datasets': [PFileDataset@testdata-0.pfile,1],
 'verbosity': 0,
 'warn': False}
[2014-06-27 13:29:24,319] >> Compiling theano model
[2014-06-27 13:29:25,455] PFileDataset@testdata-0.pfile,1: errors = 0.326823, cost = 1.554708
```

### 161:80:322 MLP
```bash
$ d make mlp 161:483:322 > mlp3.json
$ d train --epochs 300 --learning-rate 10 --momentum 0.1 traindata-0.pfile validdata-0.pfile < mlp3.json > mlp3-1.json
$ d test testdata-0.pfile < mlp3-1.json 
[2014-06-27 13:29:23,732] >> Loading model
[2014-06-27 13:29:23,765] >> Loading datasets
[2014-06-27 13:29:24,299] >> Testing started with arguments:
{'batch_size': 256,
 'datasets': [PFileDataset@testdata-0.pfile,1],
 'verbosity': 0,
 'warn': False}
[2014-06-27 13:29:24,319] >> Compiling theano model
[2014-06-27 13:29:25,455] PFileDataset@testdata-0.pfile,1: errors = 0.326823, cost = 1.554708
$ d test testdata-0.pfile < mlp3-1.json
[2014-06-27 14:53:08,371] >> Loading model
[2014-06-27 14:53:08,387] >> Loading datasets
[2014-06-27 14:53:08,716] >> Testing started with arguments:
{'batch_size': 256,
 'datasets': [PFileDataset@testdata-0.pfile,1],
 'verbosity': 0,
 'warn': False}
[2014-06-27 14:53:08,743] >> Compiling theano model
[2014-06-27 14:53:09,784] PFileDataset@testdata-0.pfile,1: errors = 0.386719, cost = 1.645437
```
### 161:161:322 MLP

```bash
$ d make mlp 161:161:322 > mlp3.json
$ d train --epochs 300 --learning-rate 10 --momentum 0.1 traindata-0.pfile validdata-0.pfile < mlp3.json > mlp3-1.json
$ d test testdata-0.pfile < mlp3-1.json
[2014-06-27 16:06:29,598] >> Loading model
[2014-06-27 16:06:29,620] >> Loading datasets
[2014-06-27 16:06:30,818] >> Testing started with arguments:
{'batch_size': 256,
 'datasets': [PFileDataset@testdata-0.pfile,1],
 'verbosity': 0,
 'warn': False}
[2014-06-27 16:06:30,858] >> Compiling theano model
[2014-06-27 16:06:32,023] PFileDataset@testdata-0.pfile,1: errors = 0.330729, cost = 1.674410
```

train more:

```bash
$ d train --epochs 600 --learning-rate 10 --momentum 0.1 traindata-0.pfile validdata-0.pfile < mlp3.json > mlp3-1.json
$ d test testdata-0.pfile < mlp3-1.json
[2014-06-27 16:24:16,323] >> Loading model
[2014-06-27 16:24:16,345] >> Loading datasets
[2014-06-27 16:24:16,709] >> Testing started with arguments:
{'batch_size': 256,
 'datasets': [PFileDataset@testdata-0.pfile,1],
 'verbosity': 0,
 'warn': False}
[2014-06-27 16:24:16,735] >> Compiling theano model
[2014-06-27 16:24:17,821] PFileDataset@testdata-0.pfile,1: errors = 0.330729, cost = 1.674410
```

### 161:161:200 MLP

```bash
$ d make mlp 161:161:200 > mlp3.json
$ d train --epochs 300 --learning-rate 10 --momentum 0.1 traindata-0.pfile validdata-0.pfile < mlp3.json > mlp3-1.json