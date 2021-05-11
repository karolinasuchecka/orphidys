import treetaggerwrapper
from stop_words import get_stop_words
import re
from urllib.request import urlopen
import bs4 as BeautifulSoup
import json
import csv
import os
import codecs
from actuariat_python.data import wolf_xml
from actuariat_python.data import enumerate_wolf_synonyms

tagger = treetaggerwrapper.TreeTagger(TAGLANG='fr')
stopwords = ["au", "aux", "avec", "ce", "ces", "dans", "de", "des", "du", "elle", "en", "et", "eux", "il", "je", "la",
             "le", "leur", "lui", "ma", "mais", "me", "même", "mes", "moi", "mon", "ne", "nos", "notre", "nous", "on",
             "ou", "par", "pas", "pour", "qu'", "que", "qui", "sa", "se", "ses", "son", "sur", "ta", "te", "tes", "toi",
             "ton", "tu", "un", "une", "vos", "votre", "vous", "c'", "d'", "j'", "l'", "à", "m'", "n'", "s'", "t'", "y",
             "été", "étée", "étées", "étés", "étant", "suis", "es", "est", "sommes", "êtes", "sont", "serai", "seras",
             "sera", "serons", "serez", "seront", "serais", "serait", "serions", "seriez", "seraient", "étais", "était",
             "étions", "étiez", "étaient", "fus", "fut", "fûmes", "fûtes", "furent", "sois", "soit", "soyons", "soyez",
             "soient", "fusse", "fusses", "fût", "fussions", "fussiez", "fussent", "ayant", "eu", "eue", "eues", "eus",
             "ai", "as", "avons", "avez", "ont", "aurai", "auras", "aura", "aurons", "aurez", "auront", "aurais",
             "aurait", "aurions", "auriez", "auraient", "avais", "avait", "avions", "aviez", "avaient", "eut", "eûmes",
             "eûtes", "eurent", "a","aie", "aies", "ait", "ayons", "ayez", "aient", "eusse", "eusses", "eût", "eussions",
             "eussiez", "eussent", "ceci", "cela", "celà", "cet", "cette", "ici", "ils", "les", "leurs", "quel",
             "quels", "quelle", "quelles", "sans", "soi", "où", "ni", "là", "avoir", "être", "aussi", "quand", "plus",
             "tandis", "si", "ô", "alors", "quand", "tel" ]

lexique = {}
with open('lexique_spec.txt', newline="") as f_lexique_spec:
    lexique_spec = csv.reader(f_lexique_spec, delimiter='\t')
    for ligne in lexique_spec:
        if ligne[0] not in lexique.keys():
            lexique[ligne[0]] = ligne

lemmes = {}
with open('lemmes.txt', newline="") as f_lemmes_spec:
    lemmes_spec = csv.reader(f_lemmes_spec, delimiter='\t')
    for ligne in lemmes_spec:
        if ligne[0] not in lemmes.keys():
            lemmes[ligne[0]] = ligne

bases_morphologiques = {}
with open('morphologie.csv', newline="") as f_morpho:
    morpho = csv.reader(f_morpho, delimiter=';')
    for ligne in morpho:
        if ligne[0] not in bases_morphologiques.keys():
            bases_morphologiques[ligne[0]] = ligne[1]
        elif (len(ligne[1]) < len(bases_morphologiques[ligne[0]])) or (len(ligne[1]) == len(bases_morphologiques[ligne[0]])
                                                                    and min(ligne[1], bases_morphologiques[ligne[0]]) == ligne[1]):
            bases_morphologiques[ligne[0]] = ligne[1]


nouveaux_mots = {}

