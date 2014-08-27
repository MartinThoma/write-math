Put all models in here. All models should be in their own folder. A model
has to be described with a `model.yml` (see exmaple)

All paths should be relative to the `write-math` root path.

## Example for `model.yml`

```yaml
preprocessed: archive/preprocessed/small-baseline
data-modification:
    multiply: 1
training: nntoolkit train --epochs 100 --learning-rate 1 --momentum 0.1 --hook='!detl test {{testing}},err=testlogs/testresult_%e.txt' {{training}}
    {{validation}} {{testing}} < {{src_model}} > {{target_model}}
features:
  - Stroke_Count: null
  - Constant_Point_Coordinates:
      - lines: 4
      - points_per_line: 20
      - fill_empty_with: 0
      - pen_down: false
model:
    type: mlp
    topology: 161:488:38

```