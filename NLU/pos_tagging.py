import nltk


def finding_nouns(search_query):

    is_noun = lambda pos: pos[:2] == 'NN'

    # do the nlp stuff
    tokenized = nltk.word_tokenize(search_query)
    nouns = [word for (word, pos) in nltk.pos_tag(tokenized) if is_noun(pos)]

    print (nouns)
    

    return nouns

#finding_nouns("tell me about Bill Gates from Wikipedia. I am gourab dasgupta. I slept for 7 hours")
