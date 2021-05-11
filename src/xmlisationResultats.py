import traitementsTal

__auteur__ = "Karolina Suchecka"
__date__ = "19/12/19"

"""
Script qui xmlise les résultats des logiciels de détection des réutilisations. Le XML produit est conforme au standard
XML:TEI. Annotation au niveau des phrases et au niveau des mots (les identifiants, les lemmes, les pos et les synonymes)
"""

"""
Fonction qui enrichi chaque phrase de la structure XML adaptée
______________________Étapes_________________________________
1. Lemmatisation des phrases
2. Pour chaque éléments de la phrase (mot ou ponctuation), on crée un élément adapté (<w> pour mots et <pc> pour la
ponctuation.
3. On soumet chaque élément à la détection des mots faibles. Quatre cas de figure : 1. mot faible : on ajoute seulement
le lemme et le pos, 2. ponctuation faible, on ajoute @force à la valeur "weak", 3. ponctuation forte : on ajoute @force
à la valeur "strong", 4. mot fort : on ajoute aussi les quatre synonymes les plus fréquents (selon crisco). Pour chaque
élément, on ajoute un identifiant (identifiant de la phrase + rang du mot) et @n à la valeur du rang.
4. On ajoute chaque structuration à l'élément XML_ligne qu'on ajoute ensuite au dictionnaire xmlisés qui sera retourné
à la fin de cette fonction
"""

def xmlisation_phrases(dictionnaire_resultats, min_mots):
    dictionnaire_xmlise = {}
    for identifiant, texte in dictionnaire_resultats.items():
        #print('texte : ', texte)
        texte_propre = traitementsTal.nettoyage_caracteres(texte)
        lignes_tagger = traitementsTal.lemmatisation(texte_propre, "fichier")
        #print ('lignes')
        #print (lignes_tagger)
        if len(lignes_tagger) > min_mots:
            lignes_tagger = lignes_tagger.values()
            rang_mot = 0
            XML_ligne = ""
            for ligne in lignes_tagger:

                mot = ligne[0]
                lemme = ligne[1]
                pos = ligne[2]
                rang_mot += 1
                indice_stopwords, type_stopword = traitementsTal.detecte_stopwords(mot, lemme, pos)
                if indice_stopwords == 1:
                    XML_ligne += "<w xml:id=\"" + identifiant + "_" + str(rang_mot) + "\" n=\"" + str(rang_mot) + "\" lemma=\"" + lemme + "\" pos=\"" + pos + "\""
                    synonymes = traitementsTal.recherche_synonymes_proches(lemme)
                    #print ("synos xmlisation")
                    #print (synonymes)
                    if synonymes != 0 and synonymes != None and len(synonymes) != 0 :
                            #print ("ok")
                            XML_ligne += " sameAs=\""
                            for synonyme in synonymes:
                                XML_ligne += synonyme + ' '
                            XML_ligne = XML_ligne[:-1] + "\""
                            #print(XML_ligne)
                    base_morphologique = traitementsTal.recherche_base_morpho(lemme)
                    if base_morphologique != 0:
                        XML_ligne += " source=\""+base_morphologique+"\""
                    antonymes = traitementsTal.recherche_antonymes(lemme)
                    if antonymes !=0 and antonymes != None and len(antonymes) != 0:
                        XML_ligne += " exclude=\""
                        for antonyme in antonymes[0:3]:
                            XML_ligne += antonyme + ' '
                        XML_ligne = XML_ligne[:-1] + "\""
                    XML_ligne += ">" + mot + "</w> "
                elif indice_stopwords == 0:
                    if type_stopword == "weak":
                        XML_ligne += "<pc xml:id=\"" + identifiant + "_" + str(rang_mot) + "\" n=\"" + str(rang_mot) +"\" force=\"weak\">" + mot + "</pc> "
                    elif type_stopword == "strong":
                        XML_ligne += "<pc xml:id=\"" + identifiant + "_" + str(rang_mot) + "\" n=\"" + str(rang_mot) + "\" force=\"strong\">" + mot + "</pc> "
                    elif type_stopword == "stopword":
                        XML_ligne += "<w xml:id=\"" + identifiant + "_" + str(rang_mot) + "\" n=\"" + str(rang_mot) + "\" lemma=\"" + lemme + "\" pos=\"" + pos + "\">" + mot + "</w> "
            #print("ligne finale : " + XML_ligne)

            dictionnaire_xmlise[identifiant] = XML_ligne
    return (dictionnaire_xmlise)


