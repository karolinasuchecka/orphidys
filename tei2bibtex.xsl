<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema"
    exclude-result-prefixes="xs tei"
    xmlns:tei="http://www.tei-c.org/ns/1.0"
    version="2.0">
    <xsl:strip-space elements="*"/>
    <xsl:output encoding="UTF-8" method="text"/>
    <xsl:template match="/">
        <xsl:for-each select=".//tei:object">
            <xsl:choose>
                <xsl:when test=".//tei:analytic">
                    <xsl:text>@incollection</xsl:text>
                </xsl:when>
                <xsl:otherwise>
                    <xsl:text>@book</xsl:text>
                </xsl:otherwise>
            </xsl:choose>
            <xsl:text>{</xsl:text><xsl:value-of select="@xml:id"/><xsl:text>,
</xsl:text>
            <xsl:if test="descendant::tei:author">
                <xsl:text>author = {</xsl:text>
                <xsl:for-each select="descendant::tei:author">
                    <xsl:apply-templates mode="head"/><xsl:if test="following-sibling::tei:author">
                        <xsl:text> and </xsl:text>
                    </xsl:if>
                </xsl:for-each>
                <xsl:text>},
</xsl:text>
            </xsl:if>
            <xsl:apply-templates/>
            <xsl:if test="descendant::tei:editor[@resp='trad']">
                        <xsl:text>translator = {</xsl:text>
                <xsl:for-each select="descendant::tei:editor[@resp='trad']">
                    <xsl:value-of select="substring-after(., ' ')"/><xsl:text>, </xsl:text><xsl:value-of select="substring-before(., ' ')"/>
                <xsl:if test="following-sibling::tei:editor[@resp = 'trad']"><xsl:text> and </xsl:text></xsl:if></xsl:for-each>
                        <xsl:text>},
</xsl:text>
            </xsl:if>
            <xsl:if test="descendant::tei:editor[not(@resp='trad')]">
                <xsl:text>editor = {</xsl:text>
                <xsl:for-each select="descendant::tei:editor[not(@resp='trad')]">
                    <xsl:value-of select="substring-after(., ' ')"/><xsl:text>, </xsl:text><xsl:value-of select="substring-before(., ' ')"/>
                    <xsl:if test="following-sibling::tei:editor[not(@resp = 'trad')]"><xsl:text> and </xsl:text></xsl:if></xsl:for-each>
                <xsl:text>},
</xsl:text>
            </xsl:if>
            <xsl:text>pages = {</xsl:text>
            <xsl:for-each select="descendant::tei:citedRange">
                <xsl:value-of select="@from"/><xsl:text>-</xsl:text><xsl:value-of select="@to"/><xsl:if test="following-sibling::tei:citedRange"><xsl:text>, </xsl:text></xsl:if>
            </xsl:for-each>
            <xsl:text>},
</xsl:text>
            <xsl:text>keywords = {</xsl:text>
            <xsl:for-each select="@*[not(name() = 'xml:id')]">
                <xsl:value-of select="."/><xsl:if test="not(position()= last())"><xsl:text>, </xsl:text></xsl:if>
            </xsl:for-each><xsl:text>},
note = {</xsl:text>
            <xsl:value-of select=".//tei:idno"/>
            <xsl:text>},
                }
            
            </xsl:text>
        </xsl:for-each>
    </xsl:template>
    
    <xsl:template match="*">
        <xsl:text>###</xsl:text>
        <xsl:apply-templates/>
        <xsl:text>###
</xsl:text>
        
    </xsl:template>
    
    <xsl:template match="tei:analytic|tei:monogr|tei:imprint|tei:biblStruct">
        <xsl:apply-templates/>
    </xsl:template>
    <xsl:template match="tei:additional|tei:surrogates|tei:objectIdentifier|tei:persName|tei:availability|tei:author|tei:citedRange|tei:editor|tei:relatedItem|tei:ref|tei:biblScope[@unit='part']"/>
    
    <xsl:template match="tei:title[not(parent::tei:series)]">
        <xsl:choose>
            <xsl:when test="parent::tei:monogr[preceding-sibling::tei:analytic]">
<xsl:text>booktitle = {</xsl:text>
                <xsl:apply-templates/>
                <xsl:text>},
</xsl:text>
            </xsl:when>
            <xsl:otherwise>
<xsl:text>title = {</xsl:text>
                <xsl:apply-templates/>
       
        <xsl:if test="following-sibling::tei:biblScope[@unit='part']">
            <xsl:text>, l. </xsl:text>
            <xsl:for-each select="following-sibling::tei:biblScope[@unit='part']"><xsl:value-of select="@n"/><xsl:if test="following-sibling::tei:biblScope[@unit='part']"><xsl:text>-</xsl:text></xsl:if></xsl:for-each>
        </xsl:if>
        <xsl:text>},
</xsl:text>
</xsl:otherwise>
        </xsl:choose>
    </xsl:template>
    
    <xsl:template match="tei:pubPlace">
        <xsl:text>address = {</xsl:text>
        <xsl:apply-templates/>
        <xsl:text>},
</xsl:text>
    </xsl:template>
    <xsl:template match="tei:publisher">
        <xsl:text>publisher = {</xsl:text>
        <xsl:apply-templates/>
        <xsl:text>},
</xsl:text>
    </xsl:template>
    <xsl:template match="tei:date">
        <xsl:text>year = {</xsl:text>
        <xsl:value-of select="@when"/>
        <xsl:text>},
</xsl:text>
    </xsl:template>
    <xsl:template match="tei:persName" mode="head">
        <xsl:value-of select="tei:surname"/><xsl:if test="descendant::tei:forename"><xsl:text>, </xsl:text><xsl:value-of select="tei:forename"/></xsl:if>
    </xsl:template>
    
    <xsl:template match="tei:biblScope[@unit='volume']">
            <xsl:text>volume = {</xsl:text>
            <xsl:value-of select="@n"/>
            <xsl:text>},
</xsl:text>
    </xsl:template>
    
    <xsl:template match="tei:biblScope[@unit='issue']">
        <xsl:text>number = {</xsl:text>
        <xsl:value-of select="@n"/>
        <xsl:text>},
</xsl:text>
    </xsl:template>
    
    <xsl:template match="tei:note">
        <xsl:text>url = {</xsl:text>
        <xsl:value-of select="tei:ref/@target"/>
        <xsl:text>},
</xsl:text>
    </xsl:template>
    
    <xsl:template match="tei:series">
        <xsl:text>series = {</xsl:text>
        <xsl:value-of select="tei:title"/>
        <xsl:text>},
</xsl:text>
    </xsl:template>
       
</xsl:stylesheet>