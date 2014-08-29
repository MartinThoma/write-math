All files that should be put in all folders for work with SLURM must have
the prefix `DO.`.


## Templating

* `{{ traindata }}` gets replaced by the relative path of a pfile
  (relative to the project root)
* `{{ validdata }}` gets replaced by the relative path of a pfile
  (relative to the project root)
* `{{ testdata }}` gets replaced by the relative path of a pfile
  (relative to the project root)
* `{{ training }}` gets replaced by the training setup
* `{{ model_folder }}` gets replaced by the folder of a model
* `{{ nntoolkit }}` gets replaced by the (path to the) binary that is specified
  in the ~/.writemathrc