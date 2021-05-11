__auteur__ = "Karolina Suchecka"
__date__ = "26/11/19"

import os
import shutil
import re
from nltk.tokenize import sent_tokenize
import traitementsTal
import traitementsSystem
import xml.etree.ElementTree as ET
import csv

"""
Ensemble de scripts pour le pretraitement du corpus pour le logiciel Tracer 
et pour le lancement du traitement. Créé un fichier texte avec, pour chaque oeuvre
du corpus, une phrase par ligne, accompagné de l'identifiant spécifique.
Modulation du traitement possible (tout le corpus / traductions vs réécritures /
ignorer les textes en ancien français). A optimiser après avoir créé la base de données
du corpus en SQL Lite.
Les traitements du TAL sont gérés par le script traitementsTal
"""


"""
Première phrase de traitement du corpus pour Tracer
___________________________Étapes_______________________
1. Transforme tous les textes du corpus du format XML au format texte en ignorant les éléments
qu'on ne veut pas faire traiter par Tracer (label, speaker, etc.). Pour ce faire, il fait appel
à une transformation en XSL.
2. Prend en compte les configurations de l'initialisation pour partager éventuellement
le corpus et supprimer les textes en ancien français
3. Transmet chaque texte à la fonction identification_phrases.
4. Sauvegarde le fichier du corpus au format demandé dans le dossier data de Tracer, avec le nom
du projet choisi par l'utilisateur
5. Demande si besoin de lemmatisation. Le cas échéant, lance traitementsTal.lemmatisation et
sauvegarde le fichier de lemmes dans le dossier du projet
6. Supprime le dossier avec le corpus en format texte
7. Lance l'initialisation du traitement avec Tracer (fonction initialisation_tracer)
___________________________Remarques_______________________ 
"""
#todo: Prise en charge des synonymes dans une étape ultérieure



