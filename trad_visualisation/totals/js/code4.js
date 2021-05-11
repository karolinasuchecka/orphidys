var indexColors = [
        "#000000", "#FFFF00", "#1CE6FF", "#FF34FF", "#FF4A46", "#008941", "#006FA6", "#A30059",
        "#FFDBE5", "#7A4900", "#0000A6", "#63FFAC", "#B79762", "#004D43", "#8FB0FF", "#997D87",
        "#5A0007", "#809693", "#FEFFE6", "#1B4400", "#4FC601", "#3B5DFF", "#4A3B53", "#FF2F80",
        "#61615A", "#BA0900", "#6B7900", "#00C2A0", "#FFAA92", "#FF90C9", "#B903AA", "#D16100",
        "#DDEFFF", "#000035", "#7B4F4B", "#A1C299", "#300018", "#0AA6D8", "#013349", "#00846F",
        "#372101", "#FFB500", "#C2FFED", "#A079BF", "#CC0744", "#C0B9B2", "#C2FF99", "#001E09",
        "#00489C", "#6F0062", "#0CBD66", "#EEC3FF", "#456D75", "#B77B68", "#7A87A1", "#788D66",
        "#885578", "#FAD09F", "#FF8A9A", "#D157A0", "#BEC459", "#456648", "#0086ED", "#886F4C",
        "#34362D", "#B4A8BD", "#00A6AA", "#452C2C", "#636375", "#A3C8C9", "#FF913F", "#938A81",
        "#575329", "#00FECF", "#B05B6F", "#8CD0FF", "#3B9700", "#04F757", "#C8A1A1", "#1E6E00",
        "#7900D7", "#A77500", "#6367A9", "#A05837", "#6B002C", "#772600", "#D790FF", "#9B9700",
        "#549E79", "#FFF69F", "#201625", "#72418F", "#BC23FF", "#99ADC0", "#3A2465", "#922329",
        "#5B4534", "#FDE8DC", "#404E55", "#0089A3", "#CB7E98", "#A4E804", "#324E72", "#6A3A4C",
        "#83AB58", "#001C1E", "#D1F7CE", "#004B28", "#C8D0F6", "#A3A489", "#806C66", "#222800",
        "#BF5650", "#E83000", "#66796D", "#DA007C", "#FF1A59", "#8ADBB4", "#1E0200", "#5B4E51",
        "#C895C5", "#320033", "#FF6832", "#66E1D3", "#CFCDAC", "#D0AC94", "#7ED379", "#012C58",
        "#7A7BFF", "#D68E01", "#353339", "#78AFA1", "#FEB2C6", "#75797C", "#837393", "#943A4D",
        "#B5F4FF", "#D2DCD5", "#9556BD", "#6A714A", "#001325", "#02525F", "#0AA3F7", "#E98176",
        "#DBD5DD", "#5EBCD1", "#3D4F44", "#7E6405", "#02684E", "#962B75", "#8D8546", "#9695C5",
        "#E773CE", "#D86A78", "#3E89BE", "#CA834E", "#518A87", "#5B113C", "#55813B", "#E704C4",
        "#00005F", "#A97399", "#4B8160", "#59738A", "#FF5DA7", "#F7C9BF", "#643127", "#513A01",
        "#6B94AA", "#51A058", "#A45B02", "#1D1702", "#E20027", "#E7AB63", "#4C6001", "#9C6966",
        "#64547B", "#97979E", "#006A66", "#391406", "#F4D749", "#0045D2", "#006C31", "#DDB6D0",
        "#7C6571", "#9FB2A4", "#00D891", "#15A08A", "#BC65E9", "#FFFFFE", "#C6DC99", "#203B3C",
        "#671190", "#6B3A64", "#F5E1FF", "#FFA0F2", "#CCAA35", "#374527", "#8BB400", "#797868",
        "#C6005A", "#3B000A", "#C86240", "#29607C", "#402334", "#7D5A44", "#CCB87C", "#B88183",
        "#AA5199", "#B5D6C3", "#A38469", "#9F94F0", "#A74571", "#B894A6", "#71BB8C", "#00B433",
        "#789EC9", "#6D80BA", "#953F00", "#5EFF03", "#E4FFFC", "#1BE177", "#BCB1E5", "#76912F",
        "#003109", "#0060CD", "#D20096", "#895563", "#29201D", "#5B3213", "#A76F42", "#89412E",
        "#1A3A2A", "#494B5A", "#A88C85", "#F4ABAA", "#A3F3AB", "#00C6C8", "#EA8B66", "#958A9F",
        "#BDC9D2", "#9FA064", "#BE4700", "#658188", "#83A485", "#453C23", "#47675D", "#3A3F00",
        "#061203", "#DFFB71", "#868E7E", "#98D058", "#6C8F7D", "#D7BFC2", "#3C3E6E", "#D83D66",
        "#2F5D9B", "#6C5E46", "#D25B88", "#5B656C", "#00B57F", "#545C46", "#866097", "#365D25",
        "#252F99", "#00CCFF", "#674E60", "#FC009C", "#92896B"
    ];

