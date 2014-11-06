#!/usr/bin/env python

import os
import natsort
import csv
#
import utils
import test


def main(models_folder, postfix="-recording", output="errors_by_epoch.csv"):
    os.chdir(models_folder)
    # Get all test errors
    #files = natsort.natsorted(os.listdir(models_folder))
    folders = [x[0] for x in os.walk(models_folder)]
    folders = filter(lambda n: n.endswith(postfix), folders)
    testerrors = []
    for i, filename in enumerate(files):
        testerrors.append((i+1, test.get_error_from_logfile(filename)))

    # Get validation errors
    validationerrors = []
    logfile = utils.get_latest_in_folder(models_folder, ".json.log")
    with open(logfile) as f:
        content = f.readlines()
    for line in content:
        if "validation error" in line:
            tmp = line.split("validation error")[1]
            validationerrors.append(float(tmp))

    # Write the csv file
    with open(output, 'wb') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',',
                                quotechar='"', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow(["epoch", "validationerror", "testerror"])
        i = 0
        for epoch, testerror in testerrors:
            spamwriter.writerow([epoch, validationerrors[i], testerror])
            i += 1

if __name__ == "__main__":
    project_root = utils.get_project_root()

    # Get latest model folder
    models_folder = os.path.join(project_root, "models")
    latest_model = utils.get_latest_folder(models_folder)

    from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
    parser = ArgumentParser(description=__doc__,
                            formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument("-m", "--model",
                        dest="model",
                        help="where is the model folder (with the info.yml)?",
                        metavar="FILE",
                        type=lambda x: utils.is_valid_folder(parser, x),
                        default=latest_model)
    args = parser.parse_args()
    main(args.model)
