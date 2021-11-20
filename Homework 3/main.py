# dataset used: https://snap.stanford.edu/data/web-Google.html

import pandas as pd
import numpy as np

# Directed graph (each unordered pair of nodes is saved once): web-Google.txt 
# Webgraph from the Google programming contest, 2002
# Nodes: 875713 Edges: 5105039
df = pd.read_csv("web-Google.txt", sep="\t")

print(f"number of edges: {len(df)}")
print(f"number of Nodes: {len(np.unique(df[['FromNodeId', 'ToNodeId']].values))}")

print(df)