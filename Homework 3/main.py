# paper used for implementation: http://www.kdd.org/kdd2016/papers/files/rfp0465-de-stefaniA.pdf
# dataset used: https://snap.stanford.edu/data/web-Google.html

import pandas as pd
import numpy as np
import random as rnd
import os
import matplotlib.pyplot as plt
from timeit import default_timer
from contextlib import contextmanager

# Directed graph (each unordered pair of nodes is saved once): web-Google.txt
### We might need to consider undirected graph, so another dataset could be used!!!!
# Webgraph from the Google programming contest, 2002
# Nodes: 875713 Edges: 5105039
df = pd.read_csv(os.path.join(os.getcwd(), "Homework 3", "web-Google.txt"), sep="\t")

print(f"number of edges: {len(df)}")
print(f"number of Nodes: {len(np.unique(df[['FromNodeId', 'ToNodeId']].values))}")

print(df)

class Action:
    ADD = 0
    REMOVE = 1

class TriestBase:

    def __init__(self, m):
        if m < 6:
            raise Exception("Limit < 6")
        self.t = 0 # total
        self.m = m # limit of edges
        self.sample = set() # edge sample of the stream
        self.tau = 0 # global number of triangles
        self.counters = {} # local counters

    def flip_coin(self):# biased coin with heads probability m/t
        return rnd.random() <= (self.m / self.t)

    def sample_edge(self, edge):
        if self.t <= self.m:
            return True
        if self.flip_coin():
            element = rnd.sample(self.sample, 1)[0]
            self.sample.remove(element)
            self.update_counters(Action.REMOVE, edge)
            return True
        return False

    def update_counters(self, operation, edge: tuple): # edge[0] = from, edge[1] = to
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
        for node in s1.intersection(s2):
            if operation is Action.ADD:
                self.tau += 1
                self.counters[node] = self.counters.get(node, 0) + 1
                self.counters[edge[0]] = self.counters.get(edge[0], 0) + 1
                self.counters[edge[1]] = self.counters.get(edge[1], 0) + 1
            elif operation is Action.REMOVE:
                self.tau -= 1
                self.counters[node] = self.counters.get(node, 0) - 1
                self.counters[edge[0]] = self.counters.get(edge[0], 0) - 1
                self.counters[edge[1]] = self.counters.get(edge[1], 0) - 1
                if self.counters[node] <= 0:
                    del self.counters[node]
                    del self.counters[edge[0]]
                    del self.counters[edge[1]]

    def run(self, data):
        total = len(data)
        for index, edge in enumerate(data):
            self.t += 1
            if self.sample_edge(edge):
                self.sample.add(edge)
                self.update_counters(Action.ADD, edge)
            print(f"Progress: {round((index/total) * 100, 1)}%", end="\r")
        x = max([1, (self.t*(self.t-1)*(self.t-2))/(self.m*(self.m-1)*(self.m-2))])
        print()# add empty line
        return self.tau * x

class TriestImprove(TriestBase):
    def __init__(self, m):
        if m < 6:
            raise Exception("Limit < 6")
        self.t = 0 # total
        self.m = m # limit of edges
        self.sample = set() # edge sample of the stream
        self.tau = 0 # global number of triangles
        self.counters = {} # local counters

    def sample_edge(self, edge):
        if self.t <= self.m:
            return True
        if self.flip_coin():
            element = rnd.sample(self.sample, 1)[0]
            self.sample.remove(element)
            return True
        return False

    def update_counters(self, edge: tuple): # edge[0] = from, edge[1] = to
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
        for node in s1.intersection(s2):
            weight = max(1, ((self.t-1)*(self.t-2))/(self.m*(self.m-1)))
            self.tau += weight
            self.counters[node] = self.counters.get(node, 0) + weight
            self.counters[edge[0]] = self.counters.get(edge[0], 0) + weight
            self.counters[edge[1]] = self.counters.get(edge[1], 0) + weight
            
    def run(self, data):
        total = len(data)
        for index, edge in enumerate(data):
            self.t += 1
            self.update_counters(edge)
            if self.sample_edge(edge):
                self.sample.add(edge)
            print(f"Progress: {round((index/total) * 100, 1)}%", end="\r")
        print()# add empty line
        return self.tau

def run_base(sample_size, data):
    print(f"Testing TRIEST with sample size {sample_size}:")
    triest = TriestBase(sample_size)
    result = triest.run(data)
    print(f"Value: {result}")
    return result

def run_improved(sample_size, data):
    print(f"Testing TRIEST-IMPR with sample size {sample_size}:")
    triest = TriestImprove(sample_size)
    result = triest.run(data)
    print(f"Value: {result}")
    return result

@contextmanager
def elapsed_timer():
    start = default_timer()
    elapser = lambda: default_timer() - start
    yield lambda: elapser()
    end = default_timer()
    elapser = lambda: end-start

if __name__=="__main__" :
    df = df[:][:10000] # pick part of the dataframe for faster computation
    #df = df.drop_duplicates(subset=['FromNodeId','ToNodeId'])
    
    data = set() # made into set, to randomize the order
    for index, row in df.iterrows():
        data.add(tuple([row["FromNodeId"], row["ToNodeId"]]))

    sizes = [500, 750, 1000, 1250, 1500, 1750, 2000]
    # diffs = []
    # times = []
    size = 1250
    # for size in sizes :
    with elapsed_timer() as elapsed:
        print(f"\n[TRIEST BASE] Size [{size}]\n")
        expected = run_base(size, data)
        true = run_base(len(data), data)
        error = abs(expected - true)
        # diffs.append(error)
        print(f"Difference: {round(error / true * 100)}%")
        print(f"Error: {error} triangles\n")
        # times.append(elapsed())

    # fig, ax1 = plt.subplots()
    
    # ax1.set_xlabel('Sample size')
    # ax1.set_ylabel('Error triangles')
    # ax1.plot(sizes, diffs, color='red')
    # ax2 = ax1.twinx()
    # ax2.set_ylabel('Elapsed time(s)')
    # ax2.plot(sizes, times, color='green')
    # plt.show()

    # for size in sizes :
    with elapsed_timer() as elapsed:
        print(f"\n[TRIEST IMPR] Size [{size}]\n")
        expected = run_improved(size, data)
        true = run_improved(len(data), data)
        error = abs(expected - true)
        # diffs.append(error)
        print(f"Difference: {round(error / true * 100)}%")
        print(f"Error: {error} triangles\n")
        # times.append(elapsed())

    # fig, ax1 = plt.subplots()
    
    # ax1.set_xlabel('Sample size')
    # ax1.set_ylabel('Error triangles')
    # ax1.plot(sizes, diffs, color='red')
    # ax2 = ax1.twinx()
    # ax2.set_ylabel('Elapsed time(s)')
    # ax2.plot(sizes, times, color='green')
    # plt.show()