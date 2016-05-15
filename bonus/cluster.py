"""
Assignment 5: K-Means. See the instructions to complete the methods below.
"""

from collections import Counter
from collections import defaultdict
import gzip
import math


class KMeans(object):

    def __init__(self, k=2):
        """ Initialize a k-means clusterer. Should not have to change this."""
        self.k = k

    def cluster(self, documents, iters=10):
        """
        Cluster a list of unlabeled documents, using iters iterations of k-means.
        Initialize the k mean vectors to be the first k documents provided.
        After each iteration, print:
        - the number of documents in each cluster
        - the error rate (the total Euclidean distance between each document and its assigned mean vector), rounded to 2 decimal places.
        See Log.txt for expected output.
        The order of operations is:
        1) initialize means
        2) Loop
          2a) compute_clusters
          2b) compute_means
          2c) print sizes and error
        """
        ###TODO
        
        self.mean_vect = {}
        
        # 1. Initialize mean vectors to be first k documents
        for i in range(self.k):
            self.mean_vect[i] = documents[i]
        
        # 2. loop on "iters" on stopping condition
        for i in range(iters):
        		
        	# 2a) compute clusters
        	self.compute_clusters(documents)
        	
        	# 2b) compute means
        	self.compute_means()
        	
        	# 2c) print sizes & error
        	temp_list = []
        	for key in self.final_cluster.keys():
        		temp_list.append( len(self.final_cluster[key]) )
        	
        	# Size of Clusters
        	print(temp_list)
        	# Error value of Cluster
        	print(self.error(documents))
        	
        	
    def compute_means(self):
        """ Compute the mean vectors for each cluster (results stored in an
        instance variable of your choosing)."""
        ###TODO
        
        for clust_id, doc_list in self.final_cluster.items():
        	
        	temp_dict = Counter()
        	vector_len = len(doc_list)
        	
        	# Compute avg of all features in dict
        	for doc_vect in doc_list:
        		temp_dict += doc_vect
        	
        	# Compute mean to all values in dict
        	for key, val in temp_dict.items():
        		
        		try:
        			temp_dict[key] = val / vector_len
        		except:
        			pass
        	
        	# update mean vector
        	self.mean_vect[clust_id] = temp_dict
        #####
        
    def compute_clusters(self, documents):
        """ Assign each document to a cluster. (Results stored in an instance
        variable of your choosing). """
        ###TODO
        
        clust_set = defaultdict(list)
        min_cluster_idx = 0
                
        # precompute mean Vector norms
        self.mean_norm = []
        for idx, mean_vect in self.mean_vect.items():
        	self.mean_norm.append( self.sqnorm(mean_vect) )
        
        for doc in documents:
        	
        	max_dist = 9999999
        	
        	# self.maen_vect is a dict with mean_vect ={0: Counter{}, 1: Counter{}, ...}
        	for cl_index, mean_vect in self.mean_vect.items():
        		# get minimum cluster distance
        		min_dist = self.distance(doc, mean_vect, self.mean_norm[cl_index])	
        		if min_dist < max_dist:
        			min_cluster_idx = cl_index
        			max_dist = min_dist
        			
        	try:
        		clust_set[min_cluster_idx].append(doc)
        	except:
        		clust_set[min_cluster_idx] = [doc]
        
        # Cluster_set will have all mean_vect-document pairs		
        self.final_cluster = clust_set
        

    def sqnorm(self, d):
        """ Return the vector length of a dictionary d, defined as the sum of
        the squared values in this dict. """
        ###TODO
        total = 0
        
        for key, val in d.items():
        	
        	total += (val**2)
        
        return total

    def distance(self, doc, mean, mean_norm):
        """ Return the Euclidean distance between a document and a mean vector.
        See here for a more efficient way to compute:
        http://en.wikipedia.org/wiki/Cosine_similarity#Properties"""
        ###TODO
        
        dotprod = 0.0
        # Get dotproduct of 2 vectors: check for doc vector for keys
        for key, val in doc.items():
        	if key in mean.keys():
        		dotprod += (val * mean[key])
        		
        # get norm of doc vector
        doc_norm = self.sqnorm(doc)
        
        # Cosine similarity & Euclidean distance 
        dist = float(doc_norm + mean_norm - (2 * dotprod))
        
        return( float(dist**0.5) )
        
        
    def error(self, documents):
        """ Return the error of the current clustering, defined as the total
        Euclidean distance between each document and its assigned mean vector."""
        ###TODO
        
        total = 0.00
        
        for cl_id, doclist in self.final_cluster.items():
        	
        	mean_vector = self.mean_vect[cl_id]
        	mean_vector_norm = self.sqnorm(mean_vector)

        	for docs in doclist:
        		#mean_vector = self.mean_vect[cl_id]
        		min_dist = self.distance(docs, mean_vector, mean_vector_norm)
        		total += float(min_dist)
        
        return round(total,2)
        
        
    def print_top_docs(self, n=10):
        """ Print the top n documents from each cluster. These are the
        documents that are the closest to the mean vector of each cluster.
        Since we store each document as a Counter object, just print the keys
        for each Counter (sorted alphabetically).
        Note: To make the output more interesting, only print documents with more than 3 distinct terms.
        See Log.txt for an example."""
        ###TODO
        
        for cl_ind, d_list in self.final_cluster.items():
        	
        	temp_dict = {}
        	
        	mean_vector = self.mean_vect[cl_ind]
        	mean_vector_norm = self.sqnorm(mean_vector)
        	
        	for i, doc_dict in enumerate(d_list):
        		
        		# got min distance between doc & mean-vect
        		dist = self.distance(doc_dict, mean_vector, mean_vector_norm)
        		temp_dict[i] = float(dist)
        	
        	# sort that dict will have tuple [(6, 2.4), (8,1.2), (1,0.5)]
        	temp_list = sorted(temp_dict.items(), key=lambda k:k[1])
        	
        	print("CLUSTER %d" %(cl_ind))
        	cnt = 0

        	for tup in temp_list:
        		
        		if cnt < n: # temp-list is of size "n:"
        		
        			# print documents with more than 3 distinct terms.
        			if len( set(d_list[tup[0]].keys()) ) > 3:
        				cnt = cnt + 1
        				term_sorted_list = sorted( d_list[tup[0]].keys() )
        				print(' '.join(term_sorted_list) )
        				
        		if cnt >= n: # Early exit: may break out of loop....
        			break
        	###
        	
        ###
        
