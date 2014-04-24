import gensim
from gensim import models, corpora
import pandas as pd


#makes csv of phi matrix and unique words in order
def phi_words(corpus, filename1, filename2):
        lda = models.LdaModel(corpus,num_topics=10)
        lda_corpus = lda[corpus]
        topics = lda.print_topics(10, topn=lda.num_terms);
        full_topics = [topic.split('+') for topic in topics]
        pairs = [[tuple(pair.split('*')) for pair in topic] for topic in full_topics]
        sorted_pairs = [sorted(pair, key=lambda pairr: int(pairr[1])) for pair in pairs]
        probs = [[word[0] for word in topic] for topic in sorted_pairs]
        dict = {}
        for i in range(1,11):
                dict[i] = probs[i-1]
        df = pd.DataFrame(dict)
        df.to_csv(filename1)
        d = corpus.dictionary.token2id
        fr = pd.DataFrame(data = d, index=[0])
        frame = fr.T
        sorted_frame = frame.sort([0])
        sorted_frame.to_csv(filename2)


#makes a vector with frequency of token in text
def token_freq(text, csv, output_file):
	
	#pull in the word list from a csv file produced
	#by phi_words. Takes a little reformatting, so 
	#we should probably get this straight from LDA
	df = pd.DataFrame.from_csv(csv)
	list_words = df.values.tolist()
	
	#create freq_dist object for text to create
	#frequency vector 
	vocab = text.vocab()
	freqs = []
	for i in range(0, len(list_words)):
		freqs.append(vocab[list_words[i][0]])
	output = pd.DataFrame(freqs)
	output.to_csv(output_file)


