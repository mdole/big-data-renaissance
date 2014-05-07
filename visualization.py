import gensim
from gensim import models, corpora
import pandas as pd
import nltk


#makes csv of phi matrix and unique words in order
def phi_words(corpus, lda, filename1, filename2):
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
	df.to_csv(filename1)
	#Get the tokens
	d = corpus.dictionary.token2id
        fr = pd.DataFrame(data = d, index=[0])
        frame = fr.T
	#sort tokens
        sorted_frame = frame.sort([0])
	sorted_frame.to_csv(filename2)
	
#makes a vector with frequency of token in text
def token_freq(textfile, csv, output_file):

	#pull in the word list from a csv file produced
	#by phi_words. Takes a little reformatting, so 
	#we should probably get this straight from LDA
	df = pd.DataFrame.from_csv(csv)
	df.reset_index( level=0, inplace=True )
	list_words = df.values.tolist()

	#create freq_dist object for text to create
	#frequency vector
	raw = open(textfile).read()
	tokens = gensim.utils.simple_preprocess(raw)
	text = nltk.Text(tokens) 
	vocab = text.vocab()
	freqs = []
	for i in range(0, len(list_words)):
		freqs.append(vocab[list_words[i][0]])
	output = pd.DataFrame(freqs)
	output.to_csv(output_file)

