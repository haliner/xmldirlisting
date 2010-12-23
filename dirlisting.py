#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2010  Stefan Haller <haliner@googlemail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

'''
This small script generates a html file containing a full listing of the
current directory. The directory tree is displayed as a tree of nested
div-elements. All files a represented as links, so the user can easily
navigate to these files. The output is valid HTML 4 (strict) and utf-8
encoded.

The main use case of this script for me is Dropbox: Dropbox lets you
share only single files, but not whole folders. But no-one prevents you
from uploading a html page that allows everyone to access every file in
the Dropbox ;)

'''

import cgi
import datetime
import optparse
import os.path
import time
import sys


html = {

'header-1':
u'''<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN">
<html>
<head>
  <title>%(title)s</title>
  <meta http-equiv="content-type" content="text/html; charset=utf-8">''',

'stylesheet-start':
u'''  <style type="text/css">''',

'stylesheet-end':
u'''  </style>''',

'stylesheet-external':
u'''  <link rel="stylesheet" type="text/css" href="%(stylesheet-path)s" />''',

'javascript-start':
u'''  <script type="text/javascript">''',

'javascript-external':
u'''  <script type="text/javascript" src="%(javascript-path)s" /></script>''',

'javascript-end':
u'''  </script>''',

'header-2':
u'''</head>
<body>
  <div id="document">
    <h1>%(title)s</h1>
    <div id="dirlisting">''',

'footer':
u'''    </div>
    <p style="margin-top: 4em; font-size: small;">Automatically generated with free software &ldquo;dirlisting.py&rdquo; at %(date)s (took %(time).2f seconds).</p>
  </div>
</body>
</html>''',

'stylesheet':
u'''body {
  color: #444;
  background-color: #eee;
  font-family: Georgia, sans;
  margin: 16px;
}

#document {
  background-color: #fff;
  padding: 32px;
  border-width: 3px;
  border-style: solid;
  border-color: #ddd #aaa #aaa #ddd;
  min-width: 600px;
}

h1 {
  font-family: "Trebuchet MS", sans;
  background-color: #aaa;
  color: #fff;
  margin-top: 8px;
  margin-bottom: 32px;
  margin-left: 16px;
  margin-right: 32px;
  padding: 16px;
  padding-left: 64px;
  border: 1px solid #444;
}

a {
  text-decoration: none;
}

a:link {
  color: #ff9900;
}

a:visited {
  color: #8f5600;
}

a:hover {
  color: #bf7300;
  text-decoration: underline;
}

a:focus {
  color: #bf7300;
}

a.js {
  color: #ff9900;
}

#dirlisting {
  line-height: 140%;
}

.directory-entry, .file-entry {
  margin-left: 5px;
  padding-left: 20px;
  border: 1px solid #fff;
}

.file-entry{
  position: relative;
}

.directory-label {
  font-style: italic;
}

.directory-label a {
  color: #555;
}

.file-label {
  margin-right: 300px;
}

.file-size, .file-mtime {
  position: absolute;
  color: #999;
  font-size: small;
  top: 0;
  bottom: 0;
}

.file-size {
  right: 200px;
}

.file-mtime {
  right: 40px;
}''',

'javascript':
u'''function highlightFile(elem, highl)
{
  elem.style.backgroundColor = highl ? "#fff0d9": "";
  elem.style.border          = highl ? "1px solid #ffd699" : "1px solid #fff";
}

function fold(root, collapse, recursive)
{
  var elem = root.firstElementChild;
  while (elem)
  {
    if ((elem.className == "file-entry") ||
        (elem.className == "directory-entry"))
    {
      elem.style.display = collapse ? "none" : "";
    }
    if ((recursive) &&
        (elem.className == "directory-entry"))
    {
      fold(elem, collapse, recursive);
    }
    elem = elem.nextElementSibling;
  }
}

function foldAll(collapse)
{
  var elem = document.getElementById("dirlisting").firstElementChild;
  while (elem)
  {
    if ((elem.className == "file-entry") ||
        (elem.className == "directory-entry"))
    {
      fold(elem, collapse, true);
    }
    elem = elem.nextElementSibling;
  }
}

function getFolding(root)
{
  var elem = root.firstElementChild;
  while (elem)
  {
    if ((elem.className == "file-entry") ||
        (elem.className == "directory-entry"))
    {
      return elem.style.display == "none"
    }
    elem = elem.nextElementSibling;
  }
  return false;
}

function toggleFolding(elem)
{
  fold(elem, !getFolding(elem), false);
}

function attachEventHandler(root)
{
  var elem = root.firstElementChild;
  while (elem)
  {
    if (elem.className == "file-entry")
    {
      elem.onmouseover = function(){highlightFile(this, true);};
      elem.onmouseout = function(){highlightFile(this, false);};
    }
    if (elem.className == "directory-label")
    {
      var html = elem.innerHTML;
      elem.innerHTML = '<a href="#">' + html + '</a>';
      elem.firstElementChild.onclick = function(){
          toggleFolding(this.parentNode.parentNode);
          return false;
        };
    }
    if (elem.className == "directory-entry")
    {
      attachEventHandler(elem);
    }
    elem = elem.nextElementSibling;
  }
}

function init()
{
  attachEventHandler(document.getElementById("dirlisting"))
  foldAll(true);

  var elem = document.createElement("p");
  elem.innerHTML =
    'Directory Tree Control: ' +
    '<a class="js" onclick="foldAll(false);return false;" href="#">' +
      'Expand All' +
    '</a> | ' +
    '<a class="js" onclick="foldAll(true);return false;" href="#">' +
      'Collapse All' +
    '</a>';
  document.getElementById("document").insertBefore(
    elem,
    document.getElementById("dirlisting"));
}

window.onload = init;'''

}


