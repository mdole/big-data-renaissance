import nltk
from nltk.corpus import PlaintextCorpusReader

#Put corpus in a form that NLTK can read (reads documents in from folder)

def make_nltk(location):
	corpus_root = lcocation
	return PlaintextCorpusReader(corpus_root, '.*')

def do_concordance(word, corpus):
	for fileid in corpus.fileids():
		nltk.Text(corpus.words(fileid)).concordance(word)
		print fileid
