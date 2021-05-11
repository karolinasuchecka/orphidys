var Colors = ['#CE4760','#495867','#3E885B', '#BDD5EA', '#FE5F55', '#8E44AD', '#412C6E', '#EE8434', '#C2B2B4','#4cb08b' , '#23CE6B', '#638475', '#425cd1','#F7B32B','#C5D86D','#86615C','#F7AEF8','#95D9C3','#8093F1','#577399', '#8BB174'];
var CouleursAuteurs = new Map;


function init(){
	var container = document.querySelector("#graph");
	var activeItem = null;
	var active = false;
	container.addEventListener("touchstart", dragStart, false);
    container.addEventListener("touchend", dragEnd, false);
    container.addEventListener("touchmove", drag, false);
    container.addEventListener("mousedown", dragStart, false);
    container.addEventListener("mouseup", dragEnd, false);
    container.addEventListener("mousemove", drag, false); 
       
}

function alignement(){
    document.getElementById("graph").style.display = "none";
    document.getElementById("champ").style.display = "none";
    document.getElementsByTagName("section")[1].style.display = 'block';
     document.getElementsByTagName('fieldset')[0].style.display = 'ruby';
    document.getElementsByTagName('h1')[0].style.display = 'block';
   
    
}

function isDescendant(parent, child) {
     var node = child.parentNode;
     while (node != null) {
         if (node == parent) {
             return true;
         }
         node = node.parentNode;
     }
     return false;
}

function affiche_correspondances(){
    var motsActifs = document.getElementsByClassName('actif');
    console.log(motsActifs);
    for (var motActif of motsActifs){
        var idMot = motActif.getAttribute('data-id');
        var correspsMot = motActif.getAttribute('data-corresp').split(' ');
        console.log(correspsMot)
        var div = document.getElementById(motActif.getAttribute('data-parent'));
        for (var motsCorrespondants of liens_mots){
            if (motsCorrespondants['source'] == idMot && correspsMot.includes(motsCorrespondants['target']))
                {
                    var target = motsCorrespondants['target'];
                    if (div.querySelector('[data-id=\''+idMot+'\']').parentElement.tagName = 'span')
                    {
                        div.querySelector('[data-id=\''+idMot+'\']').parentElement.classList.add('affiche');
                    }
                    if (div.querySelector('[data-id=\''+target+'\']').parentElement.tagName = 'span')
                    {
                        div.querySelector('[data-id=\''+target+'\']').parentElement.classList.add('affiche');
                        div.querySelector('[data-id=\''+target+'\']').classList.add(motsCorrespondants["type"]);
                        div.querySelector('[data-id=\''+target+'\']').setAttribute('data-corresp', idMot);
                        div.querySelector('[data-id=\''+target+'\']').addEventListener('mouseenter', enterCorrespondances, false);
                        div.querySelector('[data-id=\''+target+'\']').addEventListener('mouseleave', exitCorrespondances, false);
                        div.querySelector('[data-id=\''+idMot+'\']').addEventListener('mouseenter', enterCorrespondances, false);
                        div.querySelector('[data-id=\''+idMot+'\']').addEventListener('mouseleave', exitCorrespondances, false);
                        div.querySelector('[data-id=\''+idMot+'\']').classList.add('clique');
                    }
                }
            }
    
    }
}
        
    
   

function affiche_alignement(id_div, source, target){
    var mots = document.getElementsByClassName('actif');
    var div_source = document.getElementById(id_div);
    var div_target = document.querySelector('[data-id=\''+target+'\']');
    for (var mots_correspondants of liens_mots){
        if (mots_correspondants["target"].includes(target) && mots_correspondants["source"].includes(source))
        {
            /*if (div.querySelector('[data-id=\''+mots_correspondants["source"]+'\']').parentElement.tagName = 'span') 
            {
                div.querySelector('[data-id=\''+mots_correspondants["source"]+'\']').parentElement.classList.add('affiche');

            }*/
            if (div.querySelector('[data-id=\''+mots_correspondants["target"]+'\']').parentElement.tagName = 'span')
            {
                /*div.querySelector('[data-id=\''+mots_correspondants["target"]+'\']').parentElement.classList.add('affiche');*/
                div.querySelector('[data-id=\''+mots_correspondants["target"]+'\']').classList.add(mots_correspondants["type"]);
                div.querySelector('[data-id=\''+mots_correspondants["source"]+'\']').setAttribute("data-corresp", mots_correspondants["target"]);
                div.querySelector('[data-id=\''+mots_correspondants["target"]+'\']').setAttribute("data-corresp", mots_correspondants["source"]);
                div.querySelector('[data-id=\''+mots_correspondants["source"]+'\']').classList.add(mots_correspondants["type"]);
            }
        }
    }
}
  

// CORRESPONDANCES
var trouves = []
function trouve_identifiant(id, dictionnaire, ensembles){
    if (!trouves.includes(id)){
        for (var identifiant in dictionnaire){
            if (dictionnaire[identifiant] == dictionnaire[id] + 1 || dictionnaire[identifiant] == dictionnaire[id] - 1){
                console.log('trouvé', identifiant, id)
                ensembles.push(id);
                trouves.push(id);
                trouve_identifiant(identifiant, dictionnaire, ensembles);
            }
            
        }
            
}
    console.log(Array.from(new Set(ensembles)))
    return (Array.from(new Set(ensembles)))
}


function node_data(dictionnaire_resultats, idPhrases, auteurSource){
    var noeuds = [];
    console.log("1", noeuds);
    for (ligne in dictionnaire_resultats){
        if (idPhrases.includes(ligne)){
            var label = Number(ligne.substr(ligne.length-4));
            console.log(label);
            noeuds.push({data:{id:ligne, auteur:auteurSource, label:label}})
            var identifiants = dictionnaire_resultats[ligne].split(' ');
            for (identifiant of identifiants){
                var label = Number(identifiant.substr(identifiant.length-4));
                console.log(label);
                var auteur = phrases_auteurs[identifiant];
                noeuds.push({data:{id:identifiant, auteur:auteur, label:label}})
        }
            
            
        
    }
    }
    console.log(noeuds);
    return (noeuds)
    
}
function edge_data(dico_correspondances, idPhrasesSource){
    var liens = [];
    for (var id_source in dico_correspondances){
        if (idPhrasesSource.includes(id_source)){
        var correspondances = dico_correspondances[id_source].split(' ');
        for (var correspondance of correspondances){
            var id_commun = id_source+'_'+correspondance;
            liens.push({data:{id: id_commun, source : id_source, target: correspondance}})
        }
        
    }
    }
    console.log(liens);
    return (liens)
}

