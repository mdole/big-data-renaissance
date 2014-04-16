from __future__ import division
import renaissance
import renaissance.iwillbreak as iwb
import gensim, os, json, re
from gensim import models, corpora, similarities
import pandas as pd
import nltk
from nltk.corpus import stopwords

# Much of this code is referenced from the online gensim tutorials 
# found here: http://radimrehurek.com/gensim/tutorial.html

# This function allows you to search the entire Renaissance corpus for a given term
# and do LDA on the documents that search returns

def do_lda(term, topic_num, pass_num):
	# Uses LDA to generate topics from all documents in corpus
	# containing 'term'. Uses PyLucene to search through entire corpus.

	search_results = renaissance.iwillbreak.do_search(term) 	
	corpus = renaissance.iwillbreak.MyCorpus(search_results) 	
	remove_oldesw(corpus.dictionary) 	
	lda = models.LdaModel(corpus, id2word = corpus.dictionary,num_topics = topic_num, passes = pass_num); #train  LDA model
	lda_corpus = lda[corpus] 			
	topics = lda.print_topics(topic_num) 
	return topics

# The next functions should be used when the documents you wish to use LDA 
# on are all contained in a folder

def doc_lda(filepath, topic_num, pass_num):
	# Uses LDA to generate topics from all documents 
	# in a given folder.
	
	corpus = MyCorpus(filepath)
	# Remove olde English stopwords
	remove_oldesw(corpus.dictionary)
	lda = models.LdaModel(corpus, id2word = corpus.dictionary, num_topics = topic_num, passes = pass_num); 
	lda_corpus = lda[corpus]
	topics = lda.print_topics(topic_num)
	return topics

def par_lda(filepath, topic_num, pass_num):
	# Uses LDA to generate topics from all paragraphs
	# that contain a certain placename. These are in a folder.
	
	corpus = MyCorpus(filepath)
	# These paragraphs are translated to modern English, so we can use standard stopword removal techniques
	remove_engsw(corpus)
	lda = models.LdaModel(corpus, id2word = corpus.dictionary, num_topics = topic_num, passes = pass_num);
        lda_corpus = lda[corpus]
        topics = lda.print_topics(topic_num)
        return topics

#Helper Functions

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

#List of Olde English stopwords, which is incomplete and based on words that arise in topics 

stopwords = ['tooke', 'beene', 'certaine', 'gaue', 'whiche', 'vse', 'haue', 
	'vnto', 'vs', 'hee', 'shal', 'hauing', 'vnder', 'vp', 'wil', 'theyr', 
	'owne', 'themselues', 'sonne', 'euery', 'himselfe', 'giue', 'ouer', 
	'wee','hym', 'foure', 'fiue', 'twentie', 'thei','euen','seuen', 'sixe',
	'sonnes', 'vpon', 'bee', 'againe']

def remove_oldesw(dict):
	# Function to remove Olde English stopwords from corpus
	
        stop_ids = []
        for i in range(0, len(stopwords)):
                if stopwords[i] in dict.token2id:
                        stop_ids.append(dict.token2id[stopwords[i]])
        dict.filter_tokens(stop_ids)
        dict.compactify()
        return dict

#The following functions are for clean-up and analysis

def topics_df(list):
        # Creates a pandas dataframe from a list of topics.
        # Assumes list contains weighted topics separated by '+'
        
        new_list = [[word for word in lst.split('+')] for lst in list]
        # Make dictionary from split topics
        dict = {}
        for i in range(1, len(list)+1):
                dict[i] = new_list[i-1]
        return pd.DataFrame(dict)

def remove_weights(list):
	# Removes the weights from each word in a topic
	# to enable faster analysis of the content of each topic
	
        for i in range(0, len(list)):
            for j in range(0, len(list[i])):
                list[i][j] = re.sub(r'0\.\d*\*', '', list[i][j])
        return list
	
def unique_words(list):
	# Returns number of distinct words in all topics from
	# the list of topics generated from the LDA model
	
	new_list = [[word for word in lst.split('+')] for lst in list]
	remove_weights(new_list)
	lst = []
	for i in range(0,len(list)):
		for j in range(0,10):
			new_list[i][j].strip
			lst.append(new_list[i][j])
	unique_words = set(lst)
	return unique_words

def lda_to_csv(ldallocation, filename, weights = True):
    # Takes the result of an LDA output and writes a csv to file
    # You have the option to remove weights for output clarity

    entries = [entry.split('+') for entry in ldallocation.print_topics(ldallocation.num_topics)]
    if weights == False:
	entries = [[re.sub(r'0.\d*\*', '', word) for word in entry] for entry in entries] 
    dictionary = {}
    for i in range(0, len(entries)):
	dictionary['topic ' + str(i + 1)] = entries[i]
    df = pd.DataFrame(dictionary)
    if len(df.index) == 10:
	df = df.transpose()
    df.to_csv(filename)  

def csv_to_list(filename):    
    #a helper function to get the csv files back to a list format

    df = pd.DataFrame.from_csv(filename)
    list_words = df.values.tolist()
    return list_words

def csv_filtered(input_file, output_file, cutoff = 0):
    # Takes in a csv file as input, and filters out all topics less than the cutoff value

    topics = csv_to_list(input_file)
    filtered_topics = [topic for topic in topics if weight_sum(topic) > cutoff]
    list_to_csv(filtered_topics, output_file)

def weight_sum(topic):
    # A function that sums the total weight of the first 10 words in a given topic

    weights = [float(re.sub(r'\*\w*', '', word)) for word in topic]
    total = sum(weights) 
    return total

def dispersion(topics, text):
    # Function to make dispersion plot from list of topics
    # The text input is an nltk.Text class of the corpus for the given topic
    words = [[re.sub(r'\d\.\d*\*', '', word).strip() for word in topic] for topic in topics]
    for i in range(0, len(words)):
	text.dispersion_plot(words[i])

#words in set1 not in set2
def percent_change(set1, set2):
	# Given the set of topics from two different corpuses, finds
	# the number of words in the first set that are not in the second
	# and divides by the total number of words in the first set to 
	# find a "percent change" from one set to another.

	unq1 = unique_words(set1)
	unq2 = unique_words(set2)
	diff = unq1.difference(unq2)
	return len(diff)/len(unq1)
	
	
