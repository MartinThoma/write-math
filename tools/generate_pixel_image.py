#!/usr/bin/env python

import urllib
import os
import Image


def get_svg(raw_data_id):
    url = "http://localhost/write-math/website/raw-data/"
    urllib.urlretrieve("{url}{id}.svg".format(url=url, id=raw_data_id),
                       "%i.svg" % raw_data_id)


def main(raw_data_id=291889, n=28):
    get_svg(raw_data_id)
    command = ("convert -size {n}x{n} "
               "{id}.svg "
               "-resize {n}x{n} -gravity center "
               "-extent {n}x{n} "
               "-monochrome "
               "{id}.png").format(id=raw_data_id, n=n)
    os.system(command)
    im = Image.open("%i.png" % raw_data_id)
    pix = im.load()
    pixel_image = [[0 for i in range(n)] for j in range(n)]
    for x in range(n):
        for y in range(n):
            pixel_image[x][y] = pix[x, y]
    print(pixel_image)

if __name__ == '__main__':
    from argparse import ArgumentParser
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("-n", dest="n",
                        help="size of the N x N pixel image",
                        metavar="N", type=int, default=28)
    parser.add_argument("--raw_data_id", dest="raw_data_id",
                        help="raw data id that gets fetched",
                        metavar="ID", type=int, default=291889)
    args = parser.parse_args()
    main(args.raw_data_id, args.n)
