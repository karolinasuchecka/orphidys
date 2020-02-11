import xml.etree.ElementTree as ET
import traitementsTal
import re
import xmlisationResultats
import os
from nltk.tokenize import sent_tokenize
import random
import string

def alignement_mots (mot_source, mot_target, tete_groupe_source, tete_groupe_target):
    score_correspondances = 0
    type_correspondance = ''


    if mot_source.text == mot_target.text:
        score_correspondances += 5
        type_correspondance = 'mots'
        print("mots", score_correspondances)

    elif mot_source.attrib['lemma'] == mot_target.attrib['lemma']:
        score_correspondances += 5
        type_correspondance = 'lemmes'
        print("lemmes", score_correspondances)

    else:
        if 'sameAs' in mot_source.attrib:
            synonymes_source_base = mot_source.attrib['sameAs'].split(' ')
            for synonyme_source_base in synonymes_source_base:
                if synonyme_source_base == mot_target.attrib['lemma']:
                    score_correspondances += 1.2
                    type_correspondance = 'synonymeBase-lemme'
                    print(type_correspondance, score_correspondances)
                elif 'sameAs' in mot_target.attrib:
                    synonymes_target_base = mot_target.attrib['sameAs'].split(' ')
                    for synonyme_target_base in synonymes_target_base:
                        if synonyme_target_base == synonyme_source_base:
                            score_correspondances += 0.2
                            type_correspondance = 'synonymeBase-synonymeBase'
                            print(type_correspondance, score_correspondances)
        elif 'sameAs' in mot_target.attrib:
            synonymes_target_base = mot_target.attrib['sameAs'].split(' ')
            for synonyme_target_base in synonymes_target_base:
                if synonyme_target_base == mot_source.attrib['lemma']:
                    score_correspondances += 1.2
                    type_correspondance = 'lemme-synonymeBase'
                    print(type_correspondance, score_correspondances)
        if score_correspondances <= 0.2 and (mot_source.attrib['pos'] == "NOM" or mot_source.attrib['pos'] == 'ADJ'):
            synonymes_source = traitementsTal.recherche_synonymes(mot_source.attrib['lemma'], 2)
            synonymes_target = traitementsTal.recherche_synonymes(mot_target.attrib['lemma'], 2)
            if synonymes_target != 0:
                for synonyme_target in synonymes_target:
                    if synonyme_target == mot_source.attrib['lemma']:
                        score_correspondances += 0.6
                        type_correspondance = 'lemme-synonymeElargi'
                        print(type_correspondance, score_correspondances)

            if synonymes_source != 0:
                for synonyme_source in synonymes_source:
                    if synonyme_source == mot_target.attrib['lemma']:
                        score_correspondances += 0.6
                        type_correspondance = 'synonymeElargi-lemme'
                        print(type_correspondance, score_correspondances)
                    elif synonymes_target != 0:
                        for synonyme_target in synonymes_target:
                            if synonyme_source == synonyme_target:
                                score_correspondances += 0.1
                                type_correspondance = 'synonymeElargi-synonymeElargi'
                                print(type_correspondance, score_correspondances)
    if score_correspondances > 0.6 and mot_source.attrib['lemma'] == tete_groupe_source and mot_target.attrib['lemma'] == tete_groupe_target:
        score_correspondances += 5
        print("tetes", score_correspondances)
    interp = [mot_target.attrib['{http://www.w3.org/XML/1998/namespace}id'], score_correspondances, type_correspondance]
    return interp

def afficher_texte(element):
    texte = ''
    for elem in element.iter():
        if elem.text != None:
            texte += elem.text + ' '
    texte = texte[:-1]
    return texte




def trouve_auteur(id_phrase, rootResults):
    divs_auteurs = rootResults.findall('div')
    #print (id_phrase)
    for div in divs_auteurs:
        if div.find('.//s[@{http://www.w3.org/XML/1998/namespace}id = \''+id_phrase+'\']') != None:
            return div.attrib['{http://www.w3.org/XML/1998/namespace}id']
def trouve_tete(id_phrase, id_mot, rootResults):
    phrase = rootResults.find('.//s[@{http://www.w3.org/XML/1998/namespace}id = \''+id_phrase+'\']')
    if phrase != None:
        syntagmes = phrase.findall('ptr')
        for syntagme in syntagmes:
            if syntagme.find(".//w[@{http://www.w3.org/XML/1998/namespace}id = '"+id_mot+"']") != None:
                return syntagme.attrib['select']