function creerLegende(mapCouleurs, idListe)
    {
        var ul = document.createElement("ul");
     var ulSubType = document.getElementsByClassName('subtype')[0];
     var spansSubType = ulSubType.getElementsByTagName('span');
     for (var span of spansSubType){span.innerHTML = '&#9633;'};
    ul.classList.add('legendeAuteurs');
    console.log(mapCouleurs);
        var liste = document.getElementById(idListe);
     
        mapCouleurs.forEach(function(couleur, obj){//on extrait chaque objet avec la couleur qui lui a été attribuée
            if (obj != undefined){
        var ligne = document.createElement("li");//on crée une ligne de la liste
        ligne.style.color = couleur; //la couleur correspondant
        var spanObj = document.createElement("span");//on crée un span pour que ce soit uniquement la puce qui est colorié (comme l'attribution aléatoire, risques de pbs de lisibilité)
        spanObj.style.color = "#555";
        spanObj.append(document.createTextNode(obj.toString())); //on affiche l'objet
        ligne.append(spanObj); //<li> -> <span>
        ul.append(ligne);//<ul> -> <li>
            }
    });
     liste.append(ul);
     
     var infos = document.getElementById('infos');

    infos.innerHTML = "<div id=\"fermeture\" onclick=\"document.getElementById('legende').style.display = 'none'\">X</div><p>Les étiquettes affichées sur les nœuds correspondent aux numéros de phrases qui les composent. <br> Cliquez sur le lien pour afficher le texte des correspondances établies entre deux nœuds. <br> Cliquez sur le nœud composé de plusieurs phrases pour afficher le graphe détaillé de leurs correspondances.</p> <button>Remonter d'un niveau</button>"
        
    }
function modifie_id_div(phrase, id_div){
    var mots = phrase.getElementsByClassName('w');
    
    for (var mot of mots){
        if (mot.hasAttribute('onclick')){
            attributs_onclick = mot.getAttribute('onclick');
            attributs_onclick = attributs_onclick.split(')')[0];
            attributs_onclick = attributs_onclick.split('(')[1];
            attributs_onclick = attributs_onclick.replace(attributs_onclick.split(',')[0], "'"+id_div+"'");
            attributs_onclick = "affiche_correspondances_alignement("+attributs_onclick+")";
            console.log(attributs_onclick);
            mot.setAttribute('onclick', attributs_onclick);
            //console.log('mot',mot);
            }
       
    }
        return(phrase)
}
function trouveActif(mot){
    var attributsAcceptes =  ['mots', 'lemmes','synos', "antos", 'actif'];
    for (var classValue of mot.classList){
        console.log(classValue);
        if (attributsAcceptes.includes(classValue)){
            return 'true'
        }
    }
    return 'false'
}

function enterCorrespondances(e){
    console.log("c'est parti !")
    var id_element = e.target.getAttribute('data-id');
    console.log(id_element);
    e.target.classList.add('zoom');
    var corresps = document.querySelectorAll("[data-corresp ~= '"+id_element+"']")
    for (var corresp of corresps){corresp.classList.add('zoom')};
}
function exitCorrespondances(e){
    console.log("c'est parti !")
    var id_element = e.target.getAttribute('data-id');
    console.log(id_element);
    e.target.classList.remove('zoom'); 
    var corresps = document.querySelectorAll("[data-corresp ~= '"+id_element+"']")
    for (var corresp of corresps){corresp.classList.remove('zoom')};
}

function showEdgeInfo(elem){
    var div = document.createElement('div');
    div.setAttribute('data-id', 'pop');
    div.setAttribute('id', elem.data('id'));
    var fermeture = document.createElement('div');
    fermeture.setAttribute('id', 'fermeture');
    fermeture.setAttribute('onclick', "document.getElementById('"+elem.data('id')+"').style.display = 'none'");
    fermeture.innerHTML = 'X';
    div.append(fermeture);
    var divSource = document.createElement('div');
    divSource.setAttribute('class', 'source');
     var titreSource = document.createElement('h5');
     var texteSource = document.createTextNode(elem.data('auteur_source')+ ', '+elem.data('labelSource'));    
    titreSource.append(texteSource);
    divSource.append(titreSource);
    var divTarget = document.createElement('div');
    divTarget.setAttribute('class', 'target');
    var titreTarget = document.createElement('h5');
    var texteTarget = document.createTextNode(elem.data('auteur_target')+ ', '+elem.data('labelTarget'))    
    
    titreTarget.append(texteTarget);
    divTarget.append(titreTarget);
    
    if (elem.data('phrasesSource') != undefined){
    console.log(elem.data('phrasesSource'))
    var phrases_sources = elem.data('phrasesSource').split(' ');

    console.log(phrases_sources);
    for (var p_s of phrases_sources){
        var phrase_source = document.getElementById(p_s);
         phrase_source = phrase_source.cloneNode(true);
    phrase_source = modifie_id_div(phrase_source, elem.data('id'));
    divSource.append(phrase_source);
    }
    
    
    console.log(phrase_source);
    var phrases_targets = elem.data('phrasesTarget').split(' ')
    console.log(elem.data('phrasesTarget'));
    for (var p_t of phrases_targets){
        var phrase_target = document.querySelector('[data-id= \''+p_t+'\']');
        phrase_target = phrase_target.cloneNode(true);
        divTarget.append(phrase_target);
    }
    }
    else{
        console.log(elem.data('source'));
        var source = elem.data('source');
        var phrase_source = document.getElementById(source);
        phrase_source = phrase_source.cloneNode(true);
        phrase_source = modifie_id_div(phrase_source, elem.data('id'));
        divSource.append(phrase_source);
        console.log(phrase_source);
        var target = elem.data('target');
        console.log(elem.data('target'));
        var phrase_target = document.querySelector('[data-id= \''+target+'\']');
        phrase_target = phrase_target.cloneNode(true);
        divTarget.append(phrase_target);
    }
        
    
    div.append(divSource);
    div.append(divTarget);
    document.getElementById('graph').append(div);
    var dragItem = document.querySelector("[data-id='pop']");
    var container = document.querySelector("#graph");
    if (elem.data('phrasesSource') != undefined){
    for (var p_s of phrases_sources){
        for (var p_t of phrases_targets){
            affiche_alignement(elem.data('id'), p_s,  p_t );
        }
    }
    }
    else{
        affiche_alignement(elem.data('id'), source, target)
    }
     var dragItem = document.querySelector("[data-id='pop']");
    var container = document.querySelector("#graph");
     var mots_actifs = div.getElementsByClassName('w');
    for (var mot_actif of mots_actifs){
        if (trouveActif(mot_actif) == 'true')
            {console.log('event ajouté')
                mot_actif.addEventListener('mouseenter', enterCorrespondances, false);
             mot_actif.addEventListener('mouseleave', exitCorrespondances, false);
            }
    }

 
}



