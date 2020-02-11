function init(){
    var parametres = location.search.substring(1).split("&");
    console.log(parametres);
    for (var parametre of parametres){
        
        var valeur = parametre.split("=")[1];
        valeur = unescape(valeur)
        console.log(valeur)
        var inputs = document.getElementsByTagName('input');
        for (var input of inputs){
            console.log(input.id)
            if (input.id == valeur){
                console.log('oui');
                input.checked;
                input.checked = 'true';
            }
        }
    }
 
    affichage_auteurs();
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
        
    
    
    /*var tableau_identifiants = targets.split(' ');
      tableau_identifiants.pop();
      console.log(id_div);
   var div = document.getElementById(id_div);
    console.log(div);
        for (target of tableau_identifiants){
            console.log(source);
            for (var mots_correspondants of liens_mots)
            {
                if (mots_correspondants["target"] == target && mots_correspondants["source"] == source)
                {
                    console.log(mots_correspondants["type"]);
                    console.log(target);
                    {
                    if (div.querySelector('[data-id=\''+source+'\']').parentElement.tagName = 'span')
                        div.querySelector('[data-id=\''+source+'\']').parentElement.classList.add('affiche');
                    }
                    if (div.querySelector('[data-id=\''+target+'\']').parentElement.tagName = 'span')
                    {
                        div.querySelector('[data-id=\''+target+'\']').parentElement.classList.add('affiche');
                        div.querySelector('[data-id=\''+target+'\']').classList.add(mots_correspondants["type"]);
                        div.querySelector('[data-id=\''+target+'\']').setAttribute('data-corresp', source);
                        div.querySelector('[data-id=\''+target+'\']').addEventListener('mouseenter', enterCorrespondances, false);
                        div.querySelector('[data-id=\''+target+'\']').addEventListener('mouseleave', exitCorrespondances, false);
                        div.querySelector('[data-id=\''+source+'\']').addEventListener('mouseenter', enterCorrespondances, false);
                        div.querySelector('[data-id=\''+source+'\']').addEventListener('mouseleave', exitCorrespondances, false);
                        div.querySelector('[data-id=\''+source+'\']').classList.add('clique');
                        
            
                                                                                                     
                }
                }
            }
        }*/
  

function affiche_alignement(id_div, source, target){
    var mots = document.getElementsByClassName('actif');
    var div = document.getElementById(id_div);
    for (var mots_correspondants of liens_mots){
        if (mots_correspondants["target"].includes(target) && mots_correspondants["source"].includes(source))
        {
            if (div.querySelector('[data-id=\''+mots_correspondants["source"]+'\']').parentElement.tagName = 'span') 
            {
                div.querySelector('[data-id=\''+mots_correspondants["source"]+'\']').parentElement.classList.add('affiche');

            }
            if (div.querySelector('[data-id=\''+mots_correspondants["target"]+'\']').parentElement.tagName = 'span')
            {
                div.querySelector('[data-id=\''+mots_correspondants["target"]+'\']').parentElement.classList.add('affiche');
                div.querySelector('[data-id=\''+mots_correspondants["target"]+'\']').classList.add(mots_correspondants["type"]);
                div.querySelector('[data-id=\''+mots_correspondants["source"]+'\']').setAttribute("data-corresp", mots_correspondants["target"]);
                div.querySelector('[data-id=\''+mots_correspondants["target"]+'\']').setAttribute("data-corresp", mots_correspondants["source"]);
                div.querySelector('[data-id=\''+mots_correspondants["source"]+'\']').classList.add(mots_correspondants["type"]);
            }
        }
        else
        {
            if(!mots_correspondants["target"].includes(target) && mots_correspondants["source"].includes(source))
            {
                div.querySelector('[data-id=\''+mots_correspondants["source"]+'\']').classList.remove('actif');
            }
        }
    }
     
   
    
        }
  
function affichage_auteurs(){
    console.log('yes')
    var inputs = document.getElementsByTagName('input');
    console.log(inputs)
    for (var input of inputs)
    {
        var auteur_traite = input.id;
        if (!input.checked)
        {
            console.log ('false');
            for (var phrase in phrases_auteurs)
            {
                if (phrases_auteurs[phrase] == auteur_traite )
                {
                    document.getElementById(phrase).style.display = 'none';
                    for (var mots_correspondants of liens_mots)
                    {
                        if (mots_correspondants['target'].includes(phrase))
                        {
                            var target = document.querySelector('[data-id=\''+mots_correspondants['target']+'\']');
                            var source = document.querySelector('[data-id=\''+mots_correspondants['source']+'\']')
                            source.classList.remove('actif');
                            source.classList.remove('clique');
                            var attribs_target = target.classList
                            for (var attrib of attribs_target){
                                if (attrib != 'w'){
                                    target.classList.remove(attrib)
                                }
                            }
                            console.log(source.parentElement.tagName)
                            if  (source.parentElement.tagName == 'SPAN'){
                               console.log('affiche'); source.parentNode.classList.remove('affiche')
                            }
                            if (target.parentElement.tagName == 'SPAN'){
                               console.log('affiche'); target.parentNode.classList.remove('affiche')
                            }
                        }
                    }
                }
            }
        }
    }
    for (var input of inputs){
        var auteur_traite = input.id;
        if (input.checked){
                for (var phrase in phrases_auteurs){
                    if (phrases_auteurs[phrase] == auteur_traite ){
                        document.getElementById(phrase).style.display = 'block';
                        for (var mots_correspondants of liens_mots){
                            if (mots_correspondants['target'].includes(phrase))
                                {
                                    document.querySelector('[data-id=\''+mots_correspondants['source']+'\']').classList.add('actif');
                                }
                        }
                    }
                }
            }
            
        }
    affiche_correspondances()
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
    console.log(ensembles)
    return (Array.from(new Set(ensembles)))
}


function node_data(dictionnaire_resultats){
    var noeuds = []
    console.log("1", noeuds)
    for (ligne in dictionnaire_resultats){
        var identifiants = dictionnaire_resultats[ligne];
        var auteur = phrases_auteurs[identifiants[0]];
        if (identifiants.length > 1){
        for (identifiant of identifiants){
            parent = ligne.toString();
            console.log(parent)
            noeuds.push({data:{id:identifiant, parent : parent, auteur:auteur}})
        }
            noeuds.push({data:{id:parent, auteur : auteur}})
        }
        else{
            noeuds.push({data:{id:identifiants[0], auteur : auteur}})
        }
    }
    console.log(noeuds);
    return (noeuds)
    
}
function edge_data(dico_correspondances){
    var liens = [];
    for (id_source in dico_correspondances){
        var correspondances = dico_correspondances[id_source].split(' ');
        for (var correspondance of correspondances){
            var id_commun = id_source+'_'+correspondance;
            liens.push({data:{id: id_commun, source : id_source, target: correspondance}})
        }
        
    }
    console.log(liens);
    return (liens)
}

function creerLegende(mapCouleurs, idListe)
    {var ul = document.createElement("ul")
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
     liste.append(ul)
        
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
    var attributsAcceptes =  ['mots', 'lemmes','synonymeBase-lemme', "lemme-synonymeBase", 'synonymeElargi-lemme','synonymeBase-synonymeBase','synonymeElargi-synonymeElargi', 'actif'];
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
    if (phrases_auteurs[elem.data('source')] != undefined){
        var texteSource = document.createTextNode(phrases_auteurs[elem.data('source')]+ ', '+elem.data('source'))    
    }
    else{
         var auteur = window.location.href.split(".html")[0];
        auteur = auteur.split("HTML/")[1]
        var texteSource = document.createTextNode(auteur+ ', '+elem.data('source'))  
    }
    titreSource.append(texteSource);
    divSource.append(titreSource);
    var divTarget = document.createElement('div');
    divTarget.setAttribute('class', 'target');
    var titreTarget = document.createElement('h5');
    if (phrases_auteurs[elem.data('target')] != undefined){
        var texteTarget = document.createTextNode(phrases_auteurs[elem.data('target')]+ ', '+elem.data('target'))    
    }
    else{console.log('#######',auteur);
         auteur = window.location.href.split(".html")[0];
        auteur = auteur.split("HTML/")[1]
        
        var texteTarget = document.createTextNode(auteur+ ', '+elem.data('target'))  
    }
    titreTarget.append(texteTarget);
    divTarget.append(titreTarget);
    
    phrase_source = document.getElementById(elem.data('source'));
    phrase_source = phrase_source.cloneNode(true);
    phrase_source = modifie_id_div(phrase_source, elem.data('id'));
    divSource.append(phrase_source);
    console.log(elem.data('target'));
    phrase_target = document.getElementById(elem.data('target'));
    phrase_target = phrase_target.cloneNode(true);
    divTarget.append(phrase_target);
    div.append(divSource);
    div.append(divTarget);
    document.getElementById('graph').append(div)
    affiche_alignement(elem.data('id'), elem.data('source'),  elem.data('target') );
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
    document.getElementById('graph').style.display = 'block';
    document.getElementById('champ').style.display = 'none';
    document.getElementsByTagName('section')[1].style.display = 'none';
    document.getElementsByTagName('fieldset')[0].style.display = 'none';
    document.getElementsByTagName('h1')[0].style.display = 'none';
    var tableauID = {}
    for (var ID in correspondances_phrases){
        tableauID[ID] = Number(ID)
        console.log(Number(ID))
        var tableau_corresp = correspondances_phrases[ID].split(' ');
        for (var corresp of tableau_corresp){
            tableauID[corresp] = Number(corresp)
        }
        
    }
    console.log(tableauID)
    var i = 1;
    var resultats = {}
    for (var identifiant in tableauID){
        if (!trouves.includes(identifiant)){
            var ensemble = [];
            ensemble = trouve_identifiant(identifiant, tableauID, ensemble);
            if (ensemble.length == 0){ensemble.push(identifiant)}
            resultats[i] = ensemble;
            i = i+1
            }
    }
    console.log(resultats);
    var CouleursAuteurs = new Map();
    var cy = cytoscape({
        
        container : document.getElementById('cy'),
        elements : 
            {
                nodes: node_data(resultats),
                edges : edge_data(correspondances_phrases),
                
            },
            layout : 
            {
           name: 'cose-bilkent',
           nodeDimensionsIncludeLabels: false,
            animate : false,
                
                  nodeRepulsion: 4000,
            },
            style: [
                {
                    selector : 'node',
                    style : {
                        'label' : 'data(id)',
                        'width': '300px',
                        'height' : '300px',
                        'font-family': 'Raleway',
                        'font-size' : '50px',
                        'text-valign': 'center',
        'text-halign': 'center',
                        'opacity' : function(ele){
                            if (ele.data('id').length < 7){
                                return (0.2)
                            }
                            else{
                                return (1)
                            }
                        },
                        'background-color': function(ele) //function qui attribue une couleur aléatoire au noeud et extrait les données pour tabs id, occurrences et CouleursAuteurs
                    { // boléen pour tenter de différencier les couleurs aléatoires
                        var auteur = ele.data('auteur');
                        if (auteur == undefined){
                            auteur = window.location.href.split(".html")[0];
                            auteur = auteur.split("HTML/")[1]
                            
                        }
                        var colorType = 0;
                        //si plus qu'un auteur, on colorie selon les noms d'auteurs
                            //si auteur présent dans CouleursAuteurs, l'élément en cours prend la couleur attribué. On ajoute une occurrence pour cet auteur pour #stats1
                            if (CouleursAuteurs.has(auteur))
                            {
                                return CouleursAuteurs.get(auteur)
                            }
                            else
                            {
                                if(colorType == 0)
                                {
                                    //sinon, on attribue une couleur en traitant deux gammes aléatoires
                                    var couleur = randomColor({luminosity:'dark'});
                                    colorType = 1
                                }
                                else
                                {
                                    var couleur = randomColor({luminosity:'light'});
                                    colorType = 0
                                }
                                CouleursAuteurs.set(auteur, couleur); return couleur} //on retourne la couleur
                        
                        
                    }}
                    
                    
      
          
          
                },
                {
                selector : 'edge',
                    style : {
                        'width' : '5px'
                    }
                },
                {
                selector : 'edge:selected',
                    style : {'label' :  function(ele){showEdgeInfo(ele);}
                        
                    }
                }
            ]
        
    });
    creerLegende(CouleursAuteurs, "legende")
    
         
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
            animate : false,
                
                  nodeRepulsion: 6000,
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
