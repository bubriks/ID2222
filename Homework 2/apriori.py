import numpy
import itertools
import collections

def read_baskets():
    with open("T10I4D100K.dat", "r") as f:
        lines = f.read().splitlines()
        group_list = [list(set(i.strip().split(" "))) for i in lines] #list(set) to remove duplicates on the basket (not interesting for us)
    return group_list

def generate_candidates(frequent_itemset):
    candidates = dict()
    for frequent_itemset in frequent_itemset:
        for singleton in singletons:
            if singleton[0] not in frequent_itemset:
                candidate = sorted(frequent_itemset + singleton)# to ensure that order doesnt matter
                candidates[tuple(candidate)] = 0
    return candidates

def count_candidates(candidates, tuple_size):
    for basket in baskets:
        basket_variations = itertools.combinations(basket, tuple_size) #all variation for the tuple size
        for combination in basket_variations:
            if combination in candidates:
                candidates[combination] += 1
    return candidates

baskets = read_baskets()

frequent_itemsets = []
support = 1000

#singletons
candidates = collections.Counter(list(numpy.concatenate(baskets).flat))
singletons = [(value,) for value, count in candidates.items() if count >= support]
frequent_itemsets.append(singletons)

#multitons (not sure if its a word :D )
k = 0
while len(frequent_itemsets[k]) > 1: # more than 1 element in the list
    tuple_size = k + 2
    candidates = generate_candidates(frequent_itemsets[k]) #make candidates
    candidate_count = count_candidates(candidates, tuple_size) #count candidates
    frequent_itemset = [i for i in candidate_count if candidate_count[i] >= support] #filter candidates
    frequent_itemsets.append(frequent_itemset)#add frequent itemset
    k += 1
print(frequent_itemsets)