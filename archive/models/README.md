Put all JSON models in here. All models should be named like this:

`YYYY-MM-DD-HH-MM.json`

Additional information about the model should be organzied in a YAML file
called `YYYY-MM-DD-HH-MM.yml`. Those YAML files should have names like this:

All paths should be relative to the `write-math` root path.

```yaml
data-source: archive/handwriting_datasets-2014-08-01.pickle
data:
    training: archive/pfiles/2014-08-01-testdata.pfile
    validating: archive/pfiles/2014-08-01-validdata.pfile
    testing: archive/pfiles/2014-08-01-traindata.pfile
preprocessing:
    scale_and_shift:
    connect_lines:
    space_evenly:
        - kind: cubic
        - number: 100
    scale_and_shift:
features:
    Stroke_Count:
    Constant_Point_Coordinates:
        - lines: -1
        - points_per_line: 81
        - fill_empty_with: 0
model:
    type: mlp
    topology: '244:488:370'
    file: '/var/www/write-math/archive/2014-08-01-21-41.json'
```