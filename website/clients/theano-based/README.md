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
$ d test testdata-0.pfile < mlp3-1.json
[2014-06-27 16:35:49,233] >> Loading model
[2014-06-27 16:35:49,253] >> Loading datasets
[2014-06-27 16:35:50,069] >> Testing started with arguments:
{'batch_size': 256,
 'datasets': [PFileDataset@testdata-0.pfile,1],
 'verbosity': 0,
 'warn': False}
[2014-06-27 16:35:50,116] >> Compiling theano model
[2014-06-27 16:35:51,176] PFileDataset@testdata-0.pfile,1: errors = 0.338542, cost = 1.614269

```

### 161:161:200:200 MLP

```bash
$ d make mlp 161:161:200:200 > mlp3.json
$ d train --epochs 300 --learning-rate 10 --momentum 0.1 traindata-0.pfile validdata-0.pfile < mlp3.json > mlp3-1.json
$ d test testdata-0.pfile < mlp3.json
[2014-06-27 16:57:23,335] >> Loading model
[2014-06-27 16:57:23,360] >> Loading datasets
[2014-06-27 16:57:23,683] >> Testing started with arguments:
{'batch_size': 256,
 'datasets': [PFileDataset@testdata-0.pfile,1],
 'verbosity': 0,
 'warn': False}
[2014-06-27 16:57:23,707] >> Compiling theano model
[2014-06-27 16:57:24,806] PFileDataset@testdata-0.pfile,1: errors = 0.962240, cost = 5.298317
```

### Douglas-Peucker-Features
#### Data
```
! (68), + (80), - (92), / (78), 
0 (124), 1 (94), 2 (94), 3 (104), 4 (117), 5 (79), 6 (89), 7 (81), 8 (93), 9 (80) 
< (91), > (73), 
A (311), B (121), C (121), D (99), E (112), F (112), G (109), H (101), I (89), J (101), K (94), L (91), M (113), N (92), O (78), P (74), Q (74), R (82), S (52), T (62), U (57), V (45), W (58), X (48), Y (50), Z (68) 
[ (94), \$ (49), \% (38), \& (40), \Delta (116), \EURcr (35), \EURtm (43), \Finv (49), \Gamma (123), \Lambda (56), \Leftarrow (35), \Longleftrightarrow (40), \Omega (121), \Phi (48), \Pi (55), \Psi (50), \Rightarrow (63), \Sigma (102), \Theta (53), \Upomega (36), \Upsilon (41), \Xi (43), \_ (81), \alpha (138), \approx (45), \barwedge (71), \beta (119), \bigcap (88), \bigcup (69), \boxdot (53), \cap (79), \cdot (94), \celsius (48), \chi (50), \circ (71), \cong (58), \cup (80), \dashv (79), \delta (70), \dots (71), \dotsc (41), \dot{\cup} (67), \ell (42), \emptyset (79), \epsilon (60), \equiv (72), \eta (49), \exists (113), \fint (57), \forall (41), \gamma (100), \geq (55), \gg (57), \hbar (75), \iddots (38), \in (101), \infty (47), \int (68), \iota (47), \kappa (53), \lambda (85), \leadsto (74), \leftarrow (76), \leq (57), \lessdot (48), \libra (35), \ll (45), \lll (35), \mathbb{H} (73), \mathbb{N} (50), \mathbb{Q} (57), \mathbb{R} (48), \mathbb{Z} (66), \mu (123), \nabla (51), \neq (74), \ni (76), \nu (48), \ohm (70), \oiint (67), \oint (94), \omega (52), \parallel (79), \partial (74), \permil (35), \perp (76), \phi (63), \pi (127), \pm (85), \prec (40), \propto (77), \psi (51), \rceil (104), \rfloor (50), \rho (48), \rightarrow (106), \setminus (69), \sharp (56), \sigma (64), \sim (76), \sqint (75), \sqrt{} (88), \square (78), \subset (95), \subseteq (56), \succ (42), \succeq (41), \sum (62), \supset (90), \supseteq (60), \tau (68), \textasciitilde (47), \textbackslash (75), \textlira (37), \textlptr (79), \textrangle (50), \theta (54), \times (97), \triangleq (42), \updelta (50), \uplus (41), \upsilon (46), \varepsilon (119), \varkappa (45), \varphi (119), \varrho (45), \vdash (73), \vdots (73), \vee (73), \wedge (79), \xi (128), \zeta (65), \{ (70), \| (72), \} (85), ] (101), 
a (63), b (47), c (56), d (45), e (50), f (61), g (49), h (47), i (54), j (49), k (50), l (44), m (48), n (54), o (47), p (46), q (64), r (41), s (50), t (61), u (53), v (41), w (43), x (58), y (48), z (50) 
| (75), 
```
Classes (Nr of symbols): 205

#### Preprocessing
```
* <function scale_and_shift at 0x27a55f0> with []
* <function douglas_peucker at 0x27a56e0> with {'EPSILON': 0.2}
```
#### Features (161)
* Number of lines
* Points of symbol (maximum of 20 per line, maximum of 4 lines)
  Empty slots get filled with -1

#### Learning

```bash
$ d make mlp 161:256:282 > mlp.json
$ d test testdata.pfile < mlp.json 
    [2014-07-05 18:29:31,229] >> Loading model
    [2014-07-05 18:29:31,255] >> Loading datasets
    [2014-07-05 18:29:31,635] >> Testing started with arguments:
    {'batch_size': 256,
     'datasets': [PFileDataset@testdata.pfile,1],
     'verbosity': 0,
     'warn': False}
    [2014-07-05 18:29:31,658] >> Compiling theano model
    [2014-07-05 18:29:32,922] PFileDataset@testdata.pfile,1: errors = 0.975000, cost = 5.641907