def trouve_target_gagnant(mot_source, mots_target, rootResults, id_phrase, id_corresp):
    print("_______________MOT SOURCE________________",mot_source.text)
    tete_source = trouve_tete(id_phrase, mot_source, rootResults)
    maxScore = 0
    target_gagnant = []
    for mot_target in mots_target:
        if mot_target.text.lower() not in traitementsTal.stopwords:
            tete_target = trouve_tete(id_corresp, mot_target, rootResults)
            resultat_alignement = alignement_mots(mot_source, mot_target, tete_source, tete_target)
            if resultat_alignement[1] > maxScore and resultat_alignement[1] > 0.1:
                target_gagnant = resultat_alignement
                if target_gagnant[1] == 5:
                    print("gagnant -> ", mot_source.text, mot_target.text)
                    return target_gagnant
    if target_gagnant != [] and target_gagnant[1] > 0.2:
        print ("gagant -> ",mot_source.text, target_gagnant)
    return target_gagnant

def donne_id_suivant(id_actuel):
    #print("id_actuel", id_actuel)
    dernier_chiffre = int(id_actuel[-1:])
    #print("dernier chiffre", dernier_chiffre)
    if dernier_chiffre < 9:
        dernier_chiffre = dernier_chiffre+1
        id_suivant = id_actuel[:-1]+str(dernier_chiffre)
        return id_suivant
    else:
        dernier_chiffre = int(id_actuel[-2:])
        if dernier_chiffre < 90:
            dernier_chiffre = dernier_chiffre + 1
            id_suivant = id_actuel[:-2] + str(dernier_chiffre)
            return id_suivant
        else:
            dernier_chiffre = int(id_actuel[-3:])
            if dernier_chiffre < 900:
                dernier_chiffre = dernier_chiffre + 1
                id_suivant = id_actuel[:-3] + str(dernier_chiffre)
                return id_suivant


def trouve_relations(id_phrase, app, resultats_correspondances):
    id_suivant = donne_id_suivant(id_phrase)
    #print("id suivant", id_suivant)
    if app.attrib['corresp'] != 0:
        corresps = app.find('./lem/s').attrib['corresp'].split(' ')
        if id_suivant in resultats_correspondances.keys():
            app_suivante = resultats_correspondances[id_suivant]
            rdgs = app_suivante.findall("rdg")
            for rdg in rdgs:
                #print ("attrib rdg", rdg.attrib["xml:id"])
                if rdg.attrib["xml:id"] in corresps:
                    return(id_suivant)
    return ""


"""Structuration texte d'édiiton"""
def traite_auteur(id):
    texteResults = ET.parse("../XML/"+id+".xml")
    texteRoot = texteResults.getroot()
    os.system("xsltproc xml2text_balises.xsl ../XML/"+id+".xml > "+id+"_phrases.xml")
    fichier_src = ET.parse(id+"_phrases.xml")
    texte_src = fichier_src.getroot()
    texte_src = ET.tostring(texte_src, encoding='utf8').decode()
    texte_src = re.sub(r"<\?xml version='1\.0' encoding='utf8'\?>", r"", str(texte_src))
    texte_src = re.sub(r"\.", r". ", texte_src)
    texte_src = re.sub(r"\?", r"? ", texte_src)
    texte_src = re.sub(r"\? …", r"?…", texte_src)
    texte_src = re.sub(r"!", r"! ", texte_src)
    texte_src = re.sub(r"! …", r"!…", texte_src)
    phrases_txt = sent_tokenize(texte_src, "french")
    for phrase_txt in phrases_txt:
        print(phrases_txt.index(phrase_txt)+1, phrase_txt)
    return texteRoot, texte_src, phrases_txt

    #exit()

def alignement_groupes(groupe_source, groupe_target):
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

