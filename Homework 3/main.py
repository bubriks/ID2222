# paper used for implementation: http://www.kdd.org/kdd2016/papers/files/rfp0465-de-stefaniA.pdf
# dataset used: https://snap.stanford.edu/data/web-Google.html

import pandas as pd
import numpy as np
import random as rnd

# Directed graph (each unordered pair of nodes is saved once): web-Google.txt 
# Webgraph from the Google programming contest, 2002
# Nodes: 875713 Edges: 5105039
df = pd.read_csv("web-Google.txt", sep="\t")

print(f"number of edges: {len(df)}")
print(f"number of Nodes: {len(np.unique(df[['FromNodeId', 'ToNodeId']].values))}")

print(df)

class Action:
    ADD = 0
    REMOVE = 1

class TriestBase:

    def __init__(self, m):
        if m < 6:
            raise Exception('Limit < 6')
        self.t = 0 # total
        self.m = m # limit of edges
        self.sample = set() # sample of the stream
        self.tau = 0
        self.counters = {}

    def flip_coin(self):# biased coin with heads probability m/t
        return rnd.random() <= (self.m / self.t)

    def sample_edge(self, edge):
        if self.t < self.m:
            return True
        if self.flip_coin():
            element = rnd.sample(self.sample, 1)[0]
            self.sample.remove(element)
            self.update_counters(Action.REMOVE, edge)
            return True
        return False

    def update_counters(self, operation, edge: tuple):
        s1 = set()
        s2 = set()
        for element in self.sample:
            if element[0] == edge[0]:
                s1.add(element[1])
            if element[1] == edge[0]:
                s1.add(element[0])
            if element[0] == edge[1]:
                s2.add(element[1])
            if element[1] == edge[1]:
                s2.add(element[0])
        for element in set(s1).intersection(s2):
            if operation == Action.ADD:
                self.tau += 1
                self.counters[element] = self.counters.get(element, 0) + 1
                self.counters[edge[0]] = self.counters.get(edge[0], 0) + 1
                self.counters[edge[1]] = self.counters.get(edge[1], 0) + 1
            elif operation == Action.REMOVE:
                self.tau -= 1
                self.counters[element] = self.counters.get(element, 0) - 1
                self.counters[edge[0]] = self.counters.get(edge[0], 0) - 1
                self.counters[edge[1]] = self.counters.get(edge[1], 0) - 1
                if self.counters[element] <= 0:
                    del self.counters[element]
                    del self.counters[edge[0]]
                    del self.counters[edge[1]]

    def run(self, df):
        total = len(df)
        for index, row in df.iterrows():
            edge = tuple([row['FromNodeId'], row['ToNodeId']])
            self.t += 1
            if self.sample_edge(edge):
                self.sample.add(edge)
                self.update_counters(Action.ADD, edge)
            print(f"done: {round((index/total) * 100, 1)}%", end="\r")
        x = max([1, (self.t*(self.t-1)*(self.t-2))/(self.m*(self.m-1)*(self.m-2))])
        return self.tau * x

def run(sample_size):
    print(f"Testing TRIEST with sample size {sample_size}:")
    triest = TriestBase(sample_size)
    result = triest.run(df)
    print(f"Value: {result}")
    return result

if __name__=="__main__" :
    df = df[:][:10000] # pick part of the dataframe for faster computation

    expected = run(1000)
    true = run(len(df))
    print(f"Difference: {round(abs(expected - true) / true * 100)}%")
    print(f"Error: {abs(true - expected)} triangles")