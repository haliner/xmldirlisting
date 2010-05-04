# -*- coding: utf-8 -*-
import sys

class IndentedWriter(object):
    def __init__(self):
        self.bol = True
        self.indentation = 0
        self.f = None

    def open(self, filename):
        if filename == '-':
            self.f = sys.stdout
        else:
            self.f = open(filename, w)

    def close(self):
        if self.f is not sys.stdout:
            self.f.close()

    def indent(self):
        self.indentation += 2

    def deindent(self):
        self.indentation -= 2

    def indent_string(self, string, level):
        out = []
        for line in string.split('\n'):
            out.append(u' ' * level + line)
        return '\n'.join(out)

    def write(self, string, newline=True, indentation=0):
        string = self.indent_string(string, self.indentation + indentation)
        if newline:
            string += '\n'
        f.write(string)
