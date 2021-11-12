import math
import itertools
import collections
from compare_sets import CompareSets

class LSH:
    
    def __init__(self, band_num=100, threshold=0.8):
        self.band_num = band_num
        self.threshold = threshold

    def similar(self, signature_df):
        similar_documents = []
        
        for candidate_1, candidate_2 in self.get_candidates(signature_df):
            similarity = CompareSets.compare(
                signature_df[candidate_1].tolist(),
                signature_df[candidate_2].tolist())
            if similarity >= self.threshold:
                similar_documents.append((candidate_1, candidate_2))

        return similar_documents
        
    def get_candidates(self, signature_df):
        num_of_signatures, num_of_documents = signature_df.shape
        rows_in_band = math.ceil(num_of_signatures / self.band_num)
        
        candidate_pairs = set()
        for i in range(self.band_num):
            band = signature_df[i*rows_in_band: (i+1)*rows_in_band]

            buckets = collections.defaultdict(set)
            for j in range(num_of_documents):
                band_id = tuple(band.iloc[:,j].tolist())
                buckets[band_id].add(j)

            for bucket in buckets.values():
                for pair in itertools.combinations(bucket, 2):
                    candidate_pairs.add(pair)

        return candidate_pairs

'''
import numpy as np
lsh = LSH(2, 0.34)
arr = np.array([
    ["7", "7", "c"],
    ["4", "4", "f"], #rows are hashes
    ["s", "a", "a"]] #columns are documents
)
print(lsh.similar(arr))
'''