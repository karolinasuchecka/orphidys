import xml.etree.ElementTree as ET
import traitementsTal
import time
import re
import os

'''Initialisation'''

def init(traitement, racine):
    tps1 = time.process_time()
    """Lancement de Wolf"""
    wolf = traitementsTal.lancement_wolf()

    """Ouverture du fichier des phrases rejetées"""
    fichier_non_pertinentes = open(racine + "/" + traitement.chemin_projet + "/phrases_rejetes.csv", "w")
    fichier_non_pertinentes.write(
        "id source***id target***ratio source***ratio target***score***ratio score***phrase source***phrase target\n")

    """Ouverture du fichier results_avec_chunks"""
    treeResults = ET.parse(traitement.resultats_post)
    rootResults = treeResults.getroot()
    fichier_resultats = open(racine + "/" + traitement.chemin_projet + "/resultat_final.xml", "w")
    fichier_resultats.write("<?xml version='1.0' encoding='utf8'?><body>")
    divs = rootResults.findall(".//div")
    tout_seg = len(rootResults.findall(".//*[@corresp]"))-1
    i = 0
    for div in divs:
        fichier_resultats.write("<div id=\""+div.attrib['id']+"\">")
        phrases = div.findall(".//*[@corresp]")
        """Traitement de chaque phrase"""
        id_phrases = {}
        for phrase in phrases:
            i += 1
            print(str(i)+"/"+str(tout_seg))
            if str(00) in str(i):
                temps_courant = time.process_time()
                print ((temps_courant-tps1)/60)
            # print(afficher_texte(phrase))
            id_phrase = phrase.attrib['id']
            id_corresps = phrase.attrib['corresp'].split(' ')
            corresps = []
            for corresp in id_corresps:
                if rootResults.find(".//*[@id = '" + corresp + "']"):
                    corresps.append(corresp)

            """Liste mots source"""
            mots_source = phrase.findall('.//w')
            phrases_correspondantes = {}

            if id_phrase not in id_phrases.keys():
                id_phrases[id_phrase] = []
                """Recherche correspondanes entre les groupes"""
                phrases_non_pertinentes = {}
                for corresp in corresps:
                    # print("phrase corresp -> "+afficher_texte(rootResults.find(".//s[@id = '"+corresp+"']")))
                    score_phrase = 0
                    phrases_correspondantes[corresp] = []
                    id_phrases[id_phrase].append(corresp)
                    phrase_target = rootResults.find(".//*[@id = '" + corresp + "']")
                    # ratio_source, ratio_target = int, resultat_groupes = dico, key = groupe_source, [0] = groupe_target
                    # [1] type correspondances [2] tableau résultats (len == 1 -> lemmes, sinon : synos
                    ratio_source, ratio_target, resultat_groupes = correspondance_groupes(phrase, phrase_target,
                                                                                          wolf)
                    """A savoir que cela supprime également certaines phrases adverbiales (qui n'ont pas de <phr>).
                    Elles sont toutes peu pertinentes"""
                    if resultat_groupes == 0:
                        phrases_non_pertinentes[corresp] = [ratio_source, ratio_target, 0.0, 0.0]
                    else:
                        resultat_groupes_mots = alignement_mots(resultat_groupes, wolf)
                        # print("resultat groupes mots")
                        # print(resultat_groupes_mots)
                        """Recherche sur les mots restants"""
                        resultats_groupes_mots_restants = {}
                        mots_target = phrase_target.findall('.//w')
                        mots_target_apparies = []
                        mots_source_apparies = []
                        for id_source, resultats_alignement in resultat_groupes_mots.items():
                            mots_source_apparies.append(phrase.findall(".//w[@id='" + id_source + "']")[0])
                            for r_s in resultats_alignement[0]:
                                mots_target_apparies.append(phrase_target.findall(".//w[@id='" + r_s + "']")[0])
                        w_target_restants_tout = list(set(mots_target).symmetric_difference(mots_target_apparies))
                        w_target_restants = []
                        for w in w_target_restants_tout:
                            if traitementsTal.detecte_stopwords(w.text, w.attrib['lemma'], w.attrib['pos'])[0] == 1:
                                w_target_restants.append(w)
                        w_source_restants_tout = list(set(mots_source).symmetric_difference(mots_source_apparies))
                        w_source_restants = []
                        for w in w_source_restants_tout:
                            if traitementsTal.detecte_stopwords(w.text, w.attrib['lemma'], w.attrib['pos'])[0] == 1:
                                w_source_restants.append(w)
                        if len(w_source_restants) > 0 and len(w_target_restants) > 0:
                            mots_communs, lemmes_communs = recherche_mots_lemmes_communs(w_source_restants,
                                                                                         w_target_restants)
                            resultats_groupes_mots_restants = ajout_resultats(resultats_groupes_mots_restants,
                                                                              mots_communs, w_source_restants,
                                                                              w_target_restants, "mots", 5)
                            resultats_groupes_mots_restants = ajout_resultats(resultats_groupes_mots_restants,
                                                                              lemmes_communs, w_source_restants,
                                                                              w_target_restants, "lemmes", 5)
                            """Traitement des synonymes des mots restants"""
                            for w_s in w_source_restants:
                                if w_s.attrib['id'] not in resultats_groupes_mots_restants.keys():
                                    scoreMax, candidat = recherche_synonymes(w_s, w_target_restants, lemmes_communs,
                                                                             wolf)
                                    if candidat != []:
                                        resultats_groupes_mots_restants[w_s.attrib['id']] = [
                                            [candidat[0].attrib['id']],
                                            scoreMax,
                                            candidat[1]]
                                    else:
                                        scoreMax, candidat = recherche_antonymes(w_s, w_target_restants,
                                                                                 lemmes_communs, wolf)
                                        if candidat != []:
                                            resultats_groupes_mots_restants[w_s.attrib['id']] = [
                                                [candidat[0].attrib['id']],
                                                scoreMax,
                                                candidat[1]]
                            # print("Mots restants")
                            # print(resultats_groupes_mots_restants)
                            for restants_id in resultats_groupes_mots_restants.keys():
                                if restants_id not in resultat_groupes_mots.keys():
                                    resultat_groupes_mots[restants_id] = resultats_groupes_mots_restants[
                                        restants_id]
                        phrases_correspondantes[phrase_target] = ratio_source, ratio_target, resultat_groupes_mots

                """Ajout des phrases rejetés dans un fichier CSV (ratio source ou target == 0)"""
                for id_phrase_rejetee, details in phrases_non_pertinentes.items():
                    fichier_non_pertinentes.write(
                        phrase.attrib['id'] + "***" + id_phrase_rejetee + "***" + str(details[0]) + "***" + str(
                            details[1]) + "***" + str(
                            details[2]) + "***" + str(details[3]) + "***")
                    phraseTarget = rootResults.find(".//*[@id = \'" + id_phrase_rejetee + "\']")
                    fichier_non_pertinentes.write(afficher_texte(phrase) + "***" + afficher_texte(phraseTarget) + "\n")

            """Ajout des éléments xr et interpGrp à la phrase source"""
            phrases_a_ajouter, phrases_a_supprimer = ajout_xr(phrase, phrases_correspondantes)
            #print(phrases_a_ajouter)
            phrases_a_ajouter = re.sub(r"<\?xml version='1\.0' encoding='utf8'\?>", r"", phrases_a_ajouter)
            fichier_resultats.write(phrases_a_ajouter)
            """Ajouts des phrases à score 0 au fichier CSV"""
            if phrases_a_supprimer != {}:
                for id_phrase_rejetee, details in phrases_a_supprimer.items():
                    fichier_non_pertinentes.write(
                        phrase.attrib['id'] + "***" + id_phrase_rejetee + "***" + str(details[0]) + "***" + str(
                            details[1]) + "***" + str(
                            details[2]) + "***" + str(details[3]) + "***")
                    print(id_phrase_rejetee)
                    phraseTarget = rootResults.find(".//*[@id = \'" + id_phrase_rejetee + "\']")
                    fichier_non_pertinentes.write(
                        afficher_texte(phrase) + "***" + afficher_texte(phraseTarget) + "\n")


        fichier_resultats.write("</div>")
    fichier_resultats.write("</body>")
    #print(XML_final)
    fichier_resultats.close()
    fichier_non_pertinentes.close()
    #treeResults.write(racine+"/"+traitement.chemin_projet+"/resultat_final.xml")

    tps2 = time.process_time()
    print("#############################################")
    print(tps2-tps1)

    if len(treeResults.findall(".//seg")) > 0:
        compilation_textpair(traitement, racine)

