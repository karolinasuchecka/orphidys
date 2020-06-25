<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema"
    exclude-result-prefixes="xs tei"
    xmlns:tei="http://www.tei-c.org/ns/1.0"
    version="2.0">
    <xsl:strip-space elements="*"/>
    <xsl:output encoding="UTF-8" method="text"/>
    <xsl:template match="/">
        <xsl:text>id*type*genre*statut*auteur*titre*traducteur*infos édition*date*note
</xsl:text>
        <xsl:for-each select=".//tei:object">
            
            <xsl:value-of select="@xml:id"/><xsl:text>*</xsl:text><xsl:value-of select="@type"/><xsl:text>*</xsl:text><xsl:value-of select="@subtype"/><xsl:text>*</xsl:text><xsl:value-of select="@status"/><xsl:text>*</xsl:text>
            <xsl:choose>
                <xsl:when test="descendant::tei:author">
                <xsl:for-each select="descendant::tei:author">
                    <xsl:apply-templates mode="head"/><xsl:if test="following-sibling::tei:author">
                        <xsl:text> et </xsl:text>
                    </xsl:if>
                </xsl:for-each>    
            </xsl:when>
            <xsl:otherwise>
                <xsl:text>Anonyme</xsl:text>
            </xsl:otherwise></xsl:choose>
            <xsl:text>*</xsl:text>
            <xsl:apply-templates select="descendant::tei:title"/><xsl:text>*</xsl:text>
            <xsl:if test="descendant::tei:editor[@resp='trad']">
                <xsl:for-each select="descendant::tei:editor[@resp='trad']">
                    <xsl:value-of select="substring-after(., ' ')"/><xsl:text>, </xsl:text><xsl:value-of select="substring-before(., ' ')"/>
                <xsl:if test="following-sibling::tei:editor[@resp = 'trad']"><xsl:text> et </xsl:text></xsl:if></xsl:for-each>
            </xsl:if>
            <xsl:text>*</xsl:text>
            <xsl:if test="descendant::tei:biblScope[@unit='volume']">
                <xsl:text>vol.</xsl:text><xsl:value-of select="tei:biblScope[@unit='volume']/@n"/><xsl:text>, </xsl:text>
            </xsl:if>
            <xsl:if test="descendant::tei:biblScope[@unit='issue']">
                <xsl:text>n° </xsl:text><xsl:value-of select="tei:biblScope[@unit='issue']/@n"/><xsl:text>, </xsl:text>
            </xsl:if>
            <xsl:if test="descendant::tei:editor[not(@resp='trad')]">
                <xsl:text></xsl:text>
                <xsl:for-each select="descendant::tei:editor[not(@resp='trad')]">
                    <xsl:value-of select="substring-after(., ' ')"/><xsl:text>, </xsl:text><xsl:value-of select="substring-before(., ' ')"/>
                    <xsl:if test="following-sibling::tei:editor[not(@resp = 'trad')]"><xsl:text> and </xsl:text></xsl:if></xsl:for-each>
                <xsl:text>(éd.), </xsl:text>
            </xsl:if>
                <xsl:value-of select="descendant::tei:pubPlace"/><xsl:if test="descendant::tei:publisher"><xsl:text> : </xsl:text><xsl:value-of select="descendant::tei:publisher"/></xsl:if><xsl:text>, </xsl:text>
                <xsl:value-of select="descendant::tei:imprint/tei:date/@when"/>
                <xsl:if test="descendant::tei:citedRange">
                    <xsl:text>, </xsl:text>
                    <xsl:choose>
                        <xsl:when test="descendant::tei:citedRange[1][@unit = 'page']"><xsl:text>p. </xsl:text></xsl:when>
                        <xsl:when test="descendant::tei:citedRange[1][@unit = 'folio']"><xsl:text>fol. </xsl:text></xsl:when>
                        <xsl:when test="descendant::tei:citedRange[1][@unit = 'line']"><xsl:text>l. </xsl:text></xsl:when>
                    </xsl:choose>
                    <xsl:for-each select="descendant::tei:citedRange">
                        <xsl:value-of select="@from"/><xsl:text>-</xsl:text><xsl:value-of select="@to"/><xsl:if test="following-sibling::tei:citedRange"><xsl:text>, </xsl:text></xsl:if>
                    </xsl:for-each>
                </xsl:if><xsl:text>.*</xsl:text><xsl:value-of select="descendant::tei:imprint/tei:date/@when"/><xsl:text>*</xsl:text><xsl:value-of select="descendant::tei:idno"/><xsl:text>
</xsl:text>
        </xsl:for-each>
    </xsl:template>
    
    <xsl:template match="*"/>
        
    
    <xsl:template match="tei:title[not(parent::tei:series)]">
        <xsl:choose>
            <xsl:when test="parent::tei:monogr[preceding-sibling::tei:analytic]">
<xsl:text> ([dans:]</xsl:text>
                <xsl:apply-templates/>
                <xsl:text>)</xsl:text>
            </xsl:when>
            <xsl:otherwise>
                <xsl:apply-templates/>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>
    
    <xsl:template match="tei:persName" mode="head">
        <xsl:value-of select="tei:surname"/><xsl:if test="descendant::tei:forename"><xsl:text>, </xsl:text><xsl:value-of select="tei:forename"/></xsl:if>
    </xsl:template>
     
</xsl:stylesheet>