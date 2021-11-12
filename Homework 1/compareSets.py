from shingling import Shingling
import numpy as np
class CompareSets:

    def comparefunc(self, set1:list, set2:list)-> float:
        intersection = np.logical_and(set1, set2)
        union = np.logical_or(set1, set2)
        return intersection.sum()/union.sum()

    def __init__(self, set1:list, set2:list ) :
        self.jaccard_sim = self.comparefunc(set1, set2)

        
'''
#example
c1 = Shingling("abcabv", 2)
c2 = Shingling("abcaa",2)
print(c1.shingles)
print(c2.shingles)
sim = CompareSets(c2.shingles, c1.shingles)
print(sim.jaccard_sim)

'''
