import gensim, os, json, re
from gensim import models, corpora, similarities
import pandas as pd 
import nltk
from nltk.corpus import stopwords


def basic_lda(corpus, pass_num):
	remove_engsw(corpus)
	remove_oldesw(corpus)
	lda = models.LdaModel(corpus,  num_topics = 10, passes = pass_num)
	return lda

def remove_engsw(corpus):
        #Filters English stopwords from corpus using NLTKs stopword list

        from nltk.corpus import stopwords
        stop = stopwords.words('english')
        stop_ids = [corpus.dictionary.token2id[stopword] for stopword in stop if stopword in corpus.dictionary.token2id]
        corpus.dictionary.filter_tokens(stop_ids)

def iter_documents(top_directory):
        #Makes folder of documents iterable

        for root, dirs, files in os.walk(top_directory):
                for file in files:
                        document = open(os.path.join(root,file)).read()
                        yield gensim.utils.tokenize(document, lower=True)

class MyCorpus(object):
        # Make an iterable corpus from a folder containing
        # files of text.

  def __init__(self, top_dir):
        self.top_dir = top_dir
        self.dictionary = gensim.corpora.Dictionary(iter_documents(top_dir))
        self.dictionary.filter_extremes(no_below=1, keep_n=300000)
  def __iter__(self):
        for tokens in iter_documents(self.top_dir):
                yield self.dictionary.doc2bow(tokens)


stopwords = ['tooke', 'beene', 'certaine', 'gaue', 'whiche', 'vse', 'haue',
        'vnto', 'vs', 'hee', 'shal', 'hauing', 'vnder', 'vp', 'wil', 'theyr',
        'owne', 'themselues', 'sonne', 'euery', 'himselfe', 'giue', 'ouer',
        'wee','hym', 'foure', 'fiue', 'twentie', 'thei','euen','seuen', 'sixe',
        'sonnes', 'vpon', 'bee', 'againe', 'd', 'c', 'y', 'us', 'p', 'l', 'm',
	'e', 'de','chap','al','ye','est', 'la', 'le', 'qu', 'que', 'b', 'r', 
	'ut', 'en', 'il','i', 'unto', 'vnto', 'upon', 'ad']

def remove_oldesw(dict):
        # Function to remove Olde English stopwords from corpus

        stop_ids = []
        for i in range(0, len(stopwords)):
                if stopwords[i] in dict.token2id:
                        stop_ids.append(dict.token2id[stopwords[i]])
        dict.filter_tokens(stop_ids)
        dict.compactify()
        return dict
