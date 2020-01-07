import xml.etree.ElementTree as ET
import traitementsTal

def alignement_groupes (groupe_source, groupe_target):
    score_correspondances = 0
    if groupe_source.attrib['select'] == groupe_target.attrib['select']:
        score_correspondances += 5
    else:
        synonymes_source = traitementsTal.recherche_synonymes(groupe_source.attrib['select'], 2)
        synonymes_target = traitementsTal.recherche_synonymes(groupe_target.attrib['select'], 2)
        if synonymes_target != 0:
            for synonyme_target in synonymes_target:
                if synonyme_target == groupe_source.attrib['select']:
                    score_correspondances += 0.6

        if synonymes_source != 0:
            for synonyme_source in synonymes_source:
                if synonyme_source == groupe_target.attrib['select']:
                    score_correspondances += 0.6
                elif synonymes_target != 0:
                    for synonyme_target in synonymes_target:
                        if synonyme_source == synonyme_target:
                            score_correspondances += 0.1
    return score_correspondances

def afficher_texte(element):
    texte = ''
    for elem in element.iter():
        if elem.text != None:
            texte += elem.text + ' '
    texte = texte[:-1]
    return texte


treeResults = ET.parse("resultat_avec_chunks.xml")
rootResults = treeResults.getroot()

def trouve_auteur(id_phrase):
    divs_auteurs = rootResults.findall('div')
    print (id_phrase)
    for div in divs_auteurs:
        if div.find('.//s[@{http://www.w3.org/XML/1998/namespace}id = \''+id_phrase+'\']') != None:
            return div.attrib['{http://www.w3.org/XML/1998/namespace}id']