function graphe(){
  $.getJSON('../json/graphe_general.json', function(data){  

    document.getElementById('graph').style.display = 'block';
    document.getElementById('champ').style.display = 'none';
    document.getElementById('texte_principal').style.display = 'none';
    //document.getElementsByTagName('fieldset')[0].style.display = 'none';
    document.getElementsByTagName('h1')[0].style.display = 'none';

    var auteurs = [];
    var poidsAuteurs = {}
    var i = 0;
    for (var ligne of auteurs_graphe['elements']['nodes']){
        auteurs.push(ligne['data']['id'])
        CouleursAuteurs.set(ligne['data']['id'], Colors[i]);
        i = i+1
        poidsAuteurs[ligne['data']['id']] = ligne['data']['weight']
    }
      console.log(CouleursAuteurs)
    var metasAuteurs =[];
    for (var ligne2 of data['elements']['nodes']){
        
        if (auteurs.includes(ligne2['data']['id'])){
            ligne2['data']['weight'] = poidsAuteurs[ligne2['data']['id']];
            metasAuteurs.push(ligne2)
            
        }
    }
    //var tableauID = {}
    //for (var ID in correspondances_phrases){
        //tableauID[ID] = Number(ID)
        //console.log(Number(ID))
        //var tableau_corresp = correspondances_phrases[ID].split(' ');
        //for (var corresp of tableau_corresp){
            //tableauID[corresp] = Number(corresp)
        //}
        
    //}
    //console.log(tableauID)
    //var i = 1;
    //var resultats = {}
    //for (var identifiant in tableauID){
        //if (!trouves.includes(identifiant)){
            //var ensemble = [];
            //ensemble = trouve_identifiant(identifiant, tableauID, ensemble);
            //if (ensemble.length == 0){ensemble.push(identifiant)}
            //resultats[i] = ensemble;
            //i = i+1
            //}
    //}
    //console.log(resultats);
    //var CouleursAuteurs = new Map();
    var poidsMax = 0;
    for (var ligne of auteurs_graphe['elements']['nodes']){
        var poids = ligne['data']['weight'];
        if (poids > poidsMax){poidsMax = poids}
    }
var couleurs = { 'poésie' : '#C0392B',
                             'théâtre' : '#27AE60',
                             'prose' : '#2980B9',
                             'opéra' : '#fdd835',
                             'BD' : '#E67E22',
                             'autre' : '#8E44AD' };
    


console.log(auteurs_graphe['elements']['edges']);

    var cy = cytoscape({
        
        container : document.getElementById('cy'),
        elements:
        {
        nodes : metasAuteurs,
        edges : auteurs_graphe['elements']['edges'],
    },
            layout : 
            {
           name: 'concentric',
           nodeDimensionsIncludeLabels: false,
            animate : true,
                
                  nodeRepulsion: 4000,
            },
            style: [
                {
                    selector : 'node',
                    style : {
                        'label' : 'data(id)',
                        'width': function(ele){
                            console.log(((ele.data('weight')*100)/poidsMax) + 20)
                            return(((ele.data('weight')*100)/poidsMax) + 20)

                        },
                        'height' : function(ele){
                            return(((ele.data('weight')*100)/poidsMax) + 20)

                        },
                        'font-family': 'Raleway',
                        'font-size' : '14px',

                        'text-valign': 'center',
                        'text-halign': 'center',
                        'shape': function(ele){
                            var type = ele.data('type');
                            console.log(ele.data('type'));
                            var valeursTypes = {'modernisation':'triangle', 
                            'transmodalisation':'ellipse',
                            'parodie':'star'};
                            if (type == 'traduction'){
                                var auteur = ele.data('auteur');
                                if (auteur == 'Ovide')
                                {
                                    return('diamond')
                                }
                                else{
                                    return('hexagon')
                                }
                            }
                            else{
                                return(valeursTypes[type])
                            }
                        },
                        'label': 'data(id)',
                        'text-background-color': function(ele){

                             var subtype = ele.data('subtype');
                             return(couleurs[subtype])
                         },
                         'text-background-opacity' : 0.5,
                         'background-color': function(ele){
                            var subtype = ele.data('subtype');
                            return(couleurs[subtype])
},  
                       
                }
                    
                    
      
          
          
                },
                {
                selector : 'edge',
                    style : {
                        'width' : 'data(weight)'
                    }
                },
                
                {
                    selector : 'node:selected',
                    style:{'label' : function(ele){
                        if (ele.data('id') == auteurs_graphe["elements"]["edges"][0]["data"]["source"]){
                            creer_graphe_general()
                        } 
                                                       }
                }
                },
                {
                    selector : 'edge:selected',
                    style:{'label' : function(ele){
                        creer_graphe_target(ele)
                        } 
                                                       }
                
                },

            ]
        });

        
    });
    
    
         
};


