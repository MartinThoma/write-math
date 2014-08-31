#!/usr/bin/env python

"""Run everything again for a model. Adjust the model file if
   this is desired.
"""

import os
import logging
import sys
logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s',
                    level=logging.DEBUG,
                    stream=sys.stdout)
import yaml
import cPickle as pickle
# my modules
import utils
import preprocess_dataset
import create_pfiles
import train
import features
import create_model
import test


def update_model_description_file(model_description_file, raw_data):
    from collections import OrderedDict

    def ordered_load(stream, Loader=yaml.Loader,
                     object_pairs_hook=OrderedDict):
        class OrderedLoader(Loader):
            pass

        def construct_mapping(loader, node):
            loader.flatten_mapping(node)
            return object_pairs_hook(loader.construct_pairs(node))
        OrderedLoader.add_constructor(
            yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
            construct_mapping)
        return yaml.load(stream, OrderedLoader)

    def ordered_dump(data, stream=None, Dumper=yaml.Dumper, **kwds):
        class OrderedDumper(Dumper):
            pass

        def _dict_representer(dumper, data):
            return dumper.represent_mapping(
                yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
                data.items())
        OrderedDumper.add_representer(OrderedDict, _dict_representer)
        return yaml.dump(data, stream, OrderedDumper, **kwds)

    # Read the model description file
    with open(model_description_file, 'r') as ymlfile:
        md = ordered_load(ymlfile, yaml.SafeLoader)

    # Get the preprocessing information
    PROJECT_ROOT = utils.get_project_root()
    preprocessed = os.path.join(PROJECT_ROOT, md['preprocessed'],
                                "info.yml")
    # Read the preprocessing info file
    with open(preprocessed, 'r') as ymlfile:
        pd = ordered_load(ymlfile, yaml.SafeLoader)

    # Update data source
    datapath = raw_data.split("/archive/raw-datasets/")[1]
    datapath = os.path.join(datapath)
    pd['data-source'] = datapath

    # Write the file
    with open(preprocessed, 'w') as ymlfile:
        ymlfile.write(ordered_dump(pd,
                                   Dumper=yaml.SafeDumper,
                                   default_flow_style=False,
                                   indent=4).replace('-   ', '  - '))

    # TODO: Get raw path by looking at the preprocessed file
    # update preprocessed
    # note that this could change the number of input and output nodes

    # Update topology (input neurons)
    feature_list = features.get_features(md['features'])
    feature_count = sum(map(lambda n: n.get_dimension(), feature_list))
    all_except_first = ":".join(md['model']['topology'].split(":")[1:])
    new_top = str(feature_count) + ":" + all_except_first
    md['model']['topology'] = new_top

    # Update topology (output neurons = classes I want to recognize)
    tmp = pickle.load(open(raw_data, "rb"))
    output_neurons = len(tmp['formula_id2latex'])
    all_except_first = ":".join(md['model']['topology'].split(":")[:-1])
    new_top = all_except_first + ":" + str(output_neurons)
    md['model']['topology'] = new_top

    # Write the file
    with open(model_description_file, 'w') as ymlfile:
        ymlfile.write(ordered_dump(md,
                                   Dumper=yaml.SafeDumper,
                                   default_flow_style=False,
                                   indent=4).replace('-   ', '  - '))


def main(model_folder, latest_data):
    # Read the model description file
    model_description_file = os.path.join(model_folder, "model.yml")
    with open(model_description_file, 'r') as ymlfile:
        model_description = yaml.load(ymlfile)

    if model_description['model']['type'] != 'mlp':
        logging.info("The type of your model is '%s'.",
                     model_description['model']['type'])
        return 0

    # Make sure the user really wants to do this
    logging.info("Do you want to update the model with the dataset '%s'? ",
                 latest_data)
    refresh_it = utils.query_yes_no("Do you want to refresh the file '%s'?" %
                                    model_description_file,
                                    "no")
    if refresh_it:
        # Refresh the model
        update_model_description_file(model_description_file, latest_data)

    # Preprocessing
    refresh_it = utils.query_yes_no("Do you want to refresh the "
                                    "preprocessing file?",
                                    "no")
    if refresh_it:
        # Read the model description file
        with open(model_description_file, 'r') as ymlfile:
            md = yaml.load(ymlfile)
        # Get the preprocessing information
        PROJECT_ROOT = utils.get_project_root()
        preprocessed = os.path.join(PROJECT_ROOT, md['preprocessed'])
        preprocess_dataset.main(preprocessed)

    # Create pfiles
    refresh_it = utils.query_yes_no("Do you want to refresh the pfiles?",
                                    "no")
    if refresh_it:
        create_pfiles.main(model_folder)

    # Create model
    refresh_it = utils.query_yes_no(("Do you want to recreate the model? "
                                     "(save testresult_ if you want to "
                                     "keep them)"), "no")
    if refresh_it:
        # Delete all old test results
        models = [os.path.join(model_folder, name) for name in
                  os.listdir(model_folder)
                  if os.path.isfile(os.path.join(model_folder, name))]
        models = filter(lambda n: n.startswith("testresult_"), models)
        for model in models:
            logging.info("Removed '%s'." % model)
            os.remove(model)
        # Delete all old models
        models = [os.path.join(model_folder, name) for name in
                  os.listdir(model_folder)
                  if os.path.isfile(os.path.join(model_folder, name))]
        models = filter(lambda n: n.endswith(".json"), models)
        for model in models:
            logging.info("Removed '%s'." % model)
            os.remove(model)
        # Recreate it
        create_model.main(model_folder, override=True)

    # Train model
    refresh_it = utils.query_yes_no("Do you want to train the model?", "no")
    if refresh_it:
        train.main(model_folder)

    # Test model
    refresh_it = utils.query_yes_no("Do you want to test the model?", "no")
    if refresh_it:
        test_error = test.main(model_folder)
        logging.info("Test error: %0.4f", test_error)


if __name__ == '__main__':
    PROJECT_ROOT = utils.get_project_root()

    # Get latest model description file
    models_folder = os.path.join(PROJECT_ROOT, "archive/models")
    latest_model = utils.get_latest_folder(models_folder)

    # Get latest raw data file
    models_folder = os.path.join(PROJECT_ROOT, "archive/raw-datasets")
    latest_data = utils.get_latest_in_folder(models_folder, "raw.pickle")

    # Get command line arguments
    from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
    parser = ArgumentParser(description=__doc__,
                            formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument("-m", "--model",
                        dest="model",
                        help="where is the model folder (with model.yml)?",
                        metavar="FOLDER",
                        type=lambda x: utils.is_valid_folder(parser, x),
                        default=latest_model)
    parser.add_argument("-d", "--dataset",
                        dest="dataset",
                        help="which new dataset should be used?",
                        metavar="FILE",
                        type=lambda x: utils.is_valid_file(parser, x),
                        default=latest_data)
    args = parser.parse_args()
    main(args.model, args.dataset)