def lemmatisation(phrase, besoin):
    phrase = nettoyage_caracteres(phrase)
    #print ('phrase nettoyé', phrase)
    sorties = tagger.tag_text(phrase, notagdns=True)
    corpus_lemmes = {}

    i = 0
    if besoin == 'dictionnaire' or besoin == 'fichier':
        for sortie in sorties:
            elements = sortie.split('\t')
            mot = elements[0]
            if "-même" in mot:
                corpus_lemmes[i-1] = [corpus_lemmes[i-1][0]+mot, corpus_lemmes[i-1][1]+mot, 'PRO:PER']
                #print(corpus_lemmes[i-1])
            else:
                mots_tokenises = tokenization_mots(mot)
                for mot in mots_tokenises:
                    indice_lexique = 0
                    if mot in lexique.keys():
                        indice_lexique = 1
                    elif mot not in lemmes.keys():
                        nouveaux_mots[mot] = sortie

                    if len(mots_tokenises) == 1 and indice_lexique == 0:
                        #print(mot)
                        lemme = elements[2]
                        pos = elements[1]
                    elif len(mots_tokenises) > 1 and indice_lexique == 0 and mot in lemmes.keys():
                        #print(mots_tokenises)
                        #   print(mot)
                        lemme = lemmes[mot][2]
                        pos = lemmes[mot][1]
                    elif mot in nouveaux_mots.keys() and len(mots_tokenises) > 1:
                        #print(mots_tokenises)
                        #print(mot)
                        lemme = mot
                        pos = elements[1]
                    elif indice_lexique == 1:
                        #print(mots_tokenises)
                        #print(mot)
                        lemme = lexique[mot][2]
                        pos = lexique[mot][1]
                    else:
                        #print("Cas de figure non pris en compte : ")
                        #print(mot)
                        lemme = ''
                        pos = ''


                    corpus_lemmes[i] = [mot, lemme, pos]
                    i+=1
    else:
        for sortie in sorties:
            elements = sortie.split('\t')
            mot = elements[0]
            if mot in lexique.keys():
                elements = lexique[mot]
            elif mot not in lemmes.keys():
                nouveaux_mots[mot] = sortie
            #print(mot)
            lemme = elements[2]
            pos = elements[1]
            corpus_lemmes[i] = [mot, lemme, pos]
            i += 1

    return corpus_lemmes

def tokenization_mots(mot):
    if "-" in mot:
        print(mot)
        pronom = mot.split('-')[-1]
        print(pronom)
        if mot in lexique.keys():
            return ([mot])
        elif "'" in pronom:
            pronom1 = pronom.split("'")[0]+"'"
            pronom2 = pronom.split("'")[-1]
            print([mot.split("-")[1], pronom1, pronom2])
            return([mot.split("-")[1], pronom1, pronom2])
        elif pronom in lemmes.keys() and ("PRO:" in lemmes[pronom][1] or "DET:" in lemmes[pronom][1]):
            if mot.split('-')[-2] == "t":
                pronom = '-t-' + pronom
            else:
                pronom = '-' + pronom
            #print(mot, pronom)
            print([mot.split("-")[0], pronom])
            return([mot.split("-")[0], pronom])
        else:
            print([mot])
            return([mot])
    elif "'" in mot:
        conj = mot.split("'")[0]+"'"
        if mot in lemmes.keys():
            return ([mot])
        elif conj in lemmes.keys():
            if len(mot.split("'")[-1]) > 1:
                print ([conj, mot.split("'")[-1]])
                return([conj, mot.split("'")[-1]])
            else:
                print ([mot])
                return ([mot])
        else:
            print([mot])
            return ([mot])
    else:
        return ([mot])


