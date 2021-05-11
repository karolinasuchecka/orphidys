import traitementsTal
import xmlisationResultats
import traitementsSystem
import extractionChunks
import csv
import codecs
import json
import re
import os
import time
from nltk.tokenize import sent_tokenize

__auteur__ = "Karolina Suchecka"
__date__ = "06/11/19"
"""
Script qui initialise le post-traitement des résultats de TextPAIR, Tracer ou Galaxies. Les différents modes d'ouverture, selon le type
des fichiers sont appliqués. Renvoie ensuite vers le script xmlisationResultats pour revenir vers le format XML et obtenir à la fin
un fichier xmlisé enrichi qui rend compte des relations détectés par les logiciels.
"""

"""
Selon le type du fichier (csv pour Tracer, json pour TextPair et Galaxies), initialisation du traitement adapté.
_____________________________Étapes :__________________________________________
1. Création d'un dictionnaire avec le corpus (clé : identifiant, valeur : phrase)
2. Ouverture du fichier avec les résultats
3. Pour TextPAIR et Galaxies, lancement de la recherche des identifiants pour partager les extraits en phrases, extraction des métadonnées
4. Lancement de l'xmlisation des phrases, puis des textes (xmlisationResultats.xmlisation_phrases, xmlisation_textes)
5. Enregistrement du fichier XML
_____________________________Remarques :__________________________________________
Il faudrait trouver comment exploiter les phrases non attribuées de TextPAIR et Galaxies (probablement notes et titres,
mais peuvent s'avérer utilises (stockés déjà dans le traitement) 
"""

dictionnaire_corpus = {}
# clé : id_texte, valeurs : ids_phrases
id_textes = {}


