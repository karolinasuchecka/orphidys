import xml.etree.ElementTree as ET
import os

def recherche_groupes_nominaux(phrase,mots):
    pos_ante_anteposes_nom = ('DET:ART', 'DET:POS', 'NUM', 'PRO:REL', "PRO:DEM")
    pos_anteposes_nom = (
    'DET:ART', 'DET:POS', 'ADJ', 'NUM', 'PRO:REL', 'PRO:PER', "PRO:DEM", "PRP:det", 'NOM')  # KON et PRP ?
    pos_postposes_nom = ('ADJ', 'VER:pper', 'NOM', 'PRP:det')
    pos_post_postposes_nom = ('ADJ', 'PRP', 'NOM')
    i = 0
    groupes_nominaux = {}
    while i < len(mots):
        if mots[i].tag == 'w' and (mots[i].attrib['pos'] == 'NOM' or mots[i].attrib['pos'] == 'NAM'):
            #print (i)
            id_groupe = mots[i].attrib['n']
            groupes_nominaux[id_groupe] = []
            if i-1 >= 0 and mots[i-1].tag == 'w' and mots[i-1].attrib['pos'] in pos_anteposes_nom and mots[i-1].attrib['pos'] != mots[i].attrib['pos']:
                if i-2 >= 0 and mots[i-2].tag == 'w' and (mots[i-2].attrib['pos'] in pos_ante_anteposes_nom or mots[-1].text
                                                      == 'des') and mots[i - 2].attrib['pos'] != mots[i - 1].attrib['pos']:
                    #print(mots[i - 2].text)
                    groupes_nominaux[id_groupe].append(int(mots[i-2].attrib['n']))
                    groupes_nominaux[id_groupe].append(int(mots[i - 1].attrib['n']))
                elif i-3 >= 0 and mots[i-2].tag == 'pc' and mots[i-3].tag == 'w' and mots[i-3].attrib['pos'] == 'ADJ' and mots[i-1].attrib['pos'] == 'ADJ':
                    groupes_nominaux[id_groupe].append(int(mots[i - 3].attrib['n']))
                    groupes_nominaux[id_groupe].append(int(mots[i - 1].attrib['n']))
                elif mots[i-1].attrib['pos'] != 'PRP:det':
                    groupes_nominaux[id_groupe].append(int(mots[i - 1].attrib['n']))

            #print(mots[i].text)
            groupes_nominaux[id_groupe].append(int(mots[i].attrib['n']))
            if i+1 < len(mots) and mots[i+1].tag == 'w' and (mots[i+1].attrib['pos'] in pos_postposes_nom or
                                                             mots[i+1].text == 'd\''or mots[i+1].text == 'de')\
                    and mots[i + 1].attrib['pos'] != mots[i].attrib['pos'] and mots[i+1].attrib['lemma'] != 'ne':
                #print(mots[i + 1].text)
                groupes_nominaux[id_groupe].append(int(mots[i+1].attrib['n']))
                if i + 2 < len(mots) and mots[i + 2].tag == 'w' and mots[i + 2].attrib['pos'] in pos_post_postposes_nom \
                        and mots[i + 2].attrib['pos'] != mots[i + 1].attrib['pos']:

                    #print(mots[i + 2].text)
                    groupes_nominaux[id_groupe].append(int(mots[i + 2].attrib['n']))
            elif i+3 < len(mots) and mots[i +1].tag == 'w' and (mots[i+1].attrib['pos'] == 'DET:ART' or mots[i+1].attrib['pos'] == 'KON')\
                    and mots[i+2].tag == 'w' and mots[i+2].attrib["pos"] == 'ADV' and mots[i+3].tag == 'w' and \
                    (mots[i+3].attrib["pos"] == 'ADJ' or mots[i+3].attrib['pos'] == 'VER:pper'):
                groupes_nominaux[id_groupe].append(int(mots[i + 1].attrib['n']))
                groupes_nominaux[id_groupe].append(int(mots[i + 2].attrib['n']))
                groupes_nominaux[id_groupe].append(int(mots[i + 3].attrib['n']))
                if i+4 < len(mots) and mots[i+4].tag == 'w' and mots[i+4].attrib['pos'] == 'PRP:det':
                    groupes_nominaux[id_groupe].append(int(mots[i + 4].attrib['n']))
        i += 1
    for nom, valeurs in groupes_nominaux.items():
        for noyau_syntagme, composants in groupes_nominaux.items():
            if nom != noyau_syntagme:
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
                if (phrase.find('w[@n=\''+str(valeurs[len(valeurs)-1])+'\']').attrib['pos'] == 'PRP:det' or
                         phrase.find('w[@n=\''+str(valeurs[len(valeurs)-1])+'\']').attrib['pos'] == 'PRP'):
                    if int(valeurs[len(valeurs)-1]) +1 == int(composants[0]):
                        #print ("oui --> ajout ", phrase.find('w[@n=\''+str(valeurs[len(valeurs)-1])+'\']').text, phrase.find('w[@n=\''+str(composants[0])+'\']').text)
                        for composant in composants:
                            groupes_nominaux[nom].append(int(composant))
                    #else:
                    #    groupes_nominaux[nom].remove(valeurs[len(valeurs)-1])

    for nom, GN in groupes_nominaux.items():
        n_dernier_mot = groupes_nominaux[nom][len(GN)-1]
        #print (n_dernier_mot)
        if phrase.find('w[@n=\''+str(n_dernier_mot)+'\']').attrib['pos'] == 'PRP:det' or phrase.find('w[@n=\''+str(n_dernier_mot)+'\']').attrib['pos'] == 'PRP':
            groupes_nominaux[nom].remove(n_dernier_mot)
    texte_phrase = ''
    for elem in phrase.iter():
        if elem.text != None:
            texte_phrase += elem.text + ' '
    texte_phrase = texte_phrase[:-1]
    #print (texte_phrase)

    identifiants_noms_trouves = []
    for nom, valeurs in groupes_nominaux.items():
        #print(nom)
        #print(valeurs)
        valeurs.sort()
        for valeur in valeurs:
            #print(phrase.find('w[@n=\''+str(valeur)+'\']').text)
            identifiants_noms_trouves.append(str(valeur))
    return groupes_nominaux, identifiants_noms_trouves


