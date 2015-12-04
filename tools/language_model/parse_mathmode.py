#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import logging
import string
import collections

try:
    unicode = unicode
except NameError as e:
    # 'unicode' is undefined, must be Python 3
    logging.info("Python 3 detected")
    str = str
    unicode = str
    bytes = bytes
    basestring = (str, bytes)
else:
    # 'unicode' exists, must be Python 2
    str = str
    unicode = unicode
    bytes = str
    basestring = basestring

logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s',
                    level=logging.DEBUG,
                    stream=sys.stdout)

# TODO: \text{$x$}
#       \hbox{$x$}


class TokenStream(object):
    def __init__(self, skip_chars=None, orig=None, filename=""):
        self.tokens = []
        self.orig = orig
        self.filename = filename
        if skip_chars is None:
            self.skip_chars = []
        else:
            self.skip_chars = skip_chars

    def append(self, token):
        if token not in self.skip_chars:
            token = token.strip()
            # TODO: Language model config file
            replace_dict = {'\\cal': '\\mathcal',
                            '\\rm': '\\mathrm',
                            '\\bf': '\\mathbf',
                            '*': '\\ast',
                            '\\ge': '\\geq',
                            '\\le': '\\leq',
                            '\\ne': '\\neq',
                            '\\to': '\\rightarrow',
                            '\\mathds': '\\mathbb',
                            }
            multi_replace = {'\\max': ['m', 'a', 'x'],
                             '\\min': ['m', 'i', 'n'],
                             '\\sin': ['s', 'i', 'n'],
                             '\\cos': ['c', 'o', 's'],
                             '\\tan': ['t', 'a', 'n'],
                             '\\ln': ['l', 'n'],
                             '\\lim': ['l', 'i', 'm'],
                             '\\log': ['l', 'o', 'g'],
                             '\\det': ['d', 'e', 't'],
                             '\\arcsec': ['a', 'r', 'c', 's', 'e', 'c'],
                             '\\tanh': ['t', 'a', 'n', 'h'],
                             '\\sinh': ['s', 'i', 'n', 'h'],
                             '\\cosh': ['c', 'o', 's', 'h'],
                             '\\ll': ['<', '<'],
                             '\\gg': ['>', '>']}
            if token in replace_dict:
                token = replace_dict[token]
            if token in multi_replace:
                for t in multi_replace[token]:
                    self.tokens.append(Token(t))
            else:
                self.tokens.append(Token(token))

    def __len__(self):
        return self.tokens.__len__()

    def postprocessing(self):
        self.postprocessing_env()
        self.postprocessing_block()
        self.postprocessing_block_consumers()
        self.unblocking()

    def postprocessing_env(self):
        """deal with environments"""
        new_tokens = []
        environments = []
        started_begin = False
        started_end = False
        started_commands = False
        sbuffer = ""
        for i, token in enumerate(self.tokens):
            if token == '\\begin':
                started_begin = True
            elif token == '\\end':
                started_end = True
            elif started_begin:
                if sbuffer == "" and token == "{":
                    continue
                elif sbuffer != "" and token == "{":
                    raise SyntaxError(('Opening curly brace directy after '
                                       'beginning of environment'))
                elif sbuffer == "" and token == "}":
                    raise SyntaxError(('closing curly brace directy after '
                                       'beginning of environment'))
                elif sbuffer != "" and token == "}":
                    new_env = Environment(sbuffer)
                    if len(environments) == 0:
                        new_tokens.append(new_env)
                    else:
                        environments[-1].append(new_env)
                    environments.append(new_env)
                    sbuffer = ""
                    started_begin = False
                    if self.tokens[i+1] == "[":
                        started_commands = True
                else:
                    sbuffer += token
            elif started_commands:
                if sbuffer == "" and token == "[":
                    continue
                elif token == "]":
                    environments[-1].commands = sbuffer
                    sbuffer = ""
                    started_commands = False
                else:
                    sbuffer += token
            elif started_end:
                if sbuffer == "" and token == "{":
                    continue
                elif sbuffer != "" and token == "{":
                    raise SyntaxError(('Opening curly brace directy after '
                                       'end of environment in file %s') %
                                      self.filename)
                elif sbuffer == "" and token == "}":
                    raise SyntaxError(('closing curly brace directy after '
                                       'end of environment in file %s') %
                                      self.filename)
                elif sbuffer != "" and token == "}":
                    # Valid end of an environment
                    if sbuffer != environments[-1].name:
                        raise SyntaxError(('closed environment %s, but %s was '
                                           'last opened') %
                                          (sbuffer, environments[-1].name))
                    else:
                        environments.pop()
                        started_end = False
                else:
                    sbuffer += token
            else:
                if len(environments) == 0:
                    new_tokens.append(token)
                else:
                    environments[-1].append(token)
        self.tokens = new_tokens

    def postprocessing_block(self):
        """Deal with blocks"""
        new_tokens = []
        blocks = []
        for token in self.tokens:
            if isinstance(token, Environment):
                new_tokens.append(token)
            elif token == '{':
                block = Block()
                if len(blocks) == 0:
                    new_tokens.append(block)
                else:
                    blocks[-1].append(block)
                blocks.append(block)
            elif token == '}':
                if len(blocks) == 0:
                    raise Exception("More closing braces than opening "
                                    "braces: %s in file '%s'" %
                                    (self.orig[:80], self.filename))
                blocks.pop()
            else:
                if len(blocks) > 0:
                    blocks[-1].append(token)
                else:
                    new_tokens.append(token)
        self.tokens = new_tokens

    def postprocessing_block_consumers(self):
        consumers = {r"\cal": True, r"\mathcal": True,
                     r"\bb": True, r"\mathbb": True,
                     r"\bf": True, r"\mathbf": True,
                     r"\rm": True, r"\mathrm": True,
                     r"\\frak": True,
                     r"\\boldmath": True,
                     r"^": False,  # r"_": False,
                     r"\label": False, r"\ref": False,  # TODO: Consume one token, but then skip
                     # r"\sqrt": False, r"\bar": False,
                     # r"\vec": False, r"\overline": False,
                     # r"\tilde": False
                     }
        multi_consumers = {r"\frac"}  # r"\over",
        current_consumer = None
        new_tokens = []
        for token in self.tokens:
            if isinstance(token, Token):
                if token in consumers:
                    current_consumer = Consumer(token,
                                                splitting=consumers[token])
                elif token in multi_consumers:
                    current_consumer = MultiConsumer(token)
                elif current_consumer is not None:
                    current_consumer.consume(token)
                    if current_consumer.is_saturated():
                        new_tokens.append(current_consumer)
                        current_consumer = None
                else:
                    new_tokens.append(token)
            else:
                if current_consumer is not None:
                    current_consumer.consume(token)
                    if current_consumer.is_saturated():
                        for t in current_consumer.tokenize():
                            new_tokens.append(t)
                        current_consumer = None
                else:
                    new_tokens.append(token)
        self.tokens = new_tokens

    def unblocking(self):
        """Remove blocks."""
        new_tokens = []
        for token in self.tokens:
            if isinstance(token, (Block, Consumer, MultiConsumer)):
                for el in token.tokenize():
                    new_tokens.append(el)
            else:
                new_tokens.append(token)
        self.tokens = new_tokens

    def __repr__(self):
        return self.tokens.__repr__()

    def __iter__(self):
        return self.tokens.__iter__()


