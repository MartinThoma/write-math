#!/usr/bin/env python
# -*- coding: utf-8 -*-

from argparse import ArgumentParser
import sys


class Tree(object):
    """A tree class."""
    def __init__(self, name, parent):
        self.name = name
        self.nodes = []
        self.parent = parent
        self.options = ""
        self.arguments = []
        self.is_environment = False
        if parent is None:
            self.is_mathmode = False
        else:
            self.is_mathmode = parent.is_mathmode
        self.is_displaystyle = False
        self.is_comment = False

    def append(self, new_node):
        """
        Parameters
        ----------
        new_node : Node
            Append it to the list of nodes of the tree.
        """
        assert isinstance(new_node, Tree)
        self.nodes.append(new_node)

    def __str__(self):
        if self.is_environment:
            out = "Environment: %s" % (self.name)
        else:
            out = "Node: %s" % (self.name)

        if self.is_mathmode and not self.is_displaystyle:
            out += " (mathmode)"
        elif self.is_mathmode and self.is_displaystyle:
            out += " (mathmode, displaystyle)"

        if self.options.strip() != "":
            out += "[options:%s]" % self.options

        for arg in self.arguments:
            out += "{arg:%s} " % str(arg)
        out += "\n"
        indent = " " * 4
        for node in self.nodes:
            for line in str(node).split('\n'):
                out += indent + line + "\n"
            out += "\n"
        return out.strip()


