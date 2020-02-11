<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema"
    exclude-result-prefixes="xs"
    version="2.0">
    <xsl:strip-space elements="*"/>
    <xsl:output method="html" encoding="UTF-8"></xsl:output>
    <xsl:template match="text">
        
        <html>
            <head>
                <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
                <link href="../css/style.css" rel="stylesheet" type="text/css"/>
                <script src="../node_modules/cytoscape/dist/cytoscape.min.js"></script>
                <script src="https://cdnjs.cloudflare.com/ajax/libs/core-js/2.5.7/shim.min.js"></script>
                <script src="https://unpkg.com/layout-base/layout-base.js"></script>
                <script src="https://unpkg.com/cose-base/cose-base.js"></script>
                <script src="../node_modules/cytoscape-cose-bilkent/cytoscape-cose-bilkent.js"></script>
                <script src="../node_modules/jquery/dist/jquery.min.js">
                </script>
                <script src="../node_modules/jquery/dist/randomColor.js"></script>
                <script src="../node_modules/jquery/dist/jquery.canvasjs.min.js"></script>
                <script src="../js/script.js"></script>
            </head>
            <body onload="init()">
                <header>
                    <nav>
                <h1><xsl:value-of select=".//docAuthor"/><xsl:text> </xsl:text><em><xsl:value-of select=".//docTitle"/></em><xsl:if test="../teiHeader//titleStmt/editor"><xsl:text>, </xsl:text><xsl:value-of select="../teiHeader//titleStmt/editor"/> [trad.]</xsl:if></h1>
                
                    <ul>
                        <li><a href="../accueil.html">Graphe général</a></li>
                        <li><a onclick="graphe()" href="#">Galaxie</a></li>
                        <li><a onclick="alignement()" href="#">Alignement</a></li>
                        <li><a onclick="champs()" href="#">Champs lexicaux</a></li>
                    </ul>
                    </nav>
                <fieldset><legend>Auteurs correspondants présents</legend>
                <xsl:for-each select=".//rdg/@source[not(preceding::rdg/@source = .)]">
                    <div><input type="checkbox" id="{.}" name="corresp" value="{.}" onclick="affichage_auteurs()"/>
                    <label for="{.}"><xsl:value-of select="."/></label></div>
                </xsl:for-each>
                </fieldset>
                </header>
                <section id="graph">
                    <div id="cy"></div>
                    <div id="legende"></div>
                </section>
                <section>
                    <article id="texte_principal">
                        <xsl:apply-templates select="body"/>
                    </article>
                    <!--<article id="correspondances">
                        <xsl:apply-templates select=".//app" mode="corresps"></xsl:apply-templates>
                    </article>-->
                </section>
                <section id="champ">
                    <div id="cy2"></div>
                </section>
            </body>
            <script>
                var liens_mots = [<xsl:for-each select=".//xr">
                    <xsl:text>{"source" : "</xsl:text><xsl:value-of select="parent::w/@xml:id"/><xsl:text>",
                    "target" : "</xsl:text><xsl:value-of select="@corresp"/><xsl:text>",
                    "score" : </xsl:text><xsl:value-of select="@cert"/><xsl:text>,
                    "type" : "</xsl:text><xsl:value-of select="@type"/><xsl:text>"},
                    </xsl:text>
                </xsl:for-each>];
                var dictionnaireMots = [<xsl:for-each select=".//xr">
                    <xsl:variable name="xr_id" select="parent::w/@xml:id"/>
                    
                    <xsl:variable name="xr_corresp" select="@corresp"/>

                    <xsl:if test="not(following-sibling::xr)">
                    <xsl:text>{"id" : "</xsl:text><xsl:value-of select="parent::w/@xml:id"/><xsl:text>",
                    "mot" : "</xsl:text><xsl:value-of select="parent::w"/><xsl:text>",
                    "lemme" : "</xsl:text><xsl:value-of select="parent::w/@lemma"/><xsl:text>",
                    "pos" : "</xsl:text><xsl:value-of select="parent::w/@pos"/><xsl:text>"},
                    </xsl:text>
                        </xsl:if>
                    <xsl:if test="not(preceding::xr[@corresp = $xr_corresp])">
                        <xsl:text>{"id" : "</xsl:text><xsl:value-of select="ancestor::app/rdg//w[@xml:id = $xr_corresp]/@xml:id"/><xsl:text>",
                    "mot" : "</xsl:text><xsl:value-of select="ancestor::app/rdg//w[@xml:id = $xr_corresp]"/><xsl:text>",
                    "lemme" : "</xsl:text><xsl:value-of select="ancestor::app/rdg//w[@xml:id = $xr_corresp]/@lemma"/><xsl:text>",
                    "pos" : "</xsl:text><xsl:value-of select="ancestor::app/rdg//w[@xml:id = $xr_corresp]/@pos"/><xsl:text>"},
                    </xsl:text>
                    </xsl:if>
                </xsl:for-each>];
                var phrases_auteurs = {
                <xsl:for-each select=".//rdg">
                    <xsl:text>"</xsl:text><xsl:value-of select="@xml:id"/><xsl:text>" : "</xsl:text><xsl:value-of select="@source"/><xsl:text>",
                    </xsl:text>
                </xsl:for-each>};
                var correspondances_phrases = {
                <xsl:for-each select=".//lem">
                    <xsl:text>"</xsl:text><xsl:value-of select="s/@xml:id"/><xsl:text>" : "</xsl:text><xsl:value-of select="s/@corresp"/><xsl:text>",
                    </xsl:text>
                </xsl:for-each>};
            </script>
        </html>
    </xsl:template>
    <!--Texte sans correspondances-->
    <xsl:template match="teiHeader|front"/>
    <xsl:template match="body">
        <xsl:apply-templates/>
    </xsl:template>
    <xsl:template match="p">
        <p><xsl:apply-templates/></p>
    </xsl:template>
    <xsl:template match="q">
        <div class="q {@type}">
            <xsl:apply-templates/>
        </div>
    </xsl:template>
    <xsl:template match="opener | signed">
        <p class="{local-name()}">
            <xsl:apply-templates/>
        </p>
    </xsl:template>
    <xsl:template match="hi">
        <xsl:choose>
            <xsl:when test="@rend = 'i'">
                <em><xsl:apply-templates/></em>
            </xsl:when>
        </xsl:choose>
    </xsl:template>
    <xsl:template match="l[not(preceding-sibling::l[1])]">
        
                <ul class="poem">
                    <li><xsl:apply-templates/></li>
                    <xsl:if test="following-sibling::l[1]">
                        <xsl:call-template name="vers">
                            <xsl:with-param name="frère" select="following-sibling::l[1]"></xsl:with-param>
                        </xsl:call-template>
                    </xsl:if>
                </ul>
    </xsl:template>
    <xsl:template match="l" mode="versification">
        <xsl:if test="not(descendant::app)"><li><xsl:apply-templates/></li></xsl:if>
        
    </xsl:template>
    <xsl:template match="l[preceding-sibling::l[1]]"/>
        
    <xsl:template match="p[descendant::app]">
        <xsl:if test="app[1][preceding-sibling::text()]">
            <p><xsl:value-of select="app[1]/preceding-sibling::text()"/></p></xsl:if>
        <xsl:for-each select="descendant::app">
           
            <div class="couple" id="{@xml:id}">
        <div class="phrase_source">
            <xsl:for-each select="descendant::lem"><p id="{s/@xml:id}">
                <xsl:apply-templates/></p></xsl:for-each></div>
        <div class="correspondance" id="{@corresp}">
            <xsl:for-each select="rdg">
                <p class="phrase_target" id="{@xml:id}"><span class="auteur"><xsl:value-of select="@source"/></span><xsl:apply-templates select="."></xsl:apply-templates></p>
            </xsl:for-each>
        </div>
            </div>
        </xsl:for-each>
        <xsl:if test="app[last()][following-sibling::text()]">
            <p><xsl:value-of select="app[last()]/following-sibling::text()"/></p></xsl:if>
    </xsl:template>
    
    <xsl:template match="l[descendant::app]">
        <xsl:if test="app[1][preceding-sibling::text()]">
            <l><xsl:value-of select="app[1]/preceding-sibling::text()"/></l></xsl:if>
        <xsl:for-each select="descendant::app">
            <xsl:variable name="id_couple" select="generate-id()"/>
            <div class="couple" id="{@xml:id}">
                <div class="phrase_source"> <xsl:for-each select="descendant::lem"><p id="{s/@xml:id}">
                    <xsl:apply-templates/></p></xsl:for-each></div>
            <div class="correspondance" id="{@corresp}">
                <xsl:for-each select="rdg">
                    <p class="phrase_target" id="{@xml:id}"><span class="auteur"><xsl:value-of select="@source"/></span><xsl:apply-templates select="."></xsl:apply-templates></p>
                </xsl:for-each>
            </div>
                
            </div>
        </xsl:for-each>
        <xsl:if test="app[last()][following-sibling::text()]">
            <l><xsl:value-of select="app[last()]/following-sibling::text()"/></l></xsl:if>
        
    </xsl:template>
    
    <xsl:template name="vers">
        <xsl:param name="frère"/>
        <xsl:apply-templates select="$frère" mode="versification"/>
        <xsl:if test="$frère[following-sibling::l[1]]">
            <xsl:call-template name="vers">
                <xsl:with-param name="frère" select="$frère/following-sibling::l[1]"></xsl:with-param>
            </xsl:call-template>
        </xsl:if>
    </xsl:template>
    
    
    <!--Gestion des phrases correspondantes dans le texte-->
    <xsl:template match="app"/>
    
    <xsl:template match="lem|rdg">
        <xsl:apply-templates/>
    </xsl:template>
    <xsl:template match="phr">
        <span data-type="{@type}"><xsl:apply-templates/><xsl:if test="following-sibling::*[1]/local-name() != 'pc'"><xsl:text> </xsl:text></xsl:if></span>
    </xsl:template>
    <xsl:template match="w">
        <xsl:variable name="apostrophe">'</xsl:variable>
        <xsl:element name="span">
            <xsl:attribute name="class">w <xsl:if test="descendant::xr and ancestor::lem">actif</xsl:if></xsl:attribute>
            <xsl:attribute name="data-id"><xsl:value-of select="@xml:id"/></xsl:attribute>
            <xsl:if test="descendant::xr and ancestor::lem">
                <xsl:attribute name="data-corresp"><xsl:for-each select="descendant::xr"><xsl:value-of select="@corresp"/><xsl:if test="following-sibling::xr"><xsl:text> </xsl:text></xsl:if></xsl:for-each></xsl:attribute>
                <xsl:attribute name="data-parent"><xsl:value-of select="ancestor::app/@xml:id"/></xsl:attribute>
            </xsl:if>
            <xsl:choose>
                <xsl:when test="not(ends-with(., $apostrophe)) and following-sibling::*[1]/local-name()!= 'pc' and following-sibling::*[1]/local-name() = 'w'"><xsl:apply-templates/><xsl:text> </xsl:text></xsl:when>
                <xsl:when test="not(ends-with(., $apostrophe)) and following-sibling::*[1]/local-name() != 'pc' and following-sibling::*[1]/local-name() = 'phr'"><xsl:apply-templates/><xsl:text> </xsl:text></xsl:when>
                <xsl:when test="ends-with(., $apostrophe)"><xsl:value-of select="translate(., $apostrophe, '’')"/></xsl:when>
                <xsl:otherwise><xsl:apply-templates/></xsl:otherwise>
            </xsl:choose>
        </xsl:element>
    </xsl:template>
    <xsl:template match="pc">
        <xsl:variable name="parenthese_ouvrante">(</xsl:variable>
        <xsl:variable name="parenthese_fermante">)</xsl:variable>
        <xsl:choose>
            <xsl:when test="matches(., '[,.…]')"><xsl:apply-templates/><xsl:if test="not(following-sibling::*[1]/local-name() = 'pc')"><xsl:text> </xsl:text></xsl:if></xsl:when>
            <xsl:when test=". = $parenthese_fermante"><xsl:apply-templates/><xsl:if test="not(following-sibling::*[1]/local-name() = 'pc')"><xsl:text> </xsl:text></xsl:if></xsl:when>
            <xsl:when test=". = $parenthese_ouvrante"><xsl:text> </xsl:text><xsl:apply-templates/></xsl:when>
            <xsl:when test=". = '«'"><xsl:apply-templates/><xsl:text> </xsl:text></xsl:when>
            <xsl:otherwise><xsl:if test="not(preceding-sibling::*[1]/local-name() = 'pc')"><xsl:text> </xsl:text></xsl:if><xsl:apply-templates></xsl:apply-templates><xsl:if test="not(following-sibling::*[1]/local-name() = 'pc')"><xsl:text> </xsl:text></xsl:if></xsl:otherwise>
        </xsl:choose>
    </xsl:template>
    
</xsl:stylesheet>
