import os
import shutil
import re
import traitementsSystem
import traitementsTal

__auteur__ = "Karolina Suchecka"
__date__ = "19/12/19"
"""
Script qui initialise le traitement TextPAIR selon les paramètres indiqués dans l'initialisation
___Étapes___
1. On demande à l'utilisateur s'il a besoin d'une liste des lemmes. Si la réponse est "O", on lemmatise (pour ce faire,
il faut extraire les docs en format texte avec Odette, mais on supprime tous les sorties txt aussitôt). Le fichier avec
les lemmes est automatiquement mis dans le dossier du logiciel
2. On demande à l'utilisateur s'il veut changer les configurations. Le cas échéant, le fichier config s'affiche. Le 
script ne reprendra pas tant que l'utilisateur ne confirme pas d'avoir fini les modifications
3. On ajoute le traitement au journal et on lance textPAIR
4. On renomme le fichier des résultats en tab pour le traitement avec Galaxies
5. On demande à l'utilisateur s'il veut ouvrir Galaxies. Si "O", le logiciel s'ouvre.
"""

def initialisation_text_pair (traitement, racine):
    os.chdir(racine)
    nom_projet = traitement.nom_traitement

    lemmatisation = input('Lemmatiser ? (O/N) ')
    if lemmatisation == 'O':
        liste_xml = os.listdir(traitement.dossier_source)
        if not os.path.exists("txt"):
            os.makedirs("txt")
        for xml in liste_xml:
            nom_fichier = xml[:-4]
            os.system('xsltproc src/xml2text_etape1.xsl ' + traitement.dossier_source + '/'
                      + xml + ' > txt/' + nom_fichier + '.txt')
            os.system('cat txt/*.txt > total.txt')
            fichier_corpus = open('total.txt', 'r')
            texte_corpus = fichier_corpus.read()
            texte_corpus = re.sub(r"\.\S", r". ", texte_corpus)
            liste_lemmes = traitementsTal.lemmatisation(texte_corpus, "dictionnaire")
            fichier_lemmes = open(traitement.dossier_logiciel + '/lemmes.txt', 'w')
            for ligne in liste_lemmes.values():
                fichier_lemmes.write(ligne[1] + '\t' + ligne[0] + '\n')
            fichier_lemmes.close()
        shutil.rmtree('txt/')
        os.remove('total.txt')

    changement_configuration = input('Éditer les configurations ? (O/N) ')
    if changement_configuration == 'O':
        config = traitement.fichier_config
        os.system("gedit " + config + " &")
        poursuivre = input("prête ? (O/N) ")
    else:
        poursuivre = "O"

    if poursuivre == 'O':
        print(traitementsSystem.journal_traitements(traitement, racine, fichier='traitements_textpair.txt',
                                                    resultats='alignments.tab'))
        os.chdir(traitement.dossier_logiciel)
        print(os.system('textpair --source_files=' + racine + '/' + traitement.dossier_source + '/ --target_files='
                        + racine + '/' + traitement.dossier_target + ' --config=config.ini --workers=8 --output_path=results/'
                        + traitement.nom_traitement))
        os.rename('results/'+nom_projet+'/results/alignments.jsonl','results/'+nom_projet+'/results/alignments.tab')
        galaxies = input('Ouvrir Galaxies ? (O/N) ')
        if galaxies == 'O':
            os.chdir(racine+'/'+traitement.chemin_galaxies)
            os.system('python3 InterfaceGalaxies.py')
