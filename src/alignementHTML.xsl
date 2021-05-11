<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema"
    exclude-result-prefixes="xs"
    xpath-default-namespace="http://www.tei-c.org/ns/1.0"
    version="2.0">
    <xsl:strip-space elements="*"/>
    <xsl:template match="text">
        <xsl:result-document method="html" encoding="utf-8">
        <html>
            <head>
                <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
                <link href="../css/style.css" rel="stylesheet" type="text/css"/>
                <script src="../node_modules/cytoscape/dist/cytoscape.min.js"></script>
                <script src="https://cdnjs.cloudflare.com/ajax/libs/core-js/2.5.7/shim.min.js"></script>
                <script src="https://unpkg.com/layout-base/layout-base.js"></script>
                
                <script src="https://unpkg.com/cose-base/cose-base.js"></script>                
                <script src="../node_modules/cytoscape-cose-bilkent/cytoscape-cose-bilkent.js"></script>
                
                <script src="https://unpkg.com/webcola/WebCola/cola.min.js"></script>
                <script src="../node_modules/cytoscape.cola/cytoscape-cola.js"></script>
                
                <script src="https://cdnjs.cloudflare.com/ajax/libs/core-js/2.5.7/shim.min.js"></script>
                <script src="https://unpkg.com/avsdf-base/avsdf-base.js"></script>
                <script src="../node_modules/cytoscape-avsdf/cytoscape-avsdf.js"></script>
                
                <script src="https://unpkg.com/cytoscape-graphml/cytoscape-graphml.js"></script>
                <script src="https://raw.githack.com/iVis-at-Bilkent/cytoscape.js-layvo/unstable/cytoscape-layvo.js"></script>
                <script src="../node_modules/cytoscape-cise/cytoscape-cise.js"></script>
                
                <script src="https://cdnjs.cloudflare.com/ajax/libs/bluebird/3.5.0/bluebird.js"></script>
                <script src="https://cdnjs.cloudflare.com/ajax/libs/fetch/2.0.3/fetch.min.js"></script>
                <script src="../node_modules/cytoscape-euler/cytoscape-euler.js"></script>
                
                <script src="../node_modules/jquery/dist/jquery.min.js">
                </script>
                <script src="../node_modules/jquery/dist/randomColor.js"></script>
                <script src="../node_modules/jquery/dist/jquery.canvasjs.min.js"></script>
                <script src="../js/script.js"></script>
                <script src="json/{//structure}.js"></script>
            </head>
            <body onload="init()">
                <header>
                    
                <h1><xsl:value-of select=".//docAuthor"/><xsl:text> </xsl:text><em><xsl:value-of select=".//docTitle"/></em><xsl:if test="../teiHeader//titleStmt/editor"><xsl:text>, </xsl:text><xsl:value-of select="../teiHeader//titleStmt/editor"/> [trad.]</xsl:if></h1>
                    <nav class="menu">
                    <ul>
                        <li><a href="../accueil.html">Graphe général</a></li>
                        <li><a onclick="graphe()" href="#">Galaxie</a></li>
                        <li><a onclick="alignement()" href="#">Alignement</a></li>
                        <li><a onclick="champs()" href="#">Champs lexicaux</a></li>
                    </ul>
                    </nav>
                
                </header>
                <section id="graph">
                    <div id="cy"></div>
                    <div id="legende">
          <div id="fermeture" onclick="document.getElementById('legende').style.display = 'none'">X</div>
          <h3>Légende</h3>
      <ul class="type">
          <li><svg
   xmlns:dc="http://purl.org/dc/elements/1.1/"
   xmlns:cc="http://creativecommons.org/ns#"
   xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
   xmlns:svg="http://www.w3.org/2000/svg"
   xmlns="http://www.w3.org/2000/svg"
   xmlns:sodipodi="http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd"
   xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape"
   width="26.804016mm"
   height="26.644562mm"
   viewBox="0 0 26.804016 26.644562"
   version="1.1"
   id="svg1044"
   inkscape:version="0.92.4 (f8dce91, 2019-08-02)"
   sodipodi:docname="diamond.svg">
  <defs
     id="defs1038" />
  <sodipodi:namedview
     id="base"
     pagecolor="#ffffff"
     bordercolor="#666666"
     borderopacity="1.0"
     inkscape:pageopacity="0.0"
     inkscape:pageshadow="2"
     inkscape:zoom="0.35"
     inkscape:cx="-736.48959"
     inkscape:cy="-223.93379"
     inkscape:document-units="mm"
     inkscape:current-layer="layer1"
     showgrid="false"
     fit-margin-top="0"
     fit-margin-left="0"
     fit-margin-right="0"
     fit-margin-bottom="0"
     inkscape:window-width="1850"
     inkscape:window-height="1016"
     inkscape:window-x="70"
     inkscape:window-y="27"
     inkscape:window-maximized="1" />
  <metadata
     id="metadata1041">
    <rdf:RDF>
      <cc:Work
         rdf:about="">
        <dc:format>image/svg+xml</dc:format>
        <dc:type
           rdf:resource="http://purl.org/dc/dcmitype/StillImage" />
        <dc:title></dc:title>
      </cc:Work>
    </rdf:RDF>
  </metadata>
  <g
     inkscape:label="Calque 1"
     inkscape:groupmode="layer"
     id="layer1"
     transform="translate(-121.15751,-62.939624)">
    <path
       style="opacity:0.97399998;fill:#cccccc;fill-opacity:1;stroke:none;stroke-width:0.26458332px;stroke-linecap:butt;stroke-linejoin:miter;stroke-opacity:1"
       d="m 120.96852,76.73299 13.70164,-13.79613 13.89062,13.79613 -13.89062,13.796141 z"
       id="path52"
       inkscape:connector-curvature="0"
       inkscape:transform-center-x="-28.726191"
       inkscape:transform-center-y="-6.0476196" />
  </g>