function creer_graphe_target(arete){
    $.getJSON('../json/graphe_general.json', function(data){
        var auteur_source = arete.data('source');
        var auteur_target = arete.data('target');

        var dico_metas = {};
            for (var ligne of data['elements']['nodes']){
                if (ligne['data']['id'] == auteur_source || ligne['data']['id'] == auteur_target)
                {
                    dico_metas[ligne['data']['id']] = {'type':ligne['data']['type'], 'subtype' : ligne['data']['subtype'], 'auteur' : ligne['data']['auteur']};
                }
            }
        console.log(dico_metas)
    


    
    
    var nouveau_liens = [];
    var ids_auteurs =[];

    for (ligne_edges of liens_phrases['elements']['edges']){
        if (ligne_edges['data']['auteur_source'] == auteur_source && ligne_edges['data']['auteur_target'] == auteur_target)
        {
            nouveau_liens.push(ligne_edges);
            ids_auteurs.push(ligne_edges['data']['source']);
            ids_auteurs.push(ligne_edges['data']['target'])
        }
    }
    console.log(nouveau_liens);
    console.log(ids_auteurs);
    var nouveau_noeuds = [];
    for (ligne_nodes of liens_phrases['elements']['nodes']){
        if (ids_auteurs.includes(ligne_nodes['data']['id']))
        {
            nouveau_noeuds.push(ligne_nodes)
        }
    };

    var tableauID = {}
    for (var ID of ids_auteurs){
        tableauID[ID] = Number(ID)
        }
        
    
    console.log(tableauID)
    var i = 1;
    var resultats1 = {};
    var resultats2 = {};
    for (var identifiant in tableauID){
        console.log("###",identifiant)
        if (!trouves.includes(identifiant)){
            var ensemble = [];
            ensemble = trouve_identifiant(identifiant, tableauID, ensemble);
            if (ensemble.length == 0){ensemble.push(identifiant)}
                for (var ID_ensemble of ensemble){
                    console.log(ID_ensemble)
                    resultats1[ID_ensemble] = i;

                }
                resultats2[i] = ensemble;
            
            i = i+1
            }
    }
    console.log(resultats1);
    console.log(resultats2);
var noeuds_concats = [];
var anciensIdsPhrases = {};
var nouveauxLabels = {}
    for (var nouveau_id in resultats2){
        var noeuds_liens = resultats2[nouveau_id];
        var labels = [];
        var poids = 0;
        var auteur = '';
        var anciensIDs = []
        for (var ligne_noeuds of nouveau_noeuds){
             if (noeuds_liens.includes(ligne_noeuds['data']['id']))
            {
                var nouveau_label = Number(ligne_noeuds['data']['id'].substr(ligne_noeuds['data']['id'].length-4));
                console.log("laaaab " + nouveau_label)
                labels.push(nouveau_label);
                anciensIDs.push(ligne_noeuds['data']['id'])

        poids += 1;
        auteur = ligne_noeuds['data']['auteur'];


            }
            
            
            
        }
        labels = labels.sort()
        if (labels.length > 1){
            label = labels[0]+'-'+labels[labels.length-1];
        }
        else{
            label = labels[0];
        }
        console.log("nouveau label "+label)
        nouveauxLabels[nouveau_id] = label

        anciensIDs = anciensIDs.sort();
        if (anciensIDs.length > 1){
            var anID = '';
            for (var ancienID of anciensIDs){
                anID += ancienID+' '

            }
            anID = anID.slice(0,-1); 

        }
        else{
            var anID = anciensIDs[0]
        }

        anciensIdsPhrases[nouveau_id] = anID;
        console.log('#####'+nouveau_id)
        noeuds_concats.push({"data":{"id":nouveau_id, "label":label, "weight": poids, "auteur": auteur, "idsPhrases":anID}})

    }
    
    for (var ligne_liens of nouveau_liens){
        ligne_liens['data']['source'] = resultats1[ligne_liens['data']['source']];
        ligne_liens['data']['target'] = resultats1[ligne_liens['data']['target']];
        console.log('#####'+ligne_liens['data']['source'])
        ligne_liens['data']['phrasesSource'] = anciensIdsPhrases[ligne_liens['data']['source']];
        ligne_liens['data']['labelSource'] = nouveauxLabels[ligne_liens['data']['source']];
        ligne_liens['data']['labelTarget'] = nouveauxLabels[ligne_liens['data']['target']];
        ligne_liens['data']['phrasesTarget'] = anciensIdsPhrases[ligne_liens['data']['target']];
    }
    console.log(noeuds_concats);
    console.log(nouveau_liens);
    
    
    var couleurs = { 'poésie' : '#C0392B',
                             'théâtre' : '#27AE60',
                             'prose' : '#2980B9',
                             'opéra' : '#fdd835',
                             'BD' : '#E67E22',
                             'autre' : '#8E44AD' };
    var cy = cytoscape({
        
        container : document.getElementById('cy'),
        elements : 
            {
                nodes: noeuds_concats,
                edges : nouveau_liens,
                
            },
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
  nodeSpacing: function( node ){ return 10; }, // extra spacing around nodes
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
            style: [
                {
                    selector : 'node',
                    style : {
                        'label' : function(ele){ var label = ele.data('label');
                        var auteur = ele.data('auteur');
                        if (label.toString().includes('-')){return (auteur+',\n phrases '+label)}
                        else{return (auteur+',\n phrase '+label)}
                        
                    },
                        'width': function(ele){var poids = ele.data('weight');
                        return(poids*100)
                    },
                        'height' : function(ele){var poids = ele.data('weight');
                        return(poids*100)
                    },
                    'text-wrap' : "wrap",
                        'font-family': 'Raleway',
                        'font-size' : '18px',
                        'text-valign': 'center',
        'text-halign': 'center',
        'text-background-color' : 'white',
        'text-background-opacity' : 0.5,
                        'background-color': function(ele) //function qui attribue une couleur aléatoire au noeud et extrait les données pour tabs id, occurrences et CouleursAuteurs
                    { // boléen pour tenter de différencier les couleurs aléatoires
                        var auteur = ele.data('auteur');
                        return(CouleursAuteurs.get(auteur))
                    },
                    'border-color' : function(ele){
                        var auteur = ele.data('auteur');
                        var subtype = dico_metas[auteur]['subtype'];
                        return(couleurs[subtype]) 
                    },
                    'border' : 'solid',
                    'border-width' : '10px',
                    'shape': function(ele){
                            var auteur = ele.data('auteur');
                            var type = dico_metas[auteur]['type'];
                            var latin = dico_metas[auteur]['auteur']
                        
                            var valeursTypes = {'modernisation':'triangle', 
                            'transmodalisation':'ellipse',
                            'parodie':'star'};
                            if (type == 'traduction'){
                                if (latin == 'Ovide')
                                {
                                    return('diamond')
                                }
                                else{
                                    return('hexagon')
                                }
                            }
                            else{
                                return(valeursTypes[type])
                            }
                        },
                }
                                        },
                {
                selector : 'edge',
                    style : {
                        'width' : 'data(weight)'
                    }
                },
                {
                selector : 'edge:selected',
                    style : {'label' :  function(ele){showEdgeInfo(ele);}
                        
                    }
                }
            ]
        
    });
    changerLegende(auteur_source, auteur_target)
});
}

