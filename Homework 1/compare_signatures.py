class CompareSignatures:

    def __init__(self, threshold=0.8):
        self.threshold = threshold
    
    def similar(self, combinations, signatures_df):
        similar_documents = []
        
        for set1_id, set2_id in combinations:
            set1 = signatures_df[set1_id].tolist()
            set2 = signatures_df[set2_id].tolist()
            sim = CompareSignatures.compare(set1, set2)
            if sim >= self.threshold:
                similar_documents.append((set1_id, set2_id))

        return similar_documents    

    def compare(signatures1, signatures2):
        count = 0
        zipped = list(zip(signatures1, signatures2))
        for s1, s2 in list(zip(signatures1, signatures2)):
            if s1 == s2:
                count = count + 1

        return count/len(zipped)

# example usage
#result = CompareSignatures.compare([1,2,3,4], [3,2,5,6])
#print(result)