def ouverture_fichiers(traitement, racine):
    tps1 = time.process_time()
    # ouverture du fichier de corpus ([0] : identifiant_phrase, [1] : phrase, [3] : identifiant_texte
    with open(traitement.fichier_corpus, newline='') as fichier_corpus:
        fichier_corpus = csv.reader(fichier_corpus, delimiter='\t')
        for ligne_corpus in fichier_corpus:
            dictionnaire_corpus[ligne_corpus[0]] = ligne_corpus[1]
            if ligne_corpus[3] not in id_textes.keys():
                id_textes[ligne_corpus[3]] = []
            id_textes[ligne_corpus[3]].append(ligne_corpus[0])

    dictionnaire_resultats = {}
    document_xml = ""

    # traitement pour "alignements.tab" de TextPAIR
    if traitement.type_traitement == 'Textpair':
        liens_source = {}
        liens_target = {}
        phrases_non_attrib_source = {}
        phrases_non_attrib_target = {}
        auteurs_ID_passage = {}
        nombre_lignes = 0
        phrases_segs = {}
        for ligne_resultats in codecs.open(traitement.fichier_source, 'r', 'utf-8', errors="ignore"):
            nombre_lignes += 1
            ligne_resultats = json.loads(ligne_resultats.rstrip())

            # print(nombre_lignes)
            print(ligne_resultats)
            # on prend en compte le contexte aussi
            texte_source = ligne_resultats['source_context_before'] + ' ' + ligne_resultats['source_passage'] + ' ' + \
                           ligne_resultats['source_context_after']
            texte_target = ligne_resultats['target_context_before'] + ' ' + ligne_resultats['target_passage'] + ' ' + \
                           ligne_resultats['target_context_after']
            auteur_source = ligne_resultats['source_structure']
            # on conserve les identifiants des couples retrouvés pour regrouper plusieurs phrases d'une correspondance

            id_passage = ligne_resultats['passage_id']
            if auteur_source not in auteurs_ID_passage.keys():
                auteurs_ID_passage[auteur_source] = []
            id_phrases_source = trouve_phrases(texte_source, auteur_source)

            if len(id_phrases_source) > 0:
                auteur_target = ligne_resultats['target_structure']
                if auteur_target not in auteurs_ID_passage.keys():
                    auteurs_ID_passage[auteur_target] = []
                id_phrases_target = trouve_phrases(texte_target, auteur_target)
                if len(id_phrases_target) > 0:
                    for id_ph_s in id_phrases_source:
                        dictionnaire_resultats[str(id_ph_s)] = dictionnaire_corpus[str(id_ph_s)]
                    for id_ph_t in id_phrases_target:
                        dictionnaire_resultats[str(id_ph_t)] = dictionnaire_corpus[str(id_ph_t)]

                    liens_source[id_passage] = id_phrases_source
                    liens_target[id_passage] = id_phrases_target
                    auteurs_ID_passage[auteur_source].append(id_passage)
                    auteurs_ID_passage[auteur_target].append(id_passage)
        # for identifiant, texte in dictionnaire_resultats.items():
            # print(identifiant, '\t', texte, '\n')

        # xmlisation des resultats
        phrases_xmlises = xmlisationResultats.xmlisation_phrases(dictionnaire_resultats, min_mots=4)
        document_xml = xmlisationResultats.xmlisation_textes(id_textes, phrases_xmlises, liens_source, liens_target,
                                                             auteurs_ID_passage)

    # Traitement pour Tracer (fichier corpus-corpus.score.expanded), le moins problématique : les ids sont déjà là
    elif traitement.type_traitement == 'Tracer':
        liens = {}
        with open(traitement.fichier_source, newline='') as fichier_resultats:
            fichier_resultats = csv.reader(fichier_resultats, delimiter='\t')
            for ligne_resultats in fichier_resultats:
                id_phrase_source = ligne_resultats[0]
                if len(id_phrase_source) == 6:
                    id_phrase_source = "0" + str(id_phrase_source)
                id_phrase_target = ligne_resultats[1]
                texte_phrase_source = ligne_resultats[4]
                if len(id_phrase_target) == 6:
                    id_phrase_target = "0" + str(id_phrase_target)

                texte_phrase_target = ligne_resultats[5]
                if id_phrase_source[:2] != id_phrase_target[:2]:
                    if id_phrase_source not in dictionnaire_resultats.keys():
                        dictionnaire_resultats[id_phrase_source] = dictionnaire_corpus[id_phrase_source]
                    if id_phrase_target not in dictionnaire_resultats.keys():
                        dictionnaire_resultats[id_phrase_target] = dictionnaire_corpus[id_phrase_target]
                    if id_phrase_source not in liens.keys():
                        liens[id_phrase_source] = []
                    liens[id_phrase_source].append(id_phrase_target)
                    if id_phrase_target not in liens.keys():
                        liens[id_phrase_target] = []
                    liens[id_phrase_target].append(id_phrase_source)

        # print (dicoResultats)
        for source, targets in liens.items():
            liens[source] = set(targets)

        phrases_xmlises = xmlisationResultats.xmlisation_phrases(dictionnaire_resultats, min_mots=4)
        document_xml = xmlisationResultats.xmlisation_textes(id_textes, phrases_xmlises, liens, '', '')

    # Traitement pour Galaxies (fichier json), proche de celui de textPAIR, sauf qu'on n'a pas des ids des auteurs
    # elif traitement.type_traitement == 'Galaxies':
    #     liens_source = {}
    #     liens_target = {}
    #     auteurs_ID_passage = {}
    #     phrases_non_attrib_source = {}
    #     phrases_non_attrib_target = {}
    #     with open(traitement.fichier_source) as fichier_resultats:
    #         fichier_resultats = json.load(fichier_resultats)
    #         dictionnaire_textes = {}
    #         i = 0
    #         while i < len(fichier_resultats['elements']['nodes']):
    #             texte = fichier_resultats['elements']['nodes'][i]['data']['texte']
    #             id = fichier_resultats['elements']['nodes'][i]['data']['id']
    #             if id not in dictionnaire_textes.keys():
    #                 dictionnaire_textes[id] = texte
    #             i += 1
    #
    #         for edge in fichier_resultats['elements']['edges']:
    #
    #             ids_phrases_source = []
    #             ids_phrases_target = []
    #
    #             id_phrase_source = edge['data']['source']
    #             id_phrase_target = edge['data']['target']
    #             id_passage = id_phrase_source + id_phrase_target
    #
    #             texte_source = dictionnaire_textes[id_phrase_source]
    #             texte_target = dictionnaire_textes[id_phrase_target]
    #
    #             sentences_source = sent_tokenize(texte_source, 'french')
    #             for sentence_source in sentences_source:
    #                 id_phrase_source, phrase_source, auteur_source = trouve_phrases(sentences_source,
    #                                                                                 sentences_source.index(
    #                                                                                     sentence_source), '')
    #                 if id_phrase_source != 'none':
    #                     dictionnaire_resultats[id_phrase_source] = phrase_source
    #                     ids_phrases_source.append(id_phrase_source)
    #                     auteurs_ID_passage[auteur_source].append(id_passage)
    #                 else:
    #                     if id_passage not in phrases_non_attrib_source.keys():
    #                         phrases_non_attrib_source[id_passage] = []
    #                     phrases_non_attrib_source[id_passage].append(sentence_source)
    #             liens_source[id_passage] = ids_phrases_source
    #
    #             sentences_target = sent_tokenize(texte_target, 'french')
    #             for sentence_target in sentences_target:
    #                 id_phrase_target, phrase_target, auteur_target = trouve_phrases(sentences_target,
    #                                                                                 sentences_target.index(
    #                                                                                     sentence_target),
    #                                                                                 '')
    #                 if id_phrase_target != 'none':
    #                     dictionnaire_resultats[id_phrase_target] = phrase_target
    #                     ids_phrases_target.append(id_phrase_target)
    #                     auteurs_ID_passage[auteur_target].append(id_passage)
    #                     auteurs_ID_passage[auteur_target].append(id_passage)
    #                 else:
    #                     if id_passage not in phrases_non_attrib_target.keys():
    #                         phrases_non_attrib_target[id_passage] = []
    #                     phrases_non_attrib_target[id_passage].append(sentence_target)
    #             liens_target[id_passage] = ids_phrases_target

        #phrases_xmlises = xmlisationResultats.xmlisation_phrases(dictionnaire_resultats, min_mots=4)
        #document_xml = xmlisationResultats.xmlisation_textes(id_textes, phrases_xmlises, liens_source, liens_target,
                                                             #auteurs_ID_passage)

    # enregistrement des résultats à l'emplacement indiqué lors de l'initiation et ajout d'une note au journal
    if not os.path.exists(traitement.dossier_target):
        os.makedirs(traitement.dossier_target)
    os.chdir(racine + '/' + traitement.dossier_target)
    fichier_resultats = open("resultats.xml", "w")
    fichier_resultats.write(document_xml)
    traitementsSystem.journal_traitements(traitement, racine, "post-processing.txt", "resultats.xml")
    fichier_resultats.close()
    #chunking
    extractionChunks.extraction_chunks("resultats.xml", traitement.dossier_target, racine)
    tps2 = time.process_time()
    print('###########Temps du traitement')
    print(round((tps2 - tps1) / 60, 2))