class IndentedWriter(object):
    def __init__(self):
        self.bol = True
        self.indentation = 0
        self.stream = None


    def open(self, filename):
        if filename == u'-':
            self.stream = sys.stdout
        else:
            self.stream = open(filename, 'w')


    def close(self):
        if self.stream is not sys.stdout:
            self.stream.close()


    def indent(self, level=1):
        self.indentation += 2 * level


    def deindent(self, level=1):
        self.indentation -= 2 * level


    def indent_string(self, string, level):
        out = []
        for line in string.split(u'\n'):
            out.append(u' ' * level + line)
        return u'\n'.join(out)


    def write(self, string, newline=True, indentation=0):
        string = self.indent_string(string, self.indentation + indentation)
        if newline:
            string += u'\n'
        self.stream.write(string.encode('utf-8'))



class Dirlisting(object):
    def __init__(self):
        self.writer = None
        self.options = None
        self.args = None
        self.substitutions = None


    def parse_params(self):
        op = optparse.OptionParser(version='0.2')

        op.add_option('--print-stylesheet', dest='print_stylesheet',
                    action='store_true', default=False,
                    help='print standard stylesheet and exit')

        op.add_option('--print-javascript', dest='print_javascript',
                    action='store_true', default=False,
                    help='print standard stylesheet and exit')

        op.add_option('-t', '--title', dest='title', default='Directory Listing',
                    help='set title to TITLE', metavar='TITLE')

        op.add_option('-o', '--output', dest='filename', default='-',
                    help='write output to FILE', metavar='FILE')

