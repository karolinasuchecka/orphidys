import os
import sys

sys.path.append('/home/karolina/PycharmProjects/these/codePropre/src')
print(sys.path)
import structurationCorpus
import preprocessingTracer
import preprocessingTextPair
import postprocessingResultats
import extractionChunks

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
        self.type_traitement = input("(trad reecrit | tout) mod? ")
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

class PostProcessing:
    def __init__(self):
        self.type_traitement = "Textpair" #input("Quel type de données ? (Tracer | Textpair | Galaxies) ")
        self.manipulations = input("Quel type de traitement ? (Tout | Chunk) ")
        self.fichier_source = "src/textpair/results/traductions_mod_29-12/results/alignments.tab" #input("Indique le chemin vers le fichier source")
        self.dossier_target = "post_trad_moderne_29-12" #input("Où enregistrer les résultats ? ")
        self.fichier_corpus = "src/corpus.txt"
        self.chemin_projet = ""


if __name__ == "__main__":
    projet = Projet()
    tache = input("Qu'est-ce qu'on fait ? Corpus | Tracer | Textpair | Post")
    if "Corpus" in tache:
        traitement = Corpus()
        #structurationCorpus.structuration_corpus(traitement, projet.root)
        structurationCorpus.ajout_tei_header(traitement, projet.root)
    if "Tracer" in tache:
        traitement = Tracer()
        preprocessingTracer.preprocessing(traitement, projet.root)
        #preprocessingTracer.initialisation_tracer(traitement, projet.root)
    if "Textpair" in tache:
        traitement = TextPair()
        preprocessingTextPair.initialisation_text_pair(traitement, projet.root)
    if "Post" in tache:
        traitement = PostProcessing()
        if traitement.manipulations == 'Tout':
            postprocessingResultats.ouverture_fichiers(traitement, projet.root)
        elif traitement.manipulations == 'Chunk':
            extractionChunks.extraction_chunks("resultats.xml", traitement.dossier_target, projet.root)