def compilation_textpair(traitement, racine):
    parser = ET.XMLParser(encoding='utf-8')
    fichier = open(racine+"/"+traitement.chemin_projet+"/resultat_final.xml").read()
    treeResults = ET.fromstring(fichier, parser = parser)
    fichier_non_pertinentes = open("phrases_rejetees_2.csv", "w")
    phrases_rejetes = []

    #XML_final_TextPair = "<body>"
    divs = treeResults.findall(".//div")
    for div in divs:
        print(div.attrib['id'])
        resultats_phrases = {}
        xr_phrases = {}
        XML_final_TextPair = "<div id=\"" + div.attrib['id'] + "\">"
        segs = div.findall(".//seg")
        for seg in segs:
            print (seg.attrib)
            #XML_final_TextPair += "<seg id=\"" + seg.attrib['id'] + "\" corresp=\"" + seg.attrib['corresp'] + "\">"
            XML_final_TextPair += "<seg id=\"" + seg.attrib['id']+"\">"
            phrases = seg.findall(".//s")
            phrasesTarget = ""
            phrasesSource = ""
            for phrase in phrases:
                phrasesSource += phrase.attrib['id']+' '
                print(phrase.attrib['id'])
                print(ET.tostring(phrase))
                if phrase.attrib['id'] not in resultats_phrases.keys():
                    resultats_phrases[phrase.attrib['id']] = []
                if phrase.attrib['id'] not in xr_phrases.keys():
                    xr_phrases[phrase.attrib['id']] = phrase
                w_xr = phrase.findall(".//w[xr]")
                for w in w_xr:
                    xrs = w.findall(".//xr")
                    for xr in xrs:
                        if xr.attrib["corresp"].split("_")[0] not in phrasesTarget:
                            phrasesTarget += xr.attrib["corresp"].split("_")[0] + ' '
                        if xr.attrib["corresp"].split("_")[0] not in resultats_phrases[phrase.attrib['id']]:
                            resultats_phrases[phrase.attrib['id']].append(xr.attrib["corresp"].split("_")[0])
                        if phrase.attrib['id'] in xr_phrases.keys():
                            phrase_a_ajouter = xr_phrases[phrase.attrib['id']]
                            w_source = phrase_a_ajouter.find(".//w[@id=\"" + w.attrib['id'] + "\"]")
                            xrs_source = w_source.findall(".//xr")
                            indice = presence_xr(xr.attrib['corresp'], xrs_source)
                            if indice == 0:
                                w_source.insert(0, xr)
                                xr_phrases[phrase.attrib['id']] = phrase_a_ajouter
                print(ET.tostring(xr_phrases[phrase.attrib['id']]))

            interGrp = seg.find(".//interpGrp")
            phrasesSource = phrasesSource[:-1]
            interpSource = ET.Element("interp", attrib={"type": "phrasesSource", "corresp": phrasesSource})
            interpTarget = ET.Element("interp", attrib={"type": "phrasesTarget", "corresp": phrasesTarget})
            interGrp.insert(0, interpTarget)
            interGrp.insert(0, interpSource)
            XML_final_TextPair += ET.tostring(interGrp, encoding='utf8').decode()
            XML_final_TextPair += "</seg>"

        for id_phrase, resultats in resultats_phrases.items():
            phrase = xr_phrases[id_phrase]
            identifiants_target = ''

            xrs = phrase.findall(".//xr")
            interpGrps = []
            for it in resultats:
                print (it)
                score = 0
                for xr in xrs:
                    if it in xr.attrib['corresp']:
                        score += float(xr.attrib['cert'])
                if score > 0:
                    identifiants_target += it + ' '
                    ratio_score = calcul_ratio_score(score, phrase, treeResults.find(".//s[@id=\"" + it + "\"]"))
                    interpGrp_s = ET.Element("interpGrp", attrib={"corresp": it})
                    interpScore = ET.Element("interp", attrib={"type": "score"})
                    interpScore.text = str(round(score, 2))
                    interpRatioScore = ET.Element("interp", attrib={"type": "ratioScore"})
                    interpRatioScore.text = str(ratio_score)
                    interpGrp_s.insert(0, interpRatioScore)
                    interpGrp_s.insert(0, interpScore)
                    interpGrps.append(interpGrp_s)
                else:
                    fichier_non_pertinentes.write(id_phrase+"***"+it+"***"++"")
            identifiants_target = identifiants_target[:-1]
            phrase.set("corresp", identifiants_target)
            for ip in interpGrps:
                phrase.insert(0, ip)
            print(ET.tostring(phrase, encoding='utf8').decode())
            XML_final_TextPair += ET.tostring(phrase, encoding='utf8').decode()

        XML_final_TextPair += "</div>"

        XML_final_TextPair = re.sub(r"<\?xml version='1\.0' encoding='utf8'\?>", r"", XML_final_TextPair)
        #XML_final_TextPair = "<?xml version='1.0' encoding='utf8'?>" + XML_final_TextPair
        # print(XML_final)
        fichier_resultats = open(racine + "/" + traitement.chemin_projet + "/dossier_textes/"+div.attrib['id']+".xml", "w")
        fichier_resultats.write(XML_final_TextPair)
        fichier_resultats.close()

    os.system("cat "+ racine + "/" + traitement.chemin_projet + "/dossier_textes/*.xml >" + racine + "/" + traitement.chemin_projet + "/dossier_textes/resultats_compiles.xml")




