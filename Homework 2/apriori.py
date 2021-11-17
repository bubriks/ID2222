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
support = 700

#singletons
candidates = collections.Counter(list(numpy.concatenate(baskets).flat))
singletons = {(value,): count for value, count in candidates.items() if count >= support}
frequent_itemsets.append(singletons)

#multitons (not sure if its a word :D )
k = 0
while len(frequent_itemsets[k]) > 1: # more than 1 element in the list
    tuple_size = k + 2
    candidates = generate_candidates(frequent_itemsets[k]) #make candidates
    candidate_count = count_candidates(candidates, tuple_size) #count candidates
    frequent_itemset = {i: candidate_count[i] for i in candidate_count if candidate_count[i] >= support} #filter candidates
    frequent_itemsets.append(frequent_itemset)#add frequent itemset
    k += 1
print(frequent_itemsets)




c = 0.6

def get_confidence(frequent_itemset, effect):
    frequent_itemset_support = frequent_itemsets[len(tuple_permutation) - 1][frequent_itemset]
    effect_support = frequent_itemsets[len(effect) - 1][effect]
    return round(frequent_itemset_support / effect_support, 2)

for frequent_itemset in frequent_itemsets[1:]:# anything with more than 1 element in the tuple
    for k_tuple in frequent_itemset:
        all_possible_effect_sizes = range(1, len(k_tuple))# all possible orders of implication for the tuple A -> B, C; A,B -> C
        seen_effect = list()
        for tuple_permutation in itertools.permutations(k_tuple, len(k_tuple)):# all possible permutations of the tuple
            for effect_size in reversed(all_possible_effect_sizes):
                effect = tuple(sorted(tuple_permutation[:effect_size]))
                if effect in seen_effect:# continue if such a combinations was considered for this tuple
                    continue
                seen_effect.append(effect)
                confidence = get_confidence(tuple(sorted(tuple_permutation)), effect)
                if confidence >= c:
                    effect = tuple_permutation[:effect_size]
                    result = tuple_permutation[effect_size:]
                    print(f"{effect} -> {result} : {confidence}%")
                else:
                    break # If A,B,C→D is below confidence, so is A,B→C,D because of supp(A,B) ≥ supp(A,B,C)