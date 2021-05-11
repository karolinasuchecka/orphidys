
$.getJSON('json/graphe_general.json', function(data){

var cy = cytoscape(
    {
        container: document.getElementById('cy'),
        elements: data['elements'],
        style: [
            {
                selector: 'node',
                style: {
                    'shape': function(ele){
                        var type = ele.data('type');
                        var valeursTypes = {'modernisation':'triangle', 'transmodalisation':'ellipse', 'parodie':'star'}
                        if (type == 'traduction'){
                            var auteur = ele.data('auteur');
                            console.log(auteur)
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
                    
                    'label': function(ele){return(ele.data('id').toUpperCase())},
                    'text-background-color': function(ele){
    var couleurs = { 'poésie' : '#C0392B', 'théâtre' : '#27AE60', 'prose' : '#2980B9', 'opéra' : ' #8E44AD', 'BD' : '#E67E22', 'autre' : '#f4d03f' }
    var subtype = ele.data('subtype')
    return(couleurs[subtype])
}, 
                    'text-background-opacity' : 0.4,
		    'text-wrap' : 'wrap',
                    'color' : ' white',
		    'text-max-width' : '300px',
                    
                  'text-background-shape': 'roundrectangle',
//                    'width' : '15px',
//                    'height' : '15px',
                    'width':  function(ele){
                        if (ele.data('poids') < 25)
                            {
                                return(25)
                            }
                        else{
                            return(ele.data('poids'))
                        }
                    },
                    'height': function(ele){
                        if (ele.data('poids') < 25)
                            {
                                return(25)
                            }
                        else{
                            return(ele.data('poids'))
                        }
                    },
                    'font-family' : 'Raleway',
                    'font-size' : '19px',
                    'font-weight' : "bolder",
'background-color': function(ele){
    var couleurs = { 'poésie' : '#C0392B', 'théâtre' : '#27AE60', 'prose' : '#2980B9', 'opéra' : '#8E44AD', 'BD' : '#E67E22', 'autre' : '#f4d03f' }
    var subtype = ele.data('subtype')
    return(couleurs[subtype])
}, 
			"text-valign": "center",
      "text-halign": "center",
                    'z-index' : 0,
                }
            },
{selector: 'node:selected',
style:{
'width' : '100',
'height' : '100',
'font-size' : '40',
'label' : function(ele){showNodeInfo(ele);},
'text-wrap': 'wrap',
                  'text-max-width': '600px',
                  'text-max-height': 'auto',
                  //'border-width': '6px',
                  //'border-color': '#AAD8FF',
                  //'border-opacity': '0.5',
                  'text-outline-color': '#555',
                  'text-background-color':function(ele){
    var couleurs = { 'poésie' : '#C0392B', 'théâtre' : '#27AE60', 'prose' : '#2980B9', 'opéra' : '#8E44AD', 'BD' : '#E67E22', 'autre' : '#f4d03f' }
    var subtype = ele.data('subtype')
    return(couleurs[subtype])
},
                  'text-background-opacity':'0.9',
                  'text-background-shape': 'roundrectangle',
                  'text-background-padding': '10px',
                  'z-index': 2,
'text-halign': 'right',
'text-valign': 'center',}
},
            
            {
                selector: 'edge',
                style: 
                {
                    'line-color': '#0000',
                    
                    'background-opacity' : 0.5,
                    'width': '1px',
                    'z-index' : 0,

                    'target-arrow-shape': 'triangle',
                    'control-point-step-size': '140px'
                },
                selector: 'edge:selected',
                style: 
                { 'z-index' : 100,
                    'line-color': '#0000',
                    'text-background-opacity': 0,
                    'background-opacity' : 0.5,
                    'width': 'data(poids)',
                    'fontSize' : '20px',
                    'font-family' : 'Raleway',
                    
                    
                    'label' :  function(ele){showEdgeInfo(ele);}
                    ,
                    
                    'color' : 'white',
                 'text-max-width': '200px',
                  'text-max-height': 'auto',
                 'text-outline-color': '#555',
                  'text-background-color':'rgba(225, 225, 229)',
                  'text-background-opacity':'0.9',
                  'text-background-shape': 'roundrectangle',
                  'text-background-padding': '10px',

                    'target-arrow-shape': 'triangle',
                    'control-point-step-size': '140px'
                }
            },
            {selector: 'node.highlight',
            style: {
                //'border-color': '#FFF',
                //'border-width': '2px'
            }
        },
        {
            selector: 'node.semitransp',
            style:{ 'opacity': '0.5' }
        },
        {
            selector: 'edge.highlight',
            style: { 'mid-target-arrow-color': '#2980B9',
                    'width': 'data(poids)'
                   }
        },
        {
            selector: 'edge.semitransp',
            style:{ 'opacity': '0.2' }
        }

],
        layout: {
            name: 'concentric',
            ready: function () {
    },
    // Called on `layoutstop`
    stop: function () {
    },
    // number of ticks per frame; higher is faster but more jerky
    refresh: 30,
    // Whether to fit the network view after when done
    fit: true,
    // Padding on fit
    padding: 5,
    // Prevent the user grabbing nodes during the layout (usually with animate:true)
    ungrabifyWhileSimulating: false,
    // Type of layout animation. The option set is {'during', 'end', false}
    animate: 'end',
    // Duration for animate:end
    animationDuration: 500,   
    // How apart the nodes are
    nodeSeparation: 70,
            
            
        }
    }
);
/*var indice = 0;
cy.on('mouseover', 'node', function(e) {
    var sel = e.target;
    cy.elements()
        .difference(sel.outgoers()
            .union(sel.incomers()))
        .not(sel)
        .addClass('semitransp');
    sel.addClass('highlight')
        .outgoers()
        .union(sel.incomers())
        .addClass('highlight');
});*/
    
    var sel = '';
    cy.on('tap', 'node', function(e) {
    if (sel != e.taget && sel != ''){
    cy.elements()
        .removeClass('semitransp');
    sel.removeClass('highlight')
        .outgoers()
        .union(sel.incomers())
        .removeClass('highlight');
    }    
    sel = e.target;
    cy.elements()
        .difference(sel.outgoers()
            .union(sel.incomers()))
        .not(sel)
        .addClass('semitransp');
    sel.addClass('highlight')
        .outgoers()
        .union(sel.incomers())
        .addClass('highlight');
       
});
/*cy.on('mouseout', 'node', function(e) {
    var sel = e.target;
    cy.elements()
        .removeClass('semitransp');
    sel.removeClass('highlight')
        .outgoers()
        .union(sel.incomers())
        .removeClass('highlight');
    
});*/
var dictionnaireLiens = {};
    for (var i = 0; i < data.elements.edges.length; i++){
        var source = data.elements.edges[i].data.source;
        var target = data.elements.edges[i].data.target;
        var poids = data.elements.edges[i].data.poids;
        if (dictionnaireLiens[source] == undefined){
            dictionnaireLiens[source] = [[target, poids]]
            
        }
        else{
            dictionnaireLiens[source].push([target, poids])
        }
        if (dictionnaireLiens[target] == undefined){
            dictionnaireLiens[target] = [[source, poids]]
        }
        else{
            dictionnaireLiens[target].push([source, poids])
        }
    }
    console.log(dictionnaireLiens);
    
function showEdgeInfo(ele){
    if (ele.data('poids') > 1){
    var infoTemplate = Handlebars.compile([
			'<p><em>{{poids}}</em> phrases correspondantes ont été détectées entre <em>{{source}}</em> et <em>{{target}}</em></p>',
		].join(''));
    }
    else{
        var infoTemplate = Handlebars.compile([
			'<p><em>{{poids}}</em> phrase correspondante a été détéctée entre <em>{{source}}</em> et <em>{{target}}</em></p>',
		].join(''));
        
    }
		console.log(infoTemplate);
    
}

    function showNodeInfo(ele){
        if (ele.data('type') == 'traduction'){
            var infoTemplate = Handlebars.compile(["<p><strong>Auteur : </strong>{{auteur}}</p><p><strong>Titre : </strong> {{titre}}</p><p><strong>Traducteur : </strong> {{editeur}}</p><p><strong>Date de publication : </strong> {{date}}</p><p><strong>Lieu et maison d'édition : </strong>{{pubPlace}}, {{publisher}}</p>",].join(''));
        }
        else{
            var infoTemplate = Handlebars.compile(["<p><strong>Auteur : </strong>{{auteur}}</p><p><strong>Titre : </strong> {{titre}}</p><p><strong>Date de publication : </strong> {{date}}</p><p><strong>Lieu et maison d'édition : </strong>{{pubPlace}}, {{publisher}}</p>",].join(''));
        }
        $('#info').html(infoTemplate(ele.data())).show()
        
        var relations = dictionnaireLiens[ele.data('id')]
    console.log(relations)
    texteHTML = "<form method=\"GET\" action=\"pages/"+ele.data('id')+".html\"><fieldset><legend>Quel(s) texte(s) inclure dans la comparaison ?</legend>";
    for (var relation of relations){
        console.log(relation);
        texteHTML += "<div><input type=\"checkbox\" id=\""+relation[0]+"\" name=\"corresp\" value=\""+relation[0]+"\"><label for=\""+relation[0]+"\"> "+relation[0] + " ("+relation[1]+" corresp.)</label></div>"
        
    }
    texteHTML += "<div><button type=\"submit\">Afficher la page correspondante</button></div></fieldset>";
    console.log(texteHTML);
		$('#info').html(infoTemplate(ele.data())).show();
    document.getElementById('correspondances').innerHTML = texteHTML;
    document.getElementById('correspondances').style.display = 'block';
    
}
});


