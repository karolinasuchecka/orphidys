from stop_words import get_stop_words

stopwords = get_stop_words("french")

for word in stopwords:
    print (word)