def presence_xr(id_xr, xrs):
    for xr in xrs:
        if xr.attrib['corresp'] == id_xr:
            return 1
    return  0

def ajout_xr (phrase_source, phrases_correspondantes):
    phrases_rejetes = {}
    interpGroups = []
    xrs = {}
    identifiants_target = ""
    for phrase_target, resultats in phrases_correspondantes.items():
        if resultats != []:
            score_corresp = 0
            print(resultats)
            for id_mot_source, resultat_mot in resultats[2].items():
                id_mot_target = resultat_mot[0][0]
                score_mot = resultat_mot[1]
                score_corresp += score_mot
                type = ""
                detail = ""
                for item in resultat_mot[2]:
                    if isinstance(item, str):
                        type += item + ' '
                    else:
                        for mot in item:
                            detail += mot+' '

                type = type[:-1]
                detail = detail[:-1]
                xr = ET.Element('xr', attrib={"corresp": id_mot_target, "type": type, "cert": str(score_mot)})
                if detail != '':
                    xr.text = detail
                #xr = "<xr corresp=\""+"\" type=\""+type+"\" cert=\""+str(score_mot)+"\">"+detail+"</xr>"

                if id_mot_source not in xrs.keys():
                    xrs[id_mot_source] = [xr]
                else:
                    xrs[id_mot_source].append(xr)

            ratio_score = calcul_ratio_score(score_corresp, phrase_source, phrase_target)

            if score_corresp > 0:
                identifiants_target += phrase_target.attrib['id'] + ' '
                interpGrp = ET.Element("interpGrp", attrib={"corresp": phrase_target.attrib['id']})
                interpSource = ET.Element("interp", attrib={"type":"ratioSource"})
                interpSource.text = str(round(resultats[0], 2))
                interpTarget = ET.Element("interp", attrib={"type": "ratioTarget"})
                interpTarget.text = str(round(resultats[1],2))
                interpScore = ET.Element("interp", attrib={"type": "score"})
                interpScore.text = str(round(score_corresp, 2))
                interpRatioScore = ET.Element("interp", attrib={"type": "ratioScore"})
                interpRatioScore.text = str(ratio_score)
                interpGrp.insert(0, interpRatioScore)
                interpGrp.insert(0, interpScore)
                interpGrp.insert(0, interpTarget)
                interpGrp.insert(0, interpSource)
                interpGroups.append(interpGrp)
            else:

                phrases_rejetes[phrase_target.attrib['id']] = [resultats[0], resultats[1], score_corresp, ratio_score]



            #if score_corresp == 0:
               # print(ET.tostring(phrase_source, encoding='utf8').decode())
               # print(ET.tostring(phrase_target, encoding='utf8').decode())
               # print(resultats)

    identifiants_target = identifiants_target[:-1]
    phrase_source.set("corresp", identifiants_target)
    for ig in interpGroups:
        phrase_source.insert(0, ig)
    for id_w_source, list_xr in xrs.items():
        w_source = phrase_source.find(".//w[@id = '" + id_w_source + "']")
        if w_source != None:
            for xr in list_xr:
                w_source.insert(0, xr)

    phrase_texte = ET.tostring(phrase_source, encoding='utf8').decode()
    if identifiants_target != "":
        #print(phrase_texte)
        return phrase_texte, phrases_rejetes
    else:
        return "", phrases_rejetes

