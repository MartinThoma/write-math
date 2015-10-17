#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import logging
import string

logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s',
                    level=logging.DEBUG,
                    stream=sys.stdout)


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
            self.tokens.append(token)

    def __len__(self):
        return self.tokens.__len__()

    def postprocessing(self):
        self.postprocessing_env()
        self.postprocessing_block()

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
                                       'end of environment: %s') % self.orig)
                elif sbuffer == "" and token == "}":
                    raise SyntaxError(('closing curly brace directy after '
                                       'end of environment: %s') % self.orig)
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
                                    (self.orig, self.filename))
                blocks.pop()
            else:
                if len(blocks) > 0:
                    blocks[-1].append(token)
                else:
                    new_tokens.append(token)
        self.tokens = new_tokens

    def __repr__(self):
        return self.tokens.__repr__()

    def __iter__(self):
        return self.tokens.__iter__()


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
        self.tokens.append(token)

    def __repr__(self):
        return "BLOCK{{%s}}" % (self.tokens.__repr__())

    def __iter__(self):
        return self.tokens.__iter__()


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
    >>> tokenize(r"\sum_{i=0}^\infty i^2")
    ['\\\sum', '_', '{', 'i', '=', '0', '}', '^', '\\\infty', 'i', '^', '2']

    >>> tokenize(r"A = \{1,2\}")
    ['A', '=', '\\\{', '1', ',', '2', '\\\}']

    >>> tokenize(r"A=\{1,2\}")
    ['A', '=', '\\\{', '1', ',', '2', '\\\}']

    >>> tokenize(r"ABCDEFG")
    ['A', 'B', 'C', 'D', 'E', 'F', 'G']

    >>> tokenize("\\\\rho")
    ['\\\\rho']
    """
    text = text.strip()
    tokens = TokenStream(skip_chars=[" "], orig=text, filename=filename)
    next_token = ""
    # stopchars = [" ", "\t", "\r", "\n", "~",
    #              "=", "\\", "^", "_", "{", "}", ",", ";", "+", "-", "(", ")",
    #              ".", "/", "|", "'", "<", ">"]
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
                if char not in list(string.digits+string.letters):
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
        logging.debug(inst)
        logging.debug(text)
    return tokens


def main(filename):
    import find_mathmode
    math_mode = find_mathmode.get_math_mode(filename)
    for el in math_mode:
        tokens = tokenize(el)
        print(tokens)


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
    args = get_parser().parse_args()
    main(args.filename)
