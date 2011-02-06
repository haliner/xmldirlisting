<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">
  <xsl:output method="html" indent="yes"/>

  <!--
    This template matches the root element of the dirlisting xml file.

    The basic html structure is generated. Then the templates for the
    directories and file are applied and the elements are sorted by their
    file or directory name.
  -->
  <xsl:template match="/dirlisting">
    <html>
      <head>
        <title>Directory Listing</title>
        <link rel="stylesheet" type="text/css" href="dirlisting.css"/>
        <script type="text/javascript" src="dirlisting.js"/>
      </head>
      <body>
        <div id="document">
          <h1>Directory Listing</h1>
          <div id="dirlisting">
            <xsl:apply-templates select="directory">
              <xsl:sort select="@name"/>
            </xsl:apply-templates>
            <xsl:apply-templates select="file">
              <xsl:sort select="@name"/>
            </xsl:apply-templates>
          </div>
          <p class="generator">
            Automatically generated with free software
            “<a href="https://launchpad.net/xmldirlisting/">xmldirlisting</a>”.
          </p>
        </div>
      </body>
    </html>
  </xsl:template>

  <!--
    This template matches a directory element.

    Creates a new container and then outputs the name of the directory followed
    by a slash. The templates for directories and files are applied. The
    elements are sorted by their file or directory name.
  -->
  <xsl:template match="directory">
    <div class="directory">
      <div class="directory-label">
        <xsl:value-of select="@name"/>
        <xsl:text>/</xsl:text>
      </div>
      <xsl:apply-templates select="directory">
        <xsl:sort select="@name"/>
      </xsl:apply-templates>
      <xsl:apply-templates select="file">
        <xsl:sort select="@name"/>
      </xsl:apply-templates>
    </div>
  </xsl:template>

  <!--
    This template matches a file element.

    Creates a new container for the file and outputs a relative link to this
    file. The link starts with "./". All directory-names on the ancestor-axis
    are appended to the link. Finally the filename is appended and the link
    is completed.
  -->
  <xsl:template match="file">
    <div class="file">
      <div class="file-label">
        <a>
          <xsl:attribute name="href">
            <xsl:text>./</xsl:text>
            <xsl:for-each select="ancestor::directory">
              <xsl:value-of select="@name"/>
              <xsl:text>/</xsl:text>
            </xsl:for-each>
            <xsl:value-of select="@name"/>
          </xsl:attribute>
          <xsl:value-of select="@name"/>
        </a>
      </div>
    </div>
  </xsl:template>
</xsl:stylesheet>
