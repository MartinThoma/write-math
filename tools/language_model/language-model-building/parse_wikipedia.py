#!/usr/bin/env python

import urllib2
import parse_folder


def main():
    """
    Get the content from a wikipedia page.
    """
    url = ('http://de.wikipedia.org/w/api.php?format=json'
           '&action=query'
           '&titles=Laplace-Operator'
           '&prop=revisions&rvprop=content')
    extract_wikipedia_article(url)


def extract_wikipedia_article(article_name):
    """
    Parameters
    ----------
    article_name : str
        URL to a wikipedia article
    """
    content = urllib2.urlopen(article_name).read()
    mathexpressions = parse_folder.extract_math_mode(content,
                                                     is_wikipedia=True)
    for expr in mathexpressions:
        expr = expr.replace("\\\\", "\\")
        symbols = parse_folder.extract_symbols(expr)
        for symbol in symbols:
            print(symbol+" in "+expr)

if __name__ == '__main__':
    main()