function changerLegende(auteur_source, auteur_target){
    var ulSubType = document.getElementsByClassName('subtype')[0];
     var spansSubType = ulSubType.getElementsByTagName('span');
     for (var span of spansSubType){span.innerHTML = '&#9633;'};
    var legende = document.getElementById('legende');
    
    var ajoutLegende = document.createElement("ul");
    ajoutLegende.classList.add('legendeAuteurs')
    var liSource = document.createElement("li");
    liSource.style.color = CouleursAuteurs.get(auteur_source);
    spanSource = document.createElement("span")
    var elementSource = document.createTextNode(auteur_source);
    spanSource.appendChild(elementSource);
    spanSource.style.color = "#555";
    liSource.appendChild(spanSource);
    ajoutLegende.appendChild(liSource);
    var liTarget = document.createElement("li");
    liTarget.style.color = CouleursAuteurs.get(auteur_target);
    spanTarget = document.createElement("span")
    var elementTarget = document.createTextNode(auteur_target);
    spanTarget.appendChild(elementTarget);
    spanTarget.style.color = "#555";
    liTarget.appendChild(spanTarget);
    ajoutLegende.appendChild(liTarget);
    legende.appendChild(ajoutLegende)
    
    var infos = document.getElementById('infos');

    infos.innerHTML = "<div id=\"fermeture\" onclick=\"document.getElementById('legende').style.display = 'none'\">X</div><p>Les étiquettes affichées sur les nœuds correspondent aux numéros de phrases qui les composent. <br> Cliquez sur le lien pour afficher le texte des correspondances établies entre deux nœuds. <br> Cliquez sur le nœud composé de plusieurs phrases pour afficher le graphe détaillé de leurs correspondances.</p> <button>Remonter d'un niveau</button>"


}
 

