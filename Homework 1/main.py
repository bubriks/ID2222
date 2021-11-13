import os
import itertools
import pandas as pd
from timeit import default_timer
from contextlib import contextmanager

from shingling import Shingling
from compare_sets import CompareSets
from min_hashing import MinHashing
from compare_signatures import CompareSignatures
from lsh import LSH

def make_clean_file() :
    data_path = os.path.join(os.getcwd(),"[UCI] AAAI-13 Accepted Papers - Papers.csv")
    dataset = pd.read_csv(data_path)
    #### removed all the new line char & carrage return char
    changed_data = dataset.copy()
    for i, _ in enumerate(changed_data.iterrows()) :
        changed_data['Keywords'][i] = changed_data['Keywords'][i].lower().replace('\n\r', ' ').replace('\n', ' ').replace('  ',' ')
        changed_data['Abstract'][i] = changed_data['Abstract'][i].lower().replace('\n\r', ' ').replace('\n', ' ').replace('\em',' ').replace('"',' ').replace('  ',' ')
    changed_data.to_csv(os.path.join(os.getcwd(), "remove_newline_char.csv"))

def do_jaccard(combinations, vectors_df, threshold):
    compare = CompareSets(threshold)
    similar =  compare.similar(combinations, vectors_df)
    print(f"Sets with similarity of {threshold} in Jaccard are: {similar}")

def do_minhashing(vocabs_len, n, combinations, vectors_df, threshold):
    minHash = MinHashing(vocabs_len, n)
    signatures_df = minHash.get_df_signature(vectors_df)
    compare = CompareSignatures(threshold)
    similar = compare.similar(combinations, signatures_df)
    print(f"Sets with similarity of {threshold} in MinHashing are: {similar}")

def do_lsh(band_num, vectors_df, threshold):
    lsh = LSH(band_num, threshold)
    similar = lsh.similar(vectors_df)
    print(f"Sets with similarity of {threshold} in LSH are: {similar}")

@contextmanager
def elapsed_timer():
    start = default_timer()
    elapser = lambda: default_timer() - start
    yield lambda: elapser()
    end = default_timer()
    elapser = lambda: end-start

if __name__ == "__main__":
    ######################### call this function only once ####################
    # make_clean_file() # this function is for making clean file
    ###########################################################################

    # read real dataset
    data_path = os.path.join(os.getcwd(), "remove_newline_char.csv") # original file name : [UCI] AAAI-13 Accepted Papers - Papers.csv
    df = pd.read_csv(data_path)
    df_len = len(df)

    # all possible combinations
    combinations = list(itertools.combinations(list(range(df_len)), 2))

    #Shingling
    k = 5 # small number due to small files being compared
    shingles = df.apply(lambda row: list(Shingling(row['Keywords'], k).shingles), axis=1)
    shingles_df = pd.DataFrame(shingles, columns=["data"])
    vocabs = Shingling.get_vocabs(shingles_df) # all shingles
    vocabs_len = len(vocabs)
    Shingling.one_hot_encoder(shingles_df, vocabs)

    # transpose to make documents into columns
    vectors_df = pd.DataFrame(shingles_df["data"].tolist()).T
    del shingles_df # delete shingles_df to save memory

    threshold = 0.5 # threshold for all methods (so results could be compared)

    #Jaccard
    with elapsed_timer() as elapsed:
        do_jaccard(combinations, vectors_df, threshold)
    print(f"time taken for Jaccard {elapsed()} s\n")

    #MinHashing
    with elapsed_timer() as elapsed:
        n = 20 # number of permutations
        do_minhashing(vocabs_len, n, combinations, vectors_df, threshold)
    print(f"time taken for MinHashing {elapsed()} s\n")

    #LSH
    with elapsed_timer() as elapsed:
        band_num = 10 # number of bands
        do_lsh(band_num, vectors_df, threshold)
    print(f"time taken for LSH {elapsed()} s\n")

    # most similar
    #print(df['Keywords'][24])
    #print(df['Keywords'][37])