def preprocessing(traitement, racine):
    os.chdir(racine)
    liste_xml = os.listdir(traitement.dossier_source)
    print (liste_xml)
    if not os.path.exists("txt"):
        os.makedirs("txt")
    corpus = ''

    if "mod" in traitement.type_traitement:
        base = "src/corpus_BD.xml"
        tree_corpus = ET.parse(base)
        root_corpus = tree_corpus.getroot()
        ns = '{http://www.tei-c.org/ns/1.0}'
        for xml in liste_xml:
            identifiant = xml[:-4]
            if re.search("_prose$", identifiant):
                identifiant = re.sub("_prose", '', identifiant)
            if re.search("_vers$", identifiant):
                identifiant = re.sub("_vers", '', identifiant)
            if re.search("_tradFR$", identifiant):
                identifiant = re.sub("_tradFR", '', identifiant)
            xpath = "./" + ns + "text/" + ns + "body/" + ns + "listObject/" + ns + "object/[@{http://www.w3.org/XML/1998/namespace}id ='" + identifiant + "']"
            for biblio_oeuvre in root_corpus.findall(xpath):
                language = biblio_oeuvre.attrib['{http://www.w3.org/XML/1998/namespace}lang']
                if language == 'oFr':
                    liste_xml.remove(xml)

        #os.system('xsltproc src/xml2text_tracer.xsl ' + traitement.dossier_source + '/' + xml + ' > txt/' + nom_fichier + '.txt')

    if "trad_reecrit" in traitement.type_traitement:
        XML_reecrit = []
        XML_trad = []
        identifiant_traductions = 1
        identifiant_reecritures = 2
        base = "src/Corpus_BD.xml"
        tree_corpus = ET.parse(base)
        root_corpus = tree_corpus.getroot()
        ns = '{http://www.tei-c.org/ns/1.0}'
        for xml in liste_xml:
            identifiant = xml[:-4]
            if re.search("_prose$", identifiant):
                identifiant = re.sub("_prose", '', identifiant)
            if re.search("_vers$", identifiant):
                identifiant = re.sub("_vers", '', identifiant)
            if re.search("_tradFR$", identifiant):
                identifiant = re.sub("_tradFR", '', identifiant)
            xpath = "./" + ns + "text/" + ns + "body/" + ns + "listObject/" + ns + "object/[@{http://www.w3.org/XML/1998/namespace}id ='" + identifiant + "']"
            for biblio_oeuvre in root_corpus.findall(xpath):
                sous_corpus = biblio_oeuvre.attrib['type']
                if sous_corpus == 'traduction':
                    XML_trad.append(xml)
                else:
                    XML_reecrit.append(xml)
        for traduction in XML_trad:
            os.system("java -jar src/saxon9he.jar -xsl:src/xml2text_tracer.xsl -s:"
                      + traitement.dossier_source + '/' + traduction + ' -o:txt/' + traduction[:-4] + '.txt')
            corpus += identification_phrases(traduction, identifiant_traductions)


        for reecriture in XML_reecrit:
            os.system("java -jar src/saxon9he.jar -xsl:src/xml2text_tracer.xsl -s:"
                      + traitement.dossier_source + '/' + reecriture + ' -o:txt/' + reecriture[:-4] + '.txt')
            corpus += identification_phrases(reecriture, identifiant_reecritures)
    elif "reecrit" in traitement.type_traitement:
        XML_reecrit = []
        base = "src/Corpus_BD.xml"
        tree_corpus = ET.parse(base)
        root_corpus = tree_corpus.getroot()
        ns = '{http://www.tei-c.org/ns/1.0}'
        for xml in liste_xml:
            identifiant = xml[:-4]
            if re.search("_prose$", identifiant):
                identifiant = re.sub("_prose", '', identifiant)
            if re.search("_vers$", identifiant):
                identifiant = re.sub("_vers", '', identifiant)
            if re.search("_tradFR$", identifiant):
                identifiant = re.sub("_tradFR", '', identifiant)
            xpath = "./" + ns + "text/" + ns + "body/" + ns + "listObject/" + ns + "object/[@{http://www.w3.org/XML/1998/namespace}id ='" + identifiant + "']"
            for biblio_oeuvre in root_corpus.findall(xpath):
                sous_corpus = biblio_oeuvre.attrib['type']
                if sous_corpus != 'traduction':
                    XML_reecrit.append(xml)
        identifiant_oeuvre = 0
        for reecriture in XML_reecrit:
            identifiant_oeuvre += 1
            os.system("java -jar src/saxon9he.jar -xsl:src/xml2text_tracer.xsl -s:"
                      + traitement.dossier_source + '/' + reecriture + ' -o:txt/' + reecriture[:-4] + '.txt')
            corpus += identification_phrases(reecriture, identifiant_oeuvre)
    elif "trad" in traitement.type_traitement:
        XML_trad = []
        base = "src/Corpus_BD.xml"
        tree_corpus = ET.parse(base)
        root_corpus = tree_corpus.getroot()
        ns = '{http://www.tei-c.org/ns/1.0}'
        for xml in liste_xml:
            identifiant = xml[:-4]
            if re.search("_prose$", identifiant):
                identifiant = re.sub("_prose", '', identifiant)
            if re.search("_vers$", identifiant):
                identifiant = re.sub("_vers", '', identifiant)
            if re.search("_tradFR$", identifiant):
                identifiant = re.sub("_tradFR", '', identifiant)
            xpath = "./" + ns + "text/" + ns + "body/" + ns + "listObject/" + ns + "object/[@{http://www.w3.org/XML/1998/namespace}id ='" + identifiant + "']"
            for biblio_oeuvre in root_corpus.findall(xpath):
                sous_corpus = biblio_oeuvre.attrib['type']
                if sous_corpus == 'traduction':
                    XML_trad.append(xml)

        identifiant_oeuvre = 0
        for traduction in XML_trad:
            identifiant_oeuvre += 1
            os.system("java -jar src/saxon9he.jar -xsl:src/xml2text_tracer.xsl -s:"
                      + traitement.dossier_source + '/' + traduction + ' -o:txt/' + traduction[:-4] + '.txt')
            corpus += identification_phrases(traduction, identifiant_oeuvre)


    else:
        identifiant_oeuvre = 1
        for oeuvre in liste_xml:
            print (identifiant_oeuvre, oeuvre)
            os.system("java -jar src/saxon9he.jar -xsl:src/xml2text_tracer.xsl -s:"
                      + traitement.dossier_source + '/' + oeuvre + ' -o:txt/' + oeuvre[:-4] + '.txt')
            corpus += identification_phrases(oeuvre, identifiant_oeuvre)
            identifiant_oeuvre += 1

    chemin_projet_tracer = traitement.chemin_projet
    if not os.path.exists(chemin_projet_tracer+traitement.nom_traitement):
        os.makedirs(chemin_projet_tracer + traitement.nom_traitement)

    fichier_corpus = open(chemin_projet_tracer + traitement.nom_traitement + '/corpus.txt', 'w')
    fichier_corpus.write(corpus)
    fichier_corpus.close()

    lemmatiser = input('Lemmatiser ? (O/N)')
    if lemmatiser == 'O':
        phrases = re.findall(r"[1-9]\t(.+?)\tNULL", corpus)
        texte = ''
        for phrase in phrases:
            texte += phrase + ' '
        liste_lemmes = traitementsTal.lemmatisation(texte, "dictionnaire")

        fichier_lemmes = open(chemin_projet_tracer + traitement.nom_traitement + '/lemmes.lemma', 'w')
        for ligne in liste_lemmes.values():
            fichier_lemmes.write(ligne[0]+'\t'+ligne[1]+'\t'+ligne[2]+'\n')
        fichier_lemmes.close()

    #shutil.rmtree('txt/')

    initialisation_tracer(traitement, racine)


