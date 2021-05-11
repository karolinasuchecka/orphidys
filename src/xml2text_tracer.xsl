<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema"
    xmlns:tei="http://www.tei-c.org/ns/1.0"
    exclude-result-prefixes="xs tei regexp"
    xmlns:regexp="http://exslt.org/regular-expressions"
    version="2.0">
    <xsl:strip-space elements="*"/>
    <xsl:output encoding="UTF-8" method="text" indent="no"/>
    <xsl:template match="/">
        <xsl:apply-templates select=".//tei:body"></xsl:apply-templates>
    </xsl:template>
    <xsl:variable name="lowercase" select="'abcdefghijklmnopqrstuvwxyzéàçè'"/>
    <xsl:variable name="uppercase" select="'ABCDEFGHIJKLMNOPQRSTUVWXYZÉÀÇÈ'"/>
    <xsl:variable name="stop" select="'.?!…'"/>
    <xsl:template match="tei:pb[not(preceding-sibling::text())] |tei:note | tei:del | tei:head | tei:label | tei:teiHeader | tei:front | tei:argument | tei:label |tei:figDesc |tei:figure | tei:speaker |tei:stage|tei:dateline|tei:facsimile|tei:back"/>
    
    <xsl:template match="tei:note[preceding-sibling::text()]">
        <xsl:text> </xsl:text>
    </xsl:template>
        
    
    <xsl:template match="tei:opener">
        <xsl:apply-templates/><xsl:text> </xsl:text>
    </xsl:template>
    
    <xsl:template match="tei:signed|tei:closer">
        <xsl:text> </xsl:text><xsl:apply-templates/><!--<xsl:text> </xsl:text>-->
    </xsl:template>
    
   
    
    <xsl:template match="tei:pb[preceding-sibling::text()]">
        <xsl:text> </xsl:text>
    </xsl:template>
    
   
    
    
    <xsl:template match="tei:milestone">
       <xsl:if test="preceding::tei:milestone"><xsl:text>
</xsl:text></xsl:if><xsl:value-of select="count(preceding::tei:milestone)+1"/><xsl:text>	</xsl:text>
    </xsl:template>
    
    <xsl:template match="tei:l">
       
        <xsl:choose>
            <!--<xsl:when test="preceding-sibling::tei:l and substring(preceding-sibling::tei:l[1], string-length(preceding-sibling::tei:l[1]), 1) != '.' and substring(preceding-sibling::tei:l[1], string-length(preceding-sibling::tei:l[1]), 1) != '?' and substring(preceding-sibling::tei:l[1], string-length(preceding-sibling::tei:l[1]), 1) != '!' and substring(preceding-sibling::tei:l[1], string-length(preceding-sibling::tei:l[1]), 1) != '…' and substring(preceding-sibling::tei:l[1], string-length(preceding-sibling::tei:l[1]), 1) != '»'">
		<xsl:apply-templates mode="translate"/><xsl:text> </xsl:text>
                </xsl:when>-->
            <xsl:when test="not(tei:milestone[not(preceding-sibling::text())])">
                <xsl:text> </xsl:text><xsl:apply-templates mode="translate"/>
            </xsl:when>
            <xsl:when test="tei:milestone[preceding-sibling::text()] and not(tei:milestone[not(preceding-sibling::text())])">
                <xsl:text> </xsl:text><xsl:apply-templates select="substring-before(., tei:milestone)" mode="translate"/>
                <xsl:apply-templates select="substring-after(., tei:milestone)"/>
            </xsl:when>
            <xsl:when test="tei:milestone[preceding-sibling::text()] and tei:milestone[not(preceding-sibling::text())]">
                <xsl:apply-templates/>
            </xsl:when>
            <xsl:otherwise>
                <xsl:apply-templates/><!--<xsl:text> </xsl:text>-->
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>
    
    <xsl:template match="tei:p[not(parent::tei:note)] | tei:stage[not(preceding-sibling::*[1][name() = 'speaker']) and not(@type)]">
        
        <xsl:choose>
            <xsl:when test="not(tei:milestone[not(preceding-sibling::text())])">
                <xsl:text> </xsl:text><xsl:apply-templates/>
            </xsl:when>
            <xsl:when test="tei:milestone[preceding-sibling::text()] and not(tei:milestone[not(preceding-sibling::text())])">
                <xsl:text> </xsl:text><xsl:apply-templates select="substring-before(., tei:milestone)"/>
                <xsl:apply-templates select="substring-after(., tei:milestone)"/>
            </xsl:when>
            <xsl:when test="tei:milestone[preceding-sibling::text()] and tei:milestone[not(preceding-sibling::text())]">
                <xsl:apply-templates/>
            </xsl:when>
            <xsl:otherwise>
                <xsl:apply-templates/><!--<xsl:text> </xsl:text>-->
            </xsl:otherwise>
        </xsl:choose>
        <xsl:if test="parent::tei:p or parent::tei:l"><xsl:text> </xsl:text></xsl:if>
    </xsl:template>

<xsl:template match="*/text()" mode="translate">
<xsl:value-of select="normalize-space(concat(translate(substring(., 1, 1), $uppercase, $lowercase), substring(., 2)))"/>
</xsl:template>
    
    <xsl:template match="*/text()">
        <xsl:value-of select="normalize-space(.)"/>
    </xsl:template>

<xsl:template match="tei:note" mode="translate">
    <xsl:text> </xsl:text>
</xsl:template>
    
    <xsl:template match="tei:corr | tei:hi">
        <xsl:choose>
            <xsl:when test="@rend='b' or not(ends-with(substring-before(.., .), ' '))">
                <xsl:apply-templates/><xsl:text> </xsl:text>
            </xsl:when>
            <xsl:otherwise><xsl:text> </xsl:text><xsl:apply-templates/><xsl:text> </xsl:text></xsl:otherwise>
        </xsl:choose>
        
    </xsl:template>
    <xsl:template match="tei:corr | tei:hi" mode="translate">
        <xsl:choose>
            <xsl:when test="@rend='b' or not(ends-with(substring-before(.., .), ' '))">
                <xsl:apply-templates mode="translate"/><xsl:text> </xsl:text>
            </xsl:when>
            <xsl:otherwise><xsl:text> </xsl:text><xsl:apply-templates mode="translate"/><xsl:text> </xsl:text></xsl:otherwise>
        </xsl:choose>
        
    </xsl:template>
    
    <xsl:template match="tei:pb[preceding-sibling::text()]" mode="translate">
        <xsl:text> </xsl:text>
    </xsl:template>
    
    <xsl:template match="tei:milestone" mode="translate">
        <xsl:text>
</xsl:text><xsl:value-of select="count(preceding::tei:milestone)+1"/><xsl:text>	</xsl:text>
    </xsl:template>
</xsl:stylesheet>

