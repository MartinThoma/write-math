This folder should only contain pfiles.

The pfiles should be placed in subfolders. Every subfolder belongs to a
choice of features.

## info.yml
Every subfolder has to have an info.yml with the following structure:

```yaml
preprocessed: archive/preprocessed/baseline
features:
  - Constant_Point_Coordinates:
      - lines: 4
      - points_per_line: 20
      - fill_empty_with: 0
      - pen_down: false
```

In this file, the key `preprocessed` gives the path the the folder which
contains the preprocessing information.

## run.log

Every `run.log` has to have the folloing line as a first line

```text
timestamp: '2014-08-31 20:08:05'
```

where the timestamp is in UTC (format: '%Y-%m-%d %H:%M:%S')