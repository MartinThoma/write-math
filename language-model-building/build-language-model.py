#!/usr/bin/env python

import re
import urllib2


def extract_math_mode(text):
    singledollar = re.compile('\$(.*?)\$')
    a = singledollar.findall(text)
    doubledollar = re.compile('\$\$(.*?)\$\$')
    b = doubledollar.findall(text)
    #newmath = re.compile('\\\[(.*?)\\\]')
    #c = newmath.findall(text)
    #print(c)
    newmath = re.compile('<math>(.*?)</math>')
    c = newmath.findall(text)
    return a + b + c


def extract_symbols(text):
    symbol = re.compile(r'(\\[A-Za-z]+)')
    return symbol.findall(text)


def main():
    fn = '/home/moose/Downloads/LaTeX-examples/documents/GeoTopo/Kapitel3.tex'
    with open(fn) as f:
        content = f.read()
    content  = urllib2.urlopen('http://de.wikipedia.org/w/api.php?format=json&action=query&titles=Laplace-Operator&prop=revisions&rvprop=content').read()
    mathexpressions = extract_math_mode(content)
    for expr in mathexpressions:
        expr = expr.replace("\\\\", "\\")
        #print(expr)
        symbols = extract_symbols(expr)
        for symbol in symbols:
            print(symbol+" in "+expr)

if __name__ == "__main__":
    main()
