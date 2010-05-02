#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2010  Stefan Haller
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


import os
import os.path
import cgi
import time
import datetime
import sys


#
# Constant definitions
#

html_header = u'''<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN">
<html>
<head>
  <title>Directory Listing</title>
  <meta http-equiv="content-type" content="text/html; charset=utf-8">
%(stylesheet)s
%(javascript)s
</head>
<body onload="init()">
  <div id="document">
    <h1>Directory Listing</h1>
    <div class="dirlisting">'''

html_javascript = u'''<script type="text/javascript">
  function highlight(elem, highl)
  {
    if (highl)
    {
      elem.style.backgroundColor = "#fff0d9";
      elem.style.border = "1px solid #ffd699";
    }
    else
    {
      elem.style.backgroundColor = "";
      elem.style.border = "1px solid #fff";
    }
  }

  function init()
  {
    var elements = document.getElementsByTagName("div");
    for (i = 0; i < elements.length; i++)
    {
      var element = elements[i];
      if (element.className == "file-entry")
      {
        element.onmouseover = function(){highlight(this, true);};
        element.onmouseout = function(){highlight(this, false);};
      }
    }
  }
</script>'''

html_stylesheet = u'''<style type="text/css">
  body {
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

  .dirlisting {
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
  }
</style>'''

html_footer = u'''    </div>
    <p style="margin-top: 4em; font-size: small;">Automatically generated
      at %(date)s (took %(time).2f seconds).</p>
  </div>
</body>
</html>'''


#
# Global variables
#

bol = True
indentation = 0
f = sys.stdout


#
# Various helper functions
#

def indent():
    global indentation
    indentation += 2

def deindent():
    global indentation
    indentation -= 2

def write_indented(string, newline = True, indent = 0):
    global bol
    if bol:
        f.write(' ' * (indentation + indent))
    f.write(string)
    if newline:
        f.write('\n')
        bol = True
    else:
        bol = False

def indent_string(string, level):
    out = []
    for line in string.split('\n'):
        out.append(u' ' * level + line)
    return '\n'.join(out)

def human_readable_filesize(filesize):
    if filesize < 1024.0:
        return u'%i B' % filesize
    units = [u'KiB', u'MiB', u'GiB', u'TiB']
    for x in units:
        filesize /= 1024.0
        if filesize < 1024.0:
            return '%.1f %s' % (filesize, x)
    return '%.1f %s' % (filesize, units[-1])

def human_readable_time(t):
    dt = datetime.datetime.fromtimestamp(t)
    return dt.strftime('%d-%b-%Y %H:%M')

def print_dir(path):
   '''list all files and directories recursively'''
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
   dirs.sort(key=str.lower)
   files.sort(key=str.lower)

   # no files/directories? -> exit
   if len(dirs) + len(files) == 0:
       return

   for d in dirs:
       npath = os.path.join(path, d)
       write_indented((u'<div class="directory-entry">' \
                       u'<div class="directory-label">%s/</div>') %
                           cgi.escape(d))
       indent()
       print_dir(npath)
       deindent()
       write_indented(u'</div>')

   for f in files:
       npath = os.path.join(path, f)
       statinfo = os.stat(npath)
       filesize = cgi.escape(human_readable_filesize(statinfo.st_size))
       modified = cgi.escape(human_readable_time(statinfo.st_mtime))

       write_indented((u'<div class="file-entry">'
                       u'<div class="file-label">'
                       u'<a href="%s">%s</a>'
                       u'</div>'
                       u'<div class="file-size">%s</div>'
                       u'<div class="file-mtime">%s</div></div>') %
                           (cgi.escape(npath, True),
                            cgi.escape(f),
                            filesize,
                            modified))


if __name__ == '__main__':
    timer = time.time()
    
    write_indented(html_header % \
                   {'stylesheet':
                        indent_string(html_stylesheet, 2),
                    'javascript':
                        indent_string(html_javascript, 2)})

    indentation = 6
    print_dir('.')
    indentation = 0

    write_indented(html_footer % \
                   {'date':
                       cgi.escape(datetime.datetime.today().strftime('%c')),
                    'time': time.clock()})
                        #time.time() - timer})