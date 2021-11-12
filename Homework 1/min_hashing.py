from random import shuffle
import pandas as pd

class MinHashing:

    def __init__(self, vocab_size, n: int = 100):
        self.vocab_size = vocab_size
        self.n = n
        self.build_permutations(vocab_size) 

    def get_signature(self, vector_list):
        signature = []
        for hash_ex in self.permutations:
            df = pd.DataFrame(vector_list, index=hash_ex)
            df = df.sort_index()
            signature.append(df[df[0] == 1].first_valid_index())
        return signature

    def get_df_signature(self, vectors_df):
        signatures_df = pd.DataFrame()
        for i in vectors_df.columns.tolist():
            signatures_df[i] = self.get_signature(vectors_df[i].tolist())
        return signatures_df

    def build_permutations(self, vocab_size):
        # function for building multiple permutations
        self.permutations = []
        for _ in range(self.n):
            hash_ex = list(range(vocab_size))
            shuffle(hash_ex)
            self.permutations.append(hash_ex)

# example usage
#m = MinHashing(3, 2)
#df = pd.DataFrame([[1,1,0], [1,0,0]]).T
#result = m.get_signature(df)
#result = m.get_signature([1,0,0])
#print(result)