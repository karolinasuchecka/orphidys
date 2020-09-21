<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema"
    exclude-result-prefixes="xs regexp tei"
    xmlns:regexp="http://exslt.org/regular-expressions"
    xmlns:tei="http://www.tei-c.org/ns/1.0"
    version="1.0">
    <xsl:strip-space elements="*"/>
    <xsl:output encoding="UTF-8" method="xml" indent="yes" omit-xml-declaration="no"/>
    <xsl:template match="/">
        <xsl:apply-templates/>
    </xsl:template>
    <xsl:variable name="lowercase" select="'abcdefghijklmnopqrstuvwxyzéàçè'"/>
    <xsl:variable name="uppercase" select="'ABCDEFGHIJKLMNOPQRSTUVWXYZÉÀÇÈ'"/>
    <xsl:variable name="stop" select="'.?!…'"/>
    <!--<xsl:template match=" head | label | front | argument | label |figDesc |figure | speaker |stage[preceding-sibling::*[1][name() = 'speaker']] "/>-->
    
    <xsl:template match="/">
        <xsl:processing-instruction name="xml-model">href="http://www.tei-c.org/release/xml/tei/custom/schema/relaxng/tei_all.rng" type="application/xml" schematypens="http://relaxng.org/ns/structure/1.0"</xsl:processing-instruction>
        <xsl:processing-instruction name="xml-model">href="http://www.tei-c.org/release/xml/tei/custom/schema/relaxng/tei_all.rng" type="application/xml" schematypens="http://purl.oclc.org/dsdl/schematron"</xsl:processing-instruction>
        <TEI  xmlns="http://www.tei-c.org/ns/1.0"><xsl:apply-templates/></TEI>
        
    </xsl:template>
    
    <xsl:template match="tei:TEI">
        <xsl:apply-templates/>
    </xsl:template>
    
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
    
    <xsl:template match="tei:milestone">
        <xsl:element name="milestone">
            <xsl:attribute name="unit">sent</xsl:attribute>
            <xsl:attribute name="n"><xsl:value-of select="count(preceding::tei:milestone)+1"/></xsl:attribute>
        </xsl:element>
    </xsl:template>
    
    <!--<xsl:template match="note">
        <xsl:text> </xsl:text>
    </xsl:template>
        
    
    <xsl:template match="pb[position() != 1]">
        <xsl:text> </xsl:text>
    </xsl:template>
    
    <xsl:template match="pb[position() = 1]"/>
    -->
    
    <!--<xsl:template match="text()[parent::l or parent::p]">
        
       <xsl:choose>
           <xsl:when test="contains(., '.') or contains(., '!') or contains(., '?')">
               <xsl:variable name="texte" select="."/>
               
                   <xsl:analyze-string select="$texte" regex="[\?!\.] ">
                       <xsl:matching-substring><xsl:choose>
                           <xsl:when test="matches(substring-after($texte, .), '[A-ZÉÈÀÇ]') and not(matches(substring-before($texte, .), '[A-Z0-9]'))">
                               <xsl:value-of select="."/> <milestone/>
                           </xsl:when>
                           <xsl:otherwise>
                               <xsl:value-of select="."/>
                           </xsl:otherwise>
                       </xsl:choose></xsl:matching-substring>
                       <xsl:non-matching-substring>
                           <xsl:value-of select="."/>
                       </xsl:non-matching-substring>
                   </xsl:analyze-string>
           </xsl:when>
       </xsl:choose>
    </xsl:template>-->
   
</xsl:stylesheet>
