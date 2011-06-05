<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">

  <!--
    A HTML file should be generated.
  -->
  <xsl:output
     method="html"
     doctype-public="-//W3C//DTD XHTML 1.0 Strict//EN"
     doctype-system="http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd"
  />

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
    is completed. The modification time of the file is output as is. File
    size suffixes are used to make them more readable.
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
      <div class="file-size">
        <xsl:choose>
          <xsl:when test="@size > 1073741824">
            <xsl:value-of select="format-number(@size div 1073741824, '0.00')"/>
            <xsl:text> GB</xsl:text>
          </xsl:when>
          <xsl:when test="@size > 1048576">
            <xsl:value-of select="format-number(@size div 1048576, '0.00')"/>
            <xsl:text> MB</xsl:text>
          </xsl:when>
          <xsl:when test="@size > 1024">
            <xsl:value-of select="format-number(@size div 1024, '0.00')"/>
            <xsl:text> KB</xsl:text>
          </xsl:when>
          <xsl:otherwise>
            <xsl:value-of select="@size"/>
            <xsl:text> B</xsl:text>
          </xsl:otherwise>
        </xsl:choose>
      </div>
      <div class="file-mtime">
        <xsl:value-of select="@mtime"/>
      </div>
    </div>
  </xsl:template>
</xsl:stylesheet>