def calcul_ratio_score(score, phrase_source, phrase_target):
    w_source = phrase_source.findall(".//w")
    #print(w_source)
    w_target = phrase_target.findall(".//w")
    w_source_forts = []
    for w_s in w_source:
        if traitementsTal.detecte_stopwords(w_s.text, w_s.attrib['lemma'], w_s.attrib['pos'])[0] == 1:
            w_source_forts.append(w_s)
    w_target_forts = []
    for w_t in w_target:
        if traitementsTal.detecte_stopwords(w_t.text, w_t.attrib['lemma'], w_t.attrib['pos'])[0] == 1:
            w_target_forts.append(w_t)
    if len(w_source_forts) > len(w_target_forts):
        score_max = len(w_source_forts) * 5
    else:
        score_max = len(w_target_forts) * 5
    print("****")
    print(score_max)
    print(score)
    if score_max > 0:
        ratio_score_mots = round((score*100)/score_max, 2)
        print(ratio_score_mots)
        print("****")
        return ratio_score_mots
    else:
        return 0.0




"""Mise en correspondance des têtes des groupes (noyaux) """
def correspondance_groupes(phrase_source, phrase_target, wolf):

    """On extrait les différents groupes source et target"""
    tetes_source = []
    resultats_correspondance_groupes = {}
    groupes_source = phrase_source.findall('.//phr')
    if len(groupes_source) == 0:
        return (0,0,0)
    for groupe_source in groupes_source:
        tetes_source.append(groupe_source.attrib['select'])
    #print ("tetes_source -> " + str(tetes_source))
    tetes_target = []
    groupes_target = phrase_target.findall('.//phr')
    if len(groupes_target) == 0:
        return (0,0,0)
    for groupe_target in groupes_target:
        tetes_target.append(groupe_target.attrib['select'])
    #print("tetes_target -> " + str(tetes_target))
    """Appariement des lemmes identiques"""
    tetes_communes = list(set(tetes_source).intersection(tetes_target))
    for tete_commune in tetes_communes:
        for g_s in groupes_source:
            if g_s.attrib['select'] == tete_commune:
                corresp_target = []
                for g_t in groupes_target:
                    if g_t.attrib['select'] == tete_commune:
                        corresp_target.append(g_t)
                resultats_correspondance_groupes[g_s] = [corresp_target,
                     5,
                     ["lemmes"]
                     ]




    tetes_non_appariees = list(set(tetes_source).symmetric_difference(tetes_communes))
    #print ("tetes_communes -> " + str(tetes_communes))
    #print("tetes_à-apparier -> " + str(tetes_non_appariees))
    """Recherche sur les synonymes pour les groupes restants"""
    if len(tetes_communes) < len(tetes_source):
        tetes_restant_source = list(set(tetes_source).symmetric_difference(tetes_communes))
        tetes_restant_target = list(set(tetes_target).symmetric_difference(tetes_communes))
        correspondance_synonymique = {}
        for tete_r_s in tetes_restant_source:
            correspondance_synonymique[tete_r_s] = []
            for tete_r_t in tetes_restant_target:
                score_alignement, detail_resultats = alignement_groupes(tete_r_s, tete_r_t, wolf)
                if score_alignement > 0:
                    #print('tete source ->' + tete_r_s)
                    #print('tete target ->' + tete_r_t)
                    #print(score_alignement, detail_resultats)
                    if len(correspondance_synonymique[tete_r_s]) > 0 and correspondance_synonymique[tete_r_s][1] < score_alignement:
                        correspondance_synonymique[tete_r_s] = [tete_r_t, score_alignement, detail_resultats]
            if len(correspondance_synonymique[tete_r_s]) == 0 or correspondance_synonymique[tete_r_s][1] < 0.4:
                del correspondance_synonymique[tete_r_s]
        for tete in correspondance_synonymique.keys():
            #tetes_communes.append(tete)
            corresp_syno_source = []
            for g_syno_s in groupes_source:
                if g_syno_s.attrib['select'] == tete:
                    corresp_syno_source.append(g_syno_s)
            corresp_syno_target = []
            for g_syno_t in groupes_target:
                if g_syno_t.attrib['select'] == correspondance_synonymique[tete][0]:
                    corresp_syno_target.append(g_syno_t)
            resultats_correspondance_groupes[corresp_syno_source] = \
                [corresp_syno_target,
                 correspondance_synonymique[tete][1],
                 correspondance_synonymique[tete][2]
                 ]
            tetes_restant_source.remove(tete)
            tetes_restant_target.remove(correspondance_synonymique[tete][0])

        """Calcul du score pour la pertinence des couples"""
        if len(tetes_restant_source) != 0:
            ratio_source = 100 - (len(tetes_restant_source)*100/len(tetes_source))
        else:
            ratio_source = 100
        if len(tetes_restant_target) != 0:
            ratio_target = 100 - (len(tetes_restant_target) * 100 / len(tetes_target))
        else:
            ratio_target = 100

        if len(tetes_restant_source)*100/len(tetes_source) <= 80 or len(tetes_restant_target)*100/len(tetes_target) <= 80:
            #print("couple OK : ratio source ="+ str(100 - (len(tetes_restant_source)*100/len(tetes_source))) +"%, ratio target = "+
                #str(100 - (len(tetes_restant_target) * 100 / len(tetes_target))))
            return (ratio_source, ratio_target, resultats_correspondance_groupes)

        else:
            #print("couple NON PERTINENTE : ratio source =" + str(
                #100 - (len(tetes_restant_source) * 100 / len(tetes_source))) + "%, ratio target = " +
                #  str(100 - (len(tetes_restant_target) * 100 / len(tetes_target))))
            return (ratio_source, ratio_target, 0)
    else:
        #print("couple OK : corresp source 100 %")
        ratio_target = len(tetes_communes) * 100 / len(tetes_target)
        return (100, ratio_target, resultats_correspondance_groupes)

