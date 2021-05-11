import networkx as nx
import xml.etree.ElementTree as ET
import csv
import json
import alignementHTML
import  os

def trouve_auteur(id_phrase, id_textes):
    for auteur, phrases in id_textes.items():
        if id_phrase in phrases:
            return auteur


def creation_graphe(traitement, racine):
    """Nombre des phrases"""
    id_textes = {}
    with open(traitement.fichier_corpus, newline='') as fichier_corpus:
        fichier_corpus = csv.reader(fichier_corpus, delimiter='\t')
        for ligne_corpus in fichier_corpus:
            if ligne_corpus[3] not in id_textes.keys():
                id_textes[ligne_corpus[3]] = []
            id_textes[ligne_corpus[3]].append(ligne_corpus[0])

    nombre_phrases = {}
    for id_auteur, phrases in id_textes.items():
        print(id_auteur, max(phrases))
        numero_phrase = max(phrases)[2:]
        numero_phrase = int(numero_phrase)
        print (numero_phrase)
        nombre_phrases[id_auteur] = numero_phrase
    """Ouverture du fichier XML avec les chunks """
    parser = ET.XMLParser(encoding='utf-8')
    fichier = open(racine + "/" + traitement.resultats_post).read()
    rootResults = ET.fromstring(fichier, parser=parser)


    """Ouverture de la BD"""
    treeBD = ET.parse(traitement.base_textes)
    rootBD = treeBD.getroot()
    ns = '{http://www.tei-c.org/ns/1.0}'

    """Création du graphe"""
    graphe_general = nx.Graph()

    """Extraction des informations de la BD pour chaque auteur"""
    auteurs = rootResults.findall('div')
    phrases_auteurs = {}
    for auteur in auteurs:
        scores = []
        id_auteur = auteur.attrib['id']
        if "_" in id_auteur:
            id_BD_auteur = id_auteur.split('_')[0]
        else:
            id_BD_auteur = id_auteur
        print(id_BD_auteur)
        data_auteur = rootBD.find("./" + ns + "text/" + ns + "body/" + ns + "listObject/" + ns + "object/[@{http://www.w3.org/XML/1998/namespace}id ='" + id_BD_auteur + "']")

        type = data_auteur.attrib['type']
        if "prose" in id_auteur:
            subtype = "prose"
        elif "vers" in id_auteur:
            subtype = "poésie"
        else:
            subtype = data_auteur.attrib['subtype']
        titre = data_auteur.findall('.//'+ns+'title')[0].text
        noms_auteurs = data_auteur.findall('.//' + ns + 'persName')
        nom_auteur = ''
        if len(noms_auteurs) > 1:
            for auteur_part in noms_auteurs:
                if auteur_part.findall('./' + ns + 'forename'):
                    nom_auteur = nom_auteur + auteur_part.findall('./' + ns + 'forename')[0].text + ' '
                if auteur_part.findall('./' + ns + 'surname'):
                    nom_auteur = nom_auteur + auteur_part.findall('./' + ns + 'surname')[0].text + ', '
            nom_auteur = nom_auteur[:-2]
        if len(noms_auteurs) == 0:
            nom_auteur = 'Anonyme'
        if len(noms_auteurs) == 1:
            if noms_auteurs[0].findall('./' + ns + 'forename'):
                nom_auteur = nom_auteur + noms_auteurs[0].findall('./' + ns + 'forename')[0].text + ' '
            if noms_auteurs[0].findall('./' + ns + 'surname'):
                nom_auteur = nom_auteur + noms_auteurs[0].findall('./' + ns + 'surname')[0].text

        editeurs = data_auteur.findall('.//'+ns+'editor[@resp=\'trad\']')
        if len(editeurs) > 1:
            editeur = ''
            for ed in editeurs:
                editeur += ed.text + ', '
            editeur = editeur[:-2]
        elif len(editeurs) == 1:
            editeur = editeurs[0].text
        else:
            editeur = ''
        pubPlace = data_auteur.find('.//'+ns+'pubPlace').text
        publisher = data_auteur.find('.//'+ns+'publisher')
        if publisher == None:
            publisher = ''
        else:
            publisher = publisher.text
        date = data_auteur.find('.//'+ns+'date').attrib['when']

        print(id_auteur, type, subtype, titre, nom_auteur, editeur, pubPlace, publisher, date)
        phrases = auteur.findall(".//s")
        id_phrases = []
        id_correspondances = {}
        correspondances = []
        for phrase in phrases:
            if len(phrase.findall("interpGrp")) > 0:
                interpGrps = phrase.findall("interpGrp")
                for interpGrp in interpGrps:
                    if interpGrp.attrib['corresp'] != "" and interpGrp.attrib['corresp'] not in correspondances:
                        id_auteur_corresp = trouve_auteur(interpGrp.attrib['corresp'], id_textes)
                        interp_score_couple = interpGrp.find('interp[@type="score"]')
                        score_couple = float(interp_score_couple.text)
                        scores.append(score_couple)
                        correspondances.append(interpGrp.attrib['corresp'])
                        if id_auteur_corresp not in id_correspondances.keys():
                            id_correspondances[id_auteur_corresp] = 1
                        else:
                            id_correspondances[id_auteur_corresp] += 1


            # if "corresp" in phrase.attrib:
            #     if phrase.attrib['id'] not in id_phrases:
            #         id_phrases.append(phrase.attrib['id'])
            #     phrases_corresp = phrase.attrib["corresp"]
            #     corresps = phrases_corresp.split(' ')
            #     for corresp in corresps:
            #         if corresp not in correspondances and corresp != '':
            #             id_auteur_corresp = trouve_auteur(corresp, id_textes)
            #             correspondances.append(corresp)
            #             if id_auteur_corresp not in id_correspondances.keys():
            #                 id_correspondances[id_auteur_corresp] = 1
            #             else:
            #                 id_correspondances[id_auteur_corresp] += 1


        #phrases_auteurs[id_auteur] = id_phrases
        #weight = round((len(id_phrases)/nombre_phrases[id_auteur]) * 100, 2)
        score_final = 0
        for score in scores:
            score_final += score
        if len(scores) > 0:
            weight = round(score_final/len(scores), 2)
            print(weight)
        else:
            weight = 0
        graphe_general.add_node(id_auteur, type=type, subtype=subtype, auteur=nom_auteur, titre=titre, editeur=editeur, publisher=publisher , pubPlace=pubPlace,
                                date=date, poids=weight)
        for auteur in id_correspondances.keys():
            print (id_auteur, auteur, id_correspondances[auteur])
            graphe_general.add_edge(id_auteur, auteur, poids = id_correspondances[auteur])

        data = nx.readwrite.json_graph.cytoscape_data(graphe_general, {'link' : 'edges'})
        nx.write_gexf(graphe_general, 'test.gexf')
        if not os.path.exists(traitement.chemin_html):
            os.makedirs(traitement.chemin_html)
        os.system('cp -r ' + traitement.sources + '/* ' + traitement.chemin_html)
        with open (traitement.chemin_html+'/json/graphe_general.json', 'w') as f:
            json.dump(data, f)
    if "3" in traitement.action or "1" in traitement.action:
        alignementHTML.generation_html(traitement, racine)


