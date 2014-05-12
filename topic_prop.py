### function to produce topic proportion of corpus
### reads in dictionary, lda, and raw text file to
### produce csv file of percentage of corpus that 
### belongs to each topic

import gensim
import pandas as pd
import re

def corpus_proportion(country): #country is the name of the files produced by the pipeline.py output

	#load the requisite files
	raw = open("%s.txt" %country).read()
	dictionary = gensim.corpora.Dictionary.load("dict_%s.dict" %country)
	lda = gensim.models.LdaModel.load("lda_%s.lda" %country)

	#remove %EOS between the documents from the raw file and tokenize
	raw = re.sub(r'\%EOS', '', raw)
	tokens = gensim.utils.simple_preprocess(raw)

	#convert to bag of words and get topic proportion from lda
	corpus_vec = dictionary.doc2bow(tokens)
	proportions = lda[corpus_vec]

	#write as a csv file for later use
	df = pd.DataFrame(dict(proportions), index = [0])
	df.T.to_csv("%s_proportion.csv" %country)