"""Alignement au niveau des synonymes : noyaux des groupes"""
def alignement_groupes(tete_source, tete_target, wolf):
    score_correspondances = 0
    detail_resultats = []
    synonymes_source = traitementsTal.recherche_synonymes_eloignes(tete_source, wolf)
    synonymes_target = traitementsTal.recherche_synonymes_eloignes(tete_target, wolf)
    if synonymes_target != 0 and tete_source in synonymes_target:
            score_correspondances += 0.6
            detail_resultats.append('lemme_syno')

    if synonymes_source != 0 and tete_target in synonymes_source:
            score_correspondances += 0.6
            detail_resultats.append('syno_lemme')
    if synonymes_source != 0 and synonymes_target !=0  and len(list(set(synonymes_source).intersection(synonymes_target))) > 0:
        #print("1")
        #print(score_correspondances)
        score_correspondances += round(0.1*len(list(set(synonymes_source).intersection(synonymes_target))), 2)
        #print("2")
        #print(score_correspondances)
        detail_resultats.append('syno_syno')
        detail_resultats.append(list(set(synonymes_source).intersection(synonymes_target)))

    #print("alignement groupes")
    #print(score_correspondances, detail_resultats)
    return score_correspondances, detail_resultats

"""Mise en correspondance des mots dans les groupes correspondants"""
def alignement_mots(groupes_alignes, wolf):
    resultats_groupes_mots = {}
    for groupe_source, correspondances in groupes_alignes.items():
        groupe_target = correspondances[0]
        w_source_tout = groupe_source.findall(".//w")
        w_source = []
        for w in w_source_tout:
            if traitementsTal.detecte_stopwords(w.text, w.attrib['lemma'], w.attrib['pos'])[0] == 1:
                w_source.append(w)
        for groupe_t in groupe_target:
            w_target_tout = groupe_t.findall(".//w")
            w_target = []
            for w in w_target_tout:
                if traitementsTal.detecte_stopwords(w.text, w.attrib['lemma'], w.attrib['pos'])[0] == 1:
                    w_target.append(w)
            mots_communs, lemmes_communs = recherche_mots_lemmes_communs(w_source, w_target)
            resultats_groupes_mots = ajout_resultats(resultats_groupes_mots, mots_communs, w_source, w_target, "mots", 5)

            resultats_groupes_mots = ajout_resultats(resultats_groupes_mots, lemmes_communs, w_source, w_target, "lemmes", 5)
            """Traitement des synonymes"""
            for w_s in w_source:
                if w_s.attrib['id'] not in resultats_groupes_mots.keys():
                    scoreMax, candidat = recherche_synonymes(w_s, w_target, lemmes_communs, wolf)
                    if candidat != []:
                        resultats_groupes_mots[w_s.attrib['id']] = [candidat[0].attrib['id']], scoreMax, candidat[1]
    return resultats_groupes_mots