$ d train --epochs 300 --learning-rate 1 --momentum 0.1 traindata.pfile validdata.pfile < mlp.json > mlp-1.json
$ d test testdata.pfile < mlp-1.json  
    [2014-07-05 18:53:58,557] >> Loading model
    [2014-07-05 18:53:58,585] >> Loading datasets
    [2014-07-05 18:53:58,915] >> Testing started with arguments:
    {'batch_size': 256,
     'datasets': [PFileDataset@testdata.pfile,1],
     'verbosity': 0,
     'warn': False}
    [2014-07-05 18:53:58,935] >> Compiling theano model
    [2014-07-05 18:54:00,142] PFileDataset@testdata.pfile,1: errors = 0.306250, cost = 1.197945
$ d train --epochs 300 --learning-rate 0.5 --momentum 0.1 traindata.pfile validdata.pfile < mlp-1.json > mlp-2.json
$ d test testdata.pfile < mlp-2.json
    [2014-07-05 19:17:45,131] >> Loading model
    [2014-07-05 19:17:45,161] >> Loading datasets
    [2014-07-05 19:17:45,479] >> Testing started with arguments:
    {'batch_size': 256,
     'datasets': [PFileDataset@testdata.pfile,1],
     'verbosity': 0,
     'warn': False}
    [2014-07-05 19:17:45,499] >> Compiling theano model
    [2014-07-05 19:17:46,721] PFileDataset@testdata.pfile,1: errors = 0.278125, cost = 1.082631
```
--------------------------------------------------------------------------------
#### Features (161)
* Number of lines
* Points of symbol (maximum of 20 per line, maximum of 4 lines)
  Empty slots get filled with 0

#### Learning

```bash
$ d make mlp 161:256:282 > mlp.json
$ d test testdata.pfile < mlp.json 
    [2014-07-05 19:20:42,249] >> Loading model
    [2014-07-05 19:20:42,277] >> Loading datasets
    [2014-07-05 19:20:42,598] >> Testing started with arguments:
    {'batch_size': 256,
     'datasets': [PFileDataset@testdata.pfile,1],
     'verbosity': 0,
     'warn': False}
    [2014-07-05 19:20:42,619] >> Compiling theano model
    [2014-07-05 19:20:43,735] PFileDataset@testdata.pfile,1: errors = 0.975000, cost = 5.641907
