__auteur__ = "Karolina Suchecka"
__date__ = "26/11/19"

import xml.etree.ElementTree as ET
import os
import re

"""
Function qui envoie le corpus en format ODT vers le logiciel ODETTE pour le tranformer vers XML.
Le dossier des fichiers ODT et le dossier où les XML doivent être enregistrés est renseigné par
l'utilisateur pendant l'initialisation. Le dossier target est crée s'il n'existe pas.
_____________________________Étapes :____________________________
1. Création du dossier target si celui-ci n'existe pas
2. Copie des fichiers ODT du dossier source vers le dossier avec les feuilles de transformation
d'Odette
3. Lancement du traitement en PHP, sauvegarde des fichiers dans le dossier XML fils
4. Déplacement des fichiers XML vers le dossier target et suppression des fichiers ODT 
du dossier Odette
5. Retour au dossier de travail
6. Lancement de la fonction ajout_tei_header
_____________________________Remarques :____________________________
* Les fichiers doivent être corrigés après le traitement avec ODETTE
"""


def structuration_corpus(traitement, racine):
    if not os.path.exists(traitement.dossier_target):
        os.makedirs(traitement.dossier_target)
    os.chdir(racine)
    os.chdir(traitement.dossier_source)
    noms_fichiers = os.listdir(".")
    os.system("cp -r *.odt " + racine + "/" + traitement.odette)
    os.chdir(racine + "/" + traitement.odette)
    os.system("ls .")
    os.system("php  -f Odt2tei.php \"*.odt\" XML/")
    for fichier in noms_fichiers:
        fichier = fichier[:-3]
        print("mv "+fichier+"xml " + racine + "/" + traitement.dossier_target)
        os.system("mv "+fichier+"xml " + racine + "/" + traitement.dossier_target)
    os.system("rm *.odt")
    os.chdir(racine)
    os.chdir(traitement.dossier_target)
    print("Pensez à corriger votre XML après le traitement")
    #ajout_tei_header(traitement, racine)


"""
Fonction préliminaire qui extrait le texte de chaque document XML
avent d'envoyer l'identifiant de l'oeuvre à la fonction
enrichissement_oeuvre
_____________________________Étapes :____________________________
1. Extraction de l'élément <text> de chaque XML
2. Ajout de l'élément <facsimile> si présent dans le document
3. Envoi vers la fonction enrichissement_oeuvre pour récupérer 
le teiHeader et le front
4. Ajout de la déclaration au début du texte
5. Construction du nouveau fichier XML et son enregistrement
à la place de l'ancien
"""


def ajout_tei_header(traitement, racine):
    os.chdir(racine)
    liste_oeuvres = os.listdir(traitement.dossier_target)
    for oeuvre in liste_oeuvres:
        print("Oeuvre traitée -->" + oeuvre)
        tree_oeuvre = ET.parse(traitement.dossier_target + "/" + oeuvre)
        root_oeuvre = tree_oeuvre.getroot()
        text = root_oeuvre.findall('.//{http://www.tei-c.org/ns/1.0}text')[0]
        text = ET.tostring(text, encoding='utf8').decode('utf8')
        if len(root_oeuvre.findall('.//{http://www.tei-c.org/ns/1.0}facsimile')) > 0:
            fac_simile = root_oeuvre.findall('.//{http://www.tei-c.org/ns/1.0}facsimile')[0]
            fac_simile = ET.tostring(fac_simile, encoding='utf8').decode('utf8')
            text = fac_simile + text
        text = re.sub("( xmlns:)?ns0[:=](\"http://wwww\.tei-c\.org/ns/1\.0\")?", "", text)
        text = re.sub("<\?xml version=\"1\.0\" encoding=\"utf8\"\?>", "", text)
        text = re.sub("</?text>", "", text)
        text = re.sub(" />", "/>", text)
        new_header, front = enrichissement_oeuvre(oeuvre, traitement.base_textes)
        f = open(traitement.dossier_target + '/' + oeuvre, 'w')
        doc = """<?xml version="1.0" encoding="UTF-8"?>
        <?xml-model href="http://www.tei-c.org/release/xml/tei/custom/schema/relaxng/tei_all.rng"
        type="application/xml" schematypens="http://relaxng.org/ns/structure/1.0"?>
        <?xml-model href="http://www.tei-c.org/release/xml/tei/custom/schema/relaxng/tei_all.rng" type="application/xml" 
        schematypens="http://purl.oclc.org/dsdl/schematron"?>
        <TEI xmlns="http://www.tei-c.org/ns/1.0">"""
        doc = doc + new_header + """<text>""" + front + text + "</text></TEI>"
        # print(doc)
        f.write(doc)
        f.close()


