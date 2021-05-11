import xml.etree.ElementTree as ET
import traitementsTal
import re
import xmlisationResultats
import os
from nltk.tokenize import sent_tokenize
import random
import string
import csv
import Levenshtein

def randomString(stringLength):
    """Generate a random string with the combination of lowercase and uppercase letters """
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for i in range(stringLength))

def trouve_auteur(id_phrase, rootResults):
    divs_auteurs = rootResults.findall('div')
    #print (id_phrase)
    for div in divs_auteurs:
        if div.find('.//s[@id = \''+id_phrase+'\']') != None:
            return div.attrib['id']

def generation_html(traitement, racine):
    ET.register_namespace('', "http://www.tei-c.org/ns/1.0")
    parser = ET.XMLParser(encoding='utf-8')
    fichier = open(racine + "/" + traitement.resultats_post).read()
    rootResults = ET.fromstring(fichier, parser=parser)
    textes = rootResults.findall(".//div")
    ns = '{http://www.tei-c.org/ns/1.0}'
    if not os.path.exists(racine+"/"+traitement.chemin_xml_compile):
            os.makedirs(racine+"/"+traitement.chemin_xml_compile)
    trads = ["boxus2008", "walleys1493", "legouais1301", "york1470", "parnajon1880_prose", "parnajon1880_prose_vers",
             "nisard1869", "villenave1806", "duryer1702", "guillois1863", "fournier1876", "nisard1868", "delille1770",
             "rat1932", "desportes1846_prose", "desportes1846_vers", "cournand1805", "cogolin1750", "heguin1827", "duchemin1837", "banier1732",
             "renouard1606", "corneille1697", "gros1834", "cabaret-dupaty1897", "charpentier1831", "desfontaines1810",
             "morin1532", "bellegarde1701", "martignac1697", "habert1557", "massac1617", "fontanelle1789",
             "collognat2014", "rachmuhl2003", "tours1540", "duryer1702"]
    for texte in textes:
        listApp = ET.Element('{http://www.tei-c.org/ns/1.0}listApp')
        id_texte = texte.attrib['id']
        #if not os.path.exists(racine+"/"+traitement.chemin_xml_compile+"/" +id_texte+"_resultats.xml") and not id_texte in trads:
        #if id_texte == 'duryer1702':
        print("##############" + id_texte + "###############")
        texteResults = ET.parse(traitement.chemin_textes + "/" + id_texte + ".xml")
        texte_root = texteResults.getroot()
        print(ET.tostring(texte_root, encoding='utf8').decode('utf8'))
        phrases = texte.findall(".//s")
        for phrase in phrases:
            if 'corresp' in phrase.attrib and phrase.attrib['corresp'] != '':
                id_app = randomString(7)
                app = ET.Element('{http://www.tei-c.org/ns/1.0}app', attrib={'xml:id':id_app})
                lem = ET.Element('{http://www.tei-c.org/ns/1.0}lem')
                lem.insert(0, phrase)
                app.insert(0, lem)
                id_phrase = phrase.attrib['id']
                numero_phrase = str(int(id_phrase[2:]))
                print(numero_phrase)
                ancre_phrase = texte_root.find(".//"+ns+"milestone[@n=\""+numero_phrase+"\"]")
                ancre_phrase.attrib["corresp"] = id_app
                corresps = phrase.attrib["corresp"].split(' ')
                for corresp in corresps:
                    if corresp != '' and rootResults.find(".//s[@id = '" + corresp + "']"):
                        phrase_corresp = rootResults.find(".//s[@id = '" + corresp + "']")

                        rdg = ET.Element('{http://www.tei-c.org/ns/1.0}rdg', attrib={'xml:id': phrase_corresp.attrib['id'],
                                                        "source": trouve_auteur(phrase_corresp.attrib['id'], rootResults)})
                        rdg.append(phrase_corresp)
                        app.append(rdg)
                listApp.append(app)

        element_texte = texte_root.find(".//"+ns+"text")
        element_texte.append(listApp)
        #texte_final = ET.tostring(texte_root, encoding='utf8').decode('utf8')
        #print (texte_final)
        #fichier_texte = open(traitement.chemin_xml_compile + "/" + id_texte + "_resultats.xml", "w")
        #fichier_texte.write(texte_final)
        #fichier_texte.close()
        texteResults.write(traitement.chemin_xml_compile + "/" + id_texte + "_resultats.xml", encoding="utf8")
        if '1' in traitement.action or '4' in traitement.action:
            correction = input("Pensez à s'assurer que les fichiers produits sont corrects. Prête ? (O|N) ")
            if correction == 'O':
                os.system(
                    "java -jar src/saxon9he.jar -xsl:src/alignementHTML.xsl -s:" + traitement.chemin_xml_compile + "/"
                    + id_texte + "_resultats.xml -o:" + traitement.chemin_html)