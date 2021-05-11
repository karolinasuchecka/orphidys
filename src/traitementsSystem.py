import os
from datetime import date

__auteur__ = "Karolina Suchecka"
__date__ = "19/12/19"

"""
Les opérations sur le système et documentation du travail
"""

"""Fonction qui trouve l'emplacement d'un fichier"""
def find(name, path, location):
    os.chdir(location)
    for root, dirs, files in os.walk(path):
        if name in files:
            return os.path.join(root, name)

"""Fonction qui ajoute une ligne de documentation au journal du traitement demandé (textPAIR, Tracer, post, etc.)"""
def journal_traitements(traitement, racine, fichier, resultats):
    path = racine + '/doc/'
    journal = open(path+fichier, "a", encoding='utf-8')
    if traitement.chemin_projet != "":
        journal.write(str(date.today()) + '\t' + traitement.nom_traitement + '\t' + traitement.type_traitement + '\t' + racine + '/'
                  + traitement.chemin_projet +traitement.nom_traitement + '/' + resultats + '\n')
    else:
        journal.write(str(
            date.today()) + '\t' + traitement.type_traitement + '\t' + racine + '/'
                      + traitement.dossier_target + '/' + resultats + '\n')

    journal.close()
    return ('Ligne ajouté au journal')