</svg>Traduction d'Ovide</li>
          <li><svg
   xmlns:dc="http://purl.org/dc/elements/1.1/"
   xmlns:cc="http://creativecommons.org/ns#"
   xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
   xmlns:svg="http://www.w3.org/2000/svg"
   xmlns="http://www.w3.org/2000/svg"
   xmlns:sodipodi="http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd"
   xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape"
   width="27.214403mm"
   height="27.503075mm"
   viewBox="0 0 27.214403 27.503075"
   version="1.1"
   id="svg928"
   inkscape:version="0.92.4 (f8dce91, 2019-08-02)"
   sodipodi:docname="hexagone.svg">
  <defs
     id="defs922" />
  <sodipodi:namedview
     id="base"
     pagecolor="#ffffff"
     bordercolor="#666666"
     borderopacity="1.0"
     inkscape:pageopacity="0.0"
     inkscape:pageshadow="2"
     inkscape:zoom="0.35"
     inkscape:cx="-535.71406"
     inkscape:cy="-142.31149"
     inkscape:document-units="mm"
     inkscape:current-layer="layer1"
     showgrid="false"
     fit-margin-top="0"
     fit-margin-left="0"
     fit-margin-right="0"
     fit-margin-bottom="0"
     inkscape:window-width="1850"
     inkscape:window-height="1016"
     inkscape:window-x="70"
     inkscape:window-y="27"
     inkscape:window-maximized="1" />
  <metadata
     id="metadata925">
    <rdf:RDF>
      <cc:Work
         rdf:about="">
        <dc:format>image/svg+xml</dc:format>
        <dc:type
           rdf:resource="http://purl.org/dc/dcmitype/StillImage" />
        <dc:title></dc:title>
      </cc:Work>
    </rdf:RDF>
  </metadata>
  <g
     inkscape:label="Calque 1"
     inkscape:groupmode="layer"
     id="layer1"
     transform="translate(-68.035655,-83.677011)">
    <path
       style="opacity:0.97399998;fill:#cccccc;fill-opacity:1;stroke:none;stroke-width:0.17857143;stroke-miterlimit:4;stroke-dasharray:none;stroke-dashoffset:0;stroke-opacity:1"
       d="m 71.400697,104.32744 -3.365042,-6.852705 3.447889,-6.898861 3.447886,-6.898863 3.780967,0.025 c 2.079532,0.01376 5.085273,0.07754 6.679427,0.141739 l 2.89846,0.116729 3.479888,6.575417 c 1.913937,3.616478 3.479887,6.64378 3.479887,6.727338 0,0.360865 -6.632525,13.645566 -6.848247,13.716776 -0.131342,0.0434 -3.25319,0.10613 -6.937439,0.13948 l -6.698636,0.0606 z"
       id="path66"
       inkscape:connector-curvature="0" />
  </g>
