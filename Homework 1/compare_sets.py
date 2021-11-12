import numpy as np

class CompareSets:

    def compare(set1, set2):
        intersection = np.logical_and(set1, set2)
        union = np.logical_or(set1, set2)
        jaccard_similarity =  intersection.sum()/union.sum()
        return round(jaccard_similarity, 2)

# example usage
#result = CompareSets.compare(set([1,2,3,4]), set([3,4,5,6]))
#print(result)