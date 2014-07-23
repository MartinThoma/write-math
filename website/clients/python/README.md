1. Download latest data from server with `download_dataset.py`
2. Create crossvalidation dataset with `make_crossvalidation_dataset.py` (see also: `HandwrittenData.py`). Takes about 131,02s.
3. Apply preprocessing (see `preprocessing.py`).
4. Apply learning algorithm.

Step 3 and 4 might be done in `../theano-based`:

3. `create_pfiles.py` needs about 1351,39s