$ d train --epochs 300 --learning-rate 1 --momentum 0.1 traindata.pfile validdata.pfile < mlp.json > mlp-1.json
$ d test testdata.pfile < mlp-1.json 
    [2014-07-05 20:16:35,013] >> Loading model
    [2014-07-05 20:16:35,040] >> Loading datasets
    [2014-07-05 20:16:35,372] >> Testing started with arguments:
    {'batch_size': 256,
     'datasets': [PFileDataset@testdata.pfile,1],
     'verbosity': 0,
     'warn': False}
    [2014-07-05 20:16:35,395] >> Compiling theano model
    [2014-07-05 20:16:36,513] PFileDataset@testdata.pfile,1: errors = 0.270313, cost = 1.082142
$ d train --epochs 300 --learning-rate 0.5 --momentum 0.1 traindata.pfile validdata.pfile < mlp-1.json > mlp-2.json
$ d test testdata.pfile < mlp-2.json
    [2014-07-05 20:52:30,896] >> Loading model
    [2014-07-05 20:52:30,923] >> Loading datasets
    [2014-07-05 20:52:31,248] >> Testing started with arguments:
    {'batch_size': 256,
     'datasets': [PFileDataset@testdata.pfile,1],
     'verbosity': 0,
     'warn': False}
    [2014-07-05 20:52:31,272] >> Compiling theano model
    [2014-07-05 20:52:32,394] PFileDataset@testdata.pfile,1: errors = 0.258594, cost = 1.034283
$ d train --epochs 300 --learning-rate 2 --momentum 0.1 traindata.pfile validdata.pfile < mlp-2.json > mlp-3.json
$ d test testdata.pfile < mlp-3.json 
[2014-07-05 21:41:54,139] >> Loading model
[2014-07-05 21:41:54,166] >> Loading datasets
[2014-07-05 21:41:54,498] >> Testing started with arguments:
{'batch_size': 256,
 'datasets': [PFileDataset@testdata.pfile,1],
 'verbosity': 0,
 'warn': False}
[2014-07-05 21:41:54,521] >> Compiling theano model
[2014-07-05 21:41:55,652] PFileDataset@testdata.pfile,1: errors = 0.249219, cost = 1.073648
$ d train --epochs 300 --learning-rate 2 --momentum 0.1 traindata.pfile validdata.pfile < mlp-3.json > mlp-4.json
$ d test testdata.pfile < mlp-4.json 
    [2014-07-05 21:42:26,781] >> Loading model
    [2014-07-05 21:42:26,808] >> Loading datasets
    [2014-07-05 21:42:27,129] >> Testing started with arguments:
    {'batch_size': 256,
     'datasets': [PFileDataset@testdata.pfile,1],
     'verbosity': 0,
     'warn': False}
    [2014-07-05 21:42:27,151] >> Compiling theano model
    [2014-07-05 21:42:28,278] PFileDataset@testdata.pfile,1: errors = 0.249219, cost = 1.074607
```

--------------------------------------------------------------------------------
#### Preprocessing
```
* <function scale_and_shift at 0x28d86e0> with []
* <function douglas_peucker at 0x28d87d0> with {'EPSILON': 0.2}
* <function space_evenly at 0x28d8758> with {'KIND': 'cubic', 'number': 100}
```
#### Features (161)
* Number of lines
* Points of symbol (maximum of 20 per line, maximum of 4 lines)
  Empty slots get filled with 0

#### Learning

```bash
$ d make mlp 161:256:282 > mlp.json
$ d test testdata.pfile < mlp.json 
    [2014-07-05 21:46:01,041] >> Loading model
    [2014-07-05 21:46:01,068] >> Loading datasets
    [2014-07-05 21:46:01,401] >> Testing started with arguments:
    {'batch_size': 256,
     'datasets': [PFileDataset@testdata.pfile,1],
     'verbosity': 0,
     'warn': False}
    [2014-07-05 21:46:01,423] >> Compiling theano model
    [2014-07-05 21:46:02,538] PFileDataset@testdata.pfile,1: errors = 0.975000, cost = 5.641907
