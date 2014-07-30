#!/usr/bin/env python

import urllib
import os

raw_data_id = 291889
urllib.urlretrieve("http://www.martin-thoma.de/write-math/raw-data/%i.svg" % raw_data_id,
                   "%i.svg" % raw_data_id)
os.system("convert -size 28x28 %i.svg  -resize 28x28 -gravity center -extent 28x28 -monochrome %i.bmp" %
          (raw_data_id, raw_data_id))
