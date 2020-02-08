from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import re

def stopWord_removal(sentence):

    stop_words = set(stopwords.words('english'))
    word_tokens = word_tokenize(sentence)
    filtered_sentence = [w for w in word_tokens if not w in stop_words]
    filtered_sentence = []

    for w in word_tokens:
        if w not in stop_words:
            filtered_sentence.append(w)

    new_sentence = ' '.join(word for word in filtered_sentence)

    lamatized_sentence = cleaning(new_sentence)
    
    return lamatized_sentence

#  every punctuation and special characters(if any)
def cleaning(sentences):
    
    lemmatizer = WordNetLemmatizer()
    words = []
    clean_words = []
    t_sentences = word_tokenize(sentences)

    for s in t_sentences:
        clean = re.sub(r'[^ a-z A-Z 0-9]', " ", s)
        # print(clean)
        clean_words.append(str(clean))
    
    #for clean_sentence in clean_words:

        #w = word_tokenize(clean_sentence)

        #lemmatizing
    for i in clean_words:
        words.append(lemmatizer.lemmatize(i.lower()))

    new_words = ' '.join(word for word in words)
    
    print("new_words preprocess:",new_words)
    return new_words


# stopWord_removal(
#     "Hi, I am gourab dasgupta. Tell me about Jeff Bezos from wikipedia")