"""
Pour les traitements textPAIR et Galaxies, cherche les correspondances dans le fichier corpus.txt pour découper les
résultats en phrases et leur attribuer un ID commun
__________________Étapes__________________________
1. Si la phrase est déjà dans la liste des phrases non-trouvés, on la retourne tout de suite
2. Si elle est déjà dans le dico des phrases trouvés, on s'assure qu'elle correspond bien à la phrase de notre auteur,
si c'est le cas, on retourne l'id et la phrase
3. Sinon, on cherche les correspondances dans le corpus. Trois possibilités de correspondance : (i) équivalence à 100%,
(ii) équivalence après le lissage des accents, nettoyage des signes bruyants et uniformisation en minuscules,
(iii) équivalence au niveau des lemmes
4. Si le tableau ne contient qu'une phrase ou si c'est la dernière phrase qui est en cours, on retourne les résultats,
sinon on s'assure que la correspondance marche aussi sur la phrase suivante pour confirmer la validité de la corresp.  
"""

dictionnaire_phrases_trouvees = {}
liste_phrases_non_trouvees = []


def trouve_phrases(texte, auteur):
    # print(auteur)
    phrases_auteur = id_textes[auteur]
    phrases_corresp = []
    # indice_buts_manquants = 0
    # print(texte)
    texte = texte.lower()
    texte = re.sub(r"\s+", r" ", texte)
    texte = re.sub(r"\t+", r" ", texte)
    texte = re.sub(r"\n+", r" ", texte)
    texte = re.sub(r"’ ", r"’", texte)
    texte = re.sub(r" ’", r"’", texte)
    texte = re.sub(r" -", "-", texte)
    texte = re.sub(r" ,", ",", texte)
    texte = re.sub(r" …", "…", texte)
    # print(texte)
    texte_sans_appariements = texte
    for phrase_auteur in phrases_auteur:
        phrase = dictionnaire_corpus[phrase_auteur].lower()
        phrase = re.sub(r"[\u00a0\xa0]", r" ", phrase)
        # if phrase in texte:
        #    #print(dictionnaire_corpus[phrase_auteur].lower())
        #    phrases_corresp.append(phrase_auteur)
        #    texte_sans_appariements = re.sub(re.escape(phrase), "", texte_sans_appariements)

    #print(texte_sans_appariements)
    bouts_phrases = re.split("[\.\?\!:\]…»] ?»?\)?", texte_sans_appariements)
    print(bouts_phrases)

    doutes = []
    for bout_phrase in bouts_phrases:
        print(bout_phrase)
        candidats_corresp = []
        if bout_phrase != '' and bout_phrase != ' ':
            bout_phrase = re.sub(r"\s+", r" ", bout_phrase)
            bout_phrase = re.sub(r"\t+", r" ", bout_phrase)
            bout_phrase = re.sub(r"\n+", r" ", bout_phrase)
            bout_phrase = re.sub("^\s", "", bout_phrase)
            bout_phrase = re.sub("\s$", "", bout_phrase)
            for phrase_auteur in phrases_auteur:
                phrase = dictionnaire_corpus[phrase_auteur].lower()
                phrase = re.sub(r"[\u00a0\xa0]", r" ", phrase)
                if bout_phrase in phrase:
                    candidats_corresp.append(phrase_auteur)
                    #print(dictionnaire_corpus[phrase_auteur].lower())
        #print(candidats_corresp)
        if len(candidats_corresp) == 1:
            phrases_corresp.append(candidats_corresp[0])
            if len(doutes) > 0:
                difference_min = int(candidats_corresp[0])
                doute_retenu = ''
                for doute in doutes:
                    if abs(int(doute)-int(candidats_corresp[0])) < difference_min:
                        difference_min = abs(int(doute)-int(candidats_corresp[0]))
                        doute_retenu = doute
                print("Et le gagnant est"+doute_retenu)
                phrases_corresp.append(doute_retenu)
                doutes = []

        elif len(candidats_corresp) == 0 and bout_phrase != "" and bout_phrase != " ":
            print("phrase non trouvé", )
            print(bout_phrase)
            exit()
            indice_buts_manquants = 1
        elif len(candidats_corresp) > 1:
            if len(phrases_corresp) > 0:
                repere = phrases_corresp[0]
                difference = int(repere)
                candidat_retenu = ''
                for candidat in candidats_corresp:
                    if abs(int(candidat)-int(repere)) < difference:
                        difference = abs(int(candidat)-int(repere))
                        candidat_retenu = candidat
                print(candidat_retenu, difference)
                phrases_corresp.append(candidat_retenu)
                if len(doutes) > 0:
                    difference_min = int(candidat_retenu)
                    doute_retenu = ''
                    for doute in doutes:
                        if abs(int(doute) - int(candidat_retenu)) < difference_min:
                            difference_min = abs(int(doute) - int(candidat_retenu))
                            doute_retenu = doute
                    print("Et le gagnant est" + doute_retenu)
                    phrases_corresp.append(doute_retenu)
                    doutes = []

            else:
                print("OUPSI OUPSI DOUPS")
                print(candidats_corresp)
                print (texte)
                print (bout_phrase)
                for c_c in candidats_corresp:
                    doutes.append(c_c)
                #exit()





    if len(doutes) > 0:
        print("Doutes restent !")
        print(doutes)
        print(phrases_corresp)
        if len(phrases_corresp) > 0:
            for doute in doutes:
                if doute in phrases_corresp:
                    doutes.remove(doute)
            exit()
        else:
            phrases_corresp = doutes
            print("####Candidats faits des doutes !!!!####")

    phrases_corresp = list(set(phrases_corresp))
    if len(phrases_corresp) > 0:
        phrases_corresp = remplissage_trous(phrases_corresp)
    print(phrases_corresp)
    return(phrases_corresp)

