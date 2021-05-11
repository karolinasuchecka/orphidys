import xml.etree.ElementTree as ET
import traitementsTal
import xmlisationResultats
import extractionChunks
import re
import csv

def recherche_subordonne(mots, rang):
    i = rang
    indice_verbe = 0
    temps_verbaux = ['VER:cond', 'VER:futu', 'VER:impe', 'VER:impf', 'VER:pres', 'VER:simp', 'VER:subi', 'VER:subp']
    while i < len(mots):
        if mots[i].tag == 'w' and mots[i].attrib['pos'] in temps_verbaux:
            indice_verbe += 1
            if indice_verbe == 2:
                if mots[i-1].tag == 'w' and (mots[i-1].attrib['pos'] == 'PRO:PER' or mots[i-1].attrib['pos'] == 'NOM' or \
                mots[i-1].attrib['pos'] == 'NAM'):
                    return (i-2)
                else:
                    return (i-1)
        elif mots[i].tag == 'pc':
            return (i-1)

        i += 1
    #print (i, mots[i-2].text)
    return (i-2)



def recherche_groupes_nominaux(phrase,mots, dicoNOM):
    pos_ante_anteposes_nom = ('DET:ART', 'DET:POS', 'NUM', 'PRO:REL', "PRO:DEM")
    pos_anteposes_nom = (
    'DET:ART', 'DET:POS', 'ADJ', 'NUM', 'PRO:REL', 'PRO:PER', "PRO:DEM", "PRP:det", 'NOM')  # KON et PRP ?
    pos_postposes_nom = ('ADJ', 'VER:pper', 'NOM', 'PRP:det', 'PRP', 'DET:ART', 'NAM')
    pos_post_postposes_nom = ('ADJ', 'PRP', 'NOM', 'NAM', 'PRP:det')
    pos_anteposes_adj = (
    'DET:ART', 'DET:POS', 'ADJ', 'NUM', 'PRO:REL', 'PRO:PER', "PRO:DEM", "PRP:det")

    i = 0
    groupes_nominaux = {}
    types_groupes = {}
    while i < len(mots):
        if mots[i].tag == 'w' and mots[i].attrib['pos'] == 'NOM':
            id_groupe = mots[i].attrib['n']
            groupes_nominaux[id_groupe] = []
            for parent, graphies_nom in dicoNOM.items():
                if mots[i].text in graphies_nom or mots[i].attrib['lemma'] in graphies_nom:

                    types_groupes[id_groupe] =  ['NC', parent.attrib['{http://www.w3.org/XML/1998/namespace}id']]


            if id_groupe not in types_groupes.keys():
                types_groupes[id_groupe] = ['compl', '']

            if i - 1 >= 0 and mots[i - 1].tag == 'w' and mots[i - 1].attrib['pos'] in pos_anteposes_nom and \
                    mots[i - 1].attrib['pos'] != mots[i].attrib['pos']:
                if i - 2 >= 0 and mots[i - 2].tag == 'w' and (
                        mots[i - 2].attrib['pos'] in pos_ante_anteposes_nom or mots[-1].text
                        == 'des') and mots[i - 2].attrib['pos'] != mots[i - 1].attrib['pos']:
                    # print(mots[i - 2].text)
                    groupes_nominaux[id_groupe].append(int(mots[i - 2].attrib['n']))
                    groupes_nominaux[id_groupe].append(int(mots[i - 1].attrib['n']))
                elif i - 3 >= 0 and mots[i - 2].tag == 'pc' and mots[i - 3].tag == 'w' and mots[i - 3].attrib[
                    'pos'] == 'ADJ' and mots[i - 1].attrib['pos'] == 'ADJ':
                    groupes_nominaux[id_groupe].append(int(mots[i - 3].attrib['n']))
                    groupes_nominaux[id_groupe].append(int(mots[i - 1].attrib['n']))
                elif mots[i - 1].attrib['pos'] != 'PRP:det':
                    groupes_nominaux[id_groupe].append(int(mots[i - 1].attrib['n']))

            # print(mots[i].text)
            groupes_nominaux[id_groupe].append(int(mots[i].attrib['n']))

            if i + 1 < len(mots) and mots[i + 1].tag == 'w' and (mots[i + 1].attrib['pos'] in pos_postposes_nom or
                                                                 mots[i + 1].text == 'd\'' or mots[
                                                                     i + 1].text == 'de') \
                    and mots[i + 1].attrib['pos'] != mots[i].attrib['pos'] and mots[i + 1].attrib['lemma'] != 'ne':
                # print(mots[i + 1].text)
                groupes_nominaux[id_groupe].append(int(mots[i + 1].attrib['n']))
                if i + 2 < len(mots) and mots[i + 2].tag == 'w' and mots[i + 2].attrib[
                    'pos'] in pos_post_postposes_nom \
                        and mots[i + 2].attrib['pos'] != mots[i + 1].attrib['pos']:
                    # print(mots[i + 2].text)
                    groupes_nominaux[id_groupe].append(int(mots[i + 2].attrib['n']))
            elif i + 3 < len(mots) and mots[i + 1].tag == 'w' and ((
                    mots[i + 1].attrib['pos'] == 'DET:ART' or mots[i + 1].attrib['pos'] == 'KON') \
                    and mots[i + 2].tag == 'w' and mots[i + 2].attrib["pos"] == 'ADV' and mots[i + 3].tag == 'w' and \
                    (mots[i + 3].attrib["pos"] == 'ADJ' or mots[i + 3].attrib['pos'] == 'VER:pper') or mots[i+3].tag in pos_post_postposes_nom):
                groupes_nominaux[id_groupe].append(int(mots[i + 1].attrib['n']))
                groupes_nominaux[id_groupe].append(int(mots[i + 2].attrib['n']))
                groupes_nominaux[id_groupe].append(int(mots[i + 3].attrib['n']))
                if i + 4 < len(mots) and mots[i + 4].tag == 'w' and mots[i + 4].attrib['pos'] == 'PRP:det':
                    groupes_nominaux[id_groupe].append(int(mots[i + 4].attrib['n']))

            #print("#####", groupes_nominaux[id_groupe])
            #print("#####", types_groupes[id_groupe])

        elif mots[i].tag == "w" and (mots[i].attrib['pos'] == 'NAM' or (mots[i].attrib['pos'] == 'ADJ' and i - 1 >= 0
                                     and mots[i - 1].tag == 'w' and mots[i - 1].attrib['pos'] in pos_anteposes_adj
                                    and i+1 < len(mots) and mots[i+1].tag == 'w' and mots[i+1].attrib['pos'] != 'NOM'
                                                                        and mots[i+1].attrib['pos'] != 'NAM')):
            id_groupe = mots[i].attrib['n']
            groupes_nominaux[id_groupe] = []
            if mots[i].attrib['pos'] == 'NAM':
                types_groupes[id_groupe] = ['NP', mots[i].attrib['lemma']]
            else:
                types_groupes[id_groupe] = ['ADJ', mots[i].attrib['lemma']]
            if i - 1 >= 0 and mots[i - 1].tag == 'w' and mots[i - 1].attrib['pos'] in pos_anteposes_nom and \
                    mots[i - 1].attrib['pos'] != mots[i].attrib['pos']:
                if i - 2 >= 0 and mots[i - 2].tag == 'w' and (
                        mots[i - 2].attrib['pos'] in pos_ante_anteposes_nom or mots[-1].text
                        == 'des') and mots[i - 2].attrib['pos'] != mots[i - 1].attrib['pos']:
                    # print(mots[i - 2].text)
                    groupes_nominaux[id_groupe].append(int(mots[i - 2].attrib['n']))
                    groupes_nominaux[id_groupe].append(int(mots[i - 1].attrib['n']))
                elif i - 3 >= 0 and mots[i - 2].tag == 'pc' and mots[i - 3].tag == 'w' and mots[i - 3].attrib[
                    'pos'] == 'ADJ' and mots[i - 1].attrib['pos'] == 'ADJ':
                    groupes_nominaux[id_groupe].append(int(mots[i - 3].attrib['n']))
                    groupes_nominaux[id_groupe].append(int(mots[i - 1].attrib['n']))
                elif mots[i - 1].attrib['pos'] != 'PRP:det':
                    groupes_nominaux[id_groupe].append(int(mots[i - 1].attrib['n']))

            # print(mots[i].text)
            groupes_nominaux[id_groupe].append(int(mots[i].attrib['n']))
            if i + 1 < len(mots) and mots[i + 1].tag == 'w' and (mots[i + 1].attrib['pos'] in pos_postposes_nom or
                                                                 mots[i + 1].text == 'd\'' or mots[i + 1].text == 'de') \
                    and mots[i + 1].attrib['pos'] != mots[i].attrib['pos'] and mots[i + 1].attrib['lemma'] != 'ne':
                # print(mots[i + 1].text)
                groupes_nominaux[id_groupe].append(int(mots[i + 1].attrib['n']))
                if i + 2 < len(mots) and mots[i + 2].tag == 'w' and mots[i + 2].attrib['pos'] in pos_post_postposes_nom \
                        and mots[i + 2].attrib['pos'] != mots[i + 1].attrib['pos']:
                    # print(mots[i + 2].text)
                    groupes_nominaux[id_groupe].append(int(mots[i + 2].attrib['n']))
            elif i + 1 < len(mots) and mots[i + 1].tag == 'w' and (mots[i + 1].attrib['pos'] == 'PRO:REL' or
                mots[i + 1].attrib['lemma'] == 'que'):
                fin_subordonne = recherche_subordonne(mots, i + 2)
                j = i+1
                while j <= fin_subordonne:
                    #print(mots[j].text)
                    groupes_nominaux[id_groupe].append(int(mots[j].attrib['n']))
                    j += 1
            elif i + 2 < len(mots) and mots[i + 1].tag == "w" and mots[i + 2].tag == 'w' and mots[i + 1].attrib['pos'] == 'PRP' \
                    and mots[i + 2].attrib['pos'] == 'PRO:REL':
                fin_subordonne = recherche_subordonne(mots, i + 3)
                j = i+1
                while j <= fin_subordonne:
                    groupes_nominaux[id_groupe].append(int(mots[j].attrib['n']))
                    #print(mots[j].text)
                    j += 1

            elif i + 3 < len(mots) and mots[i + 1].tag == 'w' and (
                    mots[i + 1].attrib['pos'] == 'DET:ART' or mots[i + 1].attrib['pos'] == 'KON') \
                    and mots[i + 2].tag == 'w' and mots[i + 2].attrib["pos"] == 'ADV' and mots[i + 3].tag == 'w' and \
                    (mots[i + 3].attrib["pos"] == 'ADJ' or mots[i + 3].attrib['pos'] == 'VER:pper'):

                groupes_nominaux[id_groupe].append(int(mots[i + 1].attrib['n']))
                groupes_nominaux[id_groupe].append(int(mots[i + 2].attrib['n']))
                groupes_nominaux[id_groupe].append(int(mots[i + 3].attrib['n']))
                if i + 4 < len(mots) and mots[i + 4].tag == 'w' and mots[i + 4].attrib['pos'] == 'PRP:det':
                    groupes_nominaux[id_groupe].append(int(mots[i + 4].attrib['n']))

        elif mots[i].tag == 'w' and (mots[i].attrib['lemma'] == 'celui' or (i+1< len(mots) and mots[i+1].tag == "w" and
            mots[i].attrib["pos"] == "KON" and mots[i+1].attrib["pos"] == 'PRO:REL')):
            id_groupe = mots[i].attrib['n']
            groupes_nominaux[id_groupe] = []
            types_groupes[id_groupe] = ['SUB', 'celui']
            if i + 1 < len(mots) and mots[i + 1].tag == 'w' and (mots[i + 1].attrib['pos'] == 'PRO:REL' or
                mots[i + 1].attrib['lemma'] == 'que'):
                fin_subordonne = recherche_subordonne(mots, i+2)
                j = i
                while j <= fin_subordonne:
                    #print (mots[j].text)
                    groupes_nominaux[id_groupe].append(int(mots[j].attrib['n']))
                    j += 1
            elif mots[i+1].tag == "w" and mots[i+2].tag == 'w' and mots[i + 1].attrib['pos'] == 'PRP' \
                    and mots[i + 2].attrib['pos'] == 'PRO:REL':
                fin_subordonne = recherche_subordonne(mots, i+3)
                j = i
                while j <= fin_subordonne:
                    groupes_nominaux[id_groupe].append(int(mots[j].attrib['n']))
                    #print(mots[j].text)
                    j += 1
            else:
                groupes_nominaux[id_groupe].append(int(mots[i].attrib['n']))




        i += 1

    for nom, valeurs in groupes_nominaux.items():

        for noyau_syntagme, composants in groupes_nominaux.items():
            if nom != noyau_syntagme and len(valeurs) > 0 and len(composants) > 0:
                if nom in composants and nom < noyau_syntagme:
                    #print ("syntagme autour du mot " + phrase.find('w[@n=\''+nom+'\']').text + ' à fusionner avec celle du mot ' + phrase.find('w[@n=\''+noyau_syntagme+'\']').text)
                    for composant in composants:
                        if composant not in valeurs:
                            groupes_nominaux[nom].append(int(composant))
                else:
                    equivalence_composants = 0
                    for valeur in valeurs:
                        if valeur in composants and nom < noyau_syntagme:
                            equivalence_composants = 1
                    if equivalence_composants == 1:
                        for composant in composants:
                            if composant not in valeurs:
                                groupes_nominaux[nom].append(int(composant))
        groupes_nominaux[nom] = concatenation_groupes(nom, groupes_nominaux[nom], groupes_nominaux)
                #print (int(valeurs[len(valeurs)-1]), int(composants[0]))
                #if int(valeurs[len(valeurs)-1]) +1 == int(composants[0]):
                #    print ("oui --> ajout ", phrase.find('w[@n=\''+str(valeurs[len(valeurs)-1])+'\']').text, \
                #    phrase.find('w[@n=\''+str(composants[0])+'\']').text)
                #    for composant in valeurs:
                #        if composant not in groupes_nominaux[nom]:
                #            groupes_nominaux[nom].append(int(composant))

                #if phrase.find('*[@n=\''+str(valeurs[len(valeurs)-1])+'\']').tag == 'w' and \
                        #(phrase.find('w[@n=\''+str(valeurs[len(valeurs)-1])+'\']').attrib['pos'] == 'PRP:det' or
                        #phrase.find('w[@n=\''+str(valeurs[len(valeurs)-1])+'\']').attrib['pos'] == 'PRP'):
                    #print(phrase.find('w[@n=\''+str(valeurs[len(valeurs)-1])+'\']').attrib['pos'], str(valeurs[len(valeurs)-1]))

                    #else:
                        #groupes_nominaux[nom].remove(valeurs[len(valeurs)-1])
                        #print(phrase.find('w[@n=\''+str(valeurs[len(valeurs)-1])+'\']').attrib['pos'])
                        #print("oui --> suppression ", phrase.find('w[@n=\'' + str(valeurs[len(valeurs) - 1]) + '\']').text)

    for nom, GN in groupes_nominaux.items():
        if len(GN) > 0 and types_groupes[nom][0] != "compl":
            n_dernier_mot = groupes_nominaux[nom][len(GN)-1]
            #print (n_dernier_mot)
            pos_finaux = ['KON', 'PRO:REL']
            if phrase.find('.//*[@n=\''+str(n_dernier_mot)+'\']').attrib['pos'] in pos_finaux:
                groupes_nominaux[nom].remove(n_dernier_mot)
                #print("oui --> suppression ", phrase.find('w[@n=\'' + str(n_dernier_mot) + '\']').text)
    #texte_phrase = ''
    #for elem in phrase.iter():
    #    if elem.text != None:
    #        texte_phrase += elem.text + ' '
    #texte_phrase = texte_phrase[:-1]
    #print (texte_phrase)

    identifiants_noms_trouves = []
    for nom, valeurs in groupes_nominaux.items():
        print(nom)
        print(valeurs)
        valeurs = sorted(list(set(valeurs)))
        #print(valeurs)
        groupe = ''
        for valeur in valeurs:
            groupe += phrase.find('.//*[@n=\''+str(valeur)+'\']').text+' '
            identifiants_noms_trouves.append(valeur)
        groupes_nominaux[nom] = valeurs
        #print (groupe)
    return groupes_nominaux, identifiants_noms_trouves, types_groupes