def ajout_nouveaux_mots():
    mots_presents = {}
    print (nouveaux_mots)
    with open("src/mots_a_traiter.txt", "r") as f_nouveaux_mots:
        mots = csv.reader(f_nouveaux_mots, delimiter='\t')
        for ligne in mots:
            if ligne[0] not in mots_presents.keys():
                mots_presents[ligne[0]] = ligne
    f_nouveaux_mots.close()

    for nouveau_mot in nouveaux_mots.keys():
        if nouveau_mot not in mots_presents.keys() and nouveau_mot not in stopwords:
            mots_presents[nouveau_mot] = nouveaux_mots[nouveau_mot]

    f_nouveaux_mots = open("src/mots_a_traiter.txt", "w")
    for mot_present,ligne in mots_presents.items():
        print(ligne)
        if isinstance(ligne, list):
            ligne_a_imprimer = ''
            for item in ligne:
                ligne_a_imprimer += item+'\t'
            ligne_a_imprimer = ligne_a_imprimer[:-1]
            f_nouveaux_mots.write(ligne_a_imprimer+'\n')
        elif isinstance(ligne, str):
            f_nouveaux_mots.write(ligne+'\n')
    f_nouveaux_mots.close()




def nettoyage_caracteres(phrase):
    """fonction de nettoyage de certains caractères
    appelée dans rechercheMotsCommuns et scoreReutilisation"""
    phrase = re.sub(r"’", "'", phrase)
    phrase = re.sub(r"[œ\x9c]", "oe", phrase)
    #phrase = re.sub(r"…", "", phrase)
    #phrase = re.sub(r"-", " ", phrase)
    #phrase = re.sub(r"–", "", phrase)
    #phrase = re.sub(r"_", "", phrase)
    phrase = re.sub(r"\xa0", " ", phrase)
    pos = phrase.find("|")  # position du caractère | : suppression des alternatives
    if pos != -1:
        phrase = phrase[:pos]
    return phrase

def nettoyage_phrases(phrase):
    phrase = re.sub('\s$', '', phrase)
    phrase = re.sub(r'[\xa0\t\s]+', ' ', phrase)
    phrase = re.sub(r'(\s[,.’])', '\1', phrase)
    phrase = nettoyage_caracteres(phrase)
    phrase = accents_applatis(phrase)
    phrase = phrase.lower()
    return(phrase)

def accents_applatis(chaine):
    chaine = chaine.lower()
    chaine = re.sub(r'[èéêë]', 'e', chaine)
    chaine = re.sub(r'[àâä]', 'a', chaine)
    chaine = re.sub(r'[ôö]', 'o', chaine)
    chaine = re.sub(r'[üû]', 'u', chaine)
    chaine = re.sub(r'[ïî]', 'i', chaine)
    chaine = re.sub(r'ç', 'c', chaine)
    chaine = re.sub(r"[œ\x9c]", "oe", chaine)
    chaine = re.sub('[\\xad\\ufeff\\u2014\\xff\\xe6]', '', chaine)
    return (chaine)

def detecte_stopwords(mot, lemme, pos):
    if lemme in stopwords:
        return 0, "stopword"
    elif mot in stopwords:
        return 0, "stopword"
    elif pos == 'SENT':
        return 0, "strong"
    elif pos == 'PUN' or pos == "PUN:cit":
        return 0, "weak"
    else:
        return 1, ""

with open("synonymes_CRISCO.json", 'r') as dico:
    crisco = json.load(dico)
dico.close()

def lancement_wolf():


    if not os.path.exists("wolf-1.0b4.xml"):
        raise FileNotFoundError("wolf-1.0b4.xml")
    if os.stat("wolf-1.0b4.xml").st_size < 3000000:
        raise FileNotFoundError("Size of 'wolf-1.0b4.xml' is very small: {0}".format(os.stat("wolf-1.0b4.xml").st_size))

    wolf = {}
    for line, syn in enumerate(enumerate_wolf_synonyms("wolf-1.0b4.xml")):
        if line % 10000 == 0: print("line", line, "allsyn", len(wolf))
        clean = [_.lower() for _ in syn if " " not in _]
        if len(clean) > 1:
            for word in clean:
                if word not in wolf:
                    wolf[word] = set(clean)
                    continue
                else:
                    for cl in clean:
                        wolf[word].add(cl)
    return(wolf)

