#!/usr/bin/env python

"""
Create a json file which maps unicode decimal codepoints to descriptions.

https://github.com/w3c/xml-entities is used for that.
"""

import json

data = {}

import xml.etree.ElementTree
e = xml.etree.ElementTree.parse('xml-entities/unicode.xml').getroot()
for atype in e.findall('charlist'):
    print("## Charlist found")
    for character in atype.findall('character'):
        try:
            dec = int(character.get('dec'))
            desc = ''
            for description in character.findall('description'):
                desc = description.text
            # print("%s: - %s" % (dec, desc))
            data[dec] = desc
        except:
            # Just ignore errors
            pass

with open('unicode.json', 'w') as outfile:
    json.dump(data, outfile, sort_keys=True, indent=1)
