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
