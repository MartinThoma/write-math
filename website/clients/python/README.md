1. Download latest data from server with `download_dataset.py`.
   Takes about 175,68s-177,50s  (online, measured twice)
2. Create crossvalidation dataset with `make_crossvalidation_dataset.py` (see also: `HandwrittenData.py`). Takes about 131,02s.
3. Apply preprocessing (see `preprocessing.py` and `preprocess_dataset.py`).
4. Apply learning algorithm.

Step 3 and 4 might be done in `../theano-based`:

3. `create_pfiles.py` needs about 1351,39s

## preprocess_dataset.py

* Only 'scale and shift': 476,44s
* 'scale and shift', 'connect lines', 'douglas_peucker', 'space_evenly': 5420,27s