</svg>Traduction de Virgile</li>
          <li><svg
   xmlns:dc="http://purl.org/dc/elements/1.1/"
   xmlns:cc="http://creativecommons.org/ns#"
   xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
   xmlns:svg="http://www.w3.org/2000/svg"
   xmlns="http://www.w3.org/2000/svg"
   xmlns:sodipodi="http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd"
   xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape"
   width="26.804016mm"
   height="26.644562mm"
   viewBox="0 0 26.804016 26.644562"
   version="1.1"
   id="svg1044"
   inkscape:version="0.92.4 (f8dce91, 2019-08-02)"
   sodipodi:docname="triangle.svg">
  <defs
     id="defs1038" />
  <sodipodi:namedview
     id="base"
     pagecolor="#ffffff"
     bordercolor="#666666"
     borderopacity="1.0"
     inkscape:pageopacity="0.0"
     inkscape:pageshadow="2"
     inkscape:zoom="0.35"
     inkscape:cx="-736.48959"
     inkscape:cy="-223.93379"
     inkscape:document-units="mm"
     inkscape:current-layer="layer1"
     showgrid="false"
     fit-margin-top="0"
     fit-margin-left="0"
     fit-margin-right="0"
     fit-margin-bottom="0"
     inkscape:window-width="1850"
     inkscape:window-height="1016"
     inkscape:window-x="70"
     inkscape:window-y="27"
     inkscape:window-maximized="1" />
  <metadata
     id="metadata1041">
    <rdf:RDF>
      <cc:Work
         rdf:about="">
        <dc:format>image/svg+xml</dc:format>
        <dc:type
           rdf:resource="http://purl.org/dc/dcmitype/StillImage" />
        <dc:title></dc:title>
      </cc:Work>
    </rdf:RDF>
  </metadata>
  <g
     inkscape:label="Calque 1"
     inkscape:groupmode="layer"
     id="layer1"
     transform="translate(-121.15751,-62.939624)">
    <path
       style="opacity:0.97399998;fill:#cccccc;fill-opacity:1;stroke:none;stroke-width:0.17857143;stroke-miterlimit:4;stroke-dasharray:none;stroke-dashoffset:0;stroke-opacity:1"
       d="m 121.44584,89.4519 c -0.18765,-0.04864 -0.31522,-0.154938 -0.28348,-0.236207 0.23982,-0.614087 13.30797,-26.273921 13.38199,-26.276069 0.0523,-0.0016 3.09258,5.992889 6.75615,13.320902 l 6.66103,13.32366 -13.08725,-0.02193 c -7.19798,-0.01207 -13.24078,-0.06172 -13.42844,-0.110367 z"
       id="path64"
       inkscape:connector-curvature="0" />
  </g>
</svg>Modernisation</li>
          <li><svg
   xmlns:dc="http://purl.org/dc/elements/1.1/"
   xmlns:cc="http://creativecommons.org/ns#"
   xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
   xmlns:svg="http://www.w3.org/2000/svg"
   xmlns="http://www.w3.org/2000/svg"
   xmlns:sodipodi="http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd"
   xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape"
   width="27.214403mm"
   height="27.503075mm"
   viewBox="0 0 27.214403 27.503075"
   version="1.1"
   id="svg928"
   inkscape:version="0.92.4 (f8dce91, 2019-08-02)"
   sodipodi:docname="rond.svg">
  <defs
     id="defs922" />
  <sodipodi:namedview
     id="base"
     pagecolor="#ffffff"
     bordercolor="#666666"
     borderopacity="1.0"
     inkscape:pageopacity="0.0"
     inkscape:pageshadow="2"
     inkscape:zoom="2.8"
     inkscape:cx="188.94674"
     inkscape:cy="-26.22114"
     inkscape:document-units="mm"
     inkscape:current-layer="layer1"
     showgrid="false"
     fit-margin-top="0"
     fit-margin-left="0"
     fit-margin-right="0"
     fit-margin-bottom="0"
     inkscape:window-width="1850"
     inkscape:window-height="1016"
     inkscape:window-x="70"
     inkscape:window-y="27"
     inkscape:window-maximized="1" />
  <metadata
     id="metadata925">
    <rdf:RDF>
      <cc:Work
         rdf:about="">
        <dc:format>image/svg+xml</dc:format>
        <dc:type
           rdf:resource="http://purl.org/dc/dcmitype/StillImage" />
        <dc:title></dc:title>
      </cc:Work>
    </rdf:RDF>
  </metadata>
  <g
     inkscape:label="Calque 1"
     inkscape:groupmode="layer"
     id="layer1"
     transform="translate(-68.035655,-83.677011)">
    <ellipse
       style="opacity:0.97399998;fill:#cccccc;fill-opacity:1;stroke:none;stroke-width:0.27912214;stroke-miterlimit:4;stroke-dasharray:none;stroke-dashoffset:0;stroke-opacity:1"
       id="path60"
       cx="81.645042"
       cy="97.508041"
       rx="12.690681"
       ry="12.42014" />
  </g>