def correspondance_groupes(phrase_source, phrase_target):
    GNs_phrase_source = phrase_source.findall('.//phr[@type = \'GN\']')
    GVs_phrase_source = phrase_source.findall('phr[@type = \'GV\']')
    GAdjs_phrase_source = phrase_source.findall('phr[@type = \'GAdj\']')
    GNs_phrase_target = phrase_target.findall('.//phr[@type = \'GN\']')
    GVs_phrase_target = phrase_target.findall('phr[@type = \'GV\']')
    GAdjs_phrase_target = phrase_target.findall('phr[@type = \'GAdj\']')
    score_couple = 0
    for GN_source in GNs_phrase_source:
        max_score_GN = 0
        correspondances = {}
        for GN_target in GNs_phrase_target:
            score_alignement = alignement_groupes(GN_source, GN_target)
            if score_alignement > max_score_GN:
                if score_alignement not in correspondances.keys():
                    correspondances[score_alignement] = []
                couple = [GN_source, GN_target]
                correspondances[score_alignement].append(couple)
                max_score_GN = score_alignement

        if max_score_GN > 0.1:
            score_couple += max_score_GN

    for GV_source in GVs_phrase_source:
        max_score_GV = 0
        correspondances_GV = {}
        for GV_target in GVs_phrase_target:
            score_alignement = alignement_groupes(GV_source, GV_target)
            if score_alignement > max_score_GV:
                if score_alignement not in correspondances_GV.keys():
                    correspondances_GV[score_alignement] = []
                couple = [GV_source, GV_target]
                correspondances_GV[score_alignement].append(couple)
                max_score_GV = score_alignement

        if max_score_GV > 0.1:
            score_couple += max_score_GV

    for GAdj_source in GAdjs_phrase_source:
        max_score_GAdj = 0
        correspondances_GAdj = {}
        for GAdj_target in GAdjs_phrase_target:
            score_alignement = alignement_groupes(GAdj_source, GAdj_target)
            if score_alignement > max_score_GAdj:
                if score_alignement not in correspondances_GAdj.keys():
                    correspondances_GAdj[score_alignement] = []
                couple = [GAdj_source, GAdj_target]
                correspondances_GAdj[score_alignement].append(couple)
                max_score_GAdj = score_alignement
        if max_score_GAdj > 0.1:
            score_couple += max_score_GAdj
    print (score_couple)
    return score_couple

def randomString(stringLength):
    """Generate a random string with the combination of lowercase and uppercase letters """
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for i in range(stringLength))

