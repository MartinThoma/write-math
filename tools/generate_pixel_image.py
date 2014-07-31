#!/usr/bin/env python

import urllib
import os
import Image

raw_data_id = 291889
n = 28

url = "http://localhost/write-math/website/raw-data/"
urllib.urlretrieve("{url}{id}.svg".format(url=url, id=raw_data_id),
                   "%i.svg" % raw_data_id)
command = ("convert -size 28x28 {id}.svg  -resize {n}x{n} -gravity center "
           "-extent {n}x{n} -monochrome {id}.png").format(id=raw_data_id,
                                                          n=n,
                                                          url=url)
os.system(command)
im = Image.open("%i.png" % raw_data_id)
pix = im.load()
pixel_image = [[0 for i in range(28)] for j in range(28)]
for x in range(28):
    for y in range(28):
        pixel_image[x][y] = pix[x, y]
print(pixel_image)