textes = rootResults.findall('.//div')
for texte in textes:
    auteur_source = texte.attrib['{http://www.w3.org/XML/1998/namespace}id']
    fichier_resultats = open(auteur_source + '_alignement.csv', 'w')
    print(texte.attrib['{http://www.w3.org/XML/1998/namespace}id'])
    segs = texte.findall('seg')
    for seg in segs:
        print('###Début nouveau seg###')
        id_correspondance = seg.attrib['n']
        fichier_resultats.write(auteur_source + '\t' + id_correspondance + '\n')
        for phrase in seg.findall('s'):
            dictionnaire_correspondances = {}
            print('###Début nouvelle phrase###')
            id_phrase = phrase.attrib['{http://www.w3.org/XML/1998/namespace}id']
            ids_corresps = phrase.attrib['corresp'].split(' ')
            print(trouve_auteur(ids_corresps[0]))

            print(id_phrase)
            i = 1
            correspondances_valides = []
            while i < len(ids_corresps):
                if (int(ids_corresps[i - 1]) - int(ids_corresps[i])) < 8:
                    correspondances_valides.append(ids_corresps[i - 1])
                    correspondances_valides.append(ids_corresps[i])
                i += 1
            correspondances_valides = sorted(set(correspondances_valides))

            GNs_phrase_source = phrase.findall('.//phr[@type = \'GN\']')
            GVs_phrase_source = phrase.findall('phr[@type = \'GV\']')
            GAdjs_phrase_source = phrase.findall('phr[@type = \'GAdj\']')
            max_score_couple = 0
            correspondance_couple = {}
            for correspondance in correspondances_valides:
                score_couple = 0
                # print('###Début nouvelle correspondance###')
                # print (correspondance)
                if rootResults.find('.//s[@{http://www.w3.org/XML/1998/namespace}id = \'' + correspondance + '\']') != None:
                    candidat_phrase_correspondante = rootResults.find(
                        './/s[@{http://www.w3.org/XML/1998/namespace}id = \'' + correspondance + '\']')
                    dictionnaire_correspondances[candidat_phrase_correspondante] = []
                    GNs_candidat = candidat_phrase_correspondante.findall('.//phr[@type = \'GN\']')
                    GVs_candidat = candidat_phrase_correspondante.findall('phr[@type = \'GV\']')
                    GAdjs_candidat = candidat_phrase_correspondante.findall('phr[@type = \'GAdj\']')
                    for GN_source in GNs_phrase_source:
                        max_score_GN = 0
                        correspondances = {}
                        for GN_target in GNs_candidat:
                            score_alignement = alignement_groupes(GN_source, GN_target)
                            if score_alignement > max_score_GN:
                                if score_alignement not in correspondances.keys():
                                    correspondances[score_alignement] = []
                                couple = [GN_source, GN_target]
                                correspondances[score_alignement].append(couple)
                                max_score_GN = score_alignement

                        if max_score_GN > 0.1:
                            score_couple += max_score_GN
                            dictionnaire_correspondances[candidat_phrase_correspondante].append(correspondances[max_score_GN])
                        #     for resultats in correspondances[max_score_GN]:
                        #         print(max_score_GN)
                        #         print(resultats)
                        #         if len(resultats) > 2:
                        #             for couple in resultats:
                        #                 print("phrase source : ", afficher_texte(couple[0]))
                        #                 print("phrase target : ", afficher_texte(couple[1]))
                        #         else:
                        #             print("phrase source : ", afficher_texte(resultats[0]))
                        #             print("phrase target : ", afficher_texte(resultats[1]))

                    for GV_source in GVs_phrase_source:
                        max_score_GV = 0
                        correspondances_GV = {}
                        for GV_target in GVs_candidat:
                            score_alignement = alignement_groupes(GV_source, GV_target)
                            if score_alignement > max_score_GV:
                                if score_alignement not in correspondances_GV.keys():
                                    correspondances_GV[score_alignement] = []
                                couple = [GV_source, GV_target]
                                correspondances_GV[score_alignement].append(couple)
                                max_score_GV = score_alignement

                        if max_score_GV > 0.1:
                            score_couple += max_score_GV
                            dictionnaire_correspondances[candidat_phrase_correspondante].append(correspondances_GV[max_score_GV])
                        #     for resultats in correspondances_GV[max_score_GV]:
                        #         print(max_score_GV)
                        #         print(resultats)
                        #         if len(resultats) > 2:
                        #             for couple in resultats:
                        #                 print("phrase source : ", afficher_texte(couple[0]))
                        #                 print("phrase target : ", afficher_texte(couple[1]))
                        #         else:
                        #             print("phrase source : ", afficher_texte(resultats[0]))
                        #             print("phrase target : ", afficher_texte(resultats[1]))

                    for GAdj_source in GAdjs_phrase_source:
                        max_score_GAdj = 0
                        correspondances_GAdj = {}
                        for GAdj_target in GAdjs_candidat:
                            score_alignement = alignement_groupes(GAdj_source, GAdj_target)
                            if score_alignement > max_score_GAdj:
                                if score_alignement not in correspondances_GAdj.keys():
                                    correspondances_GAdj[score_alignement] = []
                                couple = [GAdj_source, GAdj_target]
                                correspondances_GAdj[score_alignement].append(couple)
                                max_score_GAdj = score_alignement
                        # Il se peut qu'une correspondance plus pertinente est dans les GN --> il suffit peut-être de le chercher dans le deuxième étape
                        # for GN_target in GNs_candidat:
                        #     score_alignement = alignement_GN_groupes(GAdj_source, GN_target)
                        #     if score_alignement > max_score_GAdj:
                        #         if score_alignement not in correspondances_GAdj.keys():
                        #             correspondances_GAdj[score_alignement] = []
                        #         couple = [GAdj_source, GN_target]
                        #         correspondances_GAdj[score_alignement].append(couple)
                        #         max_score_GAdj = score_alignement

                        if max_score_GAdj > 0.1:
                            score_couple += max_score_GAdj
                            dictionnaire_correspondances[candidat_phrase_correspondante].append(correspondances_GAdj[max_score_GAdj])
                        #     for resultats in correspondances_GAdj[max_score_GAdj]:
                        #         print(max_score_GAdj)
                        #         print(resultats)
                        #         if len(resultats) > 2:
                        #             for couple in resultats:
                        #                 print("phrase source : ", afficher_texte(couple[0]))
                        #                 print("phrase target : ", afficher_texte(couple[1]))
                        #         else:
                        #             print("phrase source : ", afficher_texte(resultats[0]))
                        #             print("phrase target : ", afficher_texte(resultats[1]))

                    if score_couple > max_score_couple:
                        max_score_couple = score_couple
                        correspondance_couple[max_score_couple] = candidat_phrase_correspondante
            if max_score_couple > 0:
                fichier_resultats.write(afficher_texte(phrase)+'\t'+afficher_texte(correspondance_couple[max_score_couple])+'\t'+str(max_score_couple)+'\n')
                for groupes_trouves in dictionnaire_correspondances[correspondance_couple[max_score_couple]]:
                    print('###')
                    print (groupes_trouves[0])
                    if len(groupes_trouves[0]) > 2:
                        for couple in groupes_trouves[0]:
                            fichier_resultats.write(afficher_texte(couple[0])+'\t'+afficher_texte(couple[1])+'\n')
                    else:
                        fichier_resultats.write(afficher_texte(groupes_trouves[0][0])+'\t'+afficher_texte(groupes_trouves[0][1])+"\n")
                print(correspondance_couple[max_score_couple].attrib['{http://www.w3.org/XML/1998/namespace}id'],
                      max_score_couple)
                print('correspondance gagnante : ')
                print(afficher_texte(phrase))
                print(afficher_texte(correspondance_couple[max_score_couple]))

    fichier_resultats.close()







