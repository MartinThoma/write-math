#!/usr/bin/env python

import urllib2
import parse_folder


def extract_wikipedia_article(article_name):
    content  = urllib2.urlopen('http://de.wikipedia.org/w/api.php?format=json&action=query&titles=Laplace-Operator&prop=revisions&rvprop=content').read()
    mathexpressions = parse_folder.extract_math_mode(content,
                                                     is_wikipedia=True)
    for expr in mathexpressions:
        expr = expr.replace("\\\\", "\\")
        symbols = parse_folder.extract_symbols(expr)
        for symbol in symbols:
            print(symbol+" in "+expr)