def recherche_groupes_verbaux(phrase, mots):
    temps_verbaux = ['VER:cond', 'VER:futu', 'VER:impe', 'VER:impf', 'VER:pres', 'VER:simp', 'VER:subi', 'VER:subp', 'VER:infi', 'VER:ppre']
    autres_formes = ['VER:pper', 'VER:ppre', 'VER:infi']
    composants_GV = ['ADV', 'PRO:REL', "PRO:PER","PRO:DEM", "PRP:det", 'PRP', "DET:ART", "ADV:NEG"]
    groupes_verbaux = {}
    identifiants = sorted(mots.keys())
    if len(identifiants) > 0:
        i = identifiants[0]
        while i < identifiants[len(identifiants) - 1]:
            if i in mots.keys() and mots[i].tag == 'w' and mots[i].attrib['pos'] in temps_verbaux:
                id_groupe = mots[i].attrib['n']
                groupes_verbaux[id_groupe] = []
                # print('PHRASE : ')
                texte_phrase = ''
                for elem in phrase.iter():
                    if elem.text != None:
                        texte_phrase += elem.text + ' '
                texte_phrase = texte_phrase[:-1]
                # print(texte_phrase)
                # print('###')
                if i - 1 in mots.keys() and mots[i - 1].tag == 'w' and (
                        mots[i - 1].attrib['pos'] in composants_GV or mots[i - 1].attrib['pos']
                        == 'VER:infi'):
                    if i - 2 in mots.keys() and mots[i - 2].tag == 'w' and mots[i - 2].attrib['pos'] in composants_GV:
                        if i - 3 in mots.keys() and mots[i - 3].tag == 'w' and mots[i - 3].attrib[
                            'pos'] in composants_GV:
                            # print(mots[i - 3].text, mots[i - 3].attrib['pos'])
                            groupes_verbaux[id_groupe].append(mots[i - 3].attrib['n'])
                        # print(mots[i - 2].text, mots[i - 2].attrib['pos'])
                        groupes_verbaux[id_groupe].append(mots[i - 2].attrib['n'])
                    # print (mots[i-1].text, mots[i-1].attrib['pos'])
                    groupes_verbaux[id_groupe].append(mots[i - 1].attrib['n'])
                # print (mots[i].text)
                groupes_verbaux[id_groupe].append(mots[i].attrib['n'])
                if i + 1 in mots.keys() and mots[i + 1].tag == 'w' and (
                        mots[i + 1].attrib['pos'] in composants_GV or mots[i + 1].attrib['pos'] in autres_formes) and \
                        mots[i + 1].attrib['pos'] != mots[i].attrib['pos']:
                    # print (mots[i+1].text, mots[i+1].attrib['pos'])
                    groupes_verbaux[id_groupe].append(mots[i + 1].attrib['n'])
                    if i + 2 in mots.keys() and mots[i + 2].tag == 'w' and (
                            mots[i + 2].attrib['pos'] in composants_GV or mots[i + 2].attrib['pos'] in autres_formes):
                        # print (mots[i+2].text, mots[i+2].attrib['pos'])
                        groupes_verbaux[id_groupe].append(mots[i + 2].attrib['n'])
                # print('###')
            i += 1

        # suppression des groupes qui sont déjà à l'intérieur d'un groupe
        id_groupe_a_supprimer = []
        for verbe_tete in groupes_verbaux.keys():
            for verbe, groupe in groupes_verbaux.items():
                if verbe_tete != verbe and verbe_tete in groupe and int(verbe) < int(verbe_tete):
                    id_groupe_a_supprimer.append(verbe_tete)

        for id_a_supprimer in id_groupe_a_supprimer:
            if id_a_supprimer in groupes_verbaux.keys():
                del groupes_verbaux[id_a_supprimer]

        groupes_finaux = {}
        identifiants_verbes_trouves = []
        for verbe_tete, groupe in groupes_verbaux.items():
            verbe_base = trouve_verbe_tete(groupes_verbaux[verbe_tete], phrase)
            groupes_finaux[verbe_base] = groupe
            for mot in groupe:
                identifiants_verbes_trouves.append(mot)
        return (groupes_finaux, identifiants_verbes_trouves)
    else:
        return 0,0


