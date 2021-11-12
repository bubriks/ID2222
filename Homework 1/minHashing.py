from random import shuffle
import sys
sys.path.append("..")

class minHashing :

    def create_hash_func(self, size:int):
        # function for creating the hash vector/function
        hash_ex = list(range(1, size+1))
        shuffle(hash_ex)
        return hash_ex

    def build_minhash_func(self, vocab_size:int, nbits:int):
        # function for building multiple minhash vectors
        hashes = []
        for _ in range(nbits):
            hashes.append(self.create_hash_func(vocab_size))

        return hashes

    def create_hash(self,vector_list:set):
        # function for creating signature
        signature = []
        for func in self.hashes:
            for i in range(1, self.vocab_size+1):
                idx = func.index(i)
                signature_val = vector_list[idx]
                if signature_val == 1:#smallest possible value
                    signature.append(idx)
                    break
        return signature

    def __init__(self, vocab_size:int, nbits:int):
        self.vocab_size = vocab_size
        self.hashes = self.build_minhash_func(vocab_size, nbits) 
   

# c1 = Shingling("abcab", 2)
# c2 = Shingling("abcaa",2)
# vocab = list(set(c1.shingle_set).union(c2.shingle_set))
# c1_onehot = [1 if x in c1.shingle_set else 0 for x in vocab]
# c2_onehot = [1 if x in c2.shingle_set else 0 for x in vocab]
# hashes = minHashing(len(vocab), 32)
# m1 = hashes.create_hash(c1_onehot)
# m2 = hashes.create_hash(c2_onehot)
# print(m1, m2)
