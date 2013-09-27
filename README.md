xmldirlisting
=============

What Exactly Does xmldirlisting?
--------------------------------

The xmldirlisting project allows you to easily generate an XML file which
contains the directory listing of the current working directory.  The scripts
travels downwards the whole directory tree recursively and gathers information
about the files and directories.  The resulting XML tree can be manipulated and
processed with other tools.  There are also example files included, which are
showing how to create a HTML directory listing with the help of an XSLT
stylesheet processor (will be discussed later).

Please note, that the script needs a Python 3 interpreter installed.  Most
distributions are shipping Python 2 interpreters, but they optionally provide
also the newer ones.  Because the script was written with the Python 3 syntax
in mind, another interpreter would probably fail.  So if your interpreter
complains about syntax errors, check your interpreters' version at first.


What's the License for this Project?
------------------------------------

> Copyright (C) 2010, 2011  Stefan Haller <haliner@gmail.com>
>
> This program is free software: you can redistribute it and/or modify
> it under the terms of the GNU General Public License as published by
> the Free Software Foundation, either version 3 of the License, or
> (at your option) any later version.
>
> This program is distributed in the hope that it will be useful,
> but WITHOUT ANY WARRANTY; without even the implied warranty of
> MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
> GNU General Public License for more details.
>
> You should have received a copy of the GNU General Public License
> along with this program.  If not, see <http://www.gnu.org/licenses/>.


What's Included?
----------------

 *  xmldirlisting: Python 3 script, produces XML dirlisting

 *  dirlisting.\*: Example files for use with an XML/XSLT processor.


How Should I Install the Script?
--------------------------------

There are no special needs --- you might even not install the xmldirlisting
script and instead run it within the source distribution.  But most likely you
want to install it in some way into your system.  Use the setup.py script for
doing this job.


How to Invoke?
--------------

The script will generate the directory listing for current working directory,
so you probably want to change your working directory first.  Executing the
script will make it print the xml data to it's standard output.

Example usage:

    $ ./xmldirlisting >dirlisting.xml


How Can I Further Process the XML file?
---------------------------------------

One example usage is the creation of an HTML dirlisting, which gives access to
all files of a directory.  The example files included in the source
distribution are exactly doing this.  You need an XSLT processor like
xmlstarlet, Xalan or other similar tools, if you want to use the example files.

Example usage:

    $ ./xmldirlisting >dirlisting.xml
    $ xmlstarlet tr dirlisting.xslt dirlisting.xml >index.html

The file `index.html` will now contain a full hyperlinked HTML directory
listing including all subdirectories.  It uses HTML, CSS, JavaScript and of
course XSLT for generating the HTML file.  Extending the template file might be
a good start for your own solution, which satisfies your needs.


How Can I Contact the Developer?
--------------------------------

Stefan Haller <haliner@gmail.com>

https://github.com/haliner/xmldirlisting
