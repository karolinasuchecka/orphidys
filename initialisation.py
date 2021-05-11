import os
import sys

sys.path.append('/home/karolina/PycharmProjects/these/codePropre/src')
print(sys.path)
import structurationCorpus
import preprocessingTracer
import preprocessingTextPair
import postprocessingResultats
import extractionChunks
import visualisationGenerale
import visualisationHTML
import traitementsTal
import traitementNomPropre
import xmlisationCorpus
import resultatsCompiles

__auteur__ = "Karolina Suchecka"
__date__ = "25/11/19"

""" CODE D'INITIALISATION
----
Fonctionnalité : 1. Définir si le traitement concerne TEXTPAIR, Tracer ou la structuration de corpus
2. Définit les fichiers à utiliser pour la suite de travail
3. Définit le dossier de sauvegarde des résultats
4. Permet de choisir la fonction à mettre en place pour la suite du traitement
---
Avancement actuel : 
1. Ajout de la class pour le traitement du corpus
2. Envoi automatique vers structurationCorpus.py
3. Ajoute de la classe Tracer et TextPair
4. Au lancement, l'utilisateur choisit quel traitement il veut affectuer
et l'initialisation envoie les demandes aux scripts correspondants.
"""


class Projet:
    def __init__(self):
        self.root = os.path.dirname(os.path.abspath(__file__))


class Corpus:
    def __init__(self):
        self.dossier_source = input("Insérez le chemin vers le dossier contenant le corpus en format ODT ")
        self.odette = "src/odette"
        self.base_textes = "src/Corpus_BD.xml"
        self.dossier_target = input("Insérez le chemin pour enregistrer le XML ")


class Tracer:
    def __init__(self):
        self.xslt_xml_text = "src/xml2text_tracer.xsl"
        self.dossier_source = input("Insérez le chemin vers le corpus XML ")
        self.dossier_logiciel = "src/tracer"
        self.nom_traitement = input("Comment souhaitez-vous appeler cette recherche avec Tracer ? ")
        self.fichier_config = "src/tracer/conf/tracer_config.xml"
        self.type_traitement = input("(trad_reecrit | tout | trad | reecrit) mod? ")
        self.chemin_projet = "src/tracer/data/corpora/"


class TextPair:
    def __init__(self):
        self.dossier_source = input("Insérez le chemin vers le corpus XML source ")
        self.dossier_target = input("Insérez le chemin vers le corpus XML target ")
        self.dossier_logiciel = "src/textpair"
        self.fichier_config = "src/textpair/config.ini"
        self.fichier_mots_ignores = "src/textpair/stopWords.txt"
        self.nom_traitement = input('Comment souhaitez-vous appeler cette recherche avec Textpair ? ')
        self.chemin_projet = "src/textpair/results/"
        self.chemin_galaxies = "src/galaxies/src"
        self.type_traitement = input("(trad reecrit | tout) mod?")


class PreparationCorpus:
    def __init__(self):
        self.fichier_corpus = 'src/corpus.txt'
        self.fichier_NAM = 'src/BD_NAM.xml'
        self.fichier_NOM = 'src/BD_NOM.xml'
        self.dossier_target = input("Comment souhaitez-vous appeler ce traitement ? ")


class PostProcessing:
    def __init__(self):
        self.type_traitement = "Textpair"  # input("Quel type de données ? (Tracer | Textpair | Galaxies) ")
        self.manipulations = "Tout"  # input("Quel type de traitement ? (Tout | Chunk) ")
        self.fichier_source = "src/textpair/results/0604_V5/results/alignments.tab"  # input("Indique le chemin vers le fichier source")
        self.dossier_target = "06-04_reecrit_textPAIR"  # input("Où enregistrer les résultats ? ")
        self.fichier_corpus = "src/corpus.txt"
        self.chemin_projet = ""


class Visualisation:
    def __init__(self):
        self.fichier_corpus = 'src/corpus.txt'
        self.resultats_post = '06-04_reecrit/resultat_final.xml'  # input("Indiquez le chemin du fichier avec les résultats xmlisés ")
        self.chemin_projet = '06-04_reecrit'
        self.base_textes = "src/Corpus_BD.xml"
        self.sources = "src/HTML_src"
        self.chemin_xml_compile = '06-04_reecrit/xml_pour_html'  # input('Où enregistrer les XML enrichis ? ')
        self.chemin_html = '06-04_reecrit/HTML'  # input("Où enregistrer les résultats ?")
        self.chemin_textes = "XML"
        self.seuil_chunks = 10
        self.seuil_phrases = 20
        self.action = input("Qu'est-ce qu'on fait ? 1-Tout, 2-Graphe général, 3-XML enrichi, 4-HTML 5-Compil ")
        self.manipulations = input("Quel type de traitement ? (Tout | Compil) ")


if __name__ == "__main__":
    projet = Projet()
    tache = input("Qu'est-ce qu'on fait ? Corpus | Tracer | Textpair | Post | Visu | NP ")
    if "Corpus" in tache:
        traitement = Corpus()
        # structurationCorpus.structuration_corpus(traitement, projet.root)
        structurationCorpus.ajout_tei_header(traitement, projet.root)
    if "Tracer" in tache:
        traitement = Tracer()
        preprocessingTracer.preprocessing(traitement, projet.root)
        traitementsTal.ajout_nouveaux_mots()
        # preprocessingTracer.initialisation_tracer(traitement, projet.root)
    if "Textpair" in tache:
        traitement = TextPair()
        preprocessingTextPair.initialisation_text_pair(traitement, projet.root)
        # pythotraitementsTal.ajout_nouveaux_mots()
    if "Post" in tache:
        traitement = PostProcessing()
        if traitement.manipulations == 'Tout':
            postprocessingResultats.ouverture_fichiers(traitement, projet.root)
        elif traitement.manipulations == 'Chunk':
            extractionChunks.extraction_chunks("resultats.xml", traitement.dossier_target, projet.root)
    if 'Visu' in tache:
        traitement = Visualisation()
        if "1" in traitement.action or '2' in traitement.action:
            visualisationGenerale.creation_graphe(traitement, projet.root)
        if '3' in traitement.action:
            visualisationHTML.generation_html(traitement, projet.root)
            traitementsTal.ajout_nouveaux_mots()
        if '4' in traitement.action:
            textes_a_traiter = os.listdir(traitement.chemin_xml_compile)
            for texte in textes_a_traiter:
                os.system("java -jar src/saxon9he.jar -xsl:src/alignementHTML.xsl -s:"
                          + traitement.chemin_xml_compile + '/' + texte + ' -o:' + traitement.chemin_html +
                          "/pages/" + texte.split('_resultats')[0] + '.html')
        if '5' in traitement.action:
            if traitement.manipulations == "Tout":
                resultatsCompiles.init(traitement, projet.root)
            elif traitement.manipulations == "Compil":
                resultatsCompiles.compilation_textpair(traitement, projet.root)
    if 'NP' in tache:
        traitement = PreparationCorpus()
        traitementNomPropre.init(traitement.fichier_corpus, traitement.fichier_NAM, traitement.fichier_NOM, projet.root)
        # xmlisationCorpus.init(traitement.fichier_corpus, projet.root)
        # traitementsTal.ajout_nouveaux_mots()