$ d train --epochs 300 --learning-rate 1 --momentum 0.1 traindata.pfile validdata.pfile < mlp.json > mlp-1.json
$ d test testdata.pfile < mlp-1.json  
    [2014-07-05 22:06:51,937] >> Loading model
    [2014-07-05 22:06:51,964] >> Loading datasets
    [2014-07-05 22:06:52,292] >> Testing started with arguments:
    {'batch_size': 256,
     'datasets': [PFileDataset@testdata.pfile,1],
     'verbosity': 0,
     'warn': False}
    [2014-07-05 22:06:52,315] >> Compiling theano model
    [2014-07-05 22:06:53,444] PFileDataset@testdata.pfile,1: errors = 0.350781, cost = 1.436929
$ d train --epochs 300 --learning-rate 1 --momentum 0.1 traindata.pfile validdata.pfile < mlp-1.json > mlp-2.json
$ test testdata.pfile < mlp-2.json 
[2014-07-05 22:59:26,798] >> Loading model
[2014-07-05 22:59:26,825] >> Loading datasets
[2014-07-05 22:59:28,029] >> Testing started with arguments:
{'batch_size': 256,
 'datasets': [PFileDataset@testdata.pfile,1],
 'verbosity': 0,
 'warn': False}
[2014-07-05 22:59:28,080] >> Compiling theano model
[2014-07-05 22:59:29,699] PFileDataset@testdata.pfile,1: errors = 0.338281, cost = 1.410109
```

### More Data

#### Data
```
!` (683), - (102), / (512), 
0 (124), 1 (104), 2 (108), 3 (104), 4 (117), 8 (107), < (102), 
A (314), B (121), C (126), D (104), E (113), F (112), G (109), H (101), J (102), K (102), L (101), M (113), N (102), [ (740), \# (751), \$ (292), \% (619), \& (867), \AA (517), \AE (116), \Ankh (157), \Bat (539), \Bowtie (186), \CircledA (105), \Delta (655), \Downarrow (112), \EUR (278), \EURdig (121), \EURtm (109), \Faxmachine (103), \Frowny (171), \Gamma (452), \Heart (418), \Im (113), \Lambda (304), \Leftarrow (106), \Leftrightarrow (790), \Letter (154), \Lightning (158), \Longleftrightarrow (180), \Longrightarrow (173), \MVAt (858), \Mobilefone (192), \Mundus (262), \O (161), \Omega (571), \Phi (417), \Pi (570), \Psi (314), \Re (142), \Rightarrow (1141), \S (233), \Sigma (1288), \Smiley (871), \Telefon (147), \Theta (306), \Updelta (108), \Upomega (140), \Upphi (119), \Uppi (138), \Uppsi (126), \Upsigma (232), \Upsilon (128), \Uptheta (105), \Vdash (104), \Xi (286), \Yinyang (240), \aa (156), \ae (185), \aleph (545), \alpha (1706), \amalg (143), \angle (162), \approx (1361), \ast (367), \astrosun (236), \backsim (111), \backslash (172), \barwedge (118), \because (162), \beta (791), \bigcap (276), \bigcirc (157), \bigcup (347), \bigodot (141), \bigoplus (389), \bigotimes (194), \bigstar (374), \bigvee (111), \bigwedge (193), \blacksmiley (160), \blacksquare (374), \bot (469), \bowtie (151), \boxdot (117), \boxtimes (134), \bullet (222), \cap (731), \cdot (472), \celsius (221), \checked (185), \checkmark (592), \chi (617), \circ (638), \circlearrowleft (134), \circledcirc (104), \clubsuit (186), \cong (957), \coprod (123), \copyright (170), \cup (630), \curvearrowright (120), \dag (164), \dagger (108), \dashv (172), \ddots (267), \degree (449), \delta (821), \diameter (141), \diamond (150), \div (233), \doteq (117), \dots (127), \dotsb (284), \dotsc (155), \downarrow (130), \ell (595), \emptyset (648), \epsilon (373), \equiv (1652), \eta (437), \exists (945), \female (129), \fint (212), \forall (1392), \frownie (232), \fullmoon (107), \gamma (770), \geq (585), \geqslant (209), \gg (463), \gtrsim (406), \hbar (345), \heartsuit (631), \hookrightarrow (443), \iddots (171), \idotsint (103), \iiiint (133), \iiint (164), \iint (227), \in (1472), \infty (1869), \int (2340), \iota (119), \kappa (176), \lambda (732), \langle (505), \lceil (238), \leadsto (428), \leftarrow (157), \leftrightarrow (359), \leq (724), \leqslant (262), \lesssim (492), \lfloor (302), \lightning (359), \ll (637), \llbracket (516), \longmapsto (148), \longrightarrow (175), \lozenge (106), \ltimes (148), \male (218), \mapsto (608), \mars (162), \mathbb{1} (620), \mathcal{A} (234), \mathcal{B} (113), \mathcal{C} (128), \mathcal{D} (143), \mathcal{E} (201), \mathcal{F} (262), \mathcal{H} (174), \mathcal{L} (498), \mathcal{M} (133), \mathcal{N} (219), \mathcal{O} (561), \mathcal{P} (219), \mathcal{R} (109), \mathcal{S} (117), \mathcal{T} (138), \mathcal{Z} (110), \mathds{1} (211), \mathds{C} (287), \mathds{E} (159), \mathds{N} (681), \mathds{P} (142), \mathds{Q} (152), \mathds{R} (1564), \mathds{Z} (668), \mathfrak{A} (115), \mathfrak{S} (157), \mathscr{A} (119), \mathscr{C} (137), \mathscr{D} (106), \mathscr{H} (130), \mathscr{L} (534), \mathscr{S} (145), \mid (245), \models (314), \mu (779), \nabla (791), \nearrow (137), \neg (542), \neq (993), \nexists (209), \ni (359), \nmid (246), \not\equiv (258), \notin (847), \nrightarrow (129), \nsubseteq (193), \nu (262), \o (201), \ocircle (110), \odot (340), \ohm (233), \oiint (253), \oint (827), \omega (413), \oplus (861), \otimes (691), \parallel (261), \partial (1563), \permil (133), \perp (725), \phi (470), \phone (105), \pi (1096), \pm (1012), \pounds (113), \prec (324), \preccurlyeq (129), \preceq (200), \prod (749), \propto (958), \psi (390), \rangle (101), \rceil (160), \rfloor (140), \rho (470), \rightarrow (791), \rightharpoonup (146), \rightleftharpoons (142), \rightsquigarrow (146), \rrbracket (121), \rtimes (190), \searrow (105), \setminus (356), \sharp (181), \shortrightarrow (181), \sigma (754), \sim (1278), \simeq (586), \skull (284), \smiley (802), \spadesuit (151), \sqcap (105), \sqcup (176), \sqrt{} (636), \sqsubseteq (196), \square (1334), \ss (155), \star (176), \subset (561), \subseteq (1061), \subsetneq (155), \succ (249), \succeq (155), \sum (2228), \sun (131), \supset (307), \supseteq (296), \tau (354), \textasciicircum (221), \textasciitilde (284), \textasteriskcentered (175), \textbackslash (201), \textbeta (121), \textbraceleft (293), \textbullet (110), \textchi (144), \textcopyright (164), \textdagger (107), \textdegree (234), \textdollaroldstyle (187), \textepsilon (203), \textesh (309), \textestimated (137), \textgreater (367), \textinterrobang (140), \textlambda (196), \textlangle (100), \textlbrackdbl (145), \textless (372), \textlptr (133), \textmusicalnote (154), \textomega (136), \textonehalf (161), \textordfeminine (148), \textpm (270), \textquestiondown (148), \textquotedblleft (152), \textregistered (267), \textrightarrow (133), \textsca (191), \textscripta (117), \textsection (346), \textsterling (101), \textsurd (195), \texttheta (117), \texttildelow (144), \texttimes (255), \texttrademark (130), \texttwosuperior (174), \textvisiblespace (148), \therefore (504), \theta (438), \thicksim (105), \times (1000), \top (233), \triangle (195), \triangledown (132), \trianglelefteq (129), \triangleq (403), \twoheadrightarrow (268), \upalpha (311), \uparrow (152), \upbeta (134), \upchi (126), \updelta (186), \upgamma (136), \upharpoonright (101), \uplambda (220), \uplus (142), \upmu (252), \upphi (150), \uppi (392), \upsigma (105), \uptau (183), \uptheta (121), \upvarepsilon (150), \upvarphi (328), \upvarsigma (105), \upxi (272), \vDash (336), \varepsilon (521), \varkappa (113), \varnothing (300), \varoiint (126), \varphi (1020), \varpi (107), \varrho (152), \vartheta (177), \vdash (717), \vdots (302), \vee (577), \wedge (948), \with (156), \wp (219), \xi (1783), \zeta (581), \{ (789), \| (314), \} (245), ] (234), | (418), 
```
Classes (nr of symbols): 387
#### Preprocessing
```
* <function scale_and_shift at 0x371fed8> with []
* <function douglas_peucker at 0x3720050> with {'EPSILON': 0.2}
* <function space_evenly at 0x371ff50> with {'KIND': 'cubic', 'number': 100}
```
#### Features (161)
* Number of lines
* Points of symbol (maximum of 20 per line, maximum of 4 lines)
  Empty slots get filled with -1