def recherche_synonymes_proches(lemme):
    if lemme in crisco.keys():
        i = 0
        synonymes = []
        while i <= 6 and i < len(crisco[lemme]['liste10'])-1:
            #print(data[lemme]['liste10'][i])
            synonyme = crisco[lemme]['liste10'][i]
            if re.search(" ", synonyme):
                synonyme = re.sub(r" ", "_", synonyme)
                #print ('ça marche --> ', synonyme)
            synonymes.append(synonyme)
            i += 2
        return (synonymes)
    else:
        return 0

def recherche_synonymes_eloignes(lemme, wolf):
    if lemme in crisco.keys():
        synonymes = crisco[lemme]['synonymes']
        if lemme in wolf.keys():
            synos_Wolf = wolf[lemme]
            for syno in synos_Wolf:
                if syno not in synonymes:
                    #print ("syno Wolf -->" + syno)
                    synonymes.append(syno)
        return (synonymes)
    else:
        return 0

def recherche_antonymes(lemme):
    if lemme in crisco.keys() and 'antonymes' in crisco[lemme].keys():
        antonymes = crisco[lemme]['antonymes']
        return(antonymes)
    else:
        return 0


def recherche_base_morpho(lemme):
    if lemme in bases_morphologiques.keys():
        return(bases_morphologiques[lemme])
    else:
        return 0

    # requete = accents_applatis(lemme)
    # if niveau == 1:
    #     if requete not in dictionnaire_synonymes_base.keys():
    #         dictionnaire_synonymes_base[requete] = []
    #         crisco = urlopen("https://crisco2.unicaen.fr/des/synonymes/" + requete).read()
    #         soup = BeautifulSoup.BeautifulSoup(crisco, features='html.parser')
    #         table_synonymes = soup.find('table', attrs={"border": u"1", "cellpadding": "0", "cellspacing": "0"})
    #         print ("table synos : ")
    #         print (table_synonymes)
    #         if table_synonymes == "" or table_synonymes == None or len(table_synonymes) == 0 :
    #             dictionnaire_synonymes_base[requete] = 0
    #             return 0
    #         else:
    #             table_synonymes = table_synonymes.findAll('a')
    #             synonymes = []
    #             for synonyme in table_synonymes[0:3]:
    #                 synonyme = re.sub(r"\s", "", synonyme.contents[0])
    #                 synonymes.append(synonyme)
    #             print ("synos")
    #             print (synonymes)
    #             dictionnaire_synonymes_base[requete] = synonymes
    #             return (synonymes)
    #     elif requete in dictionnaire_synonymes_base.keys():
    #         return dictionnaire_synonymes_base[requete]
    # elif niveau == 2:
    #     if requete not in dictionnaire_synonymes_elargis.keys():
    #         dictionnaire_synonymes_elargis[requete] = []
    #         crisco = urlopen("https://crisco2.unicaen.fr/des/synonymes/" + requete).read()
    #         soup = BeautifulSoup.BeautifulSoup(crisco, features='html.parser')
    #         table_synonymes = soup.find('div', attrs={"id": u"synonymes"})
    #         if table_synonymes == "" or table_synonymes == None or len(table_synonymes) == 0 :
    #             dictionnaire_synonymes_elargis[requete] = 0
    #             return 0
    #         else:
    #             table_synonymes = str(table_synonymes)
    #             commentaire = re.split('<!-- Fin titre \(vedette \+ nb de synonymes\)-->', table_synonymes)[1]
    #             commentaire = re.split('<!--Liste des antonymes-->', commentaire)[0]
    #             table_synonymes = re.findall(r'>(.+?)</a>', commentaire)
    #             dictionnaire_synonymes_elargis[requete] = table_synonymes
    #             return(table_synonymes)
    #     elif requete in dictionnaire_synonymes_elargis.keys():
    #         return dictionnaire_synonymes_elargis[requete]

