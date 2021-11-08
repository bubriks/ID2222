class CompareSets:

    def compare(set1: set, set2: set):
        intersection = set1.intersection(set2)
        union = set1.union(set2)
        jaccard_similarity =  len(intersection) / len(union)
        return round(jaccard_similarity, 2)

# example usage
result = CompareSets.compare(set([1,2,3,4]), set([3,4,5,6]))
print(result)