</svg>Transmodalisation</li>
          <li><svg
   xmlns:dc="http://purl.org/dc/elements/1.1/"
   xmlns:cc="http://creativecommons.org/ns#"
   xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
   xmlns:svg="http://www.w3.org/2000/svg"
   xmlns="http://www.w3.org/2000/svg"
   xmlns:sodipodi="http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd"
   xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape"
   width="27.214403mm"
   height="27.503075mm"
   viewBox="0 0 27.214403 27.503075"
   version="1.1"
   id="svg928"
   inkscape:version="0.92.4 (f8dce91, 2019-08-02)"
   sodipodi:docname="star.svg">
  <defs
     id="defs922" />
  <sodipodi:namedview
     id="base"
     pagecolor="#ffffff"
     bordercolor="#666666"
     borderopacity="1.0"
     inkscape:pageopacity="0.0"
     inkscape:pageshadow="2"
     inkscape:zoom="0.35"
     inkscape:cx="-535.71406"
     inkscape:cy="-142.31149"
     inkscape:document-units="mm"
     inkscape:current-layer="layer1"
     showgrid="false"
     fit-margin-top="0"
     fit-margin-left="0"
     fit-margin-right="0"
     fit-margin-bottom="0"
     inkscape:window-width="1850"
     inkscape:window-height="1016"
     inkscape:window-x="70"
     inkscape:window-y="27"
     inkscape:window-maximized="1" />
  <metadata
     id="metadata925">
    <rdf:RDF>
      <cc:Work
         rdf:about="">
        <dc:format>image/svg+xml</dc:format>
        <dc:type
           rdf:resource="http://purl.org/dc/dcmitype/StillImage" />
        <dc:title></dc:title>
      </cc:Work>
    </rdf:RDF>
  </metadata>
  <g
     inkscape:label="Calque 1"
     inkscape:groupmode="layer"
     id="layer1"
     transform="translate(-68.035655,-83.677011)">
    <path
       style="opacity:0.97399998;fill:#cccccc;fill-opacity:1;stroke:none;stroke-width:0.17857143;stroke-miterlimit:4;stroke-dasharray:none;stroke-dashoffset:0;stroke-opacity:1"
       d="m 73.446945,106.42936 0.128109,-4.5835 -1.597557,-2.267718 C 71.098842,98.330905 69.945912,96.667234 69.41543,95.881096 l -0.964509,-1.429346 3.99819,-1.096065 c 2.199003,-0.602837 4.135837,-1.235125 4.304073,-1.405089 0.168235,-0.16996 1.222943,-1.797301 2.3438,-3.616311 1.120855,-1.819011 2.142654,-3.421904 2.270665,-3.561985 0.189344,-0.207198 0.712581,0.461174 2.805973,3.584281 l 2.573226,3.838975 1.275821,0.342072 c 3.718904,0.997108 4.955786,1.343175 5.839301,1.633786 l 0.972704,0.319947 -2.640256,3.677785 -2.640259,3.677794 0.110117,2.36235 c 0.06056,1.2993 0.162796,3.36163 0.227179,4.58296 0.07575,1.43699 0.05015,2.22061 -0.07254,2.22061 -0.104278,0 -2.059483,-0.67417 -4.344892,-1.49817 l -4.15529,-1.49817 -3.915288,1.49817 c -2.153407,0.824 -3.953383,1.49817 -3.999944,1.49817 -0.04656,0 -0.02701,-2.06257 0.04345,-4.5835 z"
       id="path68"
       inkscape:connector-curvature="0" />
  </g>
