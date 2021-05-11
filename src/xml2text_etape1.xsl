<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema"
    exclude-result-prefixes="xs regexp"
    xmlns:regexp="http://exslt.org/regular-expressions"
    version="1.0">
    <xsl:strip-space elements="*"/>
    <xsl:output encoding="UTF-8" method="text"/>
    <xsl:template match="/">
        <xsl:apply-templates select=".//body"></xsl:apply-templates>
    </xsl:template>
    <xsl:variable name="lowercase" select="'abcdefghijklmnopqrstuvwxyzéàçè'"/>
    <xsl:variable name="uppercase" select="'ABCDEFGHIJKLMNOPQRSTUVWXYZÉÀÇÈ'"/>
    <xsl:variable name="stop" select="'.?!…'"/>
    <xsl:template match="speaker | note | pb | head | label | teiHeader | front | argument | label |figDesc |figure"/>
    
    <xsl:template match="p[not(parent::note)] | stage">
        <xsl:apply-templates/><xsl:text>
</xsl:text>
    </xsl:template>
    
    <xsl:template match="l">
       
        <xsl:choose>
            <xsl:when test="preceding-sibling::l and substring(preceding-sibling::l[1], string-length(preceding-sibling::l[1]), 1) != '.' and substring(preceding-sibling::l[1], string-length(preceding-sibling::l[1]), 1) != '?' and substring(preceding-sibling::l[1], string-length(preceding-sibling::l[1]), 1) != '!' and substring(preceding-sibling::l[1], string-length(preceding-sibling::l[1]), 1) != '…' and substring(preceding-sibling::l[1], string-length(preceding-sibling::l[1]), 1) != '»'">
		<xsl:apply-templates mode="translate"/><xsl:text> </xsl:text>
                </xsl:when>
            <xsl:otherwise>
                <xsl:apply-templates/><xsl:text> </xsl:text>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>

<xsl:template match="*/text()" mode="translate">
<xsl:value-of select="concat(translate(substring(., 1, 1), $uppercase, $lowercase), substring(., 2))"/>
</xsl:template>

<xsl:template match="note" mode="translate"/>
</xsl:stylesheet>