def concatenation_groupes(id_tete, membres_groupe, groupes_detectes):
    resultat = membres_groupe
    for noyau_syntagme, composants in groupes_detectes.items():
        if id_tete != noyau_syntagme and len(membres_groupe) > 0 and len(composants) > 0 and \
                int(membres_groupe[len(membres_groupe) - 1]) + 1 == int(composants[0]):
                for composant in composants:
                    if composant not in resultat:
                        resultat.append(int(composant))
    resultat_enrichi = resultat
    #print(resultat_enrichi, resultat)
    while resultat_enrichi != resultat:
        resultat_enrichi = concatenation_groupes(id_tete, resultat, groupes_detectes)

    return (resultat_enrichi)



def recherche_resultats(groupe_tete, groupe_composant, indice_prp, root_NAM):

    classe_tete = groupe_tete[0]
    classe_composant = groupe_composant[0]
    #Groupes qui commencent par un nom propre
    if groupe_tete[1].tag == 'nym':
        return groupe_tete[1].attrib["{http://www.w3.org/XML/1998/namespace}id"], "complément_NP"
    elif classe_tete == 'persName' and 'subtype' in groupe_tete[1].attrib and groupe_tete[1].attrib['subtype'] == 'mort' and 'p' in groupe_tete[3]:
        print (classe_composant)
        return('manes', 'périphrase')
    #Les deux éléments de la même classe (persName, placeName, orgName, objetName)
    elif classe_tete == classe_composant:
        type_tete = groupe_tete[1].attrib["type"]
        type_composant = groupe_tete[1].attrib["type"]
        #La tête et le complément du même @type (homme, oronyme, territoire, et.)
        if type_tete == type_composant:
            #Le complément est un nom propre et le NC à la tête exprime un lien de parenté ou de liaison amoureuse
            if groupe_composant[1].tag == 'nym' and "corresp" in groupe_tete[1].attrib and (groupe_tete[1].attrib["corresp"] == "parenté" or
                    groupe_tete[1].attrib["corresp"] == "liaison"):
                #si la liaison de parenté
                if groupe_tete[1].attrib["corresp"] == "parenté":
                    relations_parente = {}
                    relations_parente['ancêtre'] = ['père', 'mère', 'ancêtre']
                    relations_parente['descendant'] = ['fils', 'fille', 'descendant']
                    relations_parente['frère'] = ["fratrie"]
                    synch = groupe_tete[1].attrib["synch"]

                    candidats = recherche_candidats(groupe_composant[1], relations_parente[synch], ['corresp'])
                    if len(candidats) == 1:
                        return (candidats[0], 'parenté')
                    else:
                        resultat_recherche_approfondie = precision_relation(candidats, groupe_tete, root_NAM)
                        id_retenu = resultat_recherche_approfondie[0]
                        if id_retenu != 0:
                            return (id_retenu, 'parenté')
                        else:
                            print ('Informations manquants dans la BD')
                #si la liaison amoureuse
                elif groupe_tete[1].attrib["corresp"] == "liaison":
                    if groupe_composant[3] in groupe_tete[3]:
                        return groupe_composant[1].attrib["{http://www.w3.org/XML/1998/namespace}id"], 'précision_NP'
                    else:
                        candidats = recherche_candidats(groupe_composant[1], ['liaison'], ['corresp'])
                        if len(candidats) == 1:
                            return (candidats[0], 'liaison')
                        else:
                            resultat_recherche_approfondie = precision_relation(candidats, groupe_tete, root_NAM)
                            id_retenu = resultat_recherche_approfondie[0]
                            if id_retenu != 0:
                                return (id_retenu, 'liaison')
                            else:
                                print('Informations manquants dans la BD')
            # Le genre et le nombre de deux éléments sont identiques, le complement est un persName, nom propre et le groupe
            # ne contient pas de prépositions
            elif groupe_tete[3] == groupe_composant[3] and classe_composant == 'persName' and groupe_composant[1].tag == 'nym' and \
                indice_prp == 0:
                #print("PROPOSITION DE REGROUPEMENT SOUS LE MÊME ID_1")
                return groupe_composant[1].attrib["{http://www.w3.org/XML/1998/namespace}id"], 'précision_NP'
            #le composant est un placeName et un nom propre
            elif classe_composant == 'placeName' and groupe_composant[1].tag == 'nym':
                #les sous-types sont identiques
                if "subtype" in groupe_tete[1].attrib and groupe_tete[1].attrib['subtype'] == groupe_composant[1].attrib['subtype']:
                    #print("PROPOSITION DE REGROUPEMENT SOUS LE MÊME ID_2")
                    return groupe_composant[1].attrib["{http://www.w3.org/XML/1998/namespace}id"], 'expansion_lexicale'
                #les sous-types sont différents
                elif "subtype" in groupe_tete[1].attrib and groupe_tete[1].attrib['subtype'] != groupe_composant[1].attrib['subtype']:
                    precisions_lieu = ['délimiteur', 'voie', 'souterrain', 'destination', 'forestier', 'édifice']
                    #mais le nom commun correspond à un type qui exprime la méronymie (un endroit précis dans un ville, etc.)
                    if groupe_tete[1].attrib["type"] in precisions_lieu:
                        return groupe_composant[1].attrib[
                            "{http://www.w3.org/XML/1998/namespace}id"], groupe_tete[1].attrib["type"]
                    else:
                        # on regarde dans les relations pour le territoire corresponant
                            candidats = recherche_candidats(groupe_composant[1], ['territoire'], ['corresp', 'join'])
                            # l'expansion est approximative
                            if len(candidats) == 0:
                                return groupe_composant[1].attrib[
                            "{http://www.w3.org/XML/1998/namespace}id"], 'expansion_lexicale_approx'
                            #lancement de la recherche approfondie pour trouver le territoire correspondant avec le même
                            #subtype que le nom commun à la tête
                            else:
                                resultat_recherche_approfondie = precision_relation(candidats, groupe_tete, root_NAM)
                                id_retenu = resultat_recherche_approfondie[0]
                                if id_retenu != 0:
                                    if resultat_recherche_approfondie[1] == 'approx':
                                        return  id_retenu, 'territoire_approx'
                                    else:
                                        return (id_retenu, 'territoire')
                                else:
                                    return groupe_composant[1].attrib[
                                               "{http://www.w3.org/XML/1998/namespace}id"], 'expansion_lexicale_approx'


                        #else:

                         #   relations = groupe_composant[1].findall(".//relation")
                          #  candidats = []
                           # for relation in relations:
                            #    if 'territoire' in relation.attrib['name']:
                             #       if 'corresp' in relation.attrib:
                              #          for corresp in relation.attrib['corresp'].split(' '):
                               #             candidats.append(corresp)
                                #    if 'join' in relation.attrib:
                                 #       for join in relation.attrib['join'].split(' '):
                                  #          candidats.append(join)
                            #if len(candidats) == 0:
                             #   return groupe_composant[1].attrib[
                              #             "{http://www.w3.org/XML/1998/namespace}id"], 'expansion_lexicale_approx'
                            #else:
                             #   resultat_recherche_approfondie = precision_relation(candidats, groupe_tete, root_NAM)
                              #  id_retenu = resultat_recherche_approfondie[0]
                               # if id_retenu != 0:
                                #    if resultat_recherche_approfondie[1] == 'approx':
                                 #       return id_retenu, 'territoire_approx'
                                  #  else:
                                   #     return (id_retenu, 'territoire')
                                #else:
                                 #   print('Lieu manquant dans la BD')

                #else:
                    #print("PROPOSITION DE REGROUPEMENT SOUS LE MÊME ID_3")
                    #return groupe_composant[1].attrib["{http://www.w3.org/XML/1998/namespace}id"], 'expansion_lexicale'
            # Les deux éléments du même type, mais sans nom propre
            elif groupe_composant[1].tag != 'nym':
                    print("PÉRIPHRASE SANS NOM PROPRE : STATS?")
            #quelques cas spécifiques
            else:
                # relation au niveau de méronyme ou hyperonyme
                if "ana" in groupe_tete[1].attrib and ("méronyme" in groupe_tete[1].attrib['ana'] or
                                                       groupe_tete[1].attrib['ana'] == "hyperonyme"):
                    return groupe_composant[1].attrib["{http://www.w3.org/XML/1998/namespace}id"], groupe_tete[1].attrib['ana']
                    # traitement des prêtres et des célébrations
                elif 'sameAs' in groupe_tete[1].attrib and groupe_tete[1].attrib['sameAs'] == 'religion' and \
                         groupe_composant[1].tag == 'nym':
                    if groupe_composant[1].attrib['subtype'] != "dieu" and groupe_composant[1].attrib['subtype'] != "déesse":
                        candidats = recherche_candidats(groupe_composant[1], ['prêtre', 'célébration'], ['corresp', 'join'])
                        resultat_recherche_approfondie = precision_relation(candidats, groupe_tete, root_NAM)
                        id_retenu = resultat_recherche_approfondie[0]
                        if id_retenu != 0:
                            return (id_retenu, 'prêtre')
                        else:
                            print('Lieu manquant dans la BD')
                            return (groupe_tete[1].attrib["{http://www.w3.org/XML/1998/namespace}id"] + '_' +
                                    groupe_composant[1].attrib["{http://www.w3.org/XML/1998/namespace}id"], 'prêtre_indef')
                    else:
                        candidats = recherche_candidats(groupe_composant[1], ['specificationGenre'],
                                                        ['join'])
                        resultat_recherche_approfondie = precision_relation(candidats, groupe_tete, root_NAM)
                        id_retenu = resultat_recherche_approfondie[0]
                        if id_retenu != 0:
                            return (id_retenu, 'dieu')
                        else:
                            print('Lieu manquant dans la BD')
                            return (groupe_tete[1].attrib["{http://www.w3.org/XML/1998/namespace}id"] + '_' +
                                    groupe_composant[1].attrib["{http://www.w3.org/XML/1998/namespace}id"],
                                    'dieu_indef')

                #type du nom commun en tête et le même que le sous-type du nom propre
                elif "subtype" in groupe_composant[1].attrib and groupe_tete[1].attrib["type"] == groupe_composant[1].attrib["subtype"]:
                    return groupe_composant[1].attrib["{http://www.w3.org/XML/1998/namespace}id"], "expansion_lexicale"
                # le nom commun peut désigner un ensemble et le nom commun en complément peut être un ensemble (bacchantes, nymphes, etc.)
                elif "join" in groupe_composant[1].attrib and "join" in groupe_tete[1].attrib:
                    return groupe_composant[1].attrib["{http://www.w3.org/XML/1998/namespace}id"], 'join'
                # confusion persName, placeName
                elif 'sameAs' in groupe_tete[1].attrib and "règne" in groupe_tete[1].attrib['sameAs']:
                    print('ici??', groupe_tete[2].text, groupe_composant[1].attrib["{http://www.w3.org/XML/1998/namespace}id"])
                    candidats_confusion = recherche_candidats(groupe_composant[1], ['confusion'], ['corresp'])
                    #print ("cccc", candidats_confusion)
                    if len(candidats_confusion) > 0:
                        item_confondu = root_NAM.find(
                            ".//nym[@{http://www.w3.org/XML/1998/namespace}id ='" + candidats_confusion[0] + "']")
                        nouvelle_groupe_composant = [item_confondu.find('.//pos').attrib['norm'], item_confondu, groupe_composant[2], '']

                        return recherche_resultats(groupe_tete, nouvelle_groupe_composant, indice_prp, root_NAM)
                    else:
                        return groupe_tete[1].attrib["{http://www.w3.org/XML/1998/namespace}id"]+'_'+ \
                                    groupe_composant[1].attrib["{http://www.w3.org/XML/1998/namespace}id"], "relation_indef"

                #pour les noms propres qui sont définis comme morts (fantôme)
                elif 'subtype' in groupe_tete[1].attrib and groupe_tete[1].attrib['subtype'] == 'mort':
                        return groupe_composant[1].attrib["{http://www.w3.org/XML/1998/namespace}id"], 'mort'
        # les noms propres féminins en complément des noms communs du type "homme"
        elif (type_tete == 'homme' and type_composant == 'femme') or (type_tete == 'femme' and type_composant == 'homme'):
            if 'f' in groupe_tete[3] and 'f' in groupe_composant[3]:
                return groupe_composant[1].attrib["{http://www.w3.org/XML/1998/namespace}id"], 'expansion_lexicale'
        else:
            print("CAS DE FIGURE À PRENDRE EN COMPTE_3")

    # nom de personne (nom commun) en tête, nom de lieu en complément (nom propre)
    elif classe_tete == 'persName' and classe_composant == 'placeName' and groupe_composant[1].tag == 'nym' and \
            (not 'corresp' in groupe_composant[1].attrib or not 'méronyme' in groupe_composant[1].attrib['corresp']):
            if 'sameAs' in groupe_tete[1].attrib and groupe_tete[1].attrib['sameAs'] == 'règne':

                candidats = recherche_candidats(groupe_composant[1], ['règne'], ['corresp'])
            else:
                candidats = recherche_candidats(groupe_composant[1], ['patrie', 'séjour'], ['join'])

            if len(candidats) == 0:
                candidats_territoire = recherche_candidats(groupe_composant[1], ['territoire'], ['corresp'])
                if len(candidats_territoire) > 0:
                    print(candidats_territoire)
                    for candidat_territoire in candidats_territoire:

                        territoire_parent = root_NAM.find(
                            ".//nym[@{http://www.w3.org/XML/1998/namespace}id ='" + candidat_territoire + "']")
                        if 'sameAs' in groupe_tete[1].attrib and groupe_tete[1].attrib['sameAs'] == 'règne':
                            nouveaux_candidats = recherche_candidats(territoire_parent, ['règne'], ['corresp'])
                        else:
                            nouveaux_candidats = recherche_candidats(territoire_parent, ['patrie', 'séjour'], ['join'])
                        if len(nouveaux_candidats) > 0:
                            resultat_recherche_approfondie = precision_relation(nouveaux_candidats, groupe_tete, root_NAM)
                            id_retenu = resultat_recherche_approfondie[0]
                            if id_retenu != 0:
                                return (id_retenu, 'relation_approx')
                            else:
                                print ('relation inconnue dans la BD')
                                return (groupe_tete[1].attrib["{http://www.w3.org/XML/1998/namespace}id"]+'_'+
                                    groupe_composant[1].attrib["{http://www.w3.org/XML/1998/namespace}id"], "relation_indef")
                else:
                    print('relation inconnue dans la BD')
                    return (groupe_tete[1].attrib["{http://www.w3.org/XML/1998/namespace}id"] + '_' +
                            groupe_composant[1].attrib["{http://www.w3.org/XML/1998/namespace}id"], "relation_indef")
            else:
                resultat_recherche_approfondie = precision_relation(candidats, groupe_tete, root_NAM)
                id_retenu = resultat_recherche_approfondie[0]
                if id_retenu != 0:
                    return (id_retenu, 'relation')
                else:
                    print('Lieu manquant dans la BD')
                    return (groupe_tete[1].attrib["{http://www.w3.org/XML/1998/namespace}id"] + '_' +
                            groupe_composant[1].attrib["{http://www.w3.org/XML/1998/namespace}id"], 'relation_indef')
    elif groupe_tete[1].attrib["{http://www.w3.org/XML/1998/namespace}id"] == 'nom' and classe_composant == 'placeName' and groupe_composant[1].tag == 'nym':
        return (groupe_composant[1].attrib["{http://www.w3.org/XML/1998/namespace}id"], "méronyme")
    elif classe_tete == 'placeName' and classe_composant == 'persName' and groupe_composant[1].tag == 'nym':
        candidats = recherche_candidats(groupe_composant[1], ['patrie'], ['corresp'])
        print (candidats)
        if len(candidats) > 0:
            resultat_recherche = precision_relation(candidats, groupe_tete, root_NAM)
            id_retenu = resultat_recherche[0]
            if id_retenu != 0:
                return (id_retenu, 'patrie')
            else:
                return (groupe_tete[1].attrib["{http://www.w3.org/XML/1998/namespace}id"] + '_' +
                        groupe_composant[1].attrib["{http://www.w3.org/XML/1998/namespace}id"], 'patrie_indef')

    else:
        print("REGARDER DANS LES RELATIONS")


