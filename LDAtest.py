From nltk.corpus import stopwords
from gensim import corpora, models, similarities
import json
import pandas as pd
import re

#load some documents from the JSON files. You'll have to be working in raw
#folder in order for this to work. 
doc1 = json.loads(open('A10228_PURCHAS_Purchas his pilgrimage. Or Relations of the world and the_content.json').read())

doc2 = json.loads(open('A10226_PURCHAS_The kings towre and triumphant arch of London. A sermon_content.json').read())

doc3 = json.loads(open("A10235_HEYWOOD_A true relation, of the lives and deaths of two most famous_content.json").read())

doc4 = json.loads(open('A10246_QUARLES_Argalus and Parthenia The argument of ye history. Written_content.json').read())

doc5 = json.loads(open('A10251_QUARLES_Diuine fancies digested into epigrammes, meditations, and_content.json').read())

#----------------------------------------------------------------------------
#Define some functions that will put the documents in a form such that gensim
#can easily work with them

#This function takes a single json file and puts all of the content into a
#single string. It then adds that string to the list of documents in our corpus.
def json2doc(json, documents):
    text = ''
    for i in range(0,len(json)):
        for j in range(0, len(json[i]['content'])):
            text = text + ' ' + json[i]['content'][j]
    documents.append(text)
    return documents

#use this function to create a list of documents. Is there a way to make
#this that requires less repitition?
documents = []
documents = json2doc(doc1, documents)
documents = json2doc(doc2, documents)
documents = json2doc(doc3, documents)
documents = json2doc(doc4, documents)
documents = json2doc(doc5, documents)

#now we remove stop words and tokenize. This takes a minute
texts = [[word for word in document.lower().split() if word not in stopwords.words('english')] for document in documents]

#throw everything into a dictionary and then filter out unfrequent words
dictionary = corpora.Dictionary(texts)
dictionary.filter_extremes(no_below = 2)

#with the new dictionary, convert the corpus
corpus = [dictionary.doc2bow(text) for text in texts]

lda = models.LdaModel(corpus, id2word=dictionary, num_topics = 100)
lda_corpus = lda[corpus]
for doc in lda_corpus:
    print doc


pdocs = lda.print_topics(100)
new_pdocs = [[word for word in pdoc.split('+')] for pdoc in pdocs]
pandas_dict = {}
for i in range(1, 101):
    pandas_dict[str(i)] = new_pdocs[i-1]


#transform dictionary to a dataframe and export as a csv file
#change the directory path accordingly
topics_df = pd.DataFrame(pandas_dict)
topics_df.to_csv()

def remove_weights(list):
	for i in range(0, len(list)):
	    for j in range(0, len(list[i])):
    		list[i][j] = re.sub(r'0\.\d*\*', '', list[i][j])
	return list 



