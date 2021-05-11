import xmlisationResultats
import os
import traitementsTal
import traitementNomPropre
import xml.etree
import csv

def init(fichier_corpus, racine):
    id_textes = {}
    dictionnaire_corpus = {}
    with open(fichier_corpus, newline='', encoding="utf8") as fichier_corpus:
        fichier_corpus = csv.reader(fichier_corpus, delimiter='\t')
        for ligne_corpus in fichier_corpus:
            dictionnaire_corpus[ligne_corpus[0]] = ligne_corpus[1]
            id_textes[ligne_corpus[0]] = ligne_corpus[3]

    phrasesXML =xmlisationResultats.xmlisation_phrases(dictionnaire_corpus, 0)

    texte_structure = """<corpus>"""
    for identifiant, structure in phrasesXML.items():
        structure_complete = "<s xml:id=\""+identifiant+"\" corresp=\""+id_textes[identifiant]+"\">"+structure+"</s>"
        texte_structure += structure_complete+"\n"
    texte_structure += "</corpus>"

    fichier_structure = open("src/corpus.xml", "w", encoding="utf8")
    fichier_structure.write(texte_structure)
    fichier_structure.close()