function surlignerMots(idApp){
    var container = document.getElementById(idApp);
    container.getElementsByTagName('ul')[0].style.display ='block';
    var mots_actifs = container.getElementsByTagName('span');
    for (var mot_actif of mots_actifs){
        mot_actif.classList.add('active');
        mot_actif.addEventListener('mouseenter', enterCorrespondances, false);
        mot_actif.addEventListener('mouseleave', exitCorrespondances, false);
    }
}

function enterCorrespondances(e){
    console.log("c'est parti !");
    var id_element = e.target.getAttribute('data-href');
    console.log(id_element);
    e.target.classList.add('zoom');
    var corresps = document.querySelectorAll("[data-id = '"+id_element+"']");
    console.log(corresps);
    for (var corresp of corresps){
        corresp.classList.add('zoom');
        if (corresp.getElementsByTagName("span").length > 0){
            for (var span of corresp.getElementsByTagName("span")){
                span.classList.add('zoom')
            }
        }
    };
}

function exitCorrespondances(e){
    console.log("c'est parti !");
    var id_element = e.target.getAttribute('data-href');
    console.log(id_element);
    e.target.classList.remove('zoom'); 
    var corresps = document.querySelectorAll("[data-id ~= '"+id_element+"']")
    for (var corresp of corresps){
        corresp.classList.remove('zoom');
        if (corresp.getElementsByTagName("span").length > 0){
            for (var span of corresp.getElementsByTagName("span")){
                span.classList.remove('zoom')
            }
        }
    };
} 


