class CompareSignatures:

    def compare(signatures1, signatures2):
        count = 0
        zipped = list(zip(signatures1, signatures2))
        for s1, s2 in zipped:
            if s1 == s2:
                count = count + 1

        return count/len(zipped)

# example usage
#result = CompareSignatures.compare([1,2,3,4], [3,2,5,6])
#print(result)