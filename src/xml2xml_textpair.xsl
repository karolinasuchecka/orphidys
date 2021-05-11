<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema"
    exclude-result-prefixes="xs regexp"
    xmlns:regexp="http://exslt.org/regular-expressions"
    xpath-default-namespace="http://www.tei-c.org/ns/1.0"
    version="2.0">
    <xsl:strip-space elements="*"/>
    <xsl:output encoding="UTF-8" method="xml" indent="yes" omit-xml-declaration="no"/>
    <xsl:template match="/">
        <xsl:apply-templates/>
    </xsl:template>
    <xsl:variable name="lowercase" select="'abcdefghijklmnopqrstuvwxyzéàçè'"/>
    <xsl:variable name="uppercase" select="'ABCDEFGHIJKLMNOPQRSTUVWXYZÉÀÇÈ'"/>
    <xsl:variable name="stop" select="'.?!…'"/>
    <xsl:template match=" head | label | front | argument | label |figDesc |figure | speaker |stage[preceding-sibling::*[1][name() = 'speaker']] | stage[@type] | facsimile |div[@type='postface']"/>
    
    <xsl:template match="*">
        <xsl:element name="{local-name()}">
            <xsl:for-each select="@*">
                <xsl:attribute name="{local-name()}">
                    <xsl:value-of select="."/>
                </xsl:attribute>
            </xsl:for-each>
            <xsl:apply-templates/>
        </xsl:element>
    </xsl:template>
    
    <xsl:template match="note">
        <xsl:text> </xsl:text>
    </xsl:template>
        
    
    <!--<xsl:template match="pb[position() != 1]">
        <xsl:text> </xsl:text>
    </xsl:template>
    
    <xsl:template match="pb[position() = 1]"/>-->
    
    
   
</xsl:stylesheet>