def trouve_verbe_tete(identifiants_mots, phrase):
    candidats = []
    auxiliaires = ['être', 'avoir', 'pouvoir', 'vouloir', 'savoir']
    for identifiant in identifiants_mots:
        if 'VER' in phrase.find('w[@n = \''+identifiant+'\']').attrib['pos']:
            #print("oui : candidats")
            candidats.append(identifiant)
    if len(candidats) > 1:
        #print('candidats : ')
        candidats_retenus = []
        for candidat in candidats:
            #print (phrase.find('w[@n = \''+candidat+'\']').text)
            if phrase.find('w[@n = \''+candidat+'\']').attrib['lemma'] not in auxiliaires:
                #print ('tête')
                #print (phrase.find('w[@n = \''+candidat+'\']').attrib['lemma'])
                candidats_retenus.append(candidat)
        if len(candidats_retenus) == 0:
            #print('tête par défaut')
            #print(phrase.find('w[@n = \'' + candidats[len(candidats) -1] + '\']').attrib['lemma'])
            return candidats[len(candidats) -1]
        else:
            #print('tête2')
            #print(phrase.find('w[@n = \'' + candidats_retenus[len(candidats_retenus)-1] + '\']').attrib['lemma'])
            return candidats_retenus[len(candidats_retenus)-1]
    else:
        return (candidats[0])

def recherche_groupes_adjectivaux (phrase, mots):
    identifiants = sorted(mots.keys())
    if len(identifiants) > 0:
        i = identifiants[0]
        constituants = ['ADV', 'PRO:DEM', 'DET:ART', 'PRO:PER', 'PRP', 'PRP:det', "PRO:REL"]
        groupes_adjectivaux = {}
        while i < identifiants[len(identifiants) - 1]:
            if i in mots.keys() and mots[i] != None and mots[i].tag == 'w' and (
                    mots[i].attrib['pos'] == 'ADJ' or mots[i].attrib['pos'] == 'VER:pper'):
                # print('PHRASE : ')
                texte_phrase = ''
                for elem in phrase.iter():
                    if elem.text != None:
                        texte_phrase += elem.text + ' '
                texte_phrase = texte_phrase[:-1]
                # print(texte_phrase)
                groupes_adjectivaux[str(i)] = []
                if i - 1 in mots.keys() and mots[i - 1] != None and mots[i - 1].tag == 'w' and mots[i - 1].attrib[
                    'pos'] in constituants:
                    if i - 2 in mots.keys() and mots[i - 2] != None and mots[i - 2].tag == 'w' and mots[i - 2].attrib[
                        'pos'] in constituants:
                        # print(mots[i-2].text, mots[i-2].attrib['pos'])
                        groupes_adjectivaux[str(i)].append(str(i - 2))
                    # print(mots[i - 1].text, mots[i - 1].attrib['pos'])
                    groupes_adjectivaux[str(i)].append(str(i - 1))
                # print(mots[i].text, mots[i].attrib['pos'])
                # print(i)
                groupes_adjectivaux[str(i)].append(str(i))
                if i + 1 in mots.keys() and mots[i + 1] != None and mots[i + 1].tag == 'w' and mots[i + 1].attrib[
                    'pos'] in constituants:
                    # print(mots[i+1].text, mots[i+1].attrib['pos'])
                    groupes_adjectivaux[str(i)].append(str(i + 1))
                    if i + 2 in mots.keys() and mots[i + 2] != None and mots[i + 2].tag == 'w' and mots[i + 1].attrib[
                        'pos'] in constituants:
                        # print(mots[i+2].text, mots[i+2].attrib['pos'])
                        groupes_adjectivaux[str(i)].append(str(i + 2))

            i += 1

        identifiants_adjectifs_trouves = []
        for g_adj in groupes_adjectivaux.values():
            for mot in g_adj:
                #print (mot)
                identifiants_adjectifs_trouves.append(mot)

        return groupes_adjectivaux, identifiants_adjectifs_trouves
    return 0,0