"""
Fonction qui xmlise les textes à partir des résultats des logiciels
_____Étapes______
1. Pour chaque auteur présent dans les résultats, on crée un div avec l'identifiant de l'auteur
2. On insère chaque phrase de cette auteur dans laquelle on a détecté une correspondance (pour les résultats textPAIR
et Galaxies, on ajoute avant un <seg> avec l'identifiant de l'extrait détecté (parce que la correspondance a été établie
sur plusieurs phrases)
3. Chaque phrase à une @xml:id avec son identifiant et @corresp avec l'identifiant de la correspondance
"""
def xmlisation_textes(id_auteurs_corpus, phrases_xmlises, liens_source, liens_target, id_auteurs_resultats):
    XML_final = '<body>'
    # traitement Tracer (liens targets vides et id_auteurs resultats aussi : une seule table des liens)
    if liens_target == '' and id_auteurs_resultats =='':
        autors = id_auteurs_corpus
    else:
        autors = id_auteurs_resultats
    for autor in set(autors.keys()):
        div_auteur = "<div xml:id=\"" + autor + "\">\n"

        # traitement Tracer
        if liens_target == '' and id_auteurs_resultats == '':
            for source, targets in liens_source.items():
                if source in id_auteurs_corpus[autor] and source in phrases_xmlises.keys():
                    texte_annote = phrases_xmlises[source]
                    annotation_phrase = "<s xml:id=\"" + source + "\" corresp=\""
                    indice_corresp = 0
                    for target in targets:
                        if target in phrases_xmlises.keys():
                            annotation_phrase += target + " "
                            indice_corresp = 1
                    if indice_corresp == 1:
                        annotation_phrase = annotation_phrase[:-1] + "\">"
                        annotation_phrase += texte_annote + "</s>\n"
                        div_auteur += annotation_phrase
        # traitement TextPAIR et Galaxies
        else:
            liste_id_passage = autors[autor]
            for id_passage in liste_id_passage:  # idTextPair
                auteur_target = trouve_auteur(liens_target[id_passage][0], id_auteurs_corpus)
                if auteur_target == autor:
                    auteur_target = trouve_auteur(liens_source[id_passage][0], id_auteurs_corpus)
                div_auteur += "<seg n=\"" + id_passage + "\" xml:id=\""+id_passage+"_"+autor+"\" corresp=\""+id_passage+\
                              "_"+auteur_target+"\">\n"
                for lien_source in liens_source[id_passage]:  # tableau idPhrase
                    if lien_source in id_auteurs_corpus[autor] and lien_source in phrases_xmlises.keys():
                        texte_annote = phrases_xmlises[lien_source]
                        annotation_phrase = "<s xml:id=\"" + lien_source + "\">"+texte_annote + "</s>\n"
                        div_auteur += annotation_phrase

                for lien_target in liens_target[id_passage]:  # tableau idPhrase
                    if lien_target in id_auteurs_corpus[autor] and lien_target in phrases_xmlises.keys():
                        texte_annote = phrases_xmlises[lien_target]
                        annotation_phrase = "<s xml:id=\"" + lien_target + "\">"+texte_annote+"</s>"
                        div_auteur += annotation_phrase

                div_auteur += "</seg>\n"
        div_auteur += "</div>\n"
        XML_final += div_auteur
    XML_final += "</body>"
    return(XML_final)

def trouve_auteur(id_target, dico_auteurs):
    for auteur, liste_id in dico_auteurs.items():
        if id_target in liste_id:
            return auteur
