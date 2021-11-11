from shingling import Shingling
import numpy as np
class CompareSets:

    def comparefunc(self, set1:list, set2:list)-> float:
        intersection = np.logical_and(set1, set2)
        union = np.logical_or(set1, set2)
        return intersection.sum()/union.sum()

    def __init__(self, set1:list, set2:list ) :
        self.jaccard_sim = self.comparefunc(set1, set2)

        

# #example
# c1 = Shingling("abcab", 2)
# c2 = Shingling("abcaa",2)
# vocab = list(c1.shingle_set.union(c2.shingle_set))
# c1_onehot = [1 if x in c1.shingle_set else 0 for x in vocab]
# c2_onehot = [1 if x in c2.shingle_set else 0 for x in vocab]
# sim = CompareSets(c1_onehot, c2_onehot)
# print(sim.jaccard_sim)