def extraction_chunks(fichier, dossier, racine):
    os.chdir(racine+'/'+dossier)
    treeResults = ET.parse(fichier)
    rootResults = treeResults.getroot()
    for phrase in rootResults.findall(".//s"):
        #print(phrase.attrib['{http://www.w3.org/XML/1998/namespace}id'])
        mots = phrase.findall("*")
        #print(mots)
        groupes_nominaux, identifiants_noms_trouves = recherche_groupes_nominaux(phrase, mots)
        reste_mots = {}
        for mot in mots:
            if mot.attrib['n'] not in identifiants_noms_trouves:
                reste_mots[int(mot.attrib['n'])] = mot
        #print(reste_mots)
        groupes_verbaux, identifiants_verbes_trouves = recherche_groupes_verbaux(phrase, reste_mots)

        reste_mots_2 = {}
        if groupes_verbaux != 0:
            for mot in reste_mots.keys():
                if str(mot) not in identifiants_verbes_trouves:
                    reste_mots_2[mot] = phrase.find('w[@n = \''+str(mot)+'\']')
        else:
            reste_mots_2 = reste_mots
        #print(reste_mots_2)
        #for w in reste_mots_2.values():
            #if w != None:
                #print (w.text, w.attrib['pos'])
        groupes_adjectivaux, identifiants_adjectifs_trouves = recherche_groupes_adjectivaux(phrase, reste_mots_2)
        if groupes_adjectivaux != 0:
            groupes_nominaux_extension = {}
            groupes_adj_a_supprimer = []
            for adj_tete, groupe_adj in groupes_adjectivaux.items():
                if phrase.find('w[@n = \'' + groupe_adj[0] + '\']').attrib['pos'] == 'DET:ART' or phrase.find(
                        'w[@n = \'' + groupe_adj[0] + '\']').attrib['pos'] == 'PRO:DEM' or phrase.find(
                    'w[@n = \'' + groupe_adj[0] + '\']').attrib['pos'] == 'PRP:det':
                    #print('########################', phrase.attrib['{http://www.w3.org/XML/1998/namespace}id'])
                    #print(groupe_adj)
                    groupes_adj_a_supprimer.append(adj_tete)
                    nouveau_groupe = []
                    for adj in groupe_adj:
                        nouveau_groupe.append(int(adj))
                    groupes_nominaux[adj_tete] = nouveau_groupe
            for nom_tete, composants in groupes_nominaux.items():
                #print('######NOM#####"', composants[len(composants) - 1])
                nouveau_composants = composants
                for adj_tete, groupe_adj in groupes_adjectivaux.items():
                    #print('####ADJ#######"', groupe_adj[0])
                    if (int(nouveau_composants[len(nouveau_composants) - 1]) + 1 == int(groupe_adj[0])):
                        #print('extension')
                        #print('avant : ', nouveau_composants)
                        for id in groupe_adj:
                            nouveau_composants.append(int(id))
                        groupes_nominaux_extension[nom_tete] = nouveau_composants
                        groupes_adj_a_supprimer.append(adj_tete)
                        #print('après :', nouveau_composants)
                    elif (int(nouveau_composants[len(nouveau_composants) - 1]) + 2 == int(groupe_adj[0])):
                        #print('extension')
                        #print('avant : ', nouveau_composants)
                        nouveau_composants.append(int(nouveau_composants[len(nouveau_composants) - 1]) + 1)
                        for id in groupe_adj:
                            nouveau_composants.append(int(id))
                        groupes_nominaux_extension[nom_tete] = nouveau_composants
                        groupes_adj_a_supprimer.append(adj_tete)
                        #print('après :', nouveau_composants)

            for nouveau_nom_tete in groupes_nominaux_extension:
                groupes_nominaux[nouveau_nom_tete] = groupes_nominaux_extension[nouveau_nom_tete]

            for groupe_supprime in groupes_adj_a_supprimer:
                if groupe_supprime in groupes_adjectivaux.keys():
                    del groupes_adjectivaux[groupe_supprime]

        #print (groupes_nominaux)




        reste_mots_final = {}
        for mot in reste_mots_2.keys():
            if mot not in identifiants_adjectifs_trouves:
                reste_mots_final[mot] = phrase.find('*[@n = \''+str(mot)+'\']')
        #print("mots_finaux")
        #print (reste_mots_final)


        n_courant = 0
        for mot in mots:
            if int(mot.attrib['n']) > n_courant:
                #print('before ', str(n_courant))
                n_courant = int(mot.attrib['n'])
                id = mot.attrib['n']
                #print ('after ', str(n_courant))
                #GN
                if id in groupes_nominaux.keys() and phrase.find('w[@n = \''+id+'\']') != None:
                    mot_tete = phrase.find('w[@n = \''+id+'\']').attrib["lemma"]
                    groupe = ET.Element('phr', type='GN', select=mot_tete)
                    for element_GN in groupes_nominaux[id]:
                        #print (element_GN)
                        #print (groupes_nominaux.keys())
                        if str(element_GN) != id and str(element_GN) in groupes_nominaux.keys() and phrase.find('w[@n = \''+str(element_GN)+'\']') != None:
                            sous_tete = phrase.find('w[@n = \''+str(element_GN)+'\']').attrib["lemma"]
                            sous_groupe = ET.Element('phr', type='GN', select=sous_tete)
                            for sous_element_GN in groupes_nominaux[str(element_GN)]:
                                #print ('ss ', sous_element_GN)
                                if phrase.find('w[@n = \''+str(sous_element_GN)+'\']') != None:
                                    sous_groupe.append(phrase.find('w[@n = \''+str(sous_element_GN)+'\']'))
                                    phrase.remove(phrase.find('w[@n = \''+str(sous_element_GN)+'\']'))
                            groupe.append(sous_groupe)
                        else:
                            #print (str(element_GN), mot.text)
                            if phrase.find('w[@n = \''+str(element_GN)+'\']') != None:
                                groupe.append(phrase.find('w[@n = \''+str(element_GN)+'\']'))
                                phrase.remove(phrase.find('w[@n = \''+str(element_GN)+'\']'))
                    phrase.append(groupe)
                    n_courant = groupes_nominaux[id][len(groupes_nominaux[id])-1]
                #GV
                elif id in groupes_verbaux.keys() and phrase.find('w[@n = \''+id+'\']') != None:
                    mot_tete = phrase.find('w[@n = \'' + id + '\']').attrib["lemma"]
                    groupe = ET.Element('phr', type='GV', select=mot_tete)
                    for element_GV in groupes_verbaux[id]:
                        if phrase.find('w[@n = \''+str(element_GV)+'\']') != None:
                            groupe.append(phrase.find('w[@n = \'' + element_GV + '\']'))
                            phrase.remove(phrase.find('w[@n = \'' + element_GV + '\']'))
                    phrase.append(groupe)
                    n_courant = int(groupes_verbaux[id][len(groupes_verbaux[id])-1])
                #GADJ
                elif groupes_adjectivaux != 0 and id in groupes_adjectivaux.keys() and phrase.find('w[@n = \''+id+'\']') != None:
                    mot_tete = phrase.find('w[@n = \'' + id + '\']').attrib["lemma"]
                    groupe = ET.Element('phr', type='GAdj', select=mot_tete)
                    for element_GAdj in groupes_adjectivaux[id]:
                        if phrase.find('w[@n = \'' + str(element_GAdj) + '\']') != None:
                            groupe.append(phrase.find('w[@n = \'' + element_GAdj + '\']'))
                            phrase.remove(phrase.find('w[@n = \'' + element_GAdj + '\']'))
                    phrase.append(groupe)
                    n_courant = int(groupes_adjectivaux[id][len(groupes_adjectivaux[id]) - 1])
                elif int(id) in reste_mots_final.keys():
                    #print(id)
                    if phrase.find('*[@n = \'' + id + '\']') != None:
                        phrase.remove(phrase.find('*[@n = \'' + id + '\']'))
                        #print('fait')
                        phrase.append(reste_mots_final[int(id)])
                        #print('fait')
                        n_courant = int(id)
        #if phrase.find("phr") == None:
        #    print(ET.tostring(phrase))

    treeResults.write('resultat_avec_chunks_desordre.xml')
    os.system("java -jar ../src/saxon9he.jar -xsl:../src/ordre_chunks.xsl -s:resultat_avec_chunks_desordre.xml -o:resultat_avec_chunks.xml")
    #os.remove("resultat_avec_chunks_desordre.xml")
    os.chdir(racine)