def recherche_mots_lemmes_communs(w_source, w_target):
    mots_source = []
    lemmes_source = []
    for w_s in w_source:
        mots_source.append(w_s.text)
        lemmes_source.append(w_s.attrib['lemma'])
    #print(lemmes_source)
    mots_target = []
    lemmes_target = []
    for w_t in w_target:
        mots_target.append(w_t.text)
        lemmes_target.append(w_t.attrib['lemma'])
    """Mots communs"""
    mots_communs = list(set(mots_source).intersection(mots_target))
    """Lemmes communs"""
    lemmes_communs = list(set(lemmes_source).intersection(lemmes_target))
    #print(mots_communs, lemmes_communs)
    return mots_communs, lemmes_communs

def recherche_synonymes(w_s, w_target, lemmes_communs, wolf):
    scoreMax = 0.2
    candidat = []
    if 'sameAs' in w_s.attrib:
        synonymes_source_base = w_s.attrib['sameAs'].split(' ')
        for w_t in w_target:
            score = 0
            resultats_syno = []

            if w_t.attrib['lemma'] in synonymes_source_base and w_t.attrib['lemma'] not in lemmes_communs:
                score += 1.5
                resultats_syno.append('synoProche_lemme')

            if 'sameAs' in w_t.attrib and w_t.attrib['lemma'] not in lemmes_communs:
                synonymes_target_base = w_t.attrib['sameAs'].split(' ')

                if w_s.attrib['lemma'] in synonymes_target_base:
                    #print(
                        #"TROUVé : Corresp lemma source -> syno target " + w_s.attrib['lemma'] + ' -> ' + w_t.attrib[
                        #    'lemma'] + str(synonymes_target_base))
                    #score += 1.5
                    resultats_syno.append('lemme_synoProche')
                    if "synoProche_lemme" not in resultats_syno:
                        score += 1.5

                if len(list(set(synonymes_source_base).intersection(synonymes_target_base))) > 0:
                    #print(
                        #"TROUVé : Corresp synos proches -> " + w_s.attrib['lemma'] + ' -> ' + w_t.attrib['lemma'] +
                        #str(list(set(synonymes_source_base).intersection(synonymes_target_base))))
                    score += len(list(set(synonymes_source_base).intersection(synonymes_target_base))) * 0.5
                    resultats_syno.append('synoProche_synoProche')
                    for syno in list(set(synonymes_source_base).intersection(synonymes_target_base)):
                        resultats_syno.append([syno])
                else:
                    score_synos_loins, resultats_synos_loins = alignement_groupes(w_s.attrib['lemma'],
                                                                                  w_t.attrib['lemma'], wolf)
                    score += score_synos_loins
                    for r_s_l in resultats_synos_loins:
                        resultats_syno.append(r_s_l)
            if score > scoreMax:
                scoreMax = score
                candidat = [w_t, resultats_syno]
    if scoreMax > 5:
        scoreMax = 5
    return scoreMax, candidat

