import numpy as np

class CompareSets:
    
    def __init__(self, threshold=0.8):
        self.threshold = threshold
    
    def similar(self, combinations, vectors_df):
        similar_documents = []

        for set1_id, set2_id in combinations:
            set1 = vectors_df[set1_id].tolist()
            set2 = vectors_df[set2_id].tolist()
            sim = CompareSets.compare(set1, set2)
            if sim >= self.threshold:
                similar_documents.append((set1_id, set2_id))

        return similar_documents

    def compare(set1, set2):
        intersection = np.logical_and(set1, set2)
        union = np.logical_or(set1, set2)
        jaccard_similarity =  intersection.sum()/union.sum()
        return round(jaccard_similarity, 2)

# example usage
#result = CompareSets.compare(set([1,2,3,4]), set([3,4,5,6]))
#print(result)