def generation_html(traitement, racine):
    treeResults = ET.parse(traitement.resultats_post)
    rootResults = treeResults.getroot()
    textes = rootResults.findall(".//div")
    if not os.path.exists(racine+"/"+traitement.chemin_xml_compile):
            os.makedirs(racine+"/"+traitement.chemin_xml_compile)

    for texte in textes:
        id_texte = texte.attrib['{http://www.w3.org/XML/1998/namespace}id']
        if not os.path.exists(racine+"/"+traitement.chemin_xml_compile+"/" +id_texte+"_resultats.xml"):
            print("##############"+id_texte+"###############")
            phrases = texte.findall(".//s")
            id_phrases = {}
            resultats_correspondances = {}
            phrases_traites = []
            for phrase in phrases:
                # print(afficher_texte(phrase))
                id_phrase = phrase.attrib['{http://www.w3.org/XML/1998/namespace}id']
                if id_phrase not in phrases_traites:
                    phrases_communes = texte.findall(".//s[@{http://www.w3.org/XML/1998/namespace}id = '" + id_phrase + "']")
                    id_corresps = ''
                    for phrase_commune in phrases_communes:
                        id_corresps += phrase_commune.attrib['corresp'] + ' '
                    id_corresps = id_corresps[:-1]
                    corresps = id_corresps.split(' ')
                    correspondances = list(set(corresps))
                    corresps = []
                    for corresp in correspondances:
                        if rootResults.find(".//s[@{http://www.w3.org/XML/1998/namespace}id = '" + corresp + "']"):
                            corresps.append(corresp)
                    mots_source = phrase.findall('.//w')
                    phrases_correspondantes = {}
                    phrases_correspondantes_scores = {}
                    if id_phrase not in id_phrases.keys():
                        id_phrases[id_phrase] = []
                        for corresp in corresps:
                            # print(afficher_texte(rootResults.find(".//s[@{http://www.w3.org/XML/1998/namespace}id = '"+corresp+"']")))
                            score_phrase = 0
                            phrases_correspondantes[corresp] = []
                            id_phrases[id_phrase].append(corresp)
                            phrase_target = rootResults.find(
                                ".//s[@{http://www.w3.org/XML/1998/namespace}id = '" + corresp + "']")
                            score_correspondance_groupes = correspondance_groupes(phrase, phrase_target)
                            if score_correspondance_groupes >= 30:
                                mots_target = phrase_target.findall('.//w')
                                targets_trouves = {}
                                for mot_source in mots_source:
                                    #id_mot_source = mot_source.attrib['{http://www.w3.org/XML/1998/namespace}id']
                                    if mot_source.text.lower() not in traitementsTal.stopwords:
                                        target_gagnant = trouve_target_gagnant(mot_source, mots_target, rootResults, id_phrase, corresp)
                                        target_gagnant.insert(0, mot_source.attrib['{http://www.w3.org/XML/1998/namespace}id'])
                                        if len(target_gagnant) > 2 and target_gagnant[2] > 0.2:
                                            # print(mot_source.text, phrase_target.find(".//w[@{http://www.w3.org/XML/1998/namespace}id = '"+target_gagnant[0]+"']").text, target_gagnant[1], target_gagnant[2])
                                            if target_gagnant[3] == 'mot' or target_gagnant[3] == 'lemme':
                                                score_phrase += target_gagnant[2]
                                                mots_target.remove(phrase_target.find(
                                                    ".//w[@{http://www.w3.org/XML/1998/namespace}id = '" + target_gagnant[
                                                        1] + "']"))
                                                targets_trouves[target_gagnant[1]] = target_gagnant
                                                phrases_correspondantes[corresp].append(target_gagnant)
                                            elif target_gagnant[1] in targets_trouves.keys() and target_gagnant[2] > \
                                                    targets_trouves[target_gagnant[1]][2]:
                                                phrases_correspondantes[corresp].remove(targets_trouves[target_gagnant[1]])
                                                targets_trouves[target_gagnant[1]] = target_gagnant
                                                phrases_correspondantes[corresp].append(target_gagnant)
                                                score_phrase += target_gagnant[2]
                                            else:
                                                targets_trouves[target_gagnant[1]] = target_gagnant
                                                phrases_correspondantes[corresp].append(target_gagnant)
                                                score_phrase += target_gagnant[2]

                            if score_phrase > 35:
                                phrases_correspondantes_scores[corresp] = score_phrase

                        nouveau_corresp = ''
                        auteurs = []
                        app = ET.Element('app', attrib={'xml:id': randomString(7)})
                        for phrase_retenue in phrases_correspondantes_scores.keys():
                            nouveau_corresp += phrase_retenue + ' '
                            auteurs.append(trouve_auteur(phrase_retenue, rootResults))
                            resultats = phrases_correspondantes[phrase_retenue]
                            rdg = ET.Element('rdg', attrib={'xml:id': phrase_retenue, "source": trouve_auteur(phrase_retenue, rootResults)})
                            rdg.append(
                                rootResults.find(".//s[@{http://www.w3.org/XML/1998/namespace}id = '" + phrase_retenue + "']"))
                            app.append(rdg)
                            for resultat in resultats:
                                id_source = resultat[0]
                                id_target = resultat[1]
                                score = resultat[2]
                                type = resultat[3]
                                xr = ET.Element('xr', attrib={"corresp": id_target, "type": type, "cert": str(score)})
                                w_source = phrase.find(".//w[@{http://www.w3.org/XML/1998/namespace}id = '" + id_source + "']")
                                w_source.insert(0, xr)

                        nouveau_corresp = nouveau_corresp[:-1]
                        auteurs = list(set(auteurs))
                        valeur_auteurs = ''
                        for auteur in auteurs:
                            valeur_auteurs += auteur + ' '
                        valeur_auteurs = valeur_auteurs[:-1]
                        app.attrib['corresp'] = valeur_auteurs
                        phrase.attrib['corresp'] = nouveau_corresp
                        lem = ET.Element('lem')
                        lem.insert(0, phrase)
                        app.insert(0, lem)
                        resultats_correspondances[id_phrase] = app

            print('ok 1')
            # texte_root, phrases_txt, string_txt = traite_auteur(id_texte)
            texteResults = ET.parse(traitement.chemin_textes+"/" + id_texte + ".xml")
            texte_root = texteResults.getroot()
            os.system("xsltproc src/xml2text_balises.xsl " +racine+'/' + traitement.chemin_textes+'/'+
                      id_texte + ".xml > " + id_texte + "_phrases.xml")
            fichier_src = ET.parse(id_texte + "_phrases.xml")
            texte_src = fichier_src.getroot()
            texte_src = ET.tostring(texte_src, encoding='utf8').decode()
            texte_src = re.sub(r"<\?xml version='1\.0' encoding='utf8'\?>", r"", str(texte_src))
            texte_src = re.sub(r"\.", r". ", texte_src)
            texte_src = re.sub(r"\?", r"? ", texte_src)
            texte_src = re.sub(r"\? …", r"?…", texte_src)
            texte_src = re.sub(r"!", r"! ", texte_src)
            texte_src = re.sub(r"! …", r"!…", texte_src)
            phrases_txt = sent_tokenize(texte_src, "french")
            resultats_concat = {}
            relations = {}
            for id_phrase, app in resultats_correspondances.items():
                id_suivant = trouve_relations(id_phrase, app, resultats_correspondances)
                if id_suivant != "":
                    # print("id_suiv rel trouve", id_suivant)
                    if id_phrase in relations.keys():
                        app = resultats_concat[relations[id_phrase]]
                    app_suivant = resultats_correspondances[id_suivant]
                    # print(app_suivant.find('lem'))
                    app.insert(1, app_suivant.find('lem'))
                    numero_phrase_suivante = int(id_suivant[-4:])
                    texte_src = re.sub(re.escape(phrases_txt[numero_phrase_suivante - 1]), '', str(texte_src))
                    for rdg in app_suivant.findall("rdg"):
                        if rdg.attrib['xml:id'] not in app.find("lem/s").attrib['corresp']:
                            app.append(rdg)

                    if id_phrase in relations.keys():
                        relations[id_suivant] = relations[id_phrase]
                        resultats_concat[relations[id_phrase]] = app
                    else:
                        relations[id_suivant] = id_phrase
                        resultats_concat[id_phrase] = app
                else:
                    resultats_concat[id_phrase] = app
            print('ok2')
            for id_phrase, app in resultats_concat.items():
                numero_phrase = int(id_phrase[-4:])
                print (numero_phrase)
                print(phrases_txt[numero_phrase-1])
                if re.search(re.escape(phrases_txt[numero_phrase - 1]), str(texte_src)) and app.attrib['corresp'] != '':
                    print('ok remplacement')
                    texte_a_remplacer = ET.tostring(app, encoding='utf8').decode()
                    print(texte_a_remplacer)
                    texte_src = re.sub(re.escape(phrases_txt[numero_phrase - 1]), texte_a_remplacer, str(texte_src))
                # else:
                # print("pas de match !")
                # print(ET.tostring(app, encoding='utf8').decode())

            print('ok3')
            fichier_resultats = open(traitement.chemin_xml_compile+"/" + id_texte + "_resultats.xml", "w")
            nouveau_texte = """<?xml version="1.0" encoding="UTF-8"?>
                           <TEI>"""
            teiHeader = texte_root.find(".//{http://www.tei-c.org/ns/1.0}teiHeader")
            teiHeader = ET.tostring(teiHeader, encoding='utf8').decode()
            nouveau_texte += str(teiHeader)
            nouveau_texte += "<text>"
            front = texte_root.find(".//{http://www.tei-c.org/ns/1.0}front")
            front = ET.tostring(front, encoding='utf8').decode()
            nouveau_texte += str(front)
            nouveau_texte += texte_src
            nouveau_texte += "</text></TEI>"
            nouveau_texte = re.sub(r"<\?xml version='1\.0' encoding='utf8'\?>", r"", nouveau_texte)
            nouveau_texte = re.sub(r"<\?xml version='1\.0' encoding='utf8'\?>", r"", nouveau_texte)
            nouveau_texte = re.sub(r"ns0?:", r"", nouveau_texte)
            nouveau_texte = re.sub(r" id=", r" xml:id=", nouveau_texte)
            nouveau_texte = re.sub(r"xmlns0 = \"http://www\.tei-c\.org/ns/1\.0\" ", r"", nouveau_texte)

            fichier_resultats.write(nouveau_texte)
            fichier_resultats.close()
            print(nouveau_texte)
            os.remove(id_texte + "_phrases.xml")
            if '1' in traitement.action or '4' in traitement.action:
                correction = input("Pensez à s'assurer que les fichiers produits sont corrects. Prête ? (O|N) ")
                if correction == 'O':
                    os.system("java -jar src/saxon9he.jar -xsl:src/alignementHTML.xsl -s:"+traitement.chemin_xml_compile+"/"
                          + id_texte + "_resultats.xml -o:"+traitement.chemin_html+"/pages/"+id_texte+'.html')