def recherche_antonymes(w_s, w_target, lemmes_communs, wolf):
    scoreMax = 0
    candidat = []
    if "exclude" in w_s.attrib:
        antonymes_source = w_s.attrib['exclude'].split(' ')
        synonymes_source = w_s.attrib['sameAs'].split(' ')
        for w_t in w_target:
            score = 0
            type = ''
            resultats_anto = []
            if w_t.attrib['lemma'] not in lemmes_communs and "exclude" in w_t.attrib:
                antonymes_target = w_t.attrib['exclude'].split(' ')
                synonymes_target = w_t.attrib['sameAs'].split(' ')
                if len(list(set(antonymes_source).intersection(antonymes_target))) > 0:
                    score = len(list(set(antonymes_source).intersection(antonymes_target))) * 0.5
                    type = "anto_anto"
                    for anto in list(set(antonymes_source).intersection(antonymes_target)):
                        resultats_anto.append(anto)
                elif len(list(set(synonymes_source).intersection(antonymes_target))) > 0:
                    score = len(list(set(synonymes_source).intersection(antonymes_target))) * 0.5
                    type = "syno_anto"
                    for anto in list(set(synonymes_source).intersection(antonymes_target)):
                        resultats_anto.append(anto)
                elif len(list(set(antonymes_source).intersection(synonymes_target))) > 0:
                    score = len(list(set(antonymes_source).intersection(synonymes_target)))
                    type = "anto_syno"
                    for anto in list(set(antonymes_source).intersection(synonymes_target)):
                        resultats_anto.append(anto)

            if score > scoreMax:
                scoreMax = score
                candidat = [w_t, [type, resultats_anto]]

    return scoreMax, candidat








def ajout_resultats(resultats_actuels, elements_ajouts, els_source, els_target, type, score):

    for m_c in elements_ajouts:
        for w_s in els_source:
            if (w_s.text == m_c or w_s.attrib['lemma'] == m_c) and w_s.attrib['id'] not in resultats_actuels.keys():
                resultats_actuels[w_s.attrib['id']] = [[], score, [type]]
                for w_t in els_target:
                    if w_t.text == m_c or w_t.attrib['lemma'] == m_c:
                        resultats_actuels[w_s.attrib['id']][0].append(w_t.attrib['id'])
    #print("resultats actuels")
    #print (resultats_actuels)
    return resultats_actuels

def afficher_texte(element):
    texte = ''
    for elem in element.iter():
        if elem.text != None and (elem.tag == "w" or elem.tag == 'pc'):
            texte_mot = re.sub(r"[\s\t\n]", r"", elem.text)
            texte += texte_mot + ' '
    texte = texte[:-1]
    #print(texte)
    return texte