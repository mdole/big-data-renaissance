import gensim, os, json, re
from gensim import models, corpora, similarities
import pandas as pd
import nltk
from nltk.corpus import stopwords

def get_model(country):
	corpus = MyCorpus('/Users/abbystevens/BigDataRenaissance/LDA/withsep/%s'%country)
	remove_engsw(corpus)
	remove_oldesw(corpus.dictionary)
	lda = models.LdaModel(corpus, num_topics = 10, passes = 10)
	#save stuff
	lda.save('lda_%s.lda' %country)
	corpus.dictionary.save('dict_%s.dict' %country)
	corpora.MmCorpus.serialize('mm_%s.mm' %country, corpus)
	vis_csv(corpus, lda, country)
	return lda

def vis_csv(corpus, lda, country):
	lda_corpus = lda[corpus]
        #get topics 
        pairs = lda.show_topics(10, topn=lda.num_terms, formatted = False);
        #sort by tokens
        sorted_pairs = [sorted(pair, key=lambda pairr: int(pairr[1])) for pair in pairs]    
        #get data for phi matrix
        probs = [[word[0] for word in topic] for topic in sorted_pairs]
        dict = {}
        for i in range(1,11):
                dict[i] = probs[i-1]
        df = pd.DataFrame(dict)
        df.to_csv('%sPhi.csv' %country)
        
	#Get the tokens 
        d = corpus.dictionary.token2id
        fr = pd.DataFrame(data = d, index=[0])
        frame = fr.T
        #sort tokens
        sorted_frame = frame.sort([0]) 
        sorted_frame.to_csv('%sTokens.csv' %country)
	
	#pull in the word list from a csv file produced
        #by phi_words. Takes a little reformatting, so
        #we should probably get this straight from LDA
	
        #df = pd.DataFrame.from_csv(csv)
        sorted_frame.reset_index( level=0, inplace=True )
        list_words = sorted_frame.values.tolist()

        #create freq_dist object for text to create
        #frequency vector
	textfile = '/Users/abbystevens/BigDataRenaissance/LDA/withsep/%s.txt' %country
        raw = open(textfile).read()
        tokens = gensim.utils.simple_preprocess(raw)
        text = nltk.Text(tokens)
        vocab = text.vocab()
        freqs = []
        for i in range(0, len(list_words)):
                freqs.append(vocab[list_words[i][0]])
        output = pd.DataFrame(freqs)
        output.to_csv('%sFreqs.csv'%country)
	

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

def remove_engsw(corpus):
        #Filters English stopwords from corpus using NLTKs stopword list

        from nltk.corpus import stopwords
        stop = stopwords.words('english')
        stop_ids = [corpus.dictionary.token2id[stopword] for stopword in stop if stopword in corpus.dictionary.token2id]
        corpus.dictionary.filter_tokens(stop_ids)

stopwords = ['tooke', 'beene', 'certaine', 'gaue', 'whiche', 'vse', 'haue',
        'vnto', 'vs', 'hee', 'shal', 'hauing', 'vnder', 'vp', 'wil', 'theyr',
        'owne', 'themselues', 'sonne', 'euery', 'himselfe', 'giue', 'ouer',
        'wee','hym', 'foure', 'fiue', 'twentie', 'thei','euen','seuen', 'sixe',
        'sonnes', 'vpon', 'bee', 'againe', 'd', 'c', 'y', 'us', 'p', 'l', 'm',
        'e', 'de','chap','al','ye','est', 'la', 'le', 'qu', 'que', 'b', 'r',
        'ut', 'en', 'il','i', 'unto', 'vnto', 'upon', 'ad', 'eos']

def remove_oldesw(dict):
        # Function to remove Olde English stopwords from corpus

        stop_ids = []
        for i in range(0, len(stopwords)):
                if stopwords[i] in dict.token2id:
                        stop_ids.append(dict.token2id[stopwords[i]])
        dict.filter_tokens(stop_ids)
        dict.compactify()
        return dict
