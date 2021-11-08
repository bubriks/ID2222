from shingling import Shingling

class CompareSets:

    def comparefunc(self, set1:list, set2:list)-> float:
        intersection = len(list(set(set1).intersection(set2)))
        union = len(list(set(set1).union(set2)))
        print(intersection, union)
        return intersection/union

    def __init__(self, set1:list, set2:list ) :
        self.jaccard_sim = self.comparefunc(set1, set2)


        

#example
c1 = Shingling("abcab", 2) 
c2 = Shingling("abcaa",2) 
sim = CompareSets(c1.shingles, c2.shingles)
print(sim.jaccard_sim)

