<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema"
    exclude-result-prefixes="xs"
    version="1.0">
    <xsl:strip-space elements="*"/>
    <xsl:output method="xml" encoding="UTF-8" indent="yes"></xsl:output>
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
    
    <xsl:template match="phr[not(parent::phr)]">
        <xsl:variable name="last_id" select="descendant::w[last()]/@n"/>
        <xsl:variable name="suiv_id" select="following-sibling::phr[1]/descendant::w[1]/@n"/>
        <xsl:variable name="first_id" select="descendant::w[1]/@n"/>
        <xsl:variable name="prec_id" select="preceding-sibling::phr[1]/descendant::w[last()]/@n"/>
        <xsl:for-each select="preceding-sibling::w[not(parent::phr)] | preceding-sibling::pc">
            <xsl:sort select="number(@n)" data-type="number" order="ascending"/>
            <xsl:if test="number(@n) &lt; number($first_id) and number(@n) &gt; number($prec_id)">
                <xsl:element name="{local-name()}">
                    <xsl:for-each select="@*">
                        <xsl:attribute name="{local-name()}">
                            <xsl:value-of select="."/>
                        </xsl:attribute>
                    </xsl:for-each>
                    <xsl:value-of select="."/>
                </xsl:element>
            </xsl:if>
        </xsl:for-each>
        <xsl:element name="{local-name()}">
            <xsl:for-each select="@*">
                <xsl:attribute name="{local-name()}">
                    <xsl:value-of select="."/>
                </xsl:attribute>
            </xsl:for-each>
            <xsl:apply-templates/>
        </xsl:element>
        <xsl:choose>
            <xsl:when test="preceding-sibling::pc or preceding-sibling::w">
                <xsl:for-each select="preceding-sibling::w[not(parent::phr)] | preceding-sibling::pc">
                    <xsl:sort select="number(@n)" data-type="number" order="ascending"/>
                    <xsl:if test="number(@n) &gt; number($last_id) and number(@n) &lt; number($suiv_id)">
                        <xsl:element name="{local-name()}">
                            <xsl:for-each select="@*">
                                <xsl:attribute name="{local-name()}">
                                    <xsl:value-of select="."/>
                                </xsl:attribute>
                            </xsl:for-each>
                            <xsl:value-of select="."/>
                        </xsl:element>
                    </xsl:if>
                </xsl:for-each>
            </xsl:when>
        </xsl:choose>
    </xsl:template>
    
    <xsl:template match="w[not(parent::phr)] | pc">
        <xsl:choose>
            <xsl:when test="number(@n) &lt; number(following-sibling::phr[1]/w[1]/@n) and not(preceding-sibling::phr)">
            <xsl:element name="{local-name()}">
                <xsl:for-each select="@*">
                    <xsl:attribute name="{local-name()}">
                        <xsl:value-of select="."/>
                    </xsl:attribute>
                </xsl:for-each>
                <xsl:value-of select="."/>
            </xsl:element>
        </xsl:when>
        <xsl:when test="not(following-sibling::phr[1]) and number(@n) &gt; number(preceding-sibling::phr[1]/w[last()]/@n)">
            <xsl:element name="{local-name()}">
                <xsl:for-each select="@*">
                    <xsl:attribute name="{local-name()}">
                        <xsl:value-of select="."/>
                    </xsl:attribute>
                </xsl:for-each>
                <xsl:value-of select="."/>
            </xsl:element>
        </xsl:when>
            <xsl:when test="number(@n) &lt; number(following-sibling::phr[1]/w[1]) and number(@n) &gt; number(preceding-sibling::phr[1]/w[last()])">
                <xsl:element name="{local-name()}">
                <xsl:for-each select="@*">
                    <xsl:attribute name="{local-name()}">
                        <xsl:value-of select="."/>
                    </xsl:attribute>
                </xsl:for-each>
                <xsl:value-of select="."/>
                </xsl:element>
            </xsl:when>
        </xsl:choose>
    </xsl:template>
    
    <xsl:template match="s[not(descendant::phr)]">
        <xsl:element name="{local-name()}">
            <xsl:for-each select="@*">
                <xsl:attribute name="{local-name()}">
                    <xsl:value-of select="."/>
                </xsl:attribute>
            </xsl:for-each>
            <xsl:for-each select="descendant::*">
                <xsl:sort select="number(@n)" data-type="number" order="ascending"/>
                <xsl:element name="{local-name()}">
                    <xsl:for-each select="@*">
                        <xsl:attribute name="{local-name()}">
                            <xsl:value-of select="."/>
                        </xsl:attribute>
                    </xsl:for-each>
                    <xsl:value-of select="."/>
                </xsl:element>
            </xsl:for-each>
        </xsl:element>
    </xsl:template>
    
    
    <!--<xsl:template match="s">
        <xsl:element name="{local-name()}">
            <xsl:for-each select="@*">
                <xsl:attribute name="{local-name()}">
                    <xsl:value-of select="."/>
                </xsl:attribute>
            </xsl:for-each>
            <!-\-<xsl:for-each select="phr|w|pc">
                <xsl:choose>
                    <xsl:when test="phr">
                        <xsl:apply-templates/>
                        <xsl:variable name="last_id" select="descendant::w[last()]/@n"/>
                        <xsl:variable name="suiv_id" select="following-sibling::phr[1]/descendant::w[1]/@n"/>
                        <xsl:for-each select="preceding-sibling::w[not(parent::phr)] | preceding-sibling::pc">
                            
                            <xsl:if test="number(@n) &gt; number($last_id) and number(@n) &lt; number($suiv_id)">
                                <xsl:text>###OUI</xsl:text>
                                <xsl:element name="{local-name()}">
                                    <xsl:for-each select="@*">
                                        <xsl:attribute name="{local-name()}">
                                            <xsl:value-of select="."/>
                                        </xsl:attribute>
                                    </xsl:for-each>
                                    <xsl:value-of select="."/>
                                </xsl:element>
                            </xsl:if>
                        </xsl:for-each>
                    </xsl:when>
                    <xsl:otherwise>
                        <xsl:if test="number(@n) &lt; number(following-sibling::phr[1]/w[1]/@n)">
                            <xsl:text>
                                
                            </xsl:text><xsl:text>###</xsl:text><xsl:value-of select="@n"/><xsl:text>est inférieur à </xsl:text><xsl:value-of select="following-sibling::phr[1]/w[1]/@n"/><xsl:text>
                                
                            </xsl:text>
                            <xsl:element name="{local-name()}">
                                <xsl:for-each select="@*">
                                    <xsl:attribute name="{local-name()}">
                                        <xsl:value-of select="."/>
                                    </xsl:attribute>
                                </xsl:for-each>
                                <xsl:apply-templates/>
                            </xsl:element>
                        </xsl:if>
                    </xsl:otherwise>
                </xsl:choose>
            </xsl:for-each>-\->
           
             <!-\-<xsl:for-each select="phr[not(parent::phr)]">
               
                <xsl:element name="{local-name()}">
                    <xsl:for-each select="@*">
                        <xsl:attribute name="{local-name()}">
                            <xsl:value-of select="."/>
                        </xsl:attribute>
                    </xsl:for-each>
                    <xsl:apply-templates/>
                </xsl:element>
            </xsl:for-each>-\->
            
        </xsl:element>
        
        
        
    </xsl:template>-->
    
    <!--<xsl:template match="w[not(parent::phr)] | pc">
        <xsl:if test="@n &lt; following-sibling::phr[1]/w[1]/@n">
            <xsl:element name="{local-name()}">
                <xsl:for-each select="@*">
                    <xsl:attribute name="{local-name()}">
                        <xsl:value-of select="."/>
                    </xsl:attribute>
                </xsl:for-each>
                <xsl:apply-templates/>
            </xsl:element>
        </xsl:if>
    </xsl:template>-->
</xsl:stylesheet>