function creer_graphe_general(){
    $.getJSON('../json/graphe_general.json', function(data){
/*CouleursAuteurs = new Map;*/
        var dico_metas = {};
            for (var ligne of data['elements']['nodes']){
                    dico_metas[ligne['data']['id']] = {'type':ligne['data']['type'], 'subtype' : ligne['data']['subtype'], 'auteur' : ligne['data']['auteur']};
            }
        console.log(dico_metas)
    


    
    
    var nouveau_liens = [];
    var ids_auteurs =[];

    for (ligne_edges of liens_phrases['elements']['edges']){
       
            nouveau_liens.push(ligne_edges);
            ids_auteurs.push(ligne_edges['data']['source']);
            ids_auteurs.push(ligne_edges['data']['target'])
        
    }
    console.log(nouveau_liens);
    console.log(ids_auteurs);
    var nouveau_noeuds = [];
    for (ligne_nodes of liens_phrases['elements']['nodes']){
        if (ids_auteurs.includes(ligne_nodes['data']['id']))
        {
            nouveau_noeuds.push(ligne_nodes)
        }
    };

    var tableauID = {}
    for (var ID of ids_auteurs){
        tableauID[ID] = Number(ID)
        }
        
    
    console.log(tableauID)
    var i = 1;
    var resultats1 = {};
    var resultats2 = {};
    for (var identifiant in tableauID){
        console.log("###",identifiant)
        if (!trouves.includes(identifiant)){
            var ensemble = [];
            ensemble = trouve_identifiant(identifiant, tableauID, ensemble);
            if (ensemble.length == 0){ensemble.push(identifiant)}
                for (var ID_ensemble of ensemble){
                    console.log(ID_ensemble)
                    resultats1[ID_ensemble] = i;

                }
                resultats2[i] = ensemble;
            
            i = i+1
            }
    }
    console.log(resultats1);
    console.log(resultats2);
var noeuds_concats = [];
var anciensIdsPhrases = {};
var nouveauxLabels = {};
var maxPoids = 0;

    for (var nouveau_id in resultats2){
        var noeuds_liens = resultats2[nouveau_id];
        var labels = [];
        var poids = 0;
        var auteur = '';
        var anciensIDs = []
        for (var ligne_noeuds of nouveau_noeuds){
             if (noeuds_liens.includes(ligne_noeuds['data']['id']))
            {
                var nouveau_label = Number(ligne_noeuds['data']['id'].substr(ligne_noeuds['data']['id'].length-4));
                labels.push(nouveau_label);
                anciensIDs.push(ligne_noeuds['data']['id'])

        poids += 1;
        auteur = ligne_noeuds['data']['auteur'];


            }
            if (poids > maxPoids){maxPoids = poids}
            
            
        }
        labels = labels.sort((a, b) => a - b);
        //console.log("!!!!! "+nouveau_id);
        //console.log("!!!!! "+labels)
        if (labels.length > 1){
            label = labels[0]+'-'+labels[labels.length-1];
            //console.log("!!!!! "+label)
        }
        else{
            label = labels[0];
            //console.log("!!!!! "+label)
        }
        nouveauxLabels[nouveau_id] = label
        //console.log(label)

        anciensIDs = anciensIDs.sort();
        if (anciensIDs.length > 1){
            var anID = '';
            for (var ancienID of anciensIDs){
                anID += ancienID+' '

            }
            anID = anID.slice(0,-1); 

        }
        else{
            var anID = anciensIDs[0]
        }

        anciensIdsPhrases[nouveau_id] = anID;
        //console.log('#####'+nouveau_id)
        noeuds_concats.push({"data":{"id":nouveau_id, "label":label, "weight": poids, "auteur": auteur, "idsPhrases":anID}})

    }
    
    for (var ligne_liens of nouveau_liens){
        ligne_liens['data']['source'] = resultats1[ligne_liens['data']['source']];
        ligne_liens['data']['target'] = resultats1[ligne_liens['data']['target']];
        console.log('#####'+ligne_liens['data']['source'])
        ligne_liens['data']['phrasesSource'] = anciensIdsPhrases[ligne_liens['data']['source']];
        ligne_liens['data']['labelSource'] = nouveauxLabels[ligne_liens['data']['source']];
        ligne_liens['data']['labelTarget'] = nouveauxLabels[ligne_liens['data']['target']];
        ligne_liens['data']['phrasesTarget'] = anciensIdsPhrases[ligne_liens['data']['target']];
    }
    console.log(noeuds_concats);
    console.log(nouveau_liens);
    
    
    var couleurs = { 'poésie' : '#C0392B',
                             'théâtre' : '#27AE60',
                             'prose' : '#2980B9',
                             'opéra' : '#fdd835',
                             'BD' : '#E67E22',
                             'autre' : '#8E44AD' };
    var cy = cytoscape({
        
        container : document.getElementById('cy'),
        elements : 
            {
                nodes: noeuds_concats,
                edges : nouveau_liens,
                
            },
            layout : 
            {
            name: 'cose-bilkent',
           nodeDimensionsIncludeLabels: false,
            animate : false,
                nodeRepulsion: 6000,
                
           
            },
            
            style: [
                {
                    selector : 'node',
                    style : {
                        'label' : function(ele){ var label = ele.data('label');
                        var auteur = ele.data('auteur');
                        if (label.toString().includes('-')){return (auteur.toUpperCase()+',\n phrases '+label)}
                        else{return (auteur.toUpperCase()+',\n phrase '+label)}
                        
                    },
                         'width': function(ele){
                            console.log(((ele.data('weight')*200)/maxPoids) + 100)
                            return(((ele.data('weight')*200)/maxPoids) + 100)

                        },
                        'height' : function(ele){
                            return(((ele.data('weight')*200)/maxPoids) + 100)

                        },
                    'text-wrap' : "wrap",
                        'font-family': 'Raleway',
                        'font-size' : '50px',
                        'text-valign': 'center',
        'text-halign': 'center',
        'text-background-color' : 'white',
        'text-background-opacity' : 0.5,
                        'background-color': function(node) //function qui attribue une couleur aléatoire au noeud et extrait les données pour tabs id, occurrences et CouleursAuteurs
                        { // boléen pour tenter de différencier les couleurs aléatoires
                            var auteur = node.data('auteur');
                                console.log(CouleursAuteurs.get(auteur))
                                //return CouleursAuteurs.get(auteur)
                                return ('#c3c3c3')
                        
                    },
                        
                    'border-color' : function(ele){
                        var auteur = ele.data('auteur');
                        var subtype = dico_metas[auteur]['subtype'];
                        return(couleurs[subtype]) 
                    },
                    'border' : 'solid',
                    'border-width' : '10px',
                    'shape': function(ele){
                            var auteur = ele.data('auteur');
                            var type = dico_metas[auteur]['type'];
                            var latin = dico_metas[auteur]['auteur']
                        
                            var valeursTypes = {'modernisation':'triangle', 
                            'transmodalisation':'ellipse',
                            'parodie':'star'};
                            if (type == 'traduction'){
                                if (latin == 'Ovide')
                                {
                                    return('diamond')
                                }
                                else{
                                    return('hexagon')
                                }
                            }
                            else{
                                return(valeursTypes[type])
                            }
                        },
                }
                                        },
                {
                selector : 'edge',
                    style : {
                        'width' : 'data(weight)'
                    }
                },
                {
                selector : 'edge:selected',
                    style : {'label' :  function(ele){showEdgeInfo(ele);}
                        
                    }
                },
                {
                selector: 'node:selected',
                style : {
                    'label' :function(ele){creer_graphe_detaille(ele.data('idsPhrases'), ele.data('auteur'))}
                } 
                }
            ]
        
    });
    creerLegende(CouleursAuteurs, "legende")
});
}