$.getJSON("../jsons/mort_virgile.json", function (data) {
// Visualisation modulable créée dans le cadre du développement du logiciel Galaxies 2.0 (Jean-Gabriel Ganascia, (dir.)). Pour toute modification, pensez à donner des noms sémantiques aux variables et à bien commenter tous les changements.

//fonction qui sort les tableaux de la plus grande à la plus petite valeur et retourne un tableau des tuples (clé, valeur)
function sortProperties(obj)
{
    var sortable = [];
    for (var key in obj){
        if(obj.hasOwnProperty(key)){
            sortable.push([key, obj[key]])
        }
    }
        sortable.sort(function(a, b){
            return b[1]-a[1];
        });
        return sortable;
    
}

function showEdgeInfo(elem){
    var id = elem.data("id");
    document.getElementById(id).style.display = "inline-flex";

 
}
//######TRAITEMENT POUR LA VISUALISATION FOCALISEE SUR LES NOEUDS######
//tableaux de stockage des données json
var occurrencesAuteurs = []; //tableau des occurrences des auteurs pour le graphe #stats1
var occurrencesTitres = [];//tableau des occurrences des titres si un seul auteur
var occurrencesLemmes = [];
var sources = []; //tableau des sources des liens (utilité : #stats2)
var targets = []; //tableau des target des liens (utilité : #stats2)
var titres =new Map(); //titres des oeuvres. Clé : id du noeud, valeur : titre
var Colors = ['#CE4760','#495867','#3E885B', '#BDD5EA', '#FE5F55', '#8E44AD', '#412C6E', '#EE8434', '#C2B2B4','#4cb08b' , '#23CE6B', '#638475', '#425cd1','#F7B32B','#C5D86D','#86615C','#F7AEF8','#95D9C3','#8093F1','#577399', '#8BB174'];
var CouleursAuteurs = new Map;
var CouleursAuteurs = new Map(); //clé :auteur, valeur : couleur attribué
var CouleursTitres = new Map(); //si un seul auteur, clé : titre, valeur : couleur
var CouleursLemmes = new Map();
    
var id = new Map(); // clé : id, valeur : auteur

//on compte les auteurs pour savoir lequel sera l'auteur principal et s'il y en a plus qu'un (si c'est le cas, on prend en compte plutôt les titres des ouvrages)
var auteurs = {};
for (var i = 0; i< data.elements.nodes.length; i++)
{
    auteur = data.elements.nodes[i].data.auteur;
    if (auteurs[auteur] == undefined)
    {
        auteurs[auteur] = 1
    }
    else
    {
        auteurs[auteur]++
    }
}
auteurP = sortProperties(auteurs);
var auteurPrincipal = auteurP[0][0];
        
       
//on dessine le graphe focalisé sur les noeuds
var cy = cytoscape(
    {
        container: document.getElementById('cy'),
        elements: data['elements'],
        style: [
            {
                selector: 'node',
                style: {
                    'content': function(ele){
                        console.log(ele.data('id'));
                        return ele.data('auteur')+', ph. '+parseInt(ele.data('id').substr(2));
                    },
                    //'label' : 'data(id)',
                    //'content': 'data(titre)',
		    'text-wrap' : 'ellipsis',
		    'text-max-width' : '200px',
                    'width': function(ele){return ele.data('nbLiens')*50+'px'},
		    'height' : function(ele){return ele.data('nbLiens')*50+'px'},
            'border-color' : function(ele){
                var typeTrad = {
    "delille1770" : "vers",
    "charpentier1831" : "prose",
    "desportes1846_vers" : "vers",
    "guillois1863" : "vers",
    "desportes1846_prose" : "prose",
    "cogolin1750" : "vers",
    "rat1932" : "prose",
    "desfontaines1810" : "prose",
    "cabaret-dupaty1897" : "prose",
    "duchemin1837" : "prose",
    "cournand1805" : "vers",
    "nisard1868" : "prose",
    "fournier1876" : "vers",
    "heguin1827" : "prose",
};

 var couleurs = { 'vers' : '#C0392B', 'prose' : '#2980B9'};
                        var auteur = ele.data('auteur');
                        console.log(auteur, typeTrad[auteur]);
                        var subtype = typeTrad[auteur];
                        return(couleurs[subtype]) 
                    },
                    'border' : 'solid',
                    'border-width' : '10px',
		    'background-color' : function(ele) //function qui attribue une couleur aléatoire au noeud et extrait les données pour tabs id, occurrences et CouleursAuteurs
                    { // boléen pour tenter de différencier les couleurs aléatoires
                        var auteur = ele.data('auteur');
                        id[ele.data('id')] = ele.data('auteur');
                        var listeAuteurs = Object.keys(auteurs)
                        //si plus qu'un auteur, on colorie selon les noms d'auteurs
                        if (Object.keys(auteurs).length > 1)
                        {
                            //si auteur présent dans CouleursAuteurs, l'élément en cours prend la couleur attribué. On ajoute une occurrence pour cet auteur pour #stats1
                            if (CouleursAuteurs.has(auteur))
                            {
                                occurrencesAuteurs[auteur] = occurrencesAuteurs[auteur]+1;
                                //return CouleursAuteurs.get(auteur)
                                return ""
                            }
                            else
                            {
                                var couleur = Colors[listeAuteurs.indexOf(auteur)];
                                    colorType = 1
                                }
                                occurrencesAuteurs[auteur] = 1; //on ajoute la première occurrences
                                CouleursAuteurs.set(auteur, couleur);
                                return ""
                                } //on retourne la couleur
                        
                        
						
                    },
                    'shape' : 'diamond',
                    'text-wrap' : "wrap",
                        'font-family': 'Raleway',
                        'font-size' : '25px',
                        'text-valign': 'center',
        'text-halign': 'center',
        'text-background-color' : 'white',
        'text-background-opacity' : 0.5,
                    
                    'background-fit': 'contain',
                    'background-clip': 'none',
                    "z-index": 0
                }
            },
            {
              selector: "node:selected",
              style: {
                  'label': function(ele) //on concatène l'auteur, le titre et l'extrait
                  {
                      quatres = LemmesColors(ele);
                      texte = '';
                      console.log(quatres);
                      for (var lemme of quatres){
                        if (lemme != undefined){
                        texte += lemme[0]+' ('+lemme[1]+' occ.)\n'

                      }
                  }
                      return(texte) 
                  },
                    
                    'pie-size' : '100%',
                  'text-wrap': 'wrap',
                  'text-max-width': '200px',
                  'text-max-height': 'auto',
                  'border-width': '0px',
                  'border-color': '#AAD8FF',
                  'border-opacity': '0.5',
                  'pie-1-background-color' : function(ele) {return(pieNoeudsColor(ele, 0))},
                    'pie-1-background-size': function(ele){return(pieNoeudsSize(ele,0))},
                    'pie-2-background-color' : function(ele){return(pieNoeudsColor(ele, 1))},
                    'pie-2-background-size': function(ele){return(pieNoeudsSize(ele,1))},
                    'pie-3-background-color' : function(ele){return(pieNoeudsColor(ele, 2))},
                    'pie-3-background-size': function(ele){return(pieNoeudsSize(ele,2))},
                    'pie-4-background-color' : function(ele){return(pieNoeudsColor(ele, 3))},
                    'pie-4-background-size': function(ele){return(pieNoeudsSize(ele,3))},
                  'text-outline-color': '#555',
                  'text-background-color':'rgba(225, 225, 229)',
                  'text-background-opacity':'0.9',
                  'text-background-shape': 'roundrectangle',
                  //'text-background-padding': '10px',
                  'z-index': 1,
                  'font-family': 'Raleway',
                        'font-size' : '15px',
                  'text-valign': 'top',
        'text-halign': 'center',
              }
            }, 
            {
                selector: 'edge',
                style: 
                {
                    'line-color': '#91b0ad',
                    'text-background-color':
                    //function d'extraction des infos pour tabs source et target. Sans doute à optimiser.
                    function(ele)
                    {
                        var source = ele.data('source');
                        var target = ele.data('target');
                        sources.push(source);
                        targets.push(target);
                        return ('#91b0ad')
                    },
                    'text-background-opacity': 0.4,
                    'width': '5px',
                    'target-arrow-shape': 'triangle',
                    'control-point-step-size': '140px'
                }
            },
            {
                selector : 'edge:selected',
                    style : {'label' :  function(ele){showEdgeInfo(ele);}
                        
                    }
                }
        ],
        layout : 
            {
           name: 'cola',
            animate: true, // whether to show the layout as it's running
  refresh: 1, // number of ticks per frame; higher is faster but more jerky
  maxSimulationTime: 4000, // max length in ms to run the layout
  ungrabifyWhileSimulating: false, // so you can't drag nodes during layout
  fit: true, // on every layout reposition of nodes, fit the viewport
  padding: 30, // padding around the simulation
  boundingBox: undefined, // constrain layout bounds; { x1, y1, x2, y2 } or { x1, y1, w, h }
  nodeDimensionsIncludeLabels: false, // whether labels should be included in determining the space used by a node

  // layout event callbacks
  ready: function(){}, // on layoutready
  stop: function(){}, // on layoutstop

  // positioning options
  randomize: false, // use random node positions at beginning of layout
  avoidOverlap: true, // if true, prevents overlap of node bounding boxes
  handleDisconnected: true, // if true, avoids disconnected components from overlapping
  convergenceThreshold: 0.01, // when the alpha value (system energy) falls below this value, the layout stops
  nodeSpacing: function( node ){ return 30; }, // extra spacing around nodes
  flow: undefined, // use DAG/tree flow layout if specified, e.g. { axis: 'y', minSeparation: 30 }
  alignment: undefined, // relative alignment constraints on nodes, e.g. function( node ){ return { x: 0, y: 1 } }
  gapInequalities: undefined, // list of inequality constraints for the gap between the nodes, e.g. [{"axis":"y", "left":node1, "right":node2, "gap":25}]

  // different methods of specifying edge length
  // each can be a constant numerical value or a function like `function( edge ){ return 2; }`
  edgeLength: undefined, // sets edge length directly in simulation
  edgeSymDiffLength: undefined, // symmetric diff edge length in simulation
  edgeJaccardLength: undefined, // jaccard edge length in simulation

  // iterations of cola algorithm; uses default values on undefined
  unconstrIter: undefined, // unconstrained initial layout iterations
  userConstIter: undefined, // initial layout iterations with user-specified constraints
  allConstIter: undefined, // initial layout iterations with all constraints including non-overlap

  // infinite layout options
  infinite: false // overrides all other options for a forces-all-the-time mode
            },
    }
);
//fin du graphe de la visualisation focalisée sur les noeuds

//######TRAITEMENT POUR LA VISUALISATION FOCALISEE SUR LES LIENS######    
//Extraction des informations pour la visualisation focalisée sur les liens
    //On interroge le json pour mettre dans un tableau tous les mots communs associées avec un noeud (labelsNoeuds) et pour mettre dans une liste les mots présents dans la galaxie et leur nombre d'occurrences au total
    var labels = {};
    var labelsNoeuds = {};
    var labelsEdges = {};
    var labelsColors = {}
    for (var i = 0; i< data.elements.edges.length; i++)
    {
        var lemmesCommuns = data.elements.edges[i].data.label.split(' ');

        var source = data.elements.edges[i].data.source;
        var target = data.elements.edges[i].data.target;
        var label = data.elements.edges[i].data.label;
        if(labelsNoeuds[source] == undefined)
        {
            labelsNoeuds[source] = label.split(' ');
            labelsNoeuds[source].pop()
        }
        else
        {
            for (var l of label.split(' '))
                {if (l != '')
            {
                labelsNoeuds[source].push(l);
            }
        }
        }

        if (labelsEdges[source+'_'+target] == undefined)
        {
            labelsEdges[source+'_'+target] = label.split(' ');
            labelsEdges[source+'_'+target].pop()
        }

        else{
            for (var l of label.split(' '))
                {if (l != '')
            {
                labelsEdges[source+'_'+target].push(l);
            }

        }
    }

                                                 
        if(labelsNoeuds[target] == undefined)
        {
            labelsNoeuds[target] = label.split(' ');
            labelsNoeuds[target].pop()
        }
        else
        {
            for (var l of label.split(' '))
            {if (l != '')
            {
                labelsNoeuds[source].push(l);
            }
        }
        }
        for (var j = 0; j< lemmesCommuns.length; j++)
        {
            if (labels[lemmesCommuns[j]] == undefined)
            {
                labels[lemmesCommuns[j]] = 1
            }
            else{
                labels[lemmesCommuns[j]]++
            }
        }
    }
    //console.log(labelsNoeuds[source]);
    //console.log(labelsNoeuds[target]);
    
    //labels = sortProperties(labels);//on sort dans l'ordre décroissant du nombre des occurrences
    //var colorType = 0; //pour différencier au maximum les couleurs
    

//fonctions pour la visualisation focalisée sur les liens : coloration multiple des noeuds (pie charts)
// 1 : Définir la couleur de chaque partie du camembert (quatre couleurs maximum). Ele = élément, i = rang du lemme communs traité (de 0 à 3), on prend en compte les quatre lemmes le plus récurrents dans la totalité des lemmes communs du noeud source. 
function pieNoeudsColor(ele, i)
{
    var id = ele.data('id');
    var lemmes = labelsNoeuds[id];
    lemmes.sort()
    compteurLemmes = [];
    if(lemmes.length < i){return('none')}//S'il y a moins que quatre lemmes communs, on s'arrête au dernier lemme commun
    else{
        for (l of lemmes)//Sinon, on extrait tous les lemmes communs pour un noeud, on compte les occurrences pour les pondérer et on les classes de plus au moins récurrent
        {
            
                //console.log(l, labels[l])
            if(compteurLemmes[l] == undefined)
            {compteurLemmes[l] = 1
            }
            else
            {
                compteurLemmes[l] ++
            }
        
    }
        compteurLemmes = sortProperties(compteurLemmes);
        //console.log(compteurLemmes);
        if(compteurLemmes[i] != undefined)//si après la suppression des doublons, la longueur du tableau des lemmes n'est pas inférieur au rang demandé, on attribue la couleur spécifique, si le lemme n'existe pas encore dans le tableau, ou on retourne la couleur attribuée 
        {
            var lemmeTraite = compteurLemmes[i][0];
            if (CouleursLemmes.has(lemmeTraite))
            {
                occurrencesLemmes[lemmeTraite] = occurrencesLemmes[lemmeTraite]+1;
                return CouleursLemmes.get(lemmeTraite)
            }
            else
            {
                
                couleur = indexColors[0];
                indexColors.shift();
                 occurrencesLemmes[lemmeTraite] = 1; //on ajoute la première occurrence
                CouleursLemmes.set(lemmeTraite, couleur); return couleur}
        }
    }
}//fin function qui colore les noeuds selon les lemmes communs


 

    function getRandomColor() {
        var h = [0, 360];
    var s = [90, 100];
    var l = [0, 90];
    var a = [1, 1];
      var hue = getRandomNumber(h[0], h[1]);
      var saturation = getRandomNumber(s[0], s[1]);
      var lightness = getRandomNumber(l[0], l[1]);
      var alpha = getRandomNumber(a[0] * 100, a[1] * 100) / 100;
    
      //console.log(alpha);
    
      return {
        h: hue,
        s: saturation,
        l: lightness,
        a: alpha,
        hslaValue: getHSLAColor(hue, saturation, lightness, alpha)
      }
    }
    
    function getRandomNumber(low, high) {
      var r = Math.floor(Math.random() * (high - low + 1)) + low;
      return r;
    }
    
    function getHSLAColor(h, s, l, a) {
      return `hsl(${h}, ${s}%, ${l}%, ${a})`;
    }

//2: function qui détermine la taille de chaque camembert selon le nombre des occurrences du lemme pour le noeud traité. Le fonctionnement est le même que pour la fonction précédente, on retourne le pourcentage en considérant comme 100% le nombre total des occurrences pour les quatre premiers lemmes communs, s'il y en a plus dans le tableau, ou pour tous les lemmes communs, s'il y en a moins que quatre
function pieNoeudsSize(ele, i){
    var id = ele.data('id');
    var lemmes = labelsNoeuds[id];
    lemmes.sort()
    compteurLemmes = [];
    if(lemmes.length < i)
    {
        return('0%')
    }
    else
    {
        for (l of lemmes){
            //if (labels[l] > 15){
            if(compteurLemmes[l] == undefined)
            {
                compteurLemmes[l] = 1
            }
            else
            {
                compteurLemmes[l] ++
            }
        //}
    
}

        compteurLemmes = sortProperties(compteurLemmes);
        if(compteurLemmes.length <= i)
        {
            return('0%')
        }
        else
        {
            var occLemmeTraite = compteurLemmes[i][1];
            var total = 0;
            if (compteurLemmes.length < 4)
            {
                for (var j = 0; j<compteurLemmes.length; j++)
                {
                    total = total+compteurLemmes[j][1]
                }
            }
            else
            {
                for (var j = 0; j<4; j++)
                {
                    total = total+compteurLemmes[j][1]
                }
            }
            var pourcentage = (occLemmeTraite*100)/total;
            return(pourcentage+'%')
        }
    }
}//fin function qui calcule la taille des camemberts

function LemmesColors(ele){

var id = ele.data('id');
    var lemmes = labelsNoeuds[id];
    lemmes.sort()
    compteurLemmes = [];
    for (l of lemmes)
        {
            //if (labels[l] > 15){
            if(compteurLemmes[l] == undefined)
            {
                compteurLemmes[l] = 1
            }
            else
            {
                compteurLemmes[l] ++
            }
        //}
    }
        compteurLemmes = sortProperties(compteurLemmes);
        QuatreLemmes = [];
        var i = 0;
        while (i<4){
            QuatreLemmes.push(compteurLemmes[i]);
            i++

        }
        console.log(QuatreLemmes)
        return(QuatreLemmes)
}

var edgesFaits = [];
    
    //création du graphe pour la visualisation focalisée sur les liens
    var cy2 = cytoscape({
        container: document.getElementById('cy2'),
        elements: data['elements'],
        style: [
            {
                selector: 'node',
                style: 
                {'label': function(ele) //on concatène l'auteur, le titre et l'extrait
                  {
                      quatres = LemmesColors(ele);
                      texte = '';
                      console.log(quatres);
                      for (var lemme of quatres){
                        if (lemme != undefined){
                        texte += lemme[0]+'\n'

                      }
                  }
                      return(texte) 
                  },
                    'text-wrap' : 'ellipsis',
                    'text-max-width' : '200px',
                    'width': function(ele){return ele.data('nbLiens')*50+'px'},
            'height' : function(ele){return ele.data('nbLiens')*50+'px'},
                    'pie-size' : '100%',
                    //'shape' : 'hexagon',
                    //appels aux fonctions pour colorier et pondérer les camemberts
                    'pie-1-background-color' : function(ele) {return(pieNoeudsColor(ele, 0))},
                    'pie-1-background-size': function(ele){return(pieNoeudsSize(ele,0))},
                    'pie-2-background-color' : function(ele){return(pieNoeudsColor(ele, 1))},
                    'pie-2-background-size': function(ele){return(pieNoeudsSize(ele,1))},
                    'pie-3-background-color' : function(ele){return(pieNoeudsColor(ele, 2))},
                    'pie-3-background-size': function(ele){return(pieNoeudsSize(ele,2))},
                    'pie-4-background-color' : function(ele){return(pieNoeudsColor(ele, 3))},
                    'pie-4-background-size': function(ele){return(pieNoeudsSize(ele,3))},
                    
                    'text-wrap' : "wrap",
                        'font-family': 'Raleway',
                        'font-size' : '20px',
                        'text-valign': 'top',
        'text-halign': 'center',
        'text-background-color' : 'white',
        'text-background-opacity' : 0.5,
                    
                    'background-fit': 'contain',
                    'background-clip': 'none',
                    'z-index': 0
                }
            },
            {
              selector: "node:selected",
              style: 
                {
                  'content': function(ele){
                        console.log(ele.data('id'));
                        return ele.data('auteur')+', ph. '+parseInt(ele.data('id').substr(2));
                    },
                    'width': function (ele) {
                        return ele.data('weightScore')/20+'px';
                    },
                    'height': function (ele) {
                        return ele.data('weightScore')/20+'px';
                    },
                    'pie-size' : '0%',
                    'background-color' : function(ele) //function qui attribue une couleur aléatoire au noeud et extrait les données pour tabs id, occurrences et CouleursAuteurs
                    { // boléen pour tenter de différencier les couleurs aléatoires
                        var auteur = ele.data('auteur');
                        id[ele.data('id')] = ele.data('auteur');
                        var listeAuteurs = Object.keys(auteurs)
                        //si plus qu'un auteur, on colorie selon les noms d'auteurs
                        if (Object.keys(auteurs).length > 1)
                        {
                            //si auteur présent dans CouleursAuteurs, l'élément en cours prend la couleur attribué. On ajoute une occurrence pour cet auteur pour #stats1
                            if (CouleursAuteurs.has(auteur))
                            {
                                occurrencesAuteurs[auteur] = occurrencesAuteurs[auteur]+1;
                                //return CouleursAuteurs.get(auteur)
                                return ''
                            }
                            else
                            {
                                var couleur = Colors[listeAuteurs.indexOf(auteur)];
                                    colorType = 1
                                }
                                occurrencesAuteurs[auteur] = 1; //on ajoute la première occurrences
                                CouleursAuteurs.set(auteur, couleur); //return couleur
                                return ''
                                } //on retourne la couleur
                        
                        
                        
                    },
                    'shape' : 'hexagon',
                    'text-valign': 'center',
        'text-halign': 'center',
                  'text-wrap': 'wrap',
                  'text-max-width': '200px',
                  'text-max-height': 'auto',
                  'border-width': '6px',
                  'border-color': '#AAD8FF',
                  'border-opacity': '0.5',
                  //'background-opacity': '0.8',
                  'text-outline-color': '#555',
                  'text-background-color':'rgba(225, 225, 229)',
                  'text-background-opacity':'0.9',
                  'text-background-shape': 'roundrectangle',
                  'text-background-padding': '10px',
                  'z-index': 1,
              }
            }, 
            {
                selector: 'edge',
                style: 
                {
                    //'label': function(ele){var source = ele.data('source');
                      //                      var target = ele.data('target');
                        //                    if (!edgesFaits.includes(target+'_'+source))
                          //                  {
                            //                var lemmesST = labelsEdges[source+'_'+target];
                              //              var lemmesTS = labelsEdges[target+'_'+source];
                              //              var total = lemmesST.concat(lemmesTS);
                                //            var totalFiltre = total.filter((item,pos) => total.indexOf(item) === pos) 
                                  //          edgesFaits.push(source+'_'+target);
                                    //        listeTotal = ''
                                      //      for (tF of totalFiltre){
                                          //      listeTotal += tF+' '
                                        //    }

                                            //return (listeTotal)
                                        //}
                                        //else
                                        //{return('')
//
  //                                      }
//
  //                                      },
                    'text-wrap':'wrap',
                    'font-family' : 'Raleway',
                    'font-size' : '12px',
                    'text-max-width': '60px',
                    'text-max-height': 'auto',
                    'edge-text-rotation': 'autorotate',
                    'text-valign': 'center',
                    'text-halign': 'top',
                    'line-color': '#91b0ad',
                    'text-background-color':'#91b0ad',
                    'text-background-opacity': 0.4,

                    'target-arrow-shape': 'triangle',
                    'source-endpoint': 'outside-to-node',
                    'target-endpoint': 'outside-to-node',
                    //tentatives de rendre les labels des liens les plus visibles...
                    'text-halign' : "center",
                    'text-valign' : "center",
                    'source-text-offset' : '40%',
                    'target-text-offset' : '40%',
                    'z-index' : 1,
                }
            },

            {
                selector : 'edge:selected',
                    style : {'label' :  function(ele){showEdgeInfo(ele);}
                        
                    }
                }
        ],
        layout : 
            {
           name: 'cola',
            animate: true, // whether to show the layout as it's running
  refresh: 1, // number of ticks per frame; higher is faster but more jerky
  maxSimulationTime: 4000, // max length in ms to run the layout
  ungrabifyWhileSimulating: false, // so you can't drag nodes during layout
  fit: true, // on every layout reposition of nodes, fit the viewport
  padding: 30, // padding around the simulation
  boundingBox: undefined, // constrain layout bounds; { x1, y1, x2, y2 } or { x1, y1, w, h }
  nodeDimensionsIncludeLabels: true, // whether labels should be included in determining the space used by a node

  // layout event callbacks
  ready: function(){}, // on layoutready
  stop: function(){}, // on layoutstop

  // positioning options
  randomize: false, // use random node positions at beginning of layout
  avoidOverlap: true, // if true, prevents overlap of node bounding boxes
  handleDisconnected: true, // if true, avoids disconnected components from overlapping
  convergenceThreshold: 0.01, // when the alpha value (system energy) falls below this value, the layout stops
  nodeSpacing: function( node ){ return 30; }, // extra spacing around nodes
  flow: undefined, // use DAG/tree flow layout if specified, e.g. { axis: 'y', minSeparation: 30 }
  alignment: undefined, // relative alignment constraints on nodes, e.g. function( node ){ return { x: 0, y: 1 } }
  gapInequalities: undefined, // list of inequality constraints for the gap between the nodes, e.g. [{"axis":"y", "left":node1, "right":node2, "gap":25}]

  // different methods of specifying edge length
  // each can be a constant numerical value or a function like `function( edge ){ return 2; }`
  edgeLength: undefined, // sets edge length directly in simulation
  edgeSymDiffLength: undefined, // symmetric diff edge length in simulation
  edgeJaccardLength: undefined, // jaccard edge length in simulation

  // iterations of cola algorithm; uses default values on undefined
  unconstrIter: undefined, // unconstrained initial layout iterations
  userConstIter: undefined, // initial layout iterations with user-specified constraints
  allConstIter: undefined, // initial layout iterations with all constraints including non-overlap

  // infinite layout options
  infinite: false // overrides all other options for a forces-all-the-time mode
            },
    }
                       );
//fin création du graphe de la visualisation focalisée sur les liens
 


//######TRAITEMENT DES LEGENDES######
//function pour la création de la légende
var couleurs = []; 
function creerLegende(mapCouleurs, int, idListe)
    {var liste = document.getElementById(idListe); 
        liste.classList.add('legendeAuteurs');
        mapCouleurs.forEach(function(couleur, obj){//on extrait chaque objet avec la couleur qui lui a été attribuée
        if (int == 1)//si titres ou auteurs, on remplit un tableau des couleurs pour le colorSet des diagrammes
        {
            couleurs.push(couleur);//on ajoute la couleur dans l'ordre de l'apparition des objets
        }
        var ligne = document.createElement("li");//on crée une ligne de la liste
        ligne.style.color = couleur; //la couleur correspondant
        var spanObj = document.createElement("span");//on crée un span pour que ce soit uniquement la puce qui est colorié (comme l'attribution aléatoire, risques de pbs de lisibilité)
        spanObj.style.color = "#555";
        spanObj.append(document.createTextNode(obj.toString())); //on affiche l'objet
        ligne.append(spanObj); //<li> -> <span>
        liste.append(ligne);//<ul> -> <li>
    });
        
    }
//Ajout de la légende dans l'élément #volet
//tableau des couleurs pour un nouveau colorSet
var liste = document.createElement("ul"); //création d'une liste
liste.setAttribute('id', 'legendeNoeuds');
if(Object.keys(auteurs).length  == 1)//si un seul auteur, on ajoute le titre avec le nom
{
    var h3 = document.createElement("h3");
    h3.append(document.createTextNode(auteurPrincipal));
    document.getElementById('volet').append(h3);
}
document.getElementById('volet').append(liste);//<div#volet> -> <ul>
if(Object.keys(auteurs).length  == 1)//si un seul auteur, on prend en compte les titres
{
    creerLegende(CouleursTitres, 1, 'legendeNoeuds')
}
else //sinon, on prend en compte les auteurs
{
    creerLegende(CouleursAuteurs, 1, 'legendeNoeuds')
}
//Ajout de légende pour les lemmes
var listeLemmes = document.createElement("ul"); //création d'une liste
listeLemmes.setAttribute('id', 'legendeLiens');
listeLemmes.style.display = 'none';
document.getElementById('volet').append(listeLemmes);//<div#volet> -> <ul>
creerLegende(CouleursLemmes, 0,  'legendeLiens');
    
//2 : Choisir la visualisation
var j = 0;
function graphAppears(){
    if(j == 0)
    {
        document.getElementById('grapheLemmes').innerHTML = 'Focaliser les noeuds';
        document.getElementById('cy').style.visibility = 'hidden';
        document.getElementById('stats').style.visibility = 'hidden';
        document.getElementById('cy2').style.visibility = 'visible';
        document.getElementById('legendeNoeuds').style.display = 'block';
        document.getElementById('legendeLiens').style.display = 'none';
        j = 1;
        i = 0;
    }
    else
    {
        document.getElementById('grapheLemmes').innerHTML = 'Focaliser les liens';
        document.getElementById('cy').style.visibility = 'visible';
        document.getElementById('stats').style.visibility = 'hidden';
        document.getElementById('cy2').style.visibility = 'hidden';
        document.getElementById('legendeNoeuds').style.display = 'none';
        document.getElementById('legendeLiens').style.display = 'block';
        j = 0;
        i = 0;
    }
}
})
//ajout du titre
//var title = data.name;