</svg>Parodie</li>
          </ul>
          <ul class="subtype">
              <li><span style="color: #c44e52"> &#x25A0;</span> Poésie</li>
              <li><span style="color: #4c72b0"> &#x25A0;</span> Prose</li>
              <li><span style="color: #ccb974"> &#x25A0;</span> Opéra</li>
              <li><span style="color: #55a868"> &#x25A0;</span> Théâtre</li>
              <li><span style="color: #dd8452"> &#x25A0;</span> Bande dessinée</li>
              <li><span style="color: #8172b3"> &#x25A0;</span> Autre</li>
          </ul>
      </div>
                </section>
                    <article id="texte_principal">
                        <div id="center">
                            <div id="main">
                                
                            <div id="body" class="body">
                                <xsl:apply-templates select="//body"/></div>
                            </div>
                            
                        </div>
                        <xsl:apply-templates select="//listApp"></xsl:apply-templates>
                        <div class="footnotes">
                            <xsl:for-each select="//note">
                                <div class="footnote">
                                <a id="note_{count(preceding::note)+1}" href="#appel_{count(preceding::note)+1}" class="note footnote"><xsl:value-of select="count(preceding::note)+1"/></a>
                                    <xsl:choose>
                                        <xsl:when test="not(descendant::p) and not(descendant::l)">
                                            <p><xsl:apply-templates/></p>
                                        </xsl:when>
                                        <xsl:otherwise><xsl:apply-templates/></xsl:otherwise>
                                    </xsl:choose>
                                    
                                </div>
                            </xsl:for-each>
                        </div>
                    </article>
                    <!--<article id="correspondances">
                        <xsl:apply-templates select=".//app" mode="corresps"></xsl:apply-templates>
                    </article>-->
                
                <section id="champ">
                    <div id="cy2"></div>
                </section>
            </body>
            <script>
                function init(){
                change_corresp();
                surlignerMots()
                }
            </script>
        </html>
        </xsl:result-document>
        <xsl:apply-templates select="body" mode="json"></xsl:apply-templates>
    </xsl:template>
    
    <xsl:template match="body" mode="json">
        <xsl:result-document encoding="utf-8" method="text" href="json/{//structure}.js">
            var auteurs_graphe = 
            {
            "data": [],
            "directed": false,
            "multigraph": false,
            "elements":
                {
                    "nodes": 
                    [
                    {"data": {"id" : "<xsl:value-of select="//structure"/>", "weight" : <xsl:value-of select="count(//app/rdg/s)"/>}},
            <xsl:for-each select="//rdg">
                <xsl:variable name="corresp" select="@source"/>
                <xsl:if test="not(preceding::rdg[@source= $corresp])">
                    {"data": {"id" : "<xsl:value-of select="$corresp"/>", "weight" : <xsl:value-of select="count(//rdg[@source= $corresp]/s)"/>}},
                </xsl:if>
            </xsl:for-each>
               ],
               "edges":
               [
               <xsl:for-each select="//rdg">
                   <xsl:variable name="target" select="@source"/>
                   <xsl:if test="not(preceding::rdg[@source= $target])">
                       {"data": {"id" : "<xsl:value-of select="concat($target,'_',//structure)"/>", "source": "<xsl:value-of select="//structure"/>", "target" : "<xsl:value-of select="$target"/>", "weight" : <xsl:value-of select="count(//rdg[@source= $target]/s)"/>}},
                   </xsl:if>
               </xsl:for-each>
                ]
                }
               };
            var liens_phrases =  {"data": [],
            "directed": false,
            "multigraph": true,
            "elements":
            {
            "nodes":
            [
            <xsl:for-each select="//app">
                <xsl:for-each select="lem/s">
                    {"data": {"id" : "<xsl:value-of select="@id"/>", "auteur" : "<xsl:value-of select="//structure"/>", "weight" : <xsl:value-of select="count(contains(@corresp, ' '))+1"/>}},
                </xsl:for-each>
                <xsl:for-each select="rdg/s">
                    <xsl:variable name="target_id" select="@id"/>
                    <xsl:if test="not(preceding::rdg/s[@id = $target_id])">
                    {"data": {"id" : "<xsl:value-of select="@id"/>", "auteur" : "<xsl:value-of select="parent::rdg/@source"/>", "weight" : <xsl:value-of select="count(//lem/s[contains(@corresp, $target_id)])"/>}},
                    </xsl:if>
                </xsl:for-each>
            </xsl:for-each>
            ],
            "edges":
            [<xsl:for-each select="//rdg/s">
                <xsl:variable name="target" select="@id"/>
                <xsl:variable name="auteur_target" select="parent::rdg/@source"/>
                <xsl:if test="not(preceding::rdg/s[@id = $target])">
                    <xsl:for-each select="//lem/s[contains(@corresp, $target)]">
                        {"data": {"id" : "<xsl:value-of select="concat($target,'_',@id)"/>", "source": "<xsl:value-of select="@id"/>", "target" : "<xsl:value-of select="$target"/>", "weight" : <xsl:value-of select="count(descendant::xr[contains(@corresp, $target)])"/>, "auteur_source" : "<xsl:value-of select="//structure"/>", "auteur_target" : "<xsl:value-of select="$auteur_target"/>"}},
                    </xsl:for-each>

                </xsl:if>
            </xsl:for-each>
            ]
            }};
            <!--var liens_mots = [<xsl:for-each select="//xr[ancestor::lem]">
                <xsl:text>{"source" : "</xsl:text><xsl:value-of select="parent::w/@id"/><xsl:text>",
                    "target" : "</xsl:text><xsl:value-of select="@corresp"/><xsl:text>",
                    "score" : </xsl:text><xsl:value-of select="@cert"/><xsl:text>,
                    "type" : "</xsl:text><xsl:value-of select="@type"/><xsl:text>"},
                    </xsl:text>
            </xsl:for-each>];-->
            <!--var dictionnaireMots = [<xsl:for-each select="//xr">
                <xsl:variable name="xr_id" select="parent::w/@id"/>
                
                <xsl:variable name="xr_corresp" select="@corresp"/>
                
                <xsl:if test="not(following-sibling::xr)">
                    <xsl:text>{"id" : "</xsl:text><xsl:value-of select="parent::w/@id"/><xsl:text>",
                    "mot" : "</xsl:text><xsl:value-of select="parent::w/text()"/><xsl:text>",
                    "lemme" : "</xsl:text><xsl:value-of select="parent::w/@lemma"/><xsl:text>",
                    "pos" : "</xsl:text><xsl:value-of select="parent::w/@pos"/><xsl:text>"},
                    </xsl:text>
                </xsl:if>
                <xsl:if test="not(preceding::xr[@corresp = $xr_corresp]) and //w[@id = $xr_corresp]">
                    <xsl:text>{"id" : "</xsl:text><xsl:value-of select="//w[@id = $xr_corresp]/@id"/><xsl:text>",
                    "mot" : "</xsl:text><xsl:value-of select="//w[@id = $xr_corresp]/text()"/><xsl:text>",
                    "lemme" : "</xsl:text><xsl:value-of select="//w[@id = $xr_corresp]/@lemma"/><xsl:text>",
                    "pos" : "</xsl:text><xsl:value-of select="//w[@id = $xr_corresp]/@pos"/><xsl:text>"},
                    </xsl:text>
                </xsl:if>
            </xsl:for-each>];
            var phrases_auteurs = {
            <xsl:for-each select="//rdg">
                <xsl:text>"</xsl:text><xsl:value-of select="@xml:id"/><xsl:text>" : "</xsl:text><xsl:value-of select="@source"/><xsl:text>",
                    </xsl:text>
            </xsl:for-each>};
            var correspondances_phrases = {
            <xsl:for-each select="//lem">
                <xsl:text>"</xsl:text><xsl:value-of select="s/@id"/><xsl:text>" : "</xsl:text><xsl:value-of select="s/@corresp"/><xsl:text>",
                    </xsl:text>
            </xsl:for-each>};
-->        </xsl:result-document>
    </xsl:template>
    
    
    <!--Texte sans correspondances-->
    <xsl:template match="teiHeader|front"/>
    <xsl:template match="body">
        <xsl:apply-templates/>
    </xsl:template>
    <xsl:template match="div">
        <xsl:param name="level" select="count(ancestor::*) - 2"/>
        <xsl:param name="el">
            <xsl:choose>
                <xsl:when test="self::group">div</xsl:when>
                <xsl:otherwise>section</xsl:otherwise>
            </xsl:choose>
        </xsl:param>
        <xsl:element name="{$el}" namespace="http://www.w3.org/1999/xhtml">
            
            <xsl:attribute name="class">div level<xsl:value-of select="$level + 1"/></xsl:attribute>
            <!-- attributs epub3 -->
            
            <!-- First element is an empty(?) page break, may come from numerisation or text-processor -->
            <xsl:variable name="name" select="local-name()"/>
            <xsl:choose>
                <xsl:when test="not(preceding-sibling::*[$name = local-name()]) and not(preceding-sibling::p|preceding-sibling::quote)"/>
                <xsl:when test="$level &lt; 2"/>
                <xsl:when test="$level &gt; 3"/>
                <xsl:otherwise/>
            </xsl:choose>
            <xsl:apply-templates select="*">
                <xsl:with-param name="level" select="$level + 1"/>
            </xsl:apply-templates>
        </xsl:element>
    </xsl:template>
    
    <xsl:template match="p">
        <p><xsl:apply-templates/></p>
    </xsl:template>
    <xsl:template match="q">
        <div class="q {@type}">
            <xsl:apply-templates/>
        </div>
    </xsl:template>
    <xsl:template match="opener | signed | speaker | stage">
        <p class="{local-name()}">
            <xsl:apply-templates/>
        </p>
    </xsl:template>
    
    <xsl:template match="head">
        <xsl:variable name="niveau" select="count(ancestor::div)+1"/>
        <xsl:element name="{concat('h', $niveau)}">
            <xsl:apply-templates/>
        </xsl:element>
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
        
    <xsl:template match="p">
        <xsl:element name="p">
            <xsl:apply-templates></xsl:apply-templates>
        </xsl:element>
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
    <xsl:template match="listApp">
        <xsl:apply-templates/>
    </xsl:template>
    
    <xsl:template match="app">
        <div id="{@xml:id}" data-id="pop">
            <div id="fermeture" onclick="document.getElementById('{@xml:id}').style.display='none'">X</div>
            <div class="infos">
                <form action="affiche-correspondance()">
                    <legend>Choisir le texte correspondant</legend>
                    <select id="corresps" name="corresps" onchange="change_corresp('{@xml:id}')">
                    <xsl:for-each select="descendant::rdg">
                        <option value="{concat(@source, '_',@xml:id)}"><xsl:value-of select="@source"/><xsl:text>, phrase </xsl:text><xsl:value-of select="string(number(substring(@xml:id, 3)))"/></option>
                    </xsl:for-each>
                    </select>
                </form>
                <input id="mots" type="checkbox" value="MT" onchange="optionChange('{@xml:id}',2)"></input>
                <label for="mots">Mots</label>
                <ul class="legende" id="legendeMots" style="display:none">
                    <li style="background-color:#C0392B; color:#fff">Mot à mot</li>
                    <li style="background-color:#28b463; color:#fff">Synonymie</li>
                    <li style="background-color:#E67E22; color:#fff">Relations lexicales flextionnelles et dérivationnelles</li>
                </ul>
           
            <input id="groupes" type="checkbox" value="GR" onchange="optionChange('{@xml:id}',1)"/>
                <label for="groupes">Groupes des mots et noms propres</label>
                <ul class="legende" id="legendeGroupes" style="display:none">
                    <li style="background-color:#C0392B; color:#fff">Reprise mot à mot</li>
                    <li style="background-color:#28b463; color:#fff">Reformulation</li>
                    <li style="background-color:#3498db; color:#fff">Métaphore</li>
                        <li style="background-color:#8e44ad; color: #fff">Changement ou périphrase d'un nom propre</li>
                </ul>
            
            </div>
            <div class="source" id="{descendant::lem/s/@id}">
                <h5><xsl:value-of select="//structure"/><xsl:text>, phrase </xsl:text><xsl:value-of select="string(number(substring(descendant::lem/s/@id, 3)))"/></h5>
                <xsl:apply-templates select="descendant::lem"></xsl:apply-templates>
            </div>
            <div class="target">
                <xsl:for-each select="descendant::rdg">
                        <xsl:element name="div">
                            <xsl:attribute name="id"><xsl:value-of select="concat(@source, '_',@xml:id)"/></xsl:attribute>
                            <xsl:attribute name="data-id"><xsl:value-of select="descendant::s/@id"/></xsl:attribute>
                            <xsl:if test="following-sibling::rdg"><xsl:attribute name="style">display:none</xsl:attribute></xsl:if>
                            <h5><xsl:value-of select="@source"/><xsl:text>, phrase </xsl:text><xsl:value-of select="string(number(substring(@xml:id, 3)))"/></h5>
                            
                            <xsl:apply-templates select="."/>
                        </xsl:element>    
                </xsl:for-each>
            </div>
        </div>
    </xsl:template>
    
    <xsl:template match="milestone[@corresp]">
        <a class="note" onclick="affiche('{@corresp}')">✱</a>
    </xsl:template>
    
    <xsl:template match="note">
        <a class="note" id="appel_{count(preceding::note)+1}" href="#note_{count(preceding::note)+1}"><xsl:value-of select="count(preceding::note)+1"/></a>
    </xsl:template>
    
    <xsl:template match="interpGrp | xr"/>
    
    <xsl:template match="lem|rdg">
        <xsl:apply-templates/>
    </xsl:template>
    
    <xsl:template match="s">
        <p><xsl:apply-templates/></p>
    </xsl:template>
    
    
    
    <xsl:template match="phr">
        <span data-type="{@type}"><xsl:apply-templates/><xsl:if test="following-sibling::*[1]/local-name() != 'pc'"><xsl:text> </xsl:text></xsl:if></span>
    </xsl:template>
    <xsl:template match="w">
        <xsl:variable name="apostrophe">'</xsl:variable>
            <xsl:choose>
                <xsl:when test="descendant::xr and ancestor::lem">
                    <xsl:call-template name="boucle_xr"><xsl:with-param name="w" select="."></xsl:with-param><xsl:with-param name="xr" select="descendant::xr[1]"></xsl:with-param></xsl:call-template>
                    <!--<xsl:for-each select="descendant::xr">
                        <xsl:element name="span">
                            <xsl:attribute name="class"><xsl:call-template name="type_corresp"><xsl:with-param name="xr" select="."></xsl:with-param></xsl:call-template></xsl:attribute>
                            <xsl:attribute name="data-href">
                                <xsl:value-of select="@corresp"/>
                            </xsl:attribute>
                            <xsl:attribute name="data-corresp">
                                    <xsl:value-of select="concat(ancestor::app/descendant::rdg[descendant::w[@id = @corresp]]/@source, '_',@corresp)"/>
                            </xsl:attribute>
                    <xsl:choose>
                        <!-\-<xsl:when test="not(ends-with(parent::w, $apostrophe)) and parent::w/following-sibling::*[1]/local-name()!= 'pc' and parent::w/following-sibling::*[1]/local-name() = 'w'"><xsl:apply-templates/><xsl:text> </xsl:text></xsl:when>
                        <xsl:when test="not(ends-with(parent::w, $apostrophe)) and parent::w/following-sibling::*[1]/local-name() != 'pc' and parent::w/following-sibling::*[1]/local-name() = 'phr'"><xsl:apply-templates/><xsl:text> </xsl:text></xsl:when>
                        <xsl:when test="ends-with(., $apostrophe)"><xsl:value-of select="translate(., $apostrophe, '’')"/></xsl:when>-\->
                        <xsl:when test="following-sibling::xr"><xsl:apply-templates select="parent::w"></xsl:apply-templates></xsl:when>
                        <xsl:otherwise><xsl:apply-templates/></xsl:otherwise>
                    </xsl:choose>
                </xsl:element>
                    </xsl:for-each>-->
            </xsl:when>
            <xsl:when test="ancestor::rdg">
                <xsl:element name="span">
            <xsl:call-template name="corresp_target">
                <xsl:with-param name="id_mot" select="@id"/>
                <xsl:with-param name="phrase_source" select="ancestor::app/lem/s"/>
            </xsl:call-template>
                    <xsl:choose>
                        <xsl:when test="not(ends-with(., $apostrophe)) and following-sibling::*[1]/local-name()!= 'pc' and following-sibling::*[1]/local-name() = 'w'"><xsl:apply-templates/><xsl:text> </xsl:text></xsl:when>
                        <xsl:when test="not(ends-with(., $apostrophe)) and following-sibling::*[1]/local-name() != 'pc' and following-sibling::*[1]/local-name() = 'phr'"><xsl:apply-templates/><xsl:text> </xsl:text></xsl:when>
                        <xsl:when test="ends-with(., $apostrophe)"><xsl:value-of select="translate(., $apostrophe, '’')"/></xsl:when>
                        <xsl:otherwise><xsl:apply-templates/></xsl:otherwise>
                    </xsl:choose>
                </xsl:element>
            </xsl:when>
            <xsl:otherwise>
                <xsl:element name="span">
                <xsl:attribute name="class">w</xsl:attribute>
            
            <xsl:choose>
                <xsl:when test="not(ends-with(., $apostrophe)) and following-sibling::*[1]/local-name()!= 'pc' and following-sibling::*[1]/local-name() = 'w'"><xsl:apply-templates/><xsl:text> </xsl:text></xsl:when>
                <xsl:when test="not(ends-with(., $apostrophe)) and following-sibling::*[1]/local-name() != 'pc' and following-sibling::*[1]/local-name() = 'phr'"><xsl:apply-templates/><xsl:text> </xsl:text></xsl:when>
                <xsl:when test="ends-with(., $apostrophe)"><xsl:value-of select="translate(., $apostrophe, '’')"/></xsl:when>
                <xsl:otherwise><xsl:apply-templates/></xsl:otherwise>
            </xsl:choose>
                </xsl:element>
            </xsl:otherwise>
            </xsl:choose>
    </xsl:template>
    
    <xsl:template name="boucle_xr">
        <xsl:param name="w"></xsl:param>
        <xsl:param name="xr"></xsl:param>
        <xsl:variable name="apostrophe">'</xsl:variable>
        <xsl:element name="span">
            <xsl:attribute name="class"><xsl:call-template name="type_corresp"><xsl:with-param name="xr" select="$xr"></xsl:with-param></xsl:call-template></xsl:attribute>
            <xsl:attribute name="data-href">
                <xsl:value-of select="$xr/@corresp"/>
            </xsl:attribute>
            <xsl:attribute name="data-corresp">
                <xsl:value-of select="concat($xr/ancestor::app/rdg[descendant::w[@id = $xr/@corresp]]/@source, '_', substring-before($xr/@corresp, '_'))"/>
            </xsl:attribute>
            <xsl:choose>
                <xsl:when test="$xr[following-sibling::xr]">
                    <xsl:call-template name="boucle_xr"><xsl:with-param name="w" select="$w"/><xsl:with-param name="xr" select="$xr/following-sibling::xr[1]"></xsl:with-param></xsl:call-template>
                </xsl:when>
                <xsl:otherwise>
                    <xsl:choose>
                        <xsl:when test="not(ends-with($w, $apostrophe)) and $w/following-sibling::*[1]/local-name()!= 'pc' and $w/following-sibling::*[1]/local-name() = 'w'"><xsl:apply-templates/><xsl:text> </xsl:text></xsl:when>
                        <xsl:when test="not(ends-with($w, $apostrophe)) and $w/following-sibling::*[1]/local-name() != 'pc' and $w/following-sibling::*[1]/local-name() = 'phr'"><xsl:apply-templates/><xsl:text> </xsl:text></xsl:when>
                        <xsl:when test="ends-with($w, $apostrophe)"><xsl:value-of select="translate($w, $apostrophe, '’')"/></xsl:when>
                        <xsl:otherwise><xsl:apply-templates/></xsl:otherwise>
                    </xsl:choose>
                </xsl:otherwise>
                
            </xsl:choose>
        </xsl:element>
    </xsl:template>
    <xsl:template name="corresp_target">
        <xsl:param name="id_mot"/>
        <xsl:param name="phrase_source"/>
        <xsl:if test="$phrase_source//w/xr[@corresp = $id_mot]"><xsl:attribute name="class"><xsl:call-template name="type_corresp"><xsl:with-param name="xr" select="$phrase_source//w/xr[@corresp = $id_mot]"></xsl:with-param></xsl:call-template></xsl:attribute>
            <xsl:attribute name="data-id"><xsl:value-of select="$id_mot"/></xsl:attribute>
            
        
        </xsl:if>
    </xsl:template>
    
    <xsl:template name="type_corresp">
        <xsl:param name="xr"/>
        <xsl:choose>
            <xsl:when test="$xr[contains(@type, 'syno')]">
                <xsl:text>synos</xsl:text>
            </xsl:when>
            <xsl:when test="$xr[contains(@type, 'anto')] and $xr[not(contains(@type, 'syno'))]">
                <xsl:text>antos</xsl:text>
            </xsl:when>
            <xsl:otherwise>
                <xsl:value-of select="$xr/@type"/>
            </xsl:otherwise>
        </xsl:choose>
            
        
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
