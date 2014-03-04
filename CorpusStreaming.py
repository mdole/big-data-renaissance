import gensim, os, json, re
from gensim import corpora, models, similarities
from nltk.corpus import stopwords

#Iterate through documents
def iter_documents(top_directory):
       for root, dirs, files in os.walk(top_directory):
            for file in filter(lambda file: file.endswith(".json"), files):
                #document = json2doc(json.loads(open(os.path.join(root,file)).read()),document)
                document = open(os.path.join(root,file)).read()
		yield gensim.utils.tokenize(document, lower=True)

#Make an interable corpus
class MyCorpus(object):
    def __init__(self, top_dir):
	self.top_dir = top_dir
        self.dictionary = gensim.corpora.Dictionary(iter_documents(top_dir))
        self.dictionary.filter_extremes(no_below=1, keep_n=300000)
    def __iter__(self):
        for tokens in iter_documents(self.top_dir):
            yield self.dictionary.doc2bow(tokens)


