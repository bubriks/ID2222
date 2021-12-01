import pandas as pd
import os
import numpy as np
import networkx as nx
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from scipy.spatial import distance

filename = os.path.join(os.getcwd(), "Homework 4", "example1.dat")

class SpectralClustering:
    def __init__(self, nodes, k) -> None:
        self.nodes = nodes
        self.k = k
        pass

    # def CalculateValue(self, si, sj) :
    #     return np.exp(-(np.square(si-sj))/(2*np.square(self.std)))
    
    def AffinityMatrix(self, graph) :
        # make adjcent matrix
        A = np.zeros([self.nodes, self.nodes])
        for edge in graph.edges :
            if edge[0] != edge[1] :
                # non-direction graph : symmetric
                A[edge[0]-1][edge[1]-1] = 1
                A[edge[1]-1][edge[0]-1] = 1
        return A
        
    def DiagonalMatrix(self, affinityM) :
        D_sqr_root = np.sqrt(np.diag(np.sum(affinityM, axis=1)))
        D_sqr_root_inv = np.linalg.inv(D_sqr_root)
        L = np.dot(np.dot(D_sqr_root_inv, affinityM), D_sqr_root_inv)
        return L

    def FindLargestK(self, L):
        value, eigenVectors = np.linalg.eigh(L) # returned eigenvectors are sorted in accending
        return eigenVectors[:, -self.k:] # K_th largest vector

    def ReNormalizing(self, X) :
        Y = np.zeros_like(X)
        for i, row in enumerate(X) :
            x_sqr = np.dot(row, row.T)
            Y[i] = row/np.sqrt(x_sqr)
        return Y
    
    def KmeanClustering(self, Y):
        return KMeans(n_clusters=self.k).fit(Y).labels_

def saveplot(filename) :
    savename = os.path.join(os.getcwd(), 'Homework 4', filename+'.png')
    plt.savefig(savename)


if __name__=="__main__" :
    edge_list = nx.read_edgelist(filename, delimiter=",", nodetype=int, data=(("weight", int), ))
    graph = nx.Graph()
    graph.add_nodes_from(sorted(edge_list.nodes.keys()))
    graph.add_edges_from(edge_list.edges)

    nx.draw(graph, node_size=20)
    saveplot('before_clustering')
    plt.close()

    # example 1 has 4 clusters & example 2 has 2 clusters
    k = 4
    sc = SpectralClustering(len(edge_list.nodes.keys()),k)

    # 1. Form the affinity matrix (same as adjcent matrix)
    A = sc.AffinityMatrix(graph)
    # 2. Diagonal matrix
    L = sc.DiagonalMatrix(A)
    # 3. Find k largest eigenvectors of L
    X = sc.FindLargestK(L)
    # 4. Form matrix Y 
    Y = sc.ReNormalizing(X)
    # 5. K-means clustering
    labels = sc.KmeanClustering(Y)
   
    plt.figure()
    nx.draw(graph, node_size=20, node_color=labels)
    saveplot('after_cluster')
    plt.close()


     