class Token(unicode):
    def __init__(self, name):
        self.name = name

    def tokenize(self):
        return [self.name]

    def __repr__(self):
        return self.name.__repr__()


class Environment(object):
    def __init__(self, name):
        self.name = name
        self.commands = []
        self.tokens = []

    def append(self, token):
        self.tokens.append(token)

    def __repr__(self):
        return "%s[%s]{{%s}}" % (self.name,
                                 self.commands,
                                 self.tokens.__repr__())

    def __iter__(self):
        return self.tokens.__iter__()


class Block(object):
    def __init__(self):
        self.tokens = []

    def append(self, token):
        if isinstance(token, collections.Iterable):
            self.tokens.append(token)
            # for element in token:
            #    self.tokens.append(element)
        else:
            self.tokens.append(token)

    def tokenize(self):
        if len(self.tokens) == 1:
            return self.tokens
        else:
            return ['{'] + self.tokens + ['}']

    def __repr__(self):
        if len(self.tokens) == 1:
            return "%s" % self.tokens[0]
        else:
            return "BLOCK{{%s}}" % (self.tokens.__repr__())

    def __iter__(self):
        return self.tokens.__iter__()


class Consumer(object):
    def __init__(self, name, splitting=True):
        self.name = name
        self.splitting = splitting
        self.consumed = Block()
        self.is_saturated_state = False

    def consume(self, token):
        self.consumed.append(token)
        self.is_saturated_state = True

    def is_saturated(self):
        return self.is_saturated_state

    def tokenize(self):
        """
        Returns
        -------
        list
            List of Tokens
        """
        if isinstance(self.consumed, Block):
            if self.splitting:
                tokens = []
                for el in self.consumed:
                    tokens.append("%s{%s}" % (self.name, el))
            else:
                tokens = [self.name] + self.consumed.tokenize()
            return tokens
        else:
            return ["%s{%s}" % (self.name, self.consumed)]

    def __repr__(self):
        return "%s%s" % (self.name, self.consumed)


class MultiConsumer(object):
    def __init__(self, name):
        self.name = name
        self.consumed = []
        self.is_saturated_state = False

    def consume(self, token):
        block = Block()
        block.append(token)
        self.consumed.append(block)
        if len(self.consumed) == 2:
            self.is_saturated_state = True

    def is_saturated(self):
        return self.is_saturated_state

    def tokenize(self):
        """
        Returns
        -------
        list
            List of Tokens
        """
        if self.name == r'\frac':
            # TODO: That last [0]
            numerator = self.consumed[0].tokenize()[0].tokenize()
            if numerator[0] == '{' and numerator[-1] == '}':
                numerator = numerator[1:-1]
            return (['<n>'] + numerator +
                    ['</n><d>'] + self.consumed[1].tokenize() + ['</d>'])
        else:
            print("Not import")
            raise NotImplemented

    def __repr__(self):
        return "MultiConsumer%s%s" % (self.name, self.consumed)


