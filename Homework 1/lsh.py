import math
import itertools
import collections
import pandas as pd
from compare_signatures import CompareSignatures

class LSH:
    
    def __init__(self, band_num=100, threshold=0.8):
        self.band_num = band_num
        self.threshold = threshold

    def similar(self, signature_matrix):
        similar_documents = []
        df = pd.DataFrame(signature_matrix)
        
        for candidate in self.get_candidates(signature_matrix):
            similarity = CompareSignatures.compare(df[candidate[0]], df[candidate[1]])
            if similarity >= self.threshold:
                similar_documents.append(candidate)

        return similar_documents
        
    def get_candidates(self, signature_matrix):
        num_of_signatures, num_of_documents = signature_matrix.shape
        rows_in_band = math.ceil(num_of_signatures / self.band_num)
        
        candidate_pairs = set()
        for i in range(self.band_num):
            band = signature_matrix[i*rows_in_band: (i+1)*rows_in_band]

            buckets = collections.defaultdict(set)
            for j in range(num_of_documents):
                band_id = tuple(list(band[:,j]))
                buckets[band_id].add(j)

            for bucket in buckets.values():
                for pair in itertools.combinations(bucket, 2):
                    candidate_pairs.add(pair)

        return candidate_pairs

'''
import numpy as np
lsh = LSH(2)
arr = np.array([
    ["7", "7", "c"],
    ["4", "4", "f"], #rows are hashes
    ["s", "a", "a"]] #columns are documents
)
lsh.similar(arr)
'''