def recherche_candidats(nym, tab_name, tab_corresp):
    relations = nym.findall(".//relation")
    candidats = []
    for relation in relations:
        if relation.attrib['name'] in tab_name:
            for attribute in tab_corresp:
                if attribute in relation.attrib:
                    for id_candidat in relation.attrib[attribute].split(' '):
                        candidats.append(id_candidat)
    return (candidats)

def precision_relation(ids_candidats, groupe, rootNAM):
    candidats_retenus = []
    for id_candidat in ids_candidats:
        #print('candidat', id_candidat)
        candidat = rootNAM.find(".//nym[@{http://www.w3.org/XML/1998/namespace}id = '"+id_candidat+"']")
        if candidat == None:
            candidats_retenus.append([id_candidat, 'approx'])
        else:
            type = candidat.find(".//pos").attrib['norm']

            if type == groupe[0]:

                if len(candidat.findall(".//*[@norm]")) == 3:
                    gen = candidat.find(".//gen").attrib['norm']
                    numb = candidat.find(".//number").attrib['norm']
                    #print (gen, groupe[3])
                    arts = ['littérature', 'musique', 'arts', 'nature']
                    if gen in groupe[3] and "corresp" in groupe[1].attrib and groupe[1].attrib['corresp'] == 'parenté':
                        candidats_retenus.append([id_candidat, ''])

                    elif gen in groupe[3] and "sameAs" in groupe[1].attrib and (groupe[1].attrib["sameAs"] in arts or
                                    (groupe[1].attrib["sameAs"] == 'religion' and groupe[1].attrib['type'] != 'dieu')): #(numb in groupe[3] or numb =='sp' or 'sp' in groupe[3]) and \

                        if "sameAs" in candidat.attrib and groupe[1].attrib['sameAs'] in candidat.attrib["sameAs"]:
                            candidats_retenus.append([id_candidat, ''])
                        else:
                            candidats_retenus.append([id_candidat, 'approx'])
                    #elif gen in groupe[3] and (numb in groupe[3] or numb =='sp' or 'sp' in groupe[3]) and groupe[1].attrib['sameAs'] == 'règne':
                    #    if candidat.attrib['subtype'] in royautes:
                    #        candidats_retenus.append([id_candidat,'approx'])
                    #    if candidat.attrib['subtype'] == 'dieu' or candidat.attrib['subtype'] == 'déesse':
                    #        candidats_retenus.append([id_candidat, 'approx'])
                    elif gen in groupe[3]: # and \#(numb in groupe[3] or numb == 'sp' or 'sp' in groupe[3]) and \
                            #(not "sameAs" in candidat.attrib or groupe[1].attrib['sameAs'] != 'règne'):
                            #print (candidat.attrib)
                            #print(groupe[1].attrib)

                            if 'subtype' in candidat.attrib and groupe[1].attrib['type']=='dieu' and (candidat.attrib['subtype'] == 'dieu' or candidat.attrib['subtype'] == 'déesse'):
                                    candidats_retenus.append([id_candidat, ''])
                            elif 'sameAs' in groupe[1].attrib and groupe[1].attrib['sameAs'] == 'règne':
                                candidats_retenus.append([id_candidat, ''])
                            elif numb in groupe[3] or numb == 'sp' or 'sp' in groupe[3]:
                                    candidats_retenus.append([id_candidat, ''])

                    #elif 'sameAs' in groupe[1].attrib and groupe[1].attrib['sameAs'] == 'règne' :
                        #if 'p' in groupe[3] or (gen in groupe[3] and (numb in groupe[3] or numb == 'sp' or 'sp' in groupe[3])):
                            #candidats_retenus.append([id_candidat, ''])





                else:
                    #placeName
                    if 'subtype' in groupe[1].attrib and (candidat.attrib['subtype'] == groupe[1].attrib['subtype'] or \
                            candidat.attrib['subtype'] == groupe[1].attrib['{http://www.w3.org/XML/1998/namespace}id']):
                        candidats_retenus.append([id_candidat, ''])
                    elif candidat.attrib['type'] == groupe[1].attrib['type']:
                        candidats_retenus.append([id_candidat, 'approx'])
    #print (candidats_retenus)
    if len(candidats_retenus) == 1:
        return candidats_retenus[0][0], ''
    else:
        candidat_final = []
        candidats_approx = []
        for candidat_retenu in candidats_retenus:
            if candidat_retenu[1] != 'approx':
                candidat_final.append(candidat_retenu[0])
            else:
                candidats_approx.append(candidat_retenu[0])

        if len(candidat_final) == 1:
            return candidat_final[0], ''
        if len(candidat_final) > 1:
            #print ('Plusieurs candidats : ', candidat_final)
            retour = ''
            for resultat in candidat_final:
                retour += resultat +' '
            retour = retour[:-1]
            return retour, ''

        elif len(candidat_final) == 0:
            if len(candidats_approx) == 0:
                return 0, ''
            else:
                #print ('Plusieurs candidats approx :', candidats_approx)
                retour = ''
                for resultat in candidats_approx:
                    retour += resultat + ' '
                retour = retour[:-1]
                return retour, 'approx'

