import numpy
import itertools
import collections

def read_groups():
    with open("T10I4D100K.dat", "r") as f:
    #with open("temp.dat", "r") as f: # for learning 
        lines = f.read().splitlines()
        group_list = [list(set(i.strip().split(" "))) for i in lines] #list(set) to remove duplicates on the same line
    return group_list

def reduce(tuples, k):
    results = list()
    for i in tuples:
        result = set(numpy.concatenate(i).flat)
        if len(result) == k:
            results.append(tuple(result))
    return results

groups = read_groups()

frequent_itemsets = []
support = 1000

#singletons
flat_baskets = list(numpy.concatenate(groups).flat)
occurrences = collections.Counter(flat_baskets)
chosen = [(value,) for value, count in occurrences.items() if count >= support]
frequent_itemsets.append(chosen)

#multitons
k = 0
while len(frequent_itemsets[k]) > 1: # more than 1 element in the list
    tuple_size = k + 2
    tuples = set(itertools.combinations(frequent_itemsets[k], tuple_size))
    tuples = reduce(tuples, tuple_size)
    
    tp = len(tuples)
    
    chosen = []
    i = 0
    for t in tuples:
        count = 0
        for g in groups:
            if set(t).issubset(set(g)):
                count = count + 1
        if count >= support:
            chosen.append(t)
        i += 1
        print(f"\r{round((i/tp), 2)} %", flush=True, end="\r")
    
    frequent_itemsets.append(chosen)
    k = k + 1
    print(k)

print(frequent_itemsets)