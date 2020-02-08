from nltk import word_tokenize, pos_tag, ne_chunk

Q1 = "where is Texas ?"
A1 = "It is in USA."
Q2 = "where is California?"
A2 = "It is in USA"
Q3 = "where is NASA?"
A3 = "It is in USA."
Q4 = "who is Queen Elizabeth II?"
A4 = "Queen of England"
Q5 = "who is Donald Trump?"
A5 = "President of USA."

print(ne_chunk(pos_tag(word_tokenize(Q1))))
print(ne_chunk(pos_tag(word_tokenize(Q2))))
print(ne_chunk(pos_tag(word_tokenize(Q3))))
print(ne_chunk(pos_tag(word_tokenize(Q4))))
print(ne_chunk(pos_tag(word_tokenize(Q5))))