def init(fichier_corpus, bd_NAM, bd_NOM, root):
    fichier_resultats = open(root+"/NER/fichier_resultats11-11.csv", "w")
    fichier_resultats.write("classe\tid\trelation\tforme\toccurrence\tidPhrase\trang\tphrase\n")
    dictionnaire_corpus = {}
    corpus_auteurs = {}
    with open(fichier_corpus, newline='') as fichier_corpus:
        fichier_corpus = csv.reader(fichier_corpus, delimiter='\t')
        for ligne_corpus in fichier_corpus:
            dictionnaire_corpus[ligne_corpus[0]] = ligne_corpus[1]
            corpus_auteurs[ligne_corpus[0]] = ligne_corpus[3]

    treeNOM = ET.parse(bd_NOM)
    rootNOM = treeNOM.getroot()
    dicoNOM = {}
    for parent in rootNOM.findall(".//*[w]"):
        dicoNOM[parent] = []
        enfants = parent.iter()
        for w in enfants:
            dicoNOM[parent].append(w.text)

    treeNAM = ET.parse(bd_NAM)
    rootNAM = treeNAM.getroot()

            #print("###### " + w.text)
            #for identifiant, phrase in dictionnaire_corpus.items():
                #if w.text in phrase:
                    #traitementPhrase(parent, w, phrase, identifiant)
    phrases_xml = xmlisationResultats.xmlisation_phrases(dictionnaire_corpus, 2)
    fichier_ajouts = open("ajouts.csv", "w")
    mots_a_ajouter = {}
    resultats_phrases = {}

    for identifiant_xml, phrase_xml in phrases_xml.items():
        print(identifiant_xml)
        groupes_periphrases = []
        phrase_xml = "<s>" + phrase_xml + "</s>"
        phrase_xml = ET.fromstring(phrase_xml)
        mots = phrase_xml.findall("*")
        groupes_GN, identifiants, types_Groupes  = recherche_groupes_nominaux(phrase_xml, mots, dicoNOM)
        classification_groupes = {}
        groupes_attribues = {}

        #nettoyage des doublons
        doublons = {}
        listes_doubles = []
        suppression_compl = []
        for id_1, ligne_1 in groupes_GN.items():
            if ligne_1 in listes_doubles and types_Groupes[id_1][0] == 'compl':
                suppression_compl.append(id_1)
            else:
                for id_2, ligne_2 in groupes_GN.items():
                    if id_1 != id_2 and ligne_1 == ligne_2 and (id_2 not in doublons.keys() or doublons[id_2] != id_1):
                        doublons[id_1] = id_2
                        listes_doubles.append(ligne_1)

        for doublon1, doublon2 in doublons.items():
            if types_Groupes[doublon1][0] == "persName" or types_Groupes[doublon1][0] == "placeName" or \
                    types_Groupes[doublon1][0] == "orgName" or types_Groupes[doublon1][0] == "objetName":
                del groupes_GN[doublon2]
            elif doublon1 in groupes_attribues.keys():
                numero_prp = 0

                for item in groupes_GN[doublon1]:
                    w = phrase_xml.find(".//*[@n ='"+str(item)+"']")
                    if 'PRP' in w.attrib['pos']:
                        numero_prp = item
                if numero_prp != 0 :

                    ancienne_groupe = groupes_GN[doublon2]
                    nouvelle_groupe = []
                    for mot in ancienne_groupe:
                        if int(mot) > numero_prp:
                            nouvelle_groupe.append(mot)
                    if len(nouvelle_groupe) > 0:
                        groupes_GN[doublon2] = nouvelle_groupe
                    else:
                        del (groupes_GN[doublon2])
                    #print(ancienne_groupe, nouvelle_groupe)
                else:
                    del groupes_GN[doublon1]

        for id_compl in suppression_compl:
            if id_compl in groupes_GN.keys():
                del groupes_GN[id_compl]





        for id_mot_tete, ligne in groupes_GN.items():
            if types_Groupes[id_mot_tete][0] != 'compl':
                #groupe = ''
                #for item in ligne:
                    # print (item)
                    #groupe += phrase_xml.find(".//*[@n= '" + str(item) + "']").text + ' '
                    # print (phrase_xml.find(".//*[@n= '" +str(item)+"']").text+' ')
                #print(groupe)
                #print(types_Groupes[id_mot_tete])
                if types_Groupes[id_mot_tete][0] == 'NC':
                    id_nc = types_Groupes[id_mot_tete][1]
                    parent_nc = rootNOM.find(".//*[@{http://www.w3.org/XML/1998/namespace}id = '"+id_nc+"']")
                    forme_mot = phrase_xml.find("w[@n ='"+id_mot_tete+"']").text
                    classe_nc = parent_nc.tag
                    #print(forme_mot.lower())
                    mot = parent_nc.findall(".//w[.='"+forme_mot.lower()+"']")
                    if len(mot) == 0:
                        msd = ""
                        mots_a_ajouter[forme_mot] = id_nc
                    else: #moduler par la suite pour les graphies identiques
                        msd = mot[0].attrib["msd"]
                        mot = mot[0]

                    classification_groupes[id_mot_tete] = [classe_nc, parent_nc, mot, msd]
                    #print(classification_groupes[id_mot_tete])
                elif types_Groupes[id_mot_tete][0] == 'NP':
                    forme_mot = phrase_xml.find("w[@n ='"+id_mot_tete+"']").text
                    lemme_np = types_Groupes[id_mot_tete][1].lower()
                    lemme_np = re.sub(r"[éèÉÈëê]", "e", lemme_np)
                    lemme_np = re.sub(r"[àâä]", "a", lemme_np)
                    lemme_np = re.sub(r"[îï]", "i", lemme_np)
                    lemme_np = re.sub(r"[œ]", "oe", lemme_np)
                    lemme_np = re.sub(r"ç", "c", lemme_np)
                    #print(lemme_np)
                    parent_np = rootNAM.find(".//nym[@{http://www.w3.org/XML/1998/namespace}id = '"+lemme_np+"']")

                    if parent_np == None:
                        mots_a_ajouter[forme_mot] = lemme_np
                        groupes_attribues[id_mot_tete] = lemme_np, 'NP'
                    else:

                        classe_np = parent_np.find(".//pos").attrib['norm']
                        print(forme_mot)
                        mot = parent_np.findall(".//*[.='"+forme_mot.lower().capitalize()+"']")[0]
                        if len(parent_np.findall(".//*[@norm]")) == 3:
                            msd = parent_np.find(".//gramGrp/gen").attrib['norm']+parent_np.find(".//gramGrp/number").attrib['norm']
                            #print(msd)
                        else:
                            msd = ''
                        classification_groupes[id_mot_tete] = [classe_np, parent_np, mot, msd]
                        groupes_attribues[id_mot_tete] = lemme_np, 'NP'
                else:
                    #print("groupes_ADJ et autres")
                    groupe = ''
                    for item in ligne:
                        groupe += phrase_xml.find(".//*[@n= '" + str(item) + "']").text + ' '
                    # print (phrase_xml.find(".//*[@n= '" +str(item)+"']").text+' ')
                    #print(groupe)
                    #print(types_Groupes[id_mot_tete])
                    groupes_periphrases.append(id_mot_tete)

                        #indice_parente = 0
                        #indice_prp = 0
                        #for id_2, mots_2 in groupes_GN.items():
                        #    if id_mot_tete != id_2 and int(id_mot_tete) in mots_2:
                        #        indice_parente = 2
                            #elif id_mot_tete != id_2 and int(id_2) in ligne:
                                #print (lemme_np)
                                #indice_parente = 1

                        #if indice_parente == 0:
                        #    groupe = ''
                        #    for item in groupes_GN[id_mot_tete]:
                        #        if 'PRP' in phrase_xml.find(".//*[@n= '" + str(item) + "']").attrib['pos']:
                        #            indice_prp = 1
                                # print (item)
                                # if phrase_xml.find(".//w[@n= '" +str(item)+"']"):
                        #        groupe += phrase_xml.find(".//*[@n= '" + str(item) + "']").text + ' '
                                # print (phrase_xml.find(".//*[@n= '" +str(item)+"']").text+' ')
                        #    print(groupe)

                        #    if indice_prp == 0:
                        #        groupes_attribues[id_mot_tete] = lemme_np, 'NP'
                        #    else:
                        #        print('problème?')
                        #if indice_parente == 2:

                    #print(classification_groupes[id_mot_tete])

        #print (classification_groupes)
        #print (groupes_attribues)
        for mot_tete, infos in classification_groupes.items():
            if mot_tete not in groupes_attribues.keys():
                type_groupe = infos[0]
                #print(types_Groupes[mot_tete])
                for mot in groupes_GN[mot_tete]:

                    if str(mot) != mot_tete and str(mot) in groupes_GN.keys():
                        if str(mot) in classification_groupes.keys():

                            type_composant = classification_groupes[str(mot)][0]
                            #print("1" + type_groupe)
                            #print("2"+type_composant)
                            groupe = ''
                            indice_prp = 0
                            #print (groupes_GN[mot_tete])
                            for item in groupes_GN[mot_tete]:
                                # print (item)
                                # if phrase_xml.find(".//w[@n= '" +str(item)+"']"):
                                w = phrase_xml.find(".//*[@n= '" + str(item) + "']")
                                groupe += w.text + ' '
                                if 'PRP' in w.attrib['pos']:
                                    #print ("oui")
                                    indice_prp = 1
                                # print (phrase_xml.find(".//*[@n= '" +str(item)+"']").text+' ')
                            #print(indice_prp, groupe)
                            if int(mot_tete) < int(mot) and (mot_tete not in groupes_attribues.keys() or groupes_attribues[mot_tete] == None): #pour récuperer les vrais têtes
                                groupes_attribues[mot_tete] = recherche_resultats(classification_groupes[mot_tete], classification_groupes[str(mot)], indice_prp, rootNAM)

                                if groupes_attribues[mot_tete] == None:
                                    print("ououoi")
                                    #del groupes_attribues[mot_tete]
                                    groupes_periphrases.append(mot_tete)
                        elif str(mot) != mot_tete and str(mot) in groupes_attribues.keys():
                            #print("1" + type_groupe)
                            #print("3" + types_Groupes[str(mot)][0]+'->'+types_Groupes[str(mot)][1])
                            groupe = ''
                            for item in groupes_GN[mot_tete]:
                                # print (item)
                                # if phrase_xml.find(".//w[@n= '" +str(item)+"']"):
                                groupe += phrase_xml.find(".//*[@n= '" + str(item) + "']").text + ' '
                                # print (phrase_xml.find(".//*[@n= '" +str(item)+"']").text+' ')
                            #print('???', groupe)
                        else:
                            groupe = ''
                            for item in groupes_GN[mot_tete]:
                                # print (item)
                                # if phrase_xml.find(".//w[@n= '" +str(item)+"']"):
                                groupe += phrase_xml.find(".//*[@n= '" + str(item) + "']").text + ' '
                                # print (phrase_xml.find(".//*[@n= '" +str(item)+"']").text+' ')
                            #print('???', groupe)
        #print (classification_groupes)
        if len(groupes_attribues) > 0:

            ids_presents = []
            for groupe_attribue in groupes_attribues.values():
                if groupe_attribue != None and not 'indef' in groupe_attribue[1] and not ' ' in groupe_attribue[0]:
                    ids_presents.append(groupe_attribue[0])
            ids_presents = list(set(ids_presents))
            print(ids_presents)
            for id_present, groupe_attribue in groupes_attribues.items():
                if groupe_attribue != None and ' ' in groupe_attribue[0]:
                    candidats = groupe_attribue[0].split(' ')
                    retenus = ''
                    for candidat in candidats:
                        if candidat in ids_presents:
                            retenus+= candidat+' '
                    retenus = retenus[:-1]
                    if len(retenus) != 0:
                        groupes_attribues[id_present] = (retenus, groupe_attribue[1])

                elif groupe_attribue != None and 'indef' in groupe_attribue[1] and str(int(id_present) - 2) in groupes_attribues.keys() and \
                    groupes_attribues[str(int(id_present)-2)] != None and 'indef' not in groupes_attribues[str(int(id_present)-2)][1] and \
                        groupes_attribues[str(int(id_present)-2)][0] not in groupe_attribue[0]:
                    groupes_attribues[id_present] = (groupes_attribues[str(int(id_present)-2)][0], 'périphrase')

            for identifiant_periphrase in classification_groupes.keys():
                if identifiant_periphrase not in groupes_attribues.keys():
                    if classification_groupes[identifiant_periphrase][0] == 'persName' \
                            and 'subtype' in classification_groupes[identifiant_periphrase][1].attrib and \
                            classification_groupes[identifiant_periphrase][1].attrib['subtype'] == 'mort' and 'p' in classification_groupes[identifiant_periphrase][3]:
                        print("NOUVELLE DECOUVERTE!!")
                        groupe = ''
                        for item in groupes_GN[identifiant_periphrase]:
                            groupe += phrase_xml.find(".//*[@n= '" + str(item) + "']").text + ' '
                        print(groupe)
                        groupes_attribues[identifiant_periphrase] = ('manes', 'périphrase')
                    elif classification_groupes[identifiant_periphrase][0] == 'placeName' \
                            and 'subtype' in classification_groupes[identifiant_periphrase][1].attrib and \
                            classification_groupes[identifiant_periphrase][1].attrib['subtype'] == 'enfer':
                        print("NOUVELLE DECOUVERTE!!")
                        groupe = ''
                        for item in groupes_GN[identifiant_periphrase]:
                            groupe += phrase_xml.find(".//*[@n= '" + str(item) + "']").text + ' '
                        print(groupe)
                        groupes_attribues[identifiant_periphrase] = ('enfers', 'périphrase')

                    else:
                        groupes_attribues[identifiant_periphrase] = trouve_periphrase(ids_presents, identifiant_periphrase,
                        classification_groupes[identifiant_periphrase], groupes_GN[identifiant_periphrase], phrase_xml, rootNAM)
                        #print("NOUVELLE DECOUVERTE!!")
                        #indication_indef = 0
                        #lemmes_indef = ['un', 'autre']
                        #groupe = ''
                        #for item in groupes_GN[identifiant_periphrase]:

                            #if phrase_xml.find(".//*[@n= '" + str(item) + "']").attrib['lemma'] in lemmes_indef and item < int(identifiant_periphrase[:4]):
                            #    indication_indef = 1
                            #groupe += phrase_xml.find(".//*[@n= '" + str(item) + "']").text + ' '
                        #print(groupe)
                        #print(int(identifiant_periphrase[:4]))
                        #print (classification_groupes[identifiant_periphrase][2].text)
                        #if indication_indef != 1:
                            #proposition_candidat = precision_relation(ids_presents, classification_groupes[identifiant_periphrase], rootNAM)
                            #print (proposition_candidat)
                            #if proposition_candidat[0] != 0:
                                #groupes_attribues[identifiant_periphrase] = [proposition_candidat[0], 'périphrase']
                        #else:
                            #groupes_attribues[identifiant_periphrase] = [classification_groupes[identifiant_periphrase][1].attrib['{http://www.w3.org/XML/1998/namespace}id'], 'indef']

            print(identifiant_xml, groupes_attribues)
            #print(groupes_periphrases)

    #for id_mot in mots_a_ajouter:
    #    fichier_ajouts.write(mots_a_ajouter[id_mot]+'\t'+id_mot+'\n')
    #fichier_ajouts.close()

        for id_mot_tete in classification_groupes.keys():
            fichier_resultats.write(types_Groupes[id_mot_tete][0])
            fichier_resultats.write("\t")
            if id_mot_tete in groupes_attribues.keys() and groupes_attribues[id_mot_tete] != None:
                fichier_resultats.write(groupes_attribues[id_mot_tete][0])
                fichier_resultats.write("\t")
                fichier_resultats.write(groupes_attribues[id_mot_tete][1])
            else:
                fichier_resultats.write("\t")
            fichier_resultats.write("\t")
            fichier_resultats.write(phrase_xml.find(".//*[@n= '" + str(id_mot_tete) + "']").text)
            fichier_resultats.write("\t")
            groupe = ''
            for item in groupes_GN[id_mot_tete]:
                # print (item)
                # if phrase_xml.find(".//w[@n= '" +str(item)+"']"):
                groupe += phrase_xml.find(".//*[@n= '" + str(item) + "']").text + ' '
            fichier_resultats.write(groupe)
            fichier_resultats.write("\t")
            fichier_resultats.write(str(groupes_GN[id_mot_tete][0]) + "-" + str(groupes_GN[id_mot_tete][len(groupes_GN[id_mot_tete]) - 1]))
            fichier_resultats.write("\t")
            fichier_resultats.write(identifiant_xml)
            fichier_resultats.write("\t")
            fichier_resultats.write(dictionnaire_corpus[identifiant_xml])
            fichier_resultats.write("\n")

        resultats_phrases[identifiant_xml] = groupes_attribues

