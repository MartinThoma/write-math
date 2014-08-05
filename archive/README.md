Place big files here in the following way:

* `datasets`: Files should all be `.pickle` files and have filenames of the
  schema:
  * `YYYY-MM-DD-HH-MM-handwriting_datasets-raw.pickle` for datasets that were
    not preprocessed
  * `YYYY-MM-DD-HH-MM-handwriting_datasets-preprocessed.pickle` for datasets
    that were preprocessed
* `pfiles`: Files wit filenames like
  * `2014-08-01-testdata.pfile`
  * `2014-08-01-validdata.pfile`
  * `2014-08-01-traindata.pfile`
* `models`: Files with filenames like `YYYY-MM-DD-HH-MM.json`