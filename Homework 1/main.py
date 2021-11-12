import os
import pandas as pd
import itertools

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
    k = 3 # small number due to small files being compared
    shingles = df.apply(lambda row: list(Shingling(row['Keywords'], k).shingles), axis=1)
    shingles_df = pd.DataFrame(shingles, columns=["data"])
    vocabs = Shingling.get_vocabs(shingles_df) # all shingles
    vocabs_len = len(vocabs)
    Shingling.one_hot_encoder(shingles_df, vocabs)
    
    # transpose to make documents into columns
    vectors_df = pd.DataFrame(shingles_df["data"].tolist()).T
    del shingles_df # delete shingles_df to save memory
    
    #time this..
    #Jaccard
    maximum = 0
    for set1_id, set2_id in combinations:
        set1 = vectors_df[set1_id].tolist()
        set2 = vectors_df[set2_id].tolist()
        sim = CompareSets.compare(set1, set2)
        if sim > maximum:
            maximum = sim
        #print(f"set {set1_id} has similarity of {sim} to {set2_id}")
    print(maximum)
    
    #time this..
    
    #MinHashing
    n = 32 # number of permutations
    minHash = MinHashing(vocabs_len, n)
    signatures_df = minHash.get_df_signature(vectors_df)


    #CompareSignatures
    for set1_id, set2_id in combinations:
        set1 = signatures_df[set1_id].tolist()
        set2 = signatures_df[set2_id].tolist()
        sim = CompareSignatures.compare(set1, set2)
        #print(f"set {set1_id} has similarity of {sim} to {set2_id}")

    #time this..

    band_num = 5
    threshold = 0.5
    lsh = LSH(band_num, threshold)
    similar = lsh.similar(vectors_df)
    print(f"sets with similarity of {threshold} are: {similar}")

    print(df['Keywords'][90])
    print(df['Keywords'][85])