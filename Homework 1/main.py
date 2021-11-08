from shingling import Shingling
from compare_sets import CompareSets
from min_hashing import MinHashing
from compare_signatures import CompareSignatures

k = 3

s1 = Shingling("The dog which chased the cat", k)
s2 = Shingling("The dog that chased the cat", k)
s3 = Shingling("The movie 'cats' made no sense", k)

sets_compare_result = CompareSets.compare(s1.shingles, s2.shingles)
print(f"similar {sets_compare_result}")
sets_compare_result = CompareSets.compare(s1.shingles, s3.shingles)
print(f"Dissimilar {sets_compare_result}")

n = 3

min_hashing = MinHashing(n)
sinature_s1 = min_hashing.get_signature(s1.shingles)
sinature_s2 = min_hashing.get_signature(s2.shingles)
sinature_s3 = min_hashing.get_signature(s3.shingles)

signatures_compare_result = CompareSignatures.compare(sinature_s1, sinature_s2)
print(f"similar approx. {signatures_compare_result}")
signatures_compare_result = CompareSignatures.compare(sinature_s1, sinature_s3)
print(f"Distinct approx. {signatures_compare_result}")