"""
Pour chaque oeuvre du dossier target, on constuit les métadonnées à renseigner dans l'élément
<teiHeader> et <front> à partir de la base de données du corpus (src/Corpus_XML)
_____________________________Étapes :_______________________________________________________
1. Conversion du nom de fichier en son identifiant (xml:id)
2. Extraction de l'entrée correspondante dans la base de données
3. Extraction des différents éléments à intégrer dans les métadonnées (titre, auteur,
éditeur, langue, classification (sous corpus, type d'oeuvre, etc), publication)
4. Intégration des métadonnées dans la structure de teiHeader pour répondre
aux cheminements utilisés par TextPAIR (attention, certains élément ne sont pas
conformes à la TEI)
5. Intégration du titre et de l'autre pour la création de l'élément front
6. Retour des deux éléments
___________________________Remarques :________________________________________________________
* Pour les éléments comme auteur, éditeur, etc., on concatène s'il y a plusieurs valeurs
* Il est important de mettre à jour régulièrement la base de données. Le logiciel
s'interrompera si des éléments manquent : permet de contrôler la complétude d'informations
dans la BD.
* Il ne faut pas mettre les points dans les titres dans la BD. 
"""


def enrichissement_oeuvre(fichier, base):
    tree_corpus = ET.parse(base)
    root_corpus = tree_corpus.getroot()
    ns = '{http://www.tei-c.org/ns/1.0}'
    fichier = fichier[:-4]
    if re.search("_prose$", fichier):
        fichier = re.sub("_prose", '', fichier)
    if re.search("_vers$", fichier):
        fichier = re.sub("_vers", '', fichier)
    if re.search("_tradFR$", fichier):
        fichier = re.sub("_tradFR", '', fichier)
    xpath = "./" + ns + "text/" + ns + "body/" + ns + "listObject/" + ns + "object/[@{http://www.w3.org/XML/1998/namespace}id ='" + fichier + "']"
    for biblio_oeuvre in root_corpus.findall(xpath):
        titres = biblio_oeuvre.findall('.//' + ns + 'title')
        if len(titres) > 1:
            titre = ''
            for title in titres:
                if title.text != '':
                    titre = titre + title.text + '. '
            titre = titre[:-2]
        else:
            titre = titres[0].text
        auteurs = biblio_oeuvre.findall('.//' + ns + 'persName')
        auteur = ''
        if len(auteurs) > 1:
            for auteur_part in auteurs:
                if auteur_part.findall('./' + ns + 'forename'):
                    auteur = auteur + auteur_part.findall('./' + ns + 'forename')[0].text + ' '
                if auteur_part.findall('./' + ns + 'surname'):
                    auteur = auteur + auteur_part.findall('./' + ns + 'surname')[0].text + ', '
            auteur = auteur[:-2]
        if len(auteurs) == 0:
            auteur = 'Anonyme'
        if len(auteurs) == 1:
            if auteurs[0].findall('./' + ns + 'forename'):
                auteur = auteur + auteurs[0].findall('./' + ns + 'forename')[0].text + ' '
            if auteurs[0].findall('./' + ns + 'surname'):
                auteur = auteur + auteurs[0].findall('./' + ns + 'surname')[0].text
        editeurs = biblio_oeuvre.findall('.//' + ns + 'editor')
        editeur = ''
        if len(editeurs) > 1:
            for editeur_part in editeurs:
                editeur = editeur + editeur_part.text + ', '
            editeur = editeur[:-2]
        if len(editeurs) == 1:
            editeur = editeurs[0].text
        language = biblio_oeuvre.attrib['{http://www.w3.org/XML/1998/namespace}lang']
        sous_corpus = biblio_oeuvre.attrib['type']
        genre = biblio_oeuvre.attrib['subtype']
        id = fichier
        pub_place = biblio_oeuvre.findall('.//' + ns + 'pubPlace')[0].text
        publishers = biblio_oeuvre.findall('.//' + ns + 'publisher')
        publisher = ''
        if len(publishers) == 1:
            publisher = publishers[0].text
        if len(publishers) > 1:
            for publisher_part in publishers:
                publisher = publisher + publisher_part.text + ', '
            publisher = publisher[:-2]
        date = biblio_oeuvre.findall('.//' + ns + 'monogr/' + ns + 'imprint/' + ns + 'date')[0].attrib['when']
        idno = biblio_oeuvre.findall('.//' + ns + 'monogr/' + ns + 'note/' + ns + 'ref')
        ref = ""
        if len(idno) > 1:
            for lien in idno:
                ref = ref + lien.attrib['target'] + " / "
            ref = ref[:-3]
        if len(idno) == 1:
            ref = idno[0].attrib['target']
        if len(idno) == 0:
            ref = ''
        citation = biblio_oeuvre.findall('.//' + ns + 'citedRange')
        cited_range = ""
        for cite in citation:
            if cite.attrib['unit'] == "page":
                cited_range = cited_range + "p. "
            if cite.attrib['unit'] == "line":
                cited_range = cited_range + "l. "
            if cite.attrib['unit'] == "folio":
                cited_range = cited_range + "fs. "
            cited_range = cited_range + cite.attrib['from'] + '-' + cite.attrib['to'] + ', '
        cited_range = cited_range[:-2]
        print(sous_corpus, genre, pub_place, publisher, date, ref, cited_range, titre, auteur, editeur, id)
        tei_header = """<teiHeader>
        <fileDesc>
            <titleStmt>
                <title type="main">""" + titre + """</title>
                <author>""" + auteur + """</author>
                <editor>""" + editeur + """</editor>
            </titleStmt>
            <editionStmt>
                <edition>Cette édition électronique fait partie du projet de thèse intitulé « Analyse et édition d’un corpus littéraire 
                dans l’esprit des humanités numériques. Vers une édition comparative intermédiale innovante accompagnée d’une ressource pour le repérage intertextuel » 
                réalisé par Karolina Suchecka au sein du laboratoire ALITHILA à l’Université de Lille.</edition>
                <respStmt>
                    <name>Karolina Suchecka</name>
                    <resp>Chargé de l'édition</resp>
                </respStmt>
                <respStmt>
                    <name>Nathalie Gasiglia</name>
                    <resp>Co-tutrice de thèse</resp>
                </respStmt>
                <respStmt>
                    <name>Karl Zieger</name>
                    <resp>Co-tuteur de thèse</resp>
                </respStmt>
            </editionStmt>
            <publicationStmt>
                <publisher>Karolina Suchecka</publisher>
                <publisher>ALITHILA (Université Lille III)</publisher>
                <date when="2019"/>
                <availability status="restricted">
                    <licence target="http://creativecommons.org/licenses/by-nc-nd/3.0/fr/">
                        <p> Copyright © 2019 Université Charles-de-Gaulle Lille 3, agissant pour le projet de thèse 
                        « Analyse et édition d’un corpus littéraire dans l’esprit des humanités numériques. Vers une édition comparative intermédiale
                         innovante accompagnée d’une ressource pour le repérage intertextuel »</p>
                        <p> Cette ressource électronique protégée par le code de la propriété intellectuelle sur les bases de données (L341-1)
                         est mise à disposition de la communauté scientifique internationale par Karolina Suchecka, selon les termes de la licence Creative Commons :
                          « Attribution - Pas d’Utilisation Commerciale - Pas de Modification 3.0 France (CC BY-NC-ND 3.0 FR) ». </p>
                        <p> Attribution : afin de référencer la source, toute utilisation ou publication dérivée de cette ressource électroniques comportera 
                        le nom du projet et surtout l’adresse Internet de la ressource. </p>
                        <p> Pas d’Utilisation Commerciale : dans l’intérêt de la communauté scientifique, toute utilisation commerciale est interdite.</p>
                        <p> Pas de Modification : l’éditrice s’engage à améliorer et à corriger cette ressource électronique, notamment en intégrant toutes les 
                        contributions extérieures, la diffusion de versions modifiées de cette ressource n’est pas souhaitable.</p>
                    </licence>
                </availability>
                <idno>""" + ref + """</idno>
            </publicationStmt>
            <sourceDesc>
                <bibl><author>""" + auteur + """</author> / <title>""" + titre + """</title> / """ + pub_place + """ / """ + publisher + """ / """ + date + """ / """ + cited_range + """.</bibl> 
                <biblFull>
                    <titleStmt>
                        <title>""" + titre + """</title>
                    </titleStmt>
                    <publicationStmt>
                        <publisher>""" + publisher + """</publisher>
                        <pubPlace>""" + pub_place + """</pubPlace>
                        <date when=\"""" + date + """\"/>
                    </publicationStmt>
                </biblFull>
                <genre>""" + genre + """</genre>
                <structure>""" + id + """</structure>
            </sourceDesc>
        </fileDesc>
        <encodingDesc>
            <p>Nous utilisons la feuille de style Odette pour les premières transformations ODT/XML. Nous nettoyons et 
            enrichissons ensuite la structure avec des algorihtmes Python conçus au sein du projet. La structure des métadonnées a été établie en référence 
            à la manière dont le logiciel TEXTPAIR (The ARTFL Project) les extrait ensuite pour son traitement.</p>
        </encodingDesc>
        <profileDesc>
            <creation>
                <date when=\"""" + date + """\">""" + date + """</date>
            </creation>
            <language>
                <language>""" + language + """</language>
            </language>
            <textClass>
                <keywords>
                    <list>
                        <item>""" + sous_corpus + """</item>
                    </list>
                </keywords>
            </textClass>
        </profileDesc>
    </teiHeader>"""

        front = """<front><titlePage>
            <docAuthor>""" + auteur + """</docAuthor>
            <docTitle>
              <titlePart type="main">""" + titre + """</titlePart>
            </docTitle>
          </titlePage></front>
            """
        return tei_header, front