class Parser(object):
    """
    A parser which reads LaTeX text and gets the structure.

    Parameters
    ----------
    content : str
        LaTeX formatted string
    """
    def __init__(self, content):
        self.content = content
        self.symbol_table = {}
        self.root = Tree("Main", None)
        self._current_node = self.root
        self._command_name_started = False
        self._strbuffer = ""
        self._environment_name_started = False
        self._argument_started = False
        self._command_options = True
        self._readchar = -1
        self._options_started = False
        self._command_arguments = {'\\newcommand': 2, '\\documentclass': 1}

    def _append_command(self):
        """
        Append the currently handled command to the tree.
        """
        new_node = Tree(self._strbuffer, self._current_node)
        self._current_node.append(new_node)
        self._current_node = new_node

    def _ascend(self):
        """
        Go up in the tree to the parent.
        """
        self._current_node = self._current_node.parent

    def _print_status(self, line, char):
        """
        Parameters
        ----------
        line : int
        char : str
        """
        print("This should not happen (line %i)" % line)
        print("strbuffer:\t%s" % self._strbuffer)
        print("char:\t%s" % char)
        print("readchar:\t%i" % self._readchar)
        print("### State")
        print("current node name:\t%s" % self._current_node.name)
        print("options_started:\t%r" % self._options_started)
        print("arguments_started:\t%r" % self._argument_started)
        print("command_name_started:\t%r" % self._command_name_started)
        print("is_mathmode:\t\t%r" % self._current_node.is_mathmode)
        print("is_displaystyle:\t%r" % self._current_node.is_displaystyle)
        print("### Root")
        print(self.root)
        sys.exit(-1)

    def _handle_backslash(self):
        """
        A backslash was just seen. Deal with it.
        """
        if self._command_name_started:
            if self._strbuffer == "\\":
                # It's a \\
                self._strbuffer += "\\"
                self._append_command()
                self._strbuffer = ""
                self._command_name_started = False
                if self._environment_name_started or \
                   self._command_options:
                    self._print_status(90, "\\")
            else:
                # The name of the command is now over and a new command
                # begins
                self._append_command()
                self._strbuffer = "\\"
        else:
            # No command started so far
            self._command_name_started = True
            if self._strbuffer != '':
                new_node = Tree(self._strbuffer, self._current_node)
                self._current_node.append(new_node)
            self._strbuffer = "\\"

    def _handle_dollar(self):
        """
        A dollar sign was just seen. Deal with it.
        """
        if self._strbuffer == "\\":
            # escaped dollar sign
            self._strbuffer += "$"
        else:
            # It's not escapted
            if self._strbuffer == "$":
                self._strbuffer += "$"
                if self._current_node.name == "$$":
                    self._ascend()
                else:
                    self._print_status(123, "double dollar ($$)")
            else:
                new_node = Tree(self._strbuffer, self._current_node)
                if self._current_node.is_mathmode:
                    self._current_node.append(new_node)
                    self._ascend()
                    self._strbuffer = ""
                else:
                    self._current_node.append(new_node)
                    new_node = Tree("$", self._current_node)
                    new_node.is_mathmode = True
                    self._current_node.append(new_node)
                    self._strbuffer = ""
            self._command_name_started = False

    def _handle_open_bracket(self):
        """
        A '[' was just seen. Deal with it.
        """
        if self._current_node.is_mathmode:
            self._strbuffer += "["
        elif self._strbuffer == "\\":
            self._append_command()
            self._current_node.is_mathmode = True
            self._current_node.is_displaystyle = True
        elif self._command_name_started:
            # Add the new command to the tree
            self._append_command()
            # Start recording its options
            self._strbuffer = ""
            self._command_options = True
            self._command_name_started = False
        else:
            # It was something different, e.g. math mode
            self._strbuffer += "["
            self._print_status(122, "[")

    def _handle_close_bracket(self):
        """
        A ']' was just seen. Deal with it.
        """
        if self._current_node.is_mathmode:
            if self._strbuffer == "\\":
                # Finished math mode
                # self._ascend
                pass
            else:
                self._strbuffer += "]"
        elif self._command_options:
            # The options ended
            self._current_node.options = self._strbuffer
            self._strbuffer = ""
            self._command_options = False
        else:
            # It was something different, e.g. math mode
            self._strbuffer += "]"

    def _handle_space(self):
        """
        A ' ' was just seen. Deal with it.
        """
        self._current_node.append(Tree(self._strbuffer, self._current_node))
        self._strbuffer = ""
        self._command_name_started = False
        if self._environment_name_started:
            self._print_status(self, 146, " ")

    def _handle_open_curly(self):
        """
        A '{' was just seen. Deal with it.
        """
        if self._command_name_started:
            if self._strbuffer == "\\begin":
                self._environment_name_started = True
            elif self._strbuffer == "\\end":
                self._environment_name_started = False
            else:
                self._argument_started = True
                self._append_command()
                self._strbuffer = ""
                self._command_name_started = False
        if self._environment_name_started:
            self._strbuffer = ""
        else:
            self._argument_started = True

    def _handle_close_curly(self):
        """
        A '}' was just seen. Deal with it.
        """
        if self._command_name_started:
            if self._strbuffer == "\\begin":
                self._environment_name_started = True
            elif self._strbuffer == "\\end":
                self._environment_name_started = False
            elif self._argument_started:
                self._current_node.arguments.append(self._strbuffer)
                self._command_name_started = False
                self._argument_started = False

                tmp = self._command_arguments[self._current_node.name]
                if len(self._current_node.arguments) == tmp:
                    self._ascend()
            else:
                self._append_command()
                self._strbuffer = ""
                # self._ascend()
        elif self._environment_name_started:
            self._environment_name_started = False
            self._append_command()
            self._strbuffer = ""
        elif self._argument_started:
            self._current_node.arguments.append(self._strbuffer)
            self._argument_started = False
            self._strbuffer = ""
            tmp = self._command_arguments[self._current_node.name]
            if len(self._current_node.arguments) == tmp:
                self._ascend()
        else:
            self._print_status(210, "}")

    def _handle_percentage(self):
        """
        A '%' was just seen. Deal with it.
        """
        if self._strbuffer.endswith("\\"):
            self._strbuffer += "%"
        else:
            self._current_node.is_comment = True

    def _handle_newline(self):
        """
        A '\n' was just seen. Deal with it.
        """
        if self._current_node.is_comment:
            # self._ascend
            pass

    def parse(self):
        """
        Go through self.conetent and get the structure of it.

        Returns
        -------
        tuple
            (symbol table, root) - TODO - give an example
        """
        for i, char in enumerate(self.content):
            self._readchar = i
            if char == "\\":  # This is an escaped single slash
                self._handle_backslash()
            elif char == "$":
                self._handle_dollar()
            elif char == "[":
                self._handle_open_bracket()
            elif char == "]":
                self._handle_close_bracket()
            elif char == " ":
                self._handle_space()
            elif char == "{":
                self._handle_open_curly()
            elif char == "}":
                self._handle_close_curly()
            elif char == "%":
                self._handle_percentage()
            elif char == "\n":
                self._handle_newline()
            else:
                self._strbuffer += char
        return self.symbol_table, self.root


def parse(filename):
    """
    Read a file and LaTeX formatted text file and return its structure.

    Parameters
    ----------
    filename : str
        Path to a file

    Returns
    -------
    tuple
        (symbol table, root) - TODO - give an example
    """
    with open(filename) as f:
        content = f.read().strip()
    p = Parser(content[:150])
    return p.parse()

if __name__ == '__main__':
    parser = ArgumentParser()

    filename = "/home/moose/Downloads/1406.5173v1_FILES/ms.tex"
    # Add more options if you like
    parser.add_argument("-f", "--file", dest="filename",
                        default=filename,
                        help="write report to FILE", metavar="FILE")
    args = parser.parse_args()
    symbol_table, parsed = parse(args.filename)
    print(symbol_table)
    print(parsed)
