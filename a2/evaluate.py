""" Assignment 2
"""
import abc

import numpy as np


class EvaluatorFunction:
    """
    An Abstract Base Class for evaluating search results.
    """
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def evaluate(self, hits, relevant):
        """
        Do not modify.
        Params:
          hits...A list of document ids returned by the search engine, sorted
                 in descending order of relevance.
          relevant...A list of document ids that are known to be
                     relevant. Order is insignificant.
        Returns:
          A float indicating the quality of the search results, higher is better.
        """
        return


class Precision(EvaluatorFunction):

    def evaluate(self, hits, relevant):
        """
        Compute precision.

        >>> Precision().evaluate([1, 2, 3, 4], [2, 4])
        0.5
        """
        tp = 0.0
        fp = 0.0
        
        for val1 in hits:
        	
        	if val1 in relevant:
        		tp += 1.0

        
        try:
        	prec = float(tp/len(hits))
        except:
        	prec = 0.0
        
        return prec
        
    def __repr__(self):
        return 'Precision'


class Recall(EvaluatorFunction):

    def evaluate(self, hits, relevant):
        """
        Compute recall.

        >>> Recall().evaluate([1, 2, 3, 4], [2, 5])
        0.5
        """
        
        tp = 0.0
        fn = 0.0
        
        for val1 in relevant:
        	
        	if val1 in hits:
        		tp += 1.0
        		        
        try:
        	recal = float( tp/len(relevant) )
        except:
        	recal = 0.0
        
        return recal
        
        
    def __repr__(self):
        return 'Recall'


class F1(EvaluatorFunction):
    def evaluate(self, hits, relevant):
        """
        Compute F1.

        >>> F1().evaluate([1, 2, 3, 4], [2, 5])  # doctest:+ELLIPSIS
        0.333...
        """
        
        prec = Precision()
        rec = Recall()
        
        P = prec.evaluate(hits, relevant)
        R = rec.evaluate(hits, relevant)
        
        try:
        	F1 = float(2 * P * R / (P + R) )
        except ZeroDivisionError:
        	F1 = 0.0
        
        return F1

    def __repr__(self):
        return 'F1'


class MAP(EvaluatorFunction):
    def evaluate(self, hits, relevant):
        """
        Compute Mean Average Precision.

        >>> MAP().evaluate([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], [1, 4, 6, 11, 12, 13, 14, 15, 16, 17])
        0.2
        """
        
        K = float( len(relevant) )
        count = 0.0
        prec = 0.0
        
        for i, h in enumerate(hits):
        	
        	if h in relevant:
        		count += 1.0
        		prec += float(count/(i+1))
        
        try:
        	MAP = float(prec/K)
        except ZeroDivisionError:
        	MAP = 0.0
        
        return MAP
        
    def __repr__(self):
        return 'MAP'