def trouve_periphrase(ids_presents, id_tete, infos_mot_tete, groupe_nc, phrase_xml, rootNAM):
    type_determinant = ''
    groupe = ''
    for composant in groupe_nc:
        mot = phrase_xml.find(".//w[@n='"+str(composant)+"']")
        groupe += mot.text+' '
        if composant < int(id_tete):
            #print (mot.attrib['pos'])
            if mot.attrib['pos'] == 'DET:POS' or mot.attrib['pos'] == 'PRO:PER':
                #print ("possessif")
                type_determinant = 'possessif'
            elif mot.attrib['lemma'] == 'le':
                type_determinant = 'defini'
            elif mot.attrib['pos'] == 'PRO:DEM':
                type_determinant = 'demonstratif'
            elif mot.attrib['lemma'] == 'autre' or mot.attrib['lemma'] == 'un':
                type_determinant = 'indefini'
    print (groupe)
    if type_determinant == 'demonstratif':
        candidats_precision = []
        for id_candidat in ids_presents:
            candidat = rootNAM.find(".//nym[@{http://www.w3.org/XML/1998/namespace}id = '"+id_candidat+"']")
            if candidat != None and candidat.find('.//pos').attrib['norm'] == infos_mot_tete[0]:
                print ("candi", id_candidat)
                candidats_precision.append(id_candidat)
        resultat = precision_relation(candidats_precision, infos_mot_tete, rootNAM)
        if resultat[0] != 0:
            print('envoie resultat', id_tete)
            return (resultat[0], 'périphrase')
    elif type_determinant == 'possessif':
        candidats_precision = []
        for id_candidat in ids_presents:
            candidat = rootNAM.find(".//nym[@{http://www.w3.org/XML/1998/namespace}id = '"+id_candidat+"']")
            if  candidat != None and candidat.find('.//pos').attrib['norm'] == infos_mot_tete[0] and 'corresp' in infos_mot_tete[1].attrib:
                print("candi", id_candidat)
                if infos_mot_tete[1].attrib['corresp'] == 'liaison':
                    for id_cand in recherche_candidats(candidat, ['liaison'], ['corresp']):
                        candidats_precision.append(id_cand)
                elif infos_mot_tete[1].attrib['corresp'] == 'parenté':
                    relations_parente = {}
                    relations_parente['ancêtre'] = ['père', 'mère', 'ancêtre']
                    relations_parente['descendant'] = ['fils', 'fille', 'descendant']
                    relations_parente['frère'] = ["fratrie"]
                    if 'synch' in infos_mot_tete[1].attrib:
                        synch = infos_mot_tete[1].attrib["synch"]
                        for id_cand in recherche_candidats(candidat, relations_parente[synch], ['corresp']):
                            candidats_precision.append(id_cand)
                    else:
                        for famille in relations_parente.values():
                            for id_cand in recherche_candidats(candidat, famille, ['corresp']):
                                candidats_precision.append(id_cand)


        resultat = precision_relation(candidats_precision, infos_mot_tete, rootNAM)
        if resultat[0] != 0:
            print ('envoie resultat', id_tete)
            return (resultat[0], 'périphrase')

    print (groupe, type_determinant, ids_presents)












                #if groupe != '':
                #    fichier_resultats.write(types_Groupes[id_mot_tete][0])
                #    fichier_resultats.write("\t")
                #    fichier_resultats.write(types_Groupes[id_mot_tete][1])
                #    fichier_resultats.write("\t")
                #    fichier_resultats.write(phrase_xml.find(".//*[@n= '" + str(id_mot_tete) + "']").text)
                #    fichier_resultats.write("\t")
                #    fichier_resultats.write(groupe)
                #    fichier_resultats.write("\t")
                #    fichier_resultats.write(str(ligne[0]) + "-" + str(ligne[len(ligne) - 1]))
                #    fichier_resultats.write("\t")
                #    fichier_resultats.write(identifiant_xml)
                #    fichier_resultats.write("\t")
                #    fichier_resultats.write(dictionnaire_corpus[identifiant_xml])
                #    fichier_resultats.write("\n")


    #fichier_resultats.close()