def tokenize(text, filename=""):
    """
    Tokenize math mode text.

    Parameters
    ----------
    text : str
        Math mode content

    Returns
    -------
    list
        Tokens which are entries of the vocabulary

    Examples
    --------
    >>> tokenize(r"\sum_{i=0}^\infty i^2")[1:-1]
    ['\\\sum', '_', '{', 'i', '=', '0', '}', '^', '\\\infty', 'i', '^', '2']

    >>> tokenize(r"A = \{1,2\}")
    ['<s>', 'A', '=', '\\\{', '1', ',', '2', '\\\}', '</s>']

    >>> tokenize(r"A=\{1,2\}")
    ['<s>', 'A', '=', '\\\{', '1', ',', '2', '\\\}', '</s>']

    >>> tokenize(r"ABCDEFG")
    ['<s>', 'A', 'B', 'C', 'D', 'E', 'F', 'G', '</s>']

    >>> tokenize("\\\\rho")
    ['<s>', '\\\\rho', '</s>']

    >>> tokenize(r"A \in \mathcal{P}(A)")
    ['<s>', 'A', '\\\in', '\\\mathcal{P}', '(', 'A', ')', '</s>']

    >>> tokenize(r"a \cdot \\frac{x^2 + 1}{2}")[1:-1]
    ['a', '\\\cdot', '<n>', 'x', '^', '2', '+', '1', '</n><d>', '2', '</d>']
    """
    text = text.strip()
    tokens = TokenStream(skip_chars=[" ", "\t", "\r",  # TODO: language model config file
                                     "\\!", "\\;", "\\,", "~", "\\:",
                                     "\\quad", "\\qquad",
                                     "\\Hspace", "\\big",
                                     "^", "_"  # TODO: really?
                                     ],
                         orig=text,
                         filename=filename)
    next_token = ""
    single_tokens = ["=", "{", "}", ",", "^", "_"]
    escape = False
    last_was_escape = False
    for char in text:
        if char == "\\":
            if last_was_escape:
                tokens.append("\\")
                last_was_escape = False
            else:
                if next_token != "":
                    tokens.append(next_token)
                    next_token = ""
                next_token += char
                escape = True
                last_was_escape = True
        else:
            if escape:
                if char not in list(string.digits+string.ascii_letters):
                    if last_was_escape:
                        next_token += char
                        tokens.append(next_token)
                        next_token = ""
                    else:
                        if next_token != "":
                            tokens.append(next_token)
                            next_token = ""
                            escape = False
                        if char in single_tokens:
                            tokens.append(char)
                        else:
                            next_token += char
                else:
                    next_token += char
            else:
                tokens.append(char)
            last_was_escape = False
    if next_token != "":
        tokens.append(next_token)
        next_token = ""
        escape = False
    try:
        tokens.postprocessing()
    except Exception as inst:
        logging.debug("TokenStream.postprocessing failed: %s", inst)

    # Simplify for segmentation
    tokens = tokens.tokens
    return_tokens = []
    for token in ["<s>"] + tokens + ["</s>"]:
        if token == "</n><d>":
            return_tokens.append("\\frac")
        elif token in ["<n>", "</d>", "{", "}", "\\left", "\\right"]:
            continue
        elif isinstance(token, Block):
            for t in token.tokenize():
                return_tokens.append(token)
        elif isinstance(token, Consumer):
            for t in token.tokenize():
                return_tokens.append(token)
        elif isinstance(token, MultiConsumer):
            for t in token.tokenize():
                return_tokens.append(token)
        elif isinstance(token, Environment):
            continue
        else:
            return_tokens.append(token)
        tokens = return_tokens
    return return_tokens


def main(filename):
    import find_mathmode
    math_mode = find_mathmode.get_math_mode(filename)
    for i, el in enumerate(math_mode, start=1):
        tokens = tokenize(el)
        print("%i.\t%s" % (i, tokens))


def is_valid_file(parser, arg):
    """Check if arg is a valid file that already exists on the file
       system.
    """
    arg = os.path.abspath(arg)
    if not os.path.exists(arg):
        parser.error("The file %s does not exist!" % arg)
    else:
        return arg


def get_parser():
    from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
    parser = ArgumentParser(description=__doc__,
                            formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument("-f", "--file",
                        dest="filename",
                        required=True,
                        type=lambda x: is_valid_file(parser, x),
                        help="write report to FILE",
                        metavar="FILE")
    return parser


if __name__ == '__main__':
    import doctest
    doctest.testmod()
    # args = get_parser().parse_args()
    # main(args.filename)