#### Learning

```bash
$ d make mlp 161:256:282 > mlp.json
$ d test testdata.pfile < mlp.json
$ d test testdata.pfile < mlp3-1.json 
[2014-07-19 00:11:53,425] >> Loading model
[2014-07-19 00:11:53,456] >> Loading datasets
[2014-07-19 00:11:53,820] >> Testing started with arguments:
{'batch_size': 256,
 'datasets': [PFileDataset@testdata.pfile,1],
 'verbosity': 0,
 'warn': False}
[2014-07-19 00:11:53,845] >> Compiling theano model
[2014-07-19 00:11:56,915] PFileDataset@testdata.pfile,1: errors = 0.605395, cost = 3.049634

```

## Even more data

### Data
```
 (429), !` (967), - (105), / (690), 
0 (124), 1 (104), 2 (109), 3 (104), 4 (117), 8 (107), < (104), 
A (315), B (123), C (126), D (104), E (113), F (112), G (109), H (101), J (102), K (102), L (101), M (113), N (102), [ (1055), \# (1053), \$ (405), \% (877), \& (1283), \-- (100), \--- (109), \---- (105), \AA (762), \AE (174), \Ankh (212), \Bat (857), \Bowtie (263), \CircledA (142), \Cross (142), \Delta (972), \Denarius (129), \Downarrow (165), \EUR (376), \EURcr (103), \EURdig (160), \EURtm (134), \Ecommerce (115), \Faxmachine (127), \Frowny (265), \Gamma (615), \Heart (617), \Im (145), \Lambda (433), \Leftarrow (140), \Leftrightarrow (1208), \Letter (234), \Lightning (225), \Longleftrightarrow (243), \Longrightarrow (267), \MVAt (1278), \Mobilefone (221), \Mundus (418), \O (237), \Omega (806), \Phi (604), \Pi (799), \Psi (446), \Re (200), \Rightarrow (1729), \S (338), \Shilling (100), \Sigma (1882), \Smiley (1318), \Telefon (193), \Theta (459), \Updelta (146), \Upgamma (109), \Upomega (188), \Upphi (170), \Uppi (207), \Uppsi (184), \Upsigma (331), \Upsilon (172), \Uptheta (158), \Vdash (137), \Xi (402), \Yinyang (382), \aa (230), \ae (291), \aleph (755), \alpha (2499), \amalg (189), \angle (238), \approx (2000), \ast (551), \astrosun (300), \asymp (153), \backsim (177), \backslash (247), \barwedge (132), \because (221), \beta (1100), \between (110), \bigcap (336), \bigcirc (216), \bigcup (455), \bigodot (177), \bigoplus (534), \bigotimes (289), \bigsqcup (126), \bigstar (567), \bigtriangleup (114), \bigvee (152), \bigwedge (288), \blacksmiley (231), \blacksquare (611), \blacktriangleright (107), \bot (717), \bowtie (243), \boxdot (141), \boxplus (112), \boxtimes (222), \bullet (345), \cap (1075), \cdot (677), \cdotp (102), \celsius (337), \checked (275), \checkmark (868), \chi (918), \circ (941), \circlearrowleft (176), \circlearrowright (143), \circledR (125), \circledast (115), \circledcirc (127), \clubsuit (271), \cong (1372), \coprod (177), \copyright (250), \cup (908), \curvearrowright (168), \dag (253), \dagger (165), \dashv (222), \ddots (388), \degree (665), \delta (1212), \diameter (194), \diamond (244), \diamondsuit (120), \div (323), \doteq (191), \dots (150), \dotsb (390), \dotsc (168), \downarrow (201), \ell (891), \emptyset (928), \epsilon (540), \equiv (2471), \eta (673), \exists (1369), \female (171), \fint (297), \flat (122), \forall (2113), \frownie (320), \fullmoon (141), \gamma (1115), \geq (846), \geqslant (302), \gg (690), \gtrsim (635), \guillemotleft (109), \hbar (510), \heartsuit (900), \hookrightarrow (661), \iddots (240), \iiint (205), \iint (293), \in (2259), \infty (2851), \int (3415), \iota (151), \kappa (253), \lambda (1002), \langle (754), \lceil (358), \leadsto (571), \leftarrow (206), \leftmoon (108), \leftrightarrow (499), \leq (1045), \leqslant (391), \lesssim (748), \lfloor (452), \lhd (109), \lightning (548), \ll (973), \llbracket (768), \longmapsto (191), \longrightarrow (245), \lozenge (156), \ltimes (218), \male (346), \mapsfrom (125), \mapsto (907), \mars (235), \mathbb{1} (944), \mathcal{A} (355), \mathcal{B} (162), \mathcal{C} (183), \mathcal{D} (198), \mathcal{E} (282), \mathcal{F} (388), \mathcal{G} (112), \mathcal{H} (242), \mathcal{L} (732), \mathcal{M} (213), \mathcal{N} (327), \mathcal{O} (852), \mathcal{P} (358), \mathcal{R} (163), \mathcal{S} (184), \mathcal{T} (186), \mathcal{U} (114), \mathcal{X} (124), \mathcal{Z} (159), \mathds{1} (309), \mathds{C} (415), \mathds{E} (198), \mathds{N} (991), \mathds{P} (195), \mathds{Q} (218), \mathds{R} (2331), \mathds{Z} (998), \mathfrak{A} (154), \mathfrak{M} (114), \mathfrak{S} (216), \mathfrak{X} (118), \mathscr{A} (188), \mathscr{C} (213), \mathscr{D} (144), \mathscr{E} (104), \mathscr{F} (132), \mathscr{H} (203), \mathscr{L} (782), \mathscr{P} (118), \mathscr{S} (195), \mathsection (127), \mid (320), \models (467), \mp (132), \mu (1120), \multimap (115), \nRightarrow (101), \nabla (1198), \nearrow (193), \neg (826), \neq (1492), \nexists (309), \ni (479), \nmid (348), \not\equiv (379), \notin (1280), \nrightarrow (185), \nsubseteq (198), \nu (383), \nvDash (145), \o (305), \ocircle (172), \odot (492), \ohm (331), \oiint (319), \oint (1154), \omega (608), \ominus (104), \oplus (1315), \otimes (1056), \parallel (367), \partial (2365), \permil (159), \perp (1079), \phi (686), \phone (150), \pi (1551), \pitchfork (117), \pm (1502), \pounds (150), \prec (519), \preccurlyeq (183), \preceq (272), \prime (148), \prod (1091), \propto (1354), \psi (555), \rangle (154), \rceil (176), \rfloor (158), \rho (679), \rightarrow (1108), \rightharpoonup (213), \rightleftarrows (127), \rightleftharpoons (206), \rightrightarrows (137), \rightsquigarrow (218), \rrbracket (174), \rtimes (266), \searrow (143), \setminus (510), \sharp (234), \shortrightarrow (269), \sigma (1099), \sim (1912), \simeq (868), \skull (476), \smiley (1166), \spadesuit (242), \sphericalangle (106), \sqcap (151), \sqcup (258), \sqrt{} (960), \sqsubseteq (286), \square (1971), \ss (236), \star (262), \subset (772), \subseteq (1543), \subsetneq (233), \succ (361), \succeq (199), \sum (3327), \sun (167), \supset (400), \supseteq (403), \surd (121), \tau (457), \textasciicircum (352), \textasciitilde (388), \textasteriskcentered (255), \textbackslash (248), \textbar (119), \textbeta (179), \textbigcircle (118), \textbraceleft (433), \textbullet (162), \textchi (205), \textcopyright (232), \textdagger (145), \textdegree (347), \textdollar (123), \textdollaroldstyle (288), \textepsilon (320), \textesh (440), \textestimated (195), \textgreater (581), \textinterrobang (207), \textlambda (289), \textlangle (149), \textlbrackdbl (185), \textless (563), \textlptr (150), \textmusicalnote (221), \textnumero (100), \textomega (194), \textonehalf (237), \textordfeminine (202), \textphi (113), \textpm (397), \textquestiondown (233), \textquotedblleft (194), \textreferencemark (100), \textregistered (386), \textrightarrow (178), \textsca (276), \textscripta (147), \textsection (496), \textsterling (136), \textsurd (245), \texttheta (188), \texttildelow (196), \texttimes (371), \texttrademark (181), \texttwosuperior (249), \textvisiblespace (219), \textyen (129), \textyogh (136), \therefore (745), \theta (640), \thickapprox (117), \thicksim (144), \times (1479), \top (333), \triangle (309), \triangledown (194), \triangleleft (129), \trianglelefteq (173), \triangleq (562), \triangleright (140), \twoheadrightarrow (409), \upalpha (467), \uparrow (226), \upbeta (193), \upchi (173), \updelta (247), \upepsilon (105), \upeta (135), \upgamma (199), \upharpoonright (137), \uplambda (324), \uplus (184), \upmu (381), \upnu (102), \upomega (110), \upphi (218), \uppi (568), \uppsi (110), \upsigma (159), \upsilon (122), \uptau (281), \uptheta (175), \upvarepsilon (218), \upvarphi (478), \upvarsigma (148), \upxi (406), \upzeta (136), \vDash (448), \varepsilon (720), \varkappa (156), \varnothing (453), \varoiint (154), \varphi (1490), \varpi (162), \varpropto (136), \varrho (215), \vartheta (281), \vartriangle (108), \vdash (1053), \vdots (397), \vee (845), \venus (135), \wedge (1427), \with (207), \wp (346), \wr (101), \xi (2507), \zeta (850), \{ (1133), \| (367), \} (323), ] (275), | (544), 
```
Classes (nr of symbols): 453

#### Preprocessing

```
* <function scale_and_shift at 0x39c0ed8> with []
* <function douglas_peucker at 0x39c1050> with {'EPSILON': 0.2}
* <function space_evenly at 0x39c0f50> with {'KIND': 'cubic', 'number': 100}
```

#### Features (161)
* Number of lines
* Points of symbol (maximum of 20 per line, maximum of 4 lines)
  Empty slots get filled with -1

### Learning

```bash
$ d make mlp 161:256:453 > mlp.json
$ d test testdata.pfile < mlp.json 
[2014-07-23 09:56:50,661] >> Loading model
[2014-07-23 09:56:50,707] >> Loading datasets
[2014-07-23 09:56:57,512] >> Testing started with arguments:
{'batch_size': 256,
 'datasets': [PFileDataset@testdata.pfile,1],
 'verbosity': 0,
 'warn': False}
[2014-07-23 09:56:57,798] >> Compiling theano model
[2014-07-23 09:57:07,230] PFileDataset@testdata.pfile,1: errors = 0.997874, cost = 6.115892
detl test testdata.pfile < mlp.json  4,90s user 0,35s system 30% cpu 17,005 total

```