"""
Calcul et ajout des identifiants pour chaque partie du corpus (peu importe la configuration
de partage.
___________________________Étapes_______________________
1. Ouvre le fichier texte pour chaque oeuvre traité et le segmente en phrases
2. Pour chaque phrase, l'identifiant est calculé et la ligne conforme à la demande
de Tracer est ajoutée au corpus
"""


def identification_phrases(oeuvre, identifiant):
    identifiant_texte = identifiant
    nom_fichier = oeuvre[:-4]
    phrases_texte = {}
    #fichier_correspondant = open('txt/' + nom_fichier + '.txt', 'r')
    with open("txt/"+nom_fichier+".txt", "r", encoding='utf8') as f_texte:
        phrases = csv.reader(f_texte, delimiter='\t')
        for ligne in phrases:
            phrases_texte[ligne[0]] = ligne[1]
    f_texte.close()
    tableur_oeuvre = ''

    for identifiant_phrase, phrase in phrases_texte.items():
        print(identifiant_phrase)
        idenfifiant_corpus = identifiant_texte *100000 + int(identifiant_phrase)
        if len(str(idenfifiant_corpus)) == 6:
            idenfifiant_corpus = "0" + str(idenfifiant_corpus)
        else:
            idenfifiant_corpus = str(idenfifiant_corpus)
        phrase = re.sub('\n', ' ', phrase)
        ligne = idenfifiant_corpus + '\t' + phrase + '\tNULL\t' + nom_fichier + '\n'
        tableur_oeuvre += ligne

    return tableur_oeuvre


"""
Initisalise le traitement avec Tracer selon les paramètres renseignés dans l'initisalisation
___________________________Étapes_______________________
1. Ouvre le fichier de configuration pour la modification (ne pas oublier qu'il faut
changer le nom du dossier traité" --> réfléchir si automatiser, en fonction de la 
fréquence des changements de paramètres (lignes 17 et 18)
2. Attend la confirmation de la modification des configurations (O/N)
3. Fait appel à la function journal_traitements dans traitementsSystem pour ajouter
une information de la nature du traitement et de la date
4. Va dans le dossier de Tracer et lance le traitement
5. Recherche le chemin du fichier avec les scores à l'aide d'une fonction find
dans traitementsSystem et copie le fichier scores dans le même dossier que le fichier
du corpus (dossier du projet en cours)
6. Lance la commande Tracer pour obtenir le fichier tabulé avec les résultats
7. Ouvre le fichier
"""


def initialisation_tracer(traitement, racine):
    os.chdir(racine)
    nom_projet = traitement.nom_traitement

    config = traitement.fichier_config
    os.system("gedit "+config+" &")

    poursuivre = input("prête ? (O/N)")
    if poursuivre == "O":

        print(traitementsSystem.journal_traitements(traitement, racine, fichier ='traitements_tracer.txt', resultats = 'corpus-corpus.score.expanded'))
        os.chdir(traitement.dossier_logiciel)
        print (os.system('java -Xmx600m -Deu.etrap.medusa.config.ClassConfig=conf/tracer_config.xml -jar tracer.jar'))

        chemin_score = traitementsSystem.find('corpus-corpus.score', 'data/corpora/'+nom_projet, racine+'/'+traitement.dossier_logiciel)
        print ("chemin = ", chemin_score)
        os.system("cp "+chemin_score+' data/corpora/' + nom_projet + '/corpus-corpus.score')

        print(os.system('java -cp tracer.jar eu.etrap.tracer.postprocessing.DefaultOutputterMain data/corpora/' + nom_projet + '/corpus.txt  data/corpora/' + nom_projet + '/corpus-corpus.score'))

        os.system("gedit data/corpora/" + nom_projet + "/corpus-corpus.score.expanded &" )
        os.chdir(racine)