def remplissage_trous(liste_phrases):
    """On sort la liste"""
    liste_phrases = sorted([int(x) for x in liste_phrases])
    nouvelle_liste = []
    i = 1
    while i < len(liste_phrases):
        if liste_phrases[i] - liste_phrases[i-1] > 1:
            j = liste_phrases[i] - liste_phrases[i-1]
            while j > 1:
                bouche_trou = liste_phrases[i] - j
                j = j-1
                if len(str(bouche_trou)) < 7:
                    bouche_trou = "0"+str(bouche_trou)
                    nouvelle_liste.append(bouche_trou)
                else:
                    nouvelle_liste.append(str(bouche_trou))
        else:
            if len(str(liste_phrases[i])) < 7:
                phrase_str = "0" + str(liste_phrases[i])
                nouvelle_liste.append(phrase_str)
            else:
                nouvelle_liste.append(str(liste_phrases[i]))
        i += 1
    print("VOICI")
    print(nouvelle_liste)
    return nouvelle_liste



    # if tableau[rang] in liste_phrases_non_trouvees:
    #     if auteur != "":
    #         return ("none", "none")
    #     else:
    #         return ("none", "none", auteur)
    #
    # if auteur != '':
    #     liste_propos = id_textes[auteur]
    # else:
    #     liste_propos = dictionnaire_corpus.keys()
    #
    # if tableau[rang] in dictionnaire_phrases_trouvees.keys() and dictionnaire_phrases_trouvees[tableau[rang]][
    #     0] in liste_propos:
    #     if auteur != "":
    #         return (dictionnaire_phrases_trouvees[tableau[rang]][0], dictionnaire_phrases_trouvees[tableau[rang]][1])
    #     else:
    #         auteur = trouve_auteur(dictionnaire_phrases_trouvees[tableau[rang]][0])
    #         return (
    #         dictionnaire_phrases_trouvees[tableau[rang]][0], dictionnaire_phrases_trouvees[tableau[rang]][1], auteur)
    #
    # elif len(tableau) > 1 and rang < len(tableau) - 1:
    #     for identifiant in liste_propos:
    #         proposition = dictionnaire_corpus[identifiant]
    #         if tableau[rang] in proposition:
    #             #print('corresp 100%')
    #             if tableau[rang + 1] in dictionnaire_phrases_trouvees.keys():
    #                 indice_suivante = 1
    #             else:
    #                 indice_suivante = trouve_phrase_suivante(tableau[rang + 1], identifiant)
    #             if indice_suivante == 1:
    #                 dictionnaire_phrases_trouvees[tableau[rang]] = [identifiant, proposition]
    #                 if auteur != "":
    #                     return identifiant, proposition
    #                 else:
    #                     auteur = trouve_auteur(identifiant)
    #                     return identifiant, proposition, auteur
    #         else:
    #             texte_tableau = traitementsTal.nettoyage_phrases(tableau[rang])
    #             # print('texteTableau -->'+texteTableau)
    #             texte_proposition = traitementsTal.nettoyage_phrases(proposition)
    #             # print('textePropo -->' + textePropo)
    #             if texte_tableau in texte_proposition:
    #                 if tableau[rang + 1] in dictionnaire_phrases_trouvees.keys() and \
    #                         dictionnaire_phrases_trouvees[tableau[rang + 1]][0] in liste_propos:
    #                     indice_suivante = 1
    #                 elif tableau[rang + 1] in liste_phrases_non_trouvees:
    #                     indice_suivante = 0
    #                 else:
    #                     indice_suivante = trouve_phrase_suivante(tableau[rang + 1], identifiant)
    #                 if indice_suivante == 1:
    #                     dictionnaire_phrases_trouvees[tableau[rang]] = [identifiant, proposition]
    #                     if auteur != "":
    #                         return identifiant, proposition
    #                     else:
    #                         auteur = trouve_auteur(identifiant)
    #                         return identifiant, proposition, auteur
    #
    #             else:
    #                 tokens_texte_tableau = traitementsTal.lemmatisation(texte_tableau, "fichier")
    #                 tokens_texte_proposition = traitementsTal.lemmatisation(texte_proposition, "fichier")
    #                 indice = 0
    #                 for token_tableau in tokens_texte_tableau.values():
    #                     if token_tableau in tokens_texte_proposition.values():
    #                         indice += 1
    #                 if indice > len(tokens_texte_tableau) * 0.7:
    #                     #print(str(indice) + '-->' + tableau[rang] + '-->' + proposition)
    #                     if tableau[rang + 1] in dictionnaire_phrases_trouvees.keys():
    #                         indice_suivante = 1
    #                     else:
    #                         indice_suivante = trouve_phrase_suivante(tableau[rang + 1], identifiant)
    #                     if indice_suivante == 1:
    #                         dictionnaire_phrases_trouvees[tableau[rang]] = [identifiant, proposition]
    #                         if auteur != "":
    #                             return identifiant, proposition
    #                         else:
    #                             auteur = trouve_auteur(identifiant)
    #                             return identifiant, proposition, auteur
    #
    #
    # elif len(tableau) == 1 or rang == len(tableau) - 1:
    #     for identifiant in liste_propos:
    #         proposition = dictionnaire_corpus[identifiant]
    #         if tableau[rang] in proposition:
    #             #print('corresp 100%')
    #             dictionnaire_phrases_trouvees[tableau[rang]] = [identifiant, proposition]
    #             if auteur != "":
    #                 return identifiant, proposition
    #             else:
    #                 auteur = trouve_auteur(identifiant)
    #                 return identifiant, proposition, auteur
    #         else:
    #             texte_tableau = traitementsTal.nettoyage_phrases(tableau[rang])
    #             texte_proposition = traitementsTal.nettoyage_phrases(proposition)
    #             if texte_tableau in texte_proposition:
    #                 #print('corresp nettoyage')
    #                 # print("ça marche : "+texteTableau +' --> '+textePropo)
    #                 dictionnaire_phrases_trouvees[tableau[rang]] = [identifiant, proposition]
    #                 if auteur != "":
    #                     return identifiant, proposition
    #                 else:
    #                     auteur = trouve_auteur(identifiant)
    #                     return identifiant, proposition, auteur
    #             else:
    #                 tokens_texte_tableau = traitementsTal.lemmatisation(texte_tableau, "fichier")
    #                 tokens_texte_proposition = traitementsTal.lemmatisation(texte_proposition, "fichier")
    #                 indice = 0
    #                 for token_tableau in tokens_texte_tableau:
    #                     if token_tableau in tokens_texte_proposition:
    #                         indice += 1
    #
    #                 if indice > len(tokens_texte_tableau) * 0.7:
    #                     print(str(indice) + '-->' + tableau[rang] + '-->' + proposition)
    #                     dictionnaire_phrases_trouvees[tableau[rang]] = [identifiant, proposition]
    #                     if auteur != "":
    #                         return identifiant, proposition
    #                     else:
    #                         auteur = trouve_auteur(identifiant)
    #                         return identifiant, proposition, auteur
    #
    # #print('décalé fin')
    # liste_phrases_non_trouvees.append(tableau[rang])
    # if auteur != "":
    #     return ("none", "none")
    # else:
    #     return ("none", "none", auteur)