function creer_graphe_detaille(idsPhrases, auteurSource){
    $.getJSON('../json/graphe_general.json', function(data){
    var ids = idsPhrases.split(' ');
    
    
     var couleurs = { 'poésie' : '#C0392B',
                             'théâtre' : '#27AE60',
                             'prose' : '#2980B9',
                             'opéra' : '#fdd835',
                             'BD' : '#E67E22',
                             'autre' : '#8E44AD' };
    var dico_metas = {};
            for (var ligne of data['elements']['nodes']){
                    dico_metas[ligne['data']['id']] = {'type':ligne['data']['type'], 'subtype' : ligne['data']['subtype'], 'auteur' : ligne['data']['auteur']};
            }
        console.log(dico_metas)
    var cy = cytoscape({
        
        container : document.getElementById('cy'),
        elements : 
            {
                nodes: node_data(correspondances_phrases, ids, auteurSource),
                edges : edge_data(correspondances_phrases, ids)
                
            },
            layout : 
            {
             name: 'cose-bilkent',
            
  
nodeDimensionsIncludeLabels: true,
                
                  nodeRepulsion: 6000,
  
  avoidOverlap: true, // if true, prevents overlap of node bounding boxes
  handleDisconnected: true, // if true, avoids disconnected components from overlapping
  nodeSpacing: function( node ){ return 10; }, // extra spacing around nodes
  
            },
            
            style: [
                {
                    selector : 'node',
                    style : {
                        'label' : 'data(label)',
                         'width': '100px',
                        'height' : '100px',
                    'text-wrap' : "wrap",
                        'font-family': 'Raleway',
                        'font-size' : '50px',
                        'text-valign': 'center',
        'text-halign': 'center',
        'text-background-color' : 'white',
        'text-background-opacity' : 0.5,
                        'background-color': function(node) //function qui attribue une couleur aléatoire au noeud et extrait les données pour tabs id, occurrences et CouleursAuteurs
                        { // boléen pour tenter de différencier les couleurs aléatoires
                            var auteur = node.data('auteur');
                                console.log(CouleursAuteurs.get(auteur))
                                return CouleursAuteurs.get(auteur)
                        
                    },
                        
                    'border-color' : function(ele){
                        var auteur = ele.data('auteur');
                        var subtype = dico_metas[auteur]['subtype'];
                        return(couleurs[subtype]) 
                    },
                    'border' : 'solid',
                    'border-width' : '10px',
                    'shape': function(ele){
                            var auteur = ele.data('auteur');
                            var type = dico_metas[auteur]['type'];
                            var latin = dico_metas[auteur]['auteur']
                        
                            var valeursTypes = {'modernisation':'triangle', 
                            'transmodalisation':'ellipse',
                            'parodie':'star'};
                            if (type == 'traduction'){
                                if (latin == 'Ovide')
                                {
                                    return('diamond')
                                }
                                else{
                                    return('hexagon')
                                }
                            }
                            else{
                                return(valeursTypes[type])
                            }
                        },
                }
                                        },
                
                {
                selector : 'edge:selected',
                    style : {'label' :  function(ele){showEdgeInfo(ele);}
                        
                    }
                },
                {
                selector : 'node:selected',
                    style : {'label' :  function(ele){}
                        
                    }
                },
                
                
                
            ]
        
        
    });
    creerLegende(CouleursAuteurs, "legende");
    });
    
    
    
}
/*DÉPLACEMENT DES DIVS DE LA COMPARAISON*/


    function dragStart(e) {

      if (e.target !== e.currentTarget) {
        active = true;

        // this is the item we are interacting with
        activeItem = e.target;

        if (activeItem !== null && activeItem.getAttribute('data-id') == 'pop') {
          if (!activeItem.xOffset) {
            activeItem.xOffset = 0;
          }

          if (!activeItem.yOffset) {
            activeItem.yOffset = 0;
          }

          if (e.type === "touchstart") {
            activeItem.initialX = e.touches[0].clientX - activeItem.xOffset;
            activeItem.initialY = e.touches[0].clientY - activeItem.yOffset;
          } else {
            console.log("doing something!");
            activeItem.initialX = e.clientX - activeItem.xOffset;
            activeItem.initialY = e.clientY - activeItem.yOffset;
          }
        }
      }
    }

    function dragEnd(e) {
      if (activeItem !== null && activeItem.getAttribute('data-id') == 'pop') {
        activeItem.initialX = activeItem.currentX;
        activeItem.initialY = activeItem.currentY;
      }

      active = false;
      activeItem = null;
    }

    function drag(e) {
      if (active) {
        if (e.type === "touchmove") {
          e.preventDefault();

          activeItem.currentX = e.touches[0].clientX - activeItem.initialX;
          activeItem.currentY = e.touches[0].clientY - activeItem.initialY;
        } else {
          activeItem.currentX = e.clientX - activeItem.initialX;
          activeItem.currentY = e.clientY - activeItem.initialY;
        }

        activeItem.xOffset = activeItem.currentX;
        activeItem.yOffset = activeItem.currentY;

        setTranslate(activeItem.currentX, activeItem.currentY, activeItem);
      }
    }

    function setTranslate(xPos, yPos, el) {
      el.style.transform = "translate3d(" + xPos + "px, " + yPos + "px, 0)";
    }
    
  
//GESTION ONGLET CHAMPS LEXICAUX
function trouveLemme(identifiant){
    ligneMot = dictionnaireMots.filter(mot => mot['id'] == identifiant);
    return (ligneMot)
}
function trouveLemmeCorresp(idCorresp, teteActuelle, dict){
    for (var tete in dict){
        if (tete != teteActuelle && dict[tete].includes(idCorresp)
           ){
            return(tete)
        }
    }
}
function champs(){
     document.getElementById("graph").style.display = "none";
    document.getElementsByTagName("section")[1].style.display = 'none';
    document.getElementsByTagName("section")[0].style.display = 'none';
     document.getElementsByTagName('fieldset')[0].style.display = 'none';
    document.getElementsByTagName('h1')[0].style.display = 'none';
    document.getElementById('champ').style.display = 'block';
    var dictionnaireSynos = {};
    for (var ligne of liens_mots){
        var ligneMot = trouveLemme(ligne['source']);
        var lemme = ligneMot[0]["lemme"];
        var pos = ligneMot[0]["pos"].slice(0,3);
        if (pos == 'NOM' || pos == 'ADJ' || pos == 'VER' ){
        console.log(lemme);
        if (dictionnaireSynos[lemme] == undefined){
            dictionnaireSynos[lemme] = []    
        };
        dictionnaireSynos[lemme].push(ligne['source']);
        dictionnaireSynos[lemme].push(ligne['target']);
    }
    }
    console.log(dictionnaireSynos);
    var noeudsChamp = [];
    var liensChamp = [];
    for (var teteLemme in dictionnaireSynos){
        
        var graphies = [];
        var correspsLemme = {};
        for (var graphie of dictionnaireSynos[teteLemme]){
            
            for (var ligne of liens_mots){
                
                if (ligne['source'].includes(graphie.split('_')[0])){
                    var lemmeCorresp = trouveLemmeCorresp(ligne['source'], teteLemme, dictionnaireSynos);
                    console.log(lemmeCorresp);
                    if (correspsLemme[lemmeCorresp] == undefined){
                        correspsLemme[lemmeCorresp] = 1
                    }
                    else{
                        correspsLemme[lemmeCorresp] += 1
                    }
                }
                else{
                    if(ligne['target'].includes(graphie.split('_')[0])){
                        var lemmeCorresp = trouveLemmeCorresp(ligne['target'], teteLemme, dictionnaireSynos);
                         if (correspsLemme[lemmeCorresp] == undefined){
                        correspsLemme[lemmeCorresp] = 1
                    }
                    else{
                        correspsLemme[lemmeCorresp] += 1
                    }
                        
                    }
                }
                
            }
        }
        var idLemme = teteLemme;
        console.log(idLemme)
        var pos = trouveLemme(dictionnaireSynos[teteLemme][0])[0]["pos"].slice(0,3);
        console.log(pos)
        
        var score = 0;
        var graphies = [];
        for (graphie of dictionnaireSynos[teteLemme]){
            
            ligneMot = trouveLemme(graphie);
if (ligneMot.length > 0){
            if (!graphies.includes(ligneMot[0]["lemme"])){
            graphies.push(ligneMot[0]["lemme"])
        };
            score += 1; 
            
        }};
        stringGraphies = ''
        for (graphie of graphies){
            stringGraphies += graphie + ' ';
        }
        console.log(stringGraphies)
        if (pos == 'ADJ' || pos == 'NOM' || pos == 'VER'){
        scoreCorresps = 0;
        for (correspLemme in correspsLemme){
            if (correspLemme != 'undefined' && correspsLemme[correspLemme] > 2){ 
            scoreCorresps += 1;
            liensChamp.push({data:{id : teteLemme+'_'+correspLemme, source : teteLemme, target :correspLemme, score : correspsLemme[correspLemme]}});
            }
            
        }
        if (scoreCorresps != 0){
        noeudsChamp.push({data:{id : idLemme, pos : pos, score : score, graphies : stringGraphies}})
        }
    }
    }
    console.log(liensChamp)
    dessineGrapheChamps(noeudsChamp, liensChamp)
}

