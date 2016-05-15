""" Assignment 2
"""
import abc
from collections import defaultdict
import math


import index


def idf(term, index):
    """ Compute the inverse document frequency of a term according to the
    index. IDF(T) = log10(N / df_t), where N is the total number of documents
    in the index and df_t is the total number of documents that contain term
    t.

    Params:
      terms....A string representing a term.
      index....A Index object.
    Returns:
      The idf value.

    >>> idx = index.Index(['a b c a', 'c d e', 'c e f'])
    >>> idf('a', idx) # doctest:+ELLIPSIS
    0.477...
    >>> idf('d', idx) # doctest:+ELLIPSIS
    0.477...
    >>> idf('e', idx) # doctest:+ELLIPSIS
    0.176...
    """
    
    df = float(index.doc_freqs[term])
    N = float(len(index.documents))
    
    try:
    	return (math.log10(N/df))
    except:
    	return (0.0)
    

class ScoringFunction:
    """ An Abstract Base Class for ranking documents by relevance to a
    query. """
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def score(self, query_vector, index):
        """
        Do not modify.

        Params:
          query_vector...dict mapping query term to weight.
          index..........Index object.
        """
        return


class RSV(ScoringFunction):
    """
    See lecture notes for definition of RSV.

    idf(a) = log10(3/1)
    idf(d) = log10(3/1)
    idf(e) = log10(3/2)
    >>> idx = index.Index(['a b c', 'c d e', 'c e f'])
    >>> rsv = RSV()
    >>> rsv.score({'a': 1.}, idx)[1]  # doctest:+ELLIPSIS
    0.4771...
    """
    def score(self, query_vector, index):
    
        RSV_DICT = defaultdict(lambda:0.0)  
        
        for doc_word, tf_val_tuple in index.index.items():	
        	if doc_word in query_vector.keys():
        		for doc_id, tf_val in tf_val_tuple:
        			
        			RSV_DICT[doc_id] += idf(doc_word, index)
        			
       	
       	return RSV_DICT
       	
    def __repr__(self):
        return 'RSV'


class BM25(ScoringFunction):
    """
    See lecture notes for definition of BM25.

    log10(3) * (2*2) / (1(.5 + .5(4/3.333)) + 2) = log10(3) * 4 / 3.1 = .6156...
    >>> idx = index.Index(['a a b c', 'c d e', 'c e f'])
    >>> bm = BM25(k=1, b=.5)
    >>> bm.score({'a': 1.}, idx)[1]  # doctest:+ELLIPSIS
    0.61564032...
    """
    def __init__(self, k=1, b=.5):
        self.k = k
        self.b = b
        
    def score(self, query_vector, index):
    
        BM25_Score = defaultdict(lambda:0)
        
        for each_query, query_idf in query_vector.items():
        
            if each_query in index.index.keys():
        	
                for lists in index.index[each_query]:
        			
                    LD = index.doc_lengths[lists[0]]
                    U = index.mean_doc_length
                    idf_weight = float( idf(each_query, index) )
                    try:
                    	B = (1 - self.b) + (self.b * LD/U)
                    except:
                    	B = (1 - self.b)
        			
                    numerator = (self.k + 1.0) * float(lists[1])
                    denominator = self.k * B + lists[1]
                    try:
                    	bm_value = float(idf_weight * numerator/denominator)
                    except ZeroDivisionError:
                    	bm_value = 0.0
        		    
                    BM25_Score[lists[0]] += bm_value

        
        return BM25_Score
		
		
    def __repr__(self):
        return 'BM25 k=%d b=%.2f' % (self.k, self.b)


class Cosine(ScoringFunction):
    """
    See lecture notes for definition of Cosine similarity.  Be sure to use the
    precomputed document norms (in index), rather than recomputing them for
    each query.

    >>> idx = index.Index(['a a b c', 'c d e', 'c e f'])
    >>> cos = Cosine()
    >>> cos.score({'a': 1.}, idx)[1]  # doctest:+ELLIPSIS
    0.792857...
    """
    def score(self, query_vector, index):
        
        scores_dict = defaultdict(lambda:0.0)
        
        for each_query, query_idf in query_vector.items():
        
        	if each_query in index.index.keys():
        	
        		for lists in index.index[each_query]:
        			
        			tf_val = lists[1]
        			doc_id = lists[0]
        			
        			tf_weight = (1.0 + math.log10(tf_val) ) * idf(each_query, index)
        				
        			scores_dict[doc_id] += (tf_weight * query_idf)
        
        for doc_id in scores_dict:
        	try:
        		scores_dict[doc_id] /= index.doc_norms[doc_id]
        	except ZeroDivisionError:
        		scores_dict[doc_id] = 0.0
        
        
        return scores_dict
	
    def __repr__(self):
        return 'Cosine'
        
        
        
