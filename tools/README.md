## TODO after cloning this repository

* Adjust the `~/.writemathrc` to fit to your setup. If you don't have one, you
  can use `writemathrc.template.yml` as a template.

## Workflow

1. Obtain the data. This can be done in two ways:
    * **Complete data**: Download latest data from server with `download_dataset.py`.
      Takes about 175,68s-177,50s  (online, measured twice)
    * **Handwritings only**: Download the `.pickle` data from
      [dropbox](https://www.dropbox.com/s/nk8gmd9k3tanjqu/2014-08-04-18-24-handwriting_datasets-raw.pickle)
2. Create crossvalidation dataset with `make_crossvalidation_dataset.py` (see also: `HandwrittenData.py`). Takes about 131,02s.
3. Apply preprocessing (see `preprocessing.py` and `preprocess_dataset.py`).
4. Apply learning algorithm.

The 4th step might include `create_pfiles.py` needs about 1351,39s

## preprocess_dataset.py

Here are some indicators how long the different preprocessing steps might take.
It was tested once on a machine with a Pentium P6200 processor, 4GB ram and a
5200 RPM HDD. The `.pickle` file had about 170000 recordings at that time:

* Only 'scale and shift': 476,44s
* 'scale and shift', 'connect lines', 'douglas_peucker', 'space_evenly': 5420,27s

### Other script execution times

A: computer with 12GB RAM, Intel(R) Pentium(R) CPU P6200 @ 2.13GHz, INTEL SSDSA2CW16

* `create_pfiles.py`: 3min 30 secons (on A)