function dessineGrapheChamps(noeudsChamp, liensChamp){
    var cy2 = cytoscape({
        
        container : document.getElementById('cy2'),
        elements : 
            {
                nodes: noeudsChamp,
                edges : liensChamp,
                
            },
            layout : 
            {
           name: 'cose-bilkent',
          nodeDimensionsIncludeLabels: true,
                
                  nodeRepulsion: 6000,
  
  avoidOverlap: true, // if true, prevents overlap of node bounding boxes
  handleDisconnected: true, // if true, avoids disconnected components from overlapping
  nodeSpacing: function( node ){ return 10; }, // extra spacing around nodes
            },
            style: [
                {
                    selector : 'node',
                    style : {
                        'label' : 'data(id)',
                        'width': '20px',
                        'height' : '20px',
                        'font-family': 'Raleway',
                        'font-size' : '15px',
                        'text-valign': 'center',
        'text-halign': 'center',
                        'background-color': function(ele)
                        {var couleurs = {'NOM' : '#C0392B', 'VER' : '#27AE60', 'ADJ' : '#E67E22'}
                        var pos = ele.data('pos');
                        return couleurs[pos] 
                        }
                    }
                    
                    
      
          
          
                },
                {
                selector : 'edge',
                    style : {
                        'width' : '1px'
                    }
                },
                {
                selector : 'edge:selected',
                    style : {'label' :  function(ele){showEdgeInfo(ele);}
                        
                    }
                }
            ]
        
    });
   }
  //Nouveau affichage (08-12 )
                
function surlignerMots(idApp, strUser){
    var container = document.getElementById(idApp);
    var mots_actifs = container.getElementsByClassName('active');
    for (var mot_actif of mots_actifs){
    	mot_actif.addEventListener('mouseenter', enterCorrespondances, false);
    	mot_actif.addEventListener('mouseleave', exitCorrespondances, false);
    }
}

                
function change_corresp(idApp){
    console.log(idApp);
    var divApp = document.getElementById(idApp);
    var choix = divApp.getElementsByTagName('select')[0];
    var strUser = choix.options[choix.selectedIndex].value;
    var targets = divApp.getElementsByClassName('target')[0];
    var divsTarget = targets.getElementsByTagName('div');
    for (var divTarget of divsTarget){
    	if (divTarget.id == strUser){
    		divTarget.style.display = "block";
    	}
    	else{
    		divTarget.style.display = "none";
    	}
    }
    console.log(strUser);
    var source = divApp.getElementsByClassName('source')[0];
    var liste_source = source.getElementsByTagName('span');
    for (var l_s of liste_source){
    	if (l_s.hasAttribute("data-corresp")){
    		if (l_s.dataset.corresp.includes(strUser) && 
    				divApp.getElementsByTagName('input')[0].checked &&
    				!l_s.classList.contains('groupe')){
    			l_s.classList.add('active')
    		}
    		else{
    			l_s.classList.remove('active')
    		}
    	}
    } 
    var target = document.getElementById(strUser);
    var liste_target = target.getElementsByTagName('span')
    for (var l_t of liste_target){
    	if (l_t.hasAttribute("data-id")){
    		if (divApp.getElementsByTagName('input')[0].checked &&
    				!l_t.classList.contains('groupe')){
    			l_t.classList.add('active')
    		}
    		else{
    			l_t.classList.remove('active')
    		}
    	}
    }
    surlignerMots(idApp, strUser);
}
                
function optionChange(id, i){
	var infos = document.getElementById(id);
	var spans = infos.getElementsByTagName('span');
	if (infos.getElementsByTagName('input')[0].checked){
		infos.getElementsByClassName('legende')[0].style.display = "block";
	}
	else{
		infos.getElementsByClassName('legende')[0].style.display = "none";
	}
	if (infos.getElementsByTagName('input')[1].checked){
		infos.getElementsByClassName('legende')[1].style.display = "block";
	}
	else{
		infos.getElementsByClassName('legende')[1].style.display = "none";
	}
	for (var span of spans){
		console.log(span);
		if (i == 1){
			if (span.classList.contains('groupe')){
				if (infos.getElementsByTagName('input')[0].checked){
					span.classList.add('active')
					if (infos.getElementsByTagName('input')[1].checked){
						if (span.classList.contains("seul")){
							span.classList.remove("seul")
						}
						span.classList.add("avec")
					}
					else{
						if (span.classList.contains("avec")){
							span.classList.remove("avec")
						}
						span.classList.add("seul")
					}
				}
				else{	
					span.classList.remove('active')
				}
			}
		}
		else{
			if (!span.classList.contains('groupe')){
				if (infos.getElementsByTagName('input')[1].checked){
					span.classList.add('active')
				}
				else{	
					span.classList.remove('active')
				}
			}
			else{
				if (infos.getElementsByTagName('input')[0].checked){
					if (infos.getElementsByTagName('input')[1].checked){
						if (span.classList.contains("seul")){
							span.classList.remove("seul")
						}
						span.classList.add("avec")
					}
					else{
						if (span.classList.contains("avec")){
							span.classList.remove("avec")
						}
						span.classList.add("seul")
					}
				}
			}
		}
	}
	change_corresp(id);
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

function affiche(idDiv){
	document.getElementById(idDiv).style.display = 'inline-flex';
}