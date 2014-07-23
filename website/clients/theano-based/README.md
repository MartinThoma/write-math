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
$ d train --epochs 3 --learning-rate 1 --momentum 0.1 traindata.pfile validdata.pfile < mlp.json > mlp-1.json
[...]
[2014-07-23 10:09:45,636] >> Training started
[2014-07-23 10:59:25,999] >  epoch 1/628, validation error 0.920045
[2014-07-23 11:00:46,384] >  epoch 2/1256, validation error 0.866446
[2014-07-23 11:02:06,895] >  epoch 3/1884, validation error 0.825257
[2014-07-23 11:03:26,823] >  epoch 4/2512, validation error 0.794155
[2014-07-23 11:04:46,537] >  epoch 5/3140, validation error 0.762213
[2014-07-23 11:06:06,261] >  epoch 6/3768, validation error 0.728788
[2014-07-23 11:07:26,369] >  epoch 7/4396, validation error 0.716475
[2014-07-23 11:08:46,028] >  epoch 8/5024, validation error 0.686907
[2014-07-23 11:10:06,101] >  epoch 9/5652, validation error 0.672864
[2014-07-23 11:11:25,746] >  epoch 10/6280, validation error 0.657140
[2014-07-23 11:12:49,228] >  epoch 11/6908, validation error 0.644037
[2014-07-23 11:14:15,106] >  epoch 12/7536, validation error 0.633505
[2014-07-23 11:15:44,949] >  epoch 13/8164, validation error 0.619709
[2014-07-23 11:17:06,935] >  epoch 14/8792, validation error 0.609078
[2014-07-23 11:18:29,588] >  epoch 15/9420, validation error 0.603145
[2014-07-23 11:19:52,313] >  epoch 16/10048, validation error 0.599832
[2014-07-23 11:21:14,208] >  epoch 17/10676, validation error 0.590882
[2014-07-23 11:22:34,617] >  epoch 18/11304, validation error 0.582674
[2014-07-23 11:23:54,336] >  epoch 19/11932, validation error 0.579312
[2014-07-23 11:25:14,256] >  epoch 20/12560, validation error 0.569620
[2014-07-23 11:26:34,123] >  epoch 21/13188, validation error 0.566703
[2014-07-23 11:27:53,746] >  epoch 22/13816, validation error 0.569027
[2014-07-23 11:29:13,304] >  epoch 23/14444, validation error 0.568829
[2014-07-23 11:30:32,849] >  epoch 24/15072, validation error 0.564577
[2014-07-23 11:31:52,793] >  epoch 25/15700, validation error 0.558890
[2014-07-23 11:33:13,198] >  epoch 26/16328, validation error 0.553649
[2014-07-23 11:34:32,919] >  epoch 27/16956, validation error 0.551226
[2014-07-23 11:35:52,812] >  epoch 28/17584, validation error 0.545589
[2014-07-23 11:37:12,615] >  epoch 29/18212, validation error 0.539508
[2014-07-23 11:38:32,279] >  epoch 30/18840, validation error 0.536096
[2014-07-23 11:39:51,955] >  epoch 31/19468, validation error 0.534167
[2014-07-23 11:41:11,412] >  epoch 32/20096, validation error 0.531250
[2014-07-23 11:42:31,121] >  epoch 33/20724, validation error 0.530657
[2014-07-23 11:43:50,867] >  epoch 34/21352, validation error 0.528481
[2014-07-23 11:45:10,831] >  epoch 35/21980, validation error 0.526553
[2014-07-23 11:46:30,432] >  epoch 36/22608, validation error 0.526009
[2014-07-23 11:47:49,899] >  epoch 37/23236, validation error 0.524822
[2014-07-23 11:49:09,248] >  epoch 38/23864, validation error 0.525168
[2014-07-23 11:50:28,530] >  epoch 39/24492, validation error 0.523586
[2014-07-23 11:51:47,990] >  epoch 40/25120, validation error 0.517900
[2014-07-23 11:53:07,427] >  epoch 41/25748, validation error 0.514587
[2014-07-23 11:54:27,335] >  epoch 42/26376, validation error 0.512114
[2014-07-23 11:55:47,110] >  epoch 43/27004, validation error 0.511917
[2014-07-23 11:57:06,905] >  epoch 44/27632, validation error 0.512164
[2014-07-23 11:58:26,840] >  epoch 45/28260, validation error 0.511620
[2014-07-23 11:59:46,773] >  epoch 46/28888, validation error 0.507911
[2014-07-23 12:01:07,009] >  epoch 47/29516, validation error 0.507021
[2014-07-23 12:02:27,024] >  epoch 48/30144, validation error 0.504450
[2014-07-23 12:03:47,591] >  epoch 49/30772, validation error 0.502126
[2014-07-23 12:05:07,564] >  epoch 50/31400, validation error 0.500297
[2014-07-23 12:06:27,522] >  epoch 51/32028, validation error 0.498912
[2014-07-23 12:07:47,701] >  epoch 52/32656, validation error 0.497231
[2014-07-23 12:09:07,802] >  epoch 53/33284, validation error 0.496341
[2014-07-23 12:10:27,354] >  epoch 54/33912, validation error 0.496539
[2014-07-23 12:11:46,891] >  epoch 55/34540, validation error 0.496489
[2014-07-23 12:13:06,350] >  epoch 56/35168, validation error 0.496390
[2014-07-23 12:14:26,238] >  epoch 57/35796, validation error 0.496094
[2014-07-23 12:15:46,144] >  epoch 58/36424, validation error 0.495204
[2014-07-23 12:17:05,940] >  epoch 59/37052, validation error 0.493671
[2014-07-23 12:18:25,810] >  epoch 60/37680, validation error 0.491495
[2014-07-23 12:19:45,408] >  epoch 61/38308, validation error 0.490309
[2014-07-23 12:21:05,156] >  epoch 62/38936, validation error 0.489171
[2014-07-23 12:22:24,971] >  epoch 63/39564, validation error 0.487391
[2014-07-23 12:23:44,632] >  epoch 64/40192, validation error 0.485908
[2014-07-23 12:25:04,374] >  epoch 65/40820, validation error 0.485413
[2014-07-23 12:26:24,507] >  epoch 66/41448, validation error 0.485018
[2014-07-23 12:27:43,966] >  epoch 67/42076, validation error 0.486205
[2014-07-23 12:29:03,773] >  epoch 68/42704, validation error 0.486551
[2014-07-23 12:30:23,294] >  epoch 69/43332, validation error 0.485809
[2014-07-23 12:31:42,773] >  epoch 70/43960, validation error 0.484573
[2014-07-23 12:33:02,349] >  epoch 71/44588, validation error 0.482941
[2014-07-23 12:34:21,930] >  epoch 72/45216, validation error 0.481903
[2014-07-23 12:35:41,474] >  epoch 73/45844, validation error 0.480815
[2014-07-23 12:37:01,183] >  epoch 74/46472, validation error 0.480419
[2014-07-23 12:38:21,135] >  epoch 75/47100, validation error 0.479974
[2014-07-23 12:39:41,405] >  epoch 76/47728, validation error 0.479282
[2014-07-23 12:41:01,411] >  epoch 77/48356, validation error 0.478639
[2014-07-23 12:42:21,084] >  epoch 78/48984, validation error 0.477848
[2014-07-23 12:43:41,092] >  epoch 79/49612, validation error 0.477304
[2014-07-23 12:45:00,984] >  epoch 80/50240, validation error 0.477453
[2014-07-23 12:46:20,955] >  epoch 81/50868, validation error 0.477551
[2014-07-23 12:47:40,604] >  epoch 82/51496, validation error 0.477502
[2014-07-23 12:49:00,618] >  epoch 83/52124, validation error 0.476414
[2014-07-23 12:50:20,845] >  epoch 84/52752, validation error 0.475376
[2014-07-23 12:51:40,531] >  epoch 85/53380, validation error 0.474585
[2014-07-23 12:53:00,554] >  epoch 86/54008, validation error 0.474041
[2014-07-23 12:54:20,588] >  epoch 87/54636, validation error 0.472112
[2014-07-23 12:55:40,272] >  epoch 88/55264, validation error 0.473002
[2014-07-23 12:57:00,066] >  epoch 89/55892, validation error 0.473645
[2014-07-23 12:58:19,782] >  epoch 90/56520, validation error 0.473002
[2014-07-23 12:59:39,432] >  epoch 91/57148, validation error 0.472261
[2014-07-23 13:00:59,259] >  epoch 92/57776, validation error 0.471519
[2014-07-23 13:02:18,886] >  epoch 93/58404, validation error 0.471272
[2014-07-23 13:03:38,511] >  epoch 94/59032, validation error 0.471371
[2014-07-23 13:04:57,993] >  epoch 95/59660, validation error 0.472409
[2014-07-23 13:06:17,814] >  epoch 96/60288, validation error 0.473052
[2014-07-23 13:07:37,719] >  epoch 97/60916, validation error 0.471865
[2014-07-23 13:08:57,312] >  epoch 98/61544, validation error 0.471420
[2014-07-23 13:10:16,836] >  epoch 99/62172, validation error 0.470876
[2014-07-23 13:11:36,529] >  epoch 100/62800, validation error 0.469887
[2014-07-23 13:12:56,299] >  epoch 101/63428, validation error 0.468849
[2014-07-23 13:14:16,084] >  epoch 102/64056, validation error 0.468997
[2014-07-23 13:15:36,103] >  epoch 103/64684, validation error 0.468552
[2014-07-23 13:16:55,923] >  epoch 104/65312, validation error 0.468206
[2014-07-23 13:18:15,339] >  epoch 105/65940, validation error 0.467118
[2014-07-23 13:19:34,763] >  epoch 106/66568, validation error 0.466228
[2014-07-23 13:20:54,011] >  epoch 107/67196, validation error 0.466525
[2014-07-23 13:22:13,519] >  epoch 108/67824, validation error 0.466278
[2014-07-23 13:23:32,964] >  epoch 109/68452, validation error 0.466525
[2014-07-23 13:24:53,330] >  epoch 110/69080, validation error 0.467069
[2014-07-23 13:26:12,748] >  epoch 111/69708, validation error 0.466723
[2014-07-23 13:27:32,524] >  epoch 112/70336, validation error 0.466525
[2014-07-23 13:28:51,927] >  epoch 113/70964, validation error 0.466228
[2014-07-23 13:30:11,947] >  epoch 114/71592, validation error 0.465536
[2014-07-23 13:31:32,193] >  epoch 115/72220, validation error 0.464893
[2014-07-23 13:32:51,989] >  epoch 116/72848, validation error 0.464250
[2014-07-23 13:34:11,957] >  epoch 117/73476, validation error 0.463212
[2014-07-23 13:35:32,150] >  epoch 118/74104, validation error 0.463261
[2014-07-23 13:36:52,470] >  epoch 119/74732, validation error 0.462718
[2014-07-23 13:38:12,262] >  epoch 120/75360, validation error 0.462421
[2014-07-23 13:39:31,833] >  epoch 121/75988, validation error 0.462075
[2014-07-23 13:40:51,686] >  epoch 122/76616, validation error 0.461778
[2014-07-23 13:42:11,531] >  epoch 123/77244, validation error 0.461531
[2014-07-23 13:43:31,399] >  epoch 124/77872, validation error 0.462273
[2014-07-23 13:44:51,344] >  epoch 125/78500, validation error 0.462470
[2014-07-23 13:46:11,218] >  epoch 126/79128, validation error 0.462915
[2014-07-23 13:47:31,156] >  epoch 127/79756, validation error 0.462223
[2014-07-23 13:48:51,007] >  epoch 128/80384, validation error 0.462421
[2014-07-23 13:50:11,035] >  epoch 129/81012, validation error 0.461432
[2014-07-23 13:51:31,191] >  epoch 130/81640, validation error 0.461036
[2014-07-23 13:52:51,297] >  epoch 131/82268, validation error 0.460047
[2014-07-23 13:54:11,200] >  epoch 132/82896, validation error 0.459504
[2014-07-23 13:55:31,461] >  epoch 133/83524, validation error 0.459602
[2014-07-23 13:56:51,776] >  epoch 134/84152, validation error 0.459306
[2014-07-23 13:58:11,935] >  epoch 135/84780, validation error 0.459405
[2014-07-23 13:59:32,030] >  epoch 136/85408, validation error 0.459355
[2014-07-23 14:00:51,808] >  epoch 137/86036, validation error 0.458762
[2014-07-23 14:02:11,917] >  epoch 138/86664, validation error 0.458366
[2014-07-23 14:03:32,390] >  epoch 139/87292, validation error 0.458416
[2014-07-23 14:04:52,867] >  epoch 140/87920, validation error 0.458515
[2014-07-23 14:06:12,815] >  epoch 141/88548, validation error 0.459355
[2014-07-23 14:07:34,021] >  epoch 142/89176, validation error 0.458663
[2014-07-23 14:08:55,191] >  epoch 143/89804, validation error 0.459009
[2014-07-23 14:10:16,219] >  epoch 144/90432, validation error 0.458020
[2014-07-23 14:11:36,039] >  epoch 145/91060, validation error 0.458070
[2014-07-23 14:12:55,968] >  epoch 146/91688, validation error 0.457130
[2014-07-23 14:14:16,465] >  epoch 147/92316, validation error 0.457476
[2014-07-23 14:15:36,737] >  epoch 148/92944, validation error 0.456932
[2014-07-23 14:16:58,103] >  epoch 149/93572, validation error 0.456092
[2014-07-23 14:18:19,502] >  epoch 150/94200, validation error 0.455400
[2014-07-23 14:19:39,234] >  epoch 151/94828, validation error 0.455894
[2014-07-23 14:20:59,092] >  epoch 152/95456, validation error 0.455152
[2014-07-23 14:22:18,912] >  epoch 153/96084, validation error 0.455053
[2014-07-23 14:23:38,968] >  epoch 154/96712, validation error 0.455202
[2014-07-23 14:25:03,070] >  epoch 155/97340, validation error 0.454411
[2014-07-23 14:26:26,368] >  epoch 156/97968, validation error 0.453966
[2014-07-23 14:27:46,277] >  epoch 157/98596, validation error 0.455004
[2014-07-23 14:29:06,194] >  epoch 158/99224, validation error 0.454658
[2014-07-23 14:30:26,053] >  epoch 159/99852, validation error 0.455004
[2014-07-23 14:31:47,428] >  epoch 160/100480, validation error 0.454262
[2014-07-23 14:33:08,020] >  epoch 161/101108, validation error 0.454361
[2014-07-23 14:34:28,863] >  epoch 162/101736, validation error 0.454608
[2014-07-23 14:35:53,568] >  epoch 163/102364, validation error 0.454262
[2014-07-23 14:37:14,232] >  epoch 164/102992, validation error 0.453669
[2014-07-23 14:38:34,004] >  epoch 165/103620, validation error 0.453619
[2014-07-23 14:39:55,232] >  epoch 166/104248, validation error 0.453372
[2014-07-23 14:41:18,912] >  epoch 167/104876, validation error 0.453026
[2014-07-23 14:42:38,590] >  epoch 168/105504, validation error 0.453422
[2014-07-23 14:43:58,543] >  epoch 169/106132, validation error 0.453372
[2014-07-23 14:45:19,347] >  epoch 170/106760, validation error 0.453273
[2014-07-23 14:46:39,921] >  epoch 171/107388, validation error 0.452532
[2014-07-23 14:48:02,061] >  epoch 172/108016, validation error 0.453076
[2014-07-23 14:49:24,340] >  epoch 173/108644, validation error 0.451543
[2014-07-23 14:50:48,552] >  epoch 174/109272, validation error 0.451741
[2014-07-23 14:52:10,918] >  epoch 175/109900, validation error 0.452186
[2014-07-23 14:53:30,393] >  epoch 176/110528, validation error 0.451889
[2014-07-23 14:54:50,092] >  epoch 177/111156, validation error 0.451889
[2014-07-23 14:56:09,823] >  epoch 178/111784, validation error 0.451790
[2014-07-23 14:57:29,677] >  epoch 179/112412, validation error 0.450850
[2014-07-23 14:58:49,424] >  epoch 180/113040, validation error 0.450603
[2014-07-23 15:00:09,426] >  epoch 181/113668, validation error 0.449812
[2014-07-23 15:01:29,280] >  epoch 182/114296, validation error 0.449268
[2014-07-23 15:02:49,120] >  epoch 183/114924, validation error 0.449417
[2014-07-23 15:04:09,049] >  epoch 184/115552, validation error 0.449763
[2014-07-23 15:05:29,019] >  epoch 185/116180, validation error 0.450554
[2014-07-23 15:06:51,132] >  epoch 186/116808, validation error 0.450653
[2014-07-23 15:08:11,547] >  epoch 187/117436, validation error 0.450109
[2014-07-23 15:09:32,398] >  epoch 188/118064, validation error 0.450059
[2014-07-23 15:10:51,806] >  epoch 189/118692, validation error 0.450059
[2014-07-23 15:12:11,264] >  epoch 190/119320, validation error 0.450158
[2014-07-23 15:13:30,731] >  epoch 191/119948, validation error 0.450356
[2014-07-23 15:14:50,798] >  epoch 192/120576, validation error 0.449565
[2014-07-23 15:16:10,798] >  epoch 193/121204, validation error 0.449466
[2014-07-23 15:17:30,532] >  epoch 194/121832, validation error 0.449565
[2014-07-23 15:18:50,300] >  epoch 195/122460, validation error 0.449515
[2014-07-23 15:20:10,073] >  epoch 196/123088, validation error 0.449219
[2014-07-23 15:21:29,573] >  epoch 197/123716, validation error 0.448774
[2014-07-23 15:22:50,557] >  epoch 198/124344, validation error 0.448428
[2014-07-23 15:24:10,973] >  epoch 199/124972, validation error 0.447884
[2014-07-23 15:25:30,888] >  epoch 200/125600, validation error 0.447735
[2014-07-23 15:26:50,736] >  epoch 201/126228, validation error 0.448279
[2014-07-23 15:28:13,898] >  epoch 202/126856, validation error 0.448724
[2014-07-23 15:29:34,286] >  epoch 203/127484, validation error 0.447834
[2014-07-23 15:30:54,041] >  epoch 204/128112, validation error 0.447043
[2014-07-23 15:32:14,010] >  epoch 205/128740, validation error 0.446994
[2014-07-23 15:33:33,913] >  epoch 206/129368, validation error 0.447043
[2014-07-23 15:34:53,798] >  epoch 207/129996, validation error 0.446944
[2014-07-23 15:36:13,700] >  epoch 208/130624, validation error 0.446746
[2014-07-23 15:37:33,595] >  epoch 209/131252, validation error 0.446005
[2014-07-23 15:38:53,635] >  epoch 210/131880, validation error 0.446450
[2014-07-23 15:40:13,605] >  epoch 211/132508, validation error 0.446895
[2014-07-23 15:41:33,541] >  epoch 212/133136, validation error 0.445807
[2014-07-23 15:42:53,381] >  epoch 213/133764, validation error 0.446351
[2014-07-23 15:44:13,276] >  epoch 214/134392, validation error 0.446301
[2014-07-23 15:45:33,059] >  epoch 215/135020, validation error 0.446203
[2014-07-23 15:46:53,153] >  epoch 216/135648, validation error 0.445856
[2014-07-23 15:48:12,766] >  epoch 217/136276, validation error 0.445016
[2014-07-23 15:49:32,764] >  epoch 218/136904, validation error 0.444867
[2014-07-23 15:50:52,432] >  epoch 219/137532, validation error 0.445510
[2014-07-23 15:52:12,168] >  epoch 220/138160, validation error 0.445659
[2014-07-23 15:53:32,003] >  epoch 221/138788, validation error 0.445609
[2014-07-23 15:54:51,585] >  epoch 222/139416, validation error 0.445065
[2014-07-23 15:56:11,262] >  epoch 223/140044, validation error 0.444966
[2014-07-23 15:57:31,040] >  epoch 224/140672, validation error 0.445016
[2014-07-23 15:58:50,365] >  epoch 225/141300, validation error 0.444670
[2014-07-23 16:00:10,275] >  epoch 226/141928, validation error 0.443829
[2014-07-23 16:01:29,982] >  epoch 227/142556, validation error 0.444076
[2014-07-23 16:02:49,702] >  epoch 228/143184, validation error 0.444126
[2014-07-23 16:04:09,154] >  epoch 229/143812, validation error 0.443829
[2014-07-23 16:05:29,008] >  epoch 230/144440, validation error 0.444225
```