"""
Fonction qui retrouve les correspondances de la même manière que la précédente, mais pour la phrase suivante.
Le retour est un boléen (1 s'il y a une correspondance, 0 s'il n'y en a pas). Il s'agit de s'assurer que la mise
en relation n'est pas fautive (deux étapes de validation : 1. La phrase appartient au texte indiqué à l'entrée
du traitement, 2. La phrase suivante des résultats correspond à la phrase suivante du corpus.
"""


def trouve_phrase_suivante(texte, id_precedent):
    id_suivant = str(int(id_precedent) + 1)
    if len(id_suivant) == 6:
        id_suivant = '0' + id_suivant
    if id_suivant in dictionnaire_corpus.keys():
        if texte in dictionnaire_corpus[id_suivant]:
            dictionnaire_phrases_trouvees[texte] = [id_suivant, dictionnaire_corpus[id_suivant]]
            return (1)
        else:
            texte_propre = traitementsTal.nettoyage_phrases(texte)
            texte_proposition = traitementsTal.nettoyage_phrases(dictionnaire_corpus[id_suivant])
            if texte_propre in texte_proposition:
                dictionnaire_phrases_trouvees[texte] = [id_suivant, dictionnaire_corpus[id_suivant]]
                return (1)
            else:
                tokens_texte_tableau = traitementsTal.lemmatisation(texte_propre, "fichier")
                tokens_texte_proposition = traitementsTal.lemmatisation(texte_proposition, "fichier")
                indice = 0
                for token_tableau in tokens_texte_tableau.values():
                    if token_tableau in tokens_texte_proposition.values():
                        indice += 1
                if indice > len(tokens_texte_tableau) * 0.7:
                    print(str(indice) + '-->' + texte + '-->' + dictionnaire_corpus[id_suivant])
                    dictionnaire_phrases_trouvees[texte] = [id_suivant, dictionnaire_corpus[id_suivant]]
                    return (1)
                else:
                    return (0)
    else:
        return (0)


"""
Fonction qui retrouve l'auteur d'une phrase du corpus (à partir de l'id de la phrase).
"""


def trouve_auteur(id_phrase):
    for auteur, phrases in id_textes.items():
        if id_phrase in phrases:
            return auteur