#        op.add_option('-e', '--exclude', dest='exclude', action='append',
#                    help='exclude files matching PATTERN', metavar='PATTERN')
#
#        op.add_option('-r', '--exclude-regexp', dest='exclude_re', action='append',
#                    help='exclude files matching REGEXP', metavar='REGEXP')

        op.add_option('-s', '--stylesheet', dest='stylesheet',
                    help='use FILE as external stylesheet file', metavar='FILE')

        op.add_option('-j', '--javascript', dest='javascript',
                    help='use FILE as external javascript file', metavar='FILE')

        op.add_option('-d', '--disable-javascript', dest='disable_javascript',
                      action='store_true', default=False)

        (self.options, self.args) = op.parse_args()

        # decode input as utf-8
        for i in ('title', 'filename', 'stylesheet', 'javascript'):
            attr = getattr(self.options, i)
            if attr is not None:
                attr = attr.decode('utf-8')
                setattr(self.options, i, attr)


    def print_stylesheet(self):
        self.writer.write(html['stylesheet'])


    def print_javascript(self):
        self.writer.write(html['javascript'])


    def process_dir(self, path):
        def human_readable_filesize(filesize):
            units = (u'%i B', u'%.1f KiB', u'%.1f MiB', u'%.1f GiB')
            x = 0;
            while filesize / 1024**x >= 1024:
                x +=1
            if x >= len(units):
                x = len(units)-1
            return units[x] % (float(filesize) / float(1024**x))

        def human_readable_time(t):
            dt = datetime.datetime.fromtimestamp(t)
            return unicode(dt.strftime('%d-%b-%Y %H:%M'))

        filelist = os.listdir(path)

        # split filelist into directories and files
        dirs = []
        files = []
        for filename in filelist:
            p = os.path.join(path, filename)
            if os.path.isdir(p):
                dirs.append(filename)
            if os.path.isfile(p):
                files.append(filename)

        # sort lists alphabetically
        dirs.sort(key=unicode.lower)
        files.sort(key=unicode.lower)

        for d in dirs:
            npath = os.path.join(path, d)
            self.writer.write(u'<div class="directory-entry">' \
                              u'<div class="directory-label">%s/</div>' % \
                                  cgi.escape(d))
            self.writer.indent()
            self.process_dir(npath)
            self.writer.deindent()
            self.writer.write(u'</div>')

        for f in files:
            npath = os.path.join(path, f)

            if hasattr(os.path, 'samefile'):
                if self.options.filename != '-' and \
                os.path.samefile(npath, self.options.filename):
                    continue

            statinfo = os.stat(npath)
            filesize = human_readable_filesize(statinfo.st_size)
            modified = human_readable_time(statinfo.st_mtime)

            if os.sep != '/':
                npath = npath.replace(os.sep, '/')

            self.writer.write((u'<div class="file-entry">'
                               u'<div class="file-label">'
                               u'<a href="%s">%s</a>'
                               u'</div>'
                               u'<div class="file-size">%s</div>'
                               u'<div class="file-mtime">%s</div></div>') %
                                 (cgi.escape(npath, True),
                                  cgi.escape(f),
                                  cgi.escape(filesize),
                                  cgi.escape(modified)))


    def dirlisting(self):
        self.substitutions = {
            'title': cgi.escape(self.options.title),
            'date': cgi.escape(datetime.datetime.today().strftime('%c')),
            'time': time.time(),
            'stylesheet-path': self.options.stylesheet,
            'javascript-path': self.options.javascript
        }

        for i in ('stylesheet-path', 'javascript-path'):
            if self.substitutions[i] is not None:
                self.substitutions[i] = cgi.escape(self.substitutions[i], True)

        self.writer.write(html['header-1'] % self.substitutions)

        if self.substitutions['stylesheet-path'] is None:
            self.writer.write(html['stylesheet-start'] % self.substitutions)
            self.writer.indent(2)
            self.writer.write(html['stylesheet'])
            self.writer.deindent(2)
            self.writer.write(html['stylesheet-end'] % self.substitutions)
        else:
            self.writer.write(html['stylesheet-external'] % self.substitutions)

        if not self.options.disable_javascript:
            if self.substitutions['javascript-path'] is None:
                self.writer.write(html['javascript-start'] % self.substitutions)
                self.writer.indent(2)
                self.writer.write(html['javascript'])
                self.writer.deindent(2)
                self.writer.write(html['javascript-end'] % self.substitutions)
            else:
                self.writer.write(html['javascript-external'] %
                                    self.substitutions)

        self.writer.write(html['header-2'] % self.substitutions)

        self.writer.indent(3)
        self.process_dir(u'.')
        self.writer.deindent(3)

        self.substitutions['time'] = time.time() - self.substitutions['time']

        self.writer.write(html['footer'] % self.substitutions)


    def main(self):
        self.parse_params()

        self.writer = IndentedWriter()
        self.writer.open(self.options.filename)

        if self.options.print_stylesheet:
            self.print_stylesheet()
        elif self.options.print_javascript:
            self.print_javascript()
        else:
            self.dirlisting()

        self.writer.close()


if __name__ == '__main__':
    dl = Dirlisting()
    dl.main()