def prune_terms(docs, min_df=3):
    """ Remove terms that don't occur in at least min_df different
    documents. Return a list of Counters. Omit documents that are empty after
    pruning words.
    >>> prune_terms([{'a': 1, 'b': 10}, {'a': 1}, {'c': 1}], min_df=2)
    [Counter({'a': 1}), Counter({'a': 1})]
    """
    ###TODO
    
    # Used to store DF values of keys terms
    doc_freqs = {}
    pruned_vocab = []
    profiles = []
    
    # 1. Compute df values
    for dicts in docs:    
    
        for key in set(dicts.keys()):            
            try:
            	doc_freqs[key] += 1
            except:
            	doc_freqs[key] = 1
    
    # 2. Create pruned vocab of terms
    for key, df_val in doc_freqs.items():
    	if df_val >= min_df:
    		pruned_vocab.append(key)
    
    # 3. loop through dict, remove terms not in pruned_vocab
    for dicts in docs:
    	
    	some_dict = {key: val for key, val in dicts.items() if key in pruned_vocab}
    	
    	# Check for empty dictionary
    	if some_dict:
    		profiles.append(Counter(some_dict))
    
    return profiles
    
def read_profiles(filename):
    """ Read profiles into a list of Counter objects.
    DO NOT MODIFY"""
    profiles = []
    with gzip.open(filename, mode='rt', encoding='utf8') as infile:
        for line in infile:
            profiles.append(Counter(line.split()))
    return profiles


def main():
    profiles = read_profiles('profiles.txt.gz')
    print('read', len(profiles), 'profiles.')
    profiles = prune_terms(profiles, min_df=2)
    km = KMeans(k=10)
    km.cluster(profiles, iters=20)
    km.print_top_docs()

if __name__ == '__main__':
    main()
