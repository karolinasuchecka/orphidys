import treetaggerwrapper
from stop_words import get_stop_words
import re
from urllib.request import urlopen
import bs4 as BeautifulSoup
import json
import codecs

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
             "quels", "quelle", "quelles", "sans", "soi"]


def lemmatisation(phrase, besoin):
    phrase = nettoyage_caracteres(phrase)
    #print ('phrase nettoyé', phrase)
    sorties = tagger.tag_text(phrase, notagdns=True)
    corpus_lemmes = {}
    i = 0
    if besoin == 'dictionnaire':
        for sortie in sorties:
            elements = sortie.split('\t')
            mot = elements[0]
            if mot not in corpus_lemmes.keys():
                # print(mot)
                lemme = elements[2]
                pos = elements[1]
                corpus_lemmes[mot] = [mot, lemme, pos]
    else:
        for sortie in sorties:
            elements = sortie.split('\t')
            mot = elements[0]
            #print(mot)
            lemme = elements[2]
            pos = elements[1]
            corpus_lemmes[i] = [mot, lemme, pos]
            i += 1

    return corpus_lemmes


def nettoyage_caracteres(phrase):
    """fonction de nettoyage de certains caractères
    appelée dans rechercheMotsCommuns et scoreReutilisation"""
    phrase = re.sub(r"’", "'", phrase)
    phrase = re.sub(r"[œ\x9c]", "oe", phrase)
    phrase = re.sub(r"…", "", phrase)
    phrase = re.sub(r"-", " ", phrase)
    phrase = re.sub(r"–", "", phrase)
    phrase = re.sub(r"_", "", phrase)
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


data = {}
with open("src/synonymes_CRISCO.json", 'r') as dico:
    data = json.load(dico)
dico.close()

def recherche_synonymes(lemme, niveau):
    if lemme in data.keys():
        i = 0
        synonymes = []
        if niveau == 1:
            while i <= 6 and i < len(data[lemme]['liste10'])-1:
                #print(data[lemme]['liste10'][i])
                synonyme = data[lemme]['liste10'][i]
                if re.search(" ", synonyme):
                    synonyme = re.sub(r" ", "_", synonyme)
                    #print ('ça marche --> ', synonyme)
                synonymes.append(synonyme)
                i += 2
        if niveau == 2:
            synonymes = data[lemme]['synonymes']
        return (synonymes)
    else:
        return 0

def recherche_antonymes(lemme):
    if lemme in data.keys() and 'antonymes' in data[lemme].keys():
        antonymes = data[lemme]['antonymes']
        return(antonymes)
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

