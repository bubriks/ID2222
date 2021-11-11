
import numpy as np
from numpy import single

import shingling as sh
from compareSets import CompareSets
from compare_signatures import CompareSignatures
from minHashing import minHashing
from lsh import LSH
import pandas as pd
import os 
import itertools
from _operator import itemgetter

def make_clean_file() :
    data_path = os.path.join(os.getcwd(),'Homework 1', "[UCI] AAAI-13 Accepted Papers - Papers.csv")
    dataset = pd.read_csv(data_path)
    #### removed all the new line char & carrage return char
    changed_data = dataset.copy()
    for i, _ in enumerate(changed_data.iterrows()) :
        changed_data['Keywords'][i] = changed_data['Keywords'][i].lower().replace('\n\r', ' ').replace('\n', ' ').replace('  ',' ')
        changed_data['Abstract'][i] = changed_data['Abstract'][i].lower().replace('\n\r', ' ').replace('\n', ' ').replace('\em',' ').replace('"',' ').replace('  ',' ')
    changed_data.to_csv(os.path.join(os.getcwd(),'Homework 1', "remove_newline_char.csv"))

def print_results(dataset, result_dict, item='Keywords', lsh=False):

    if lsh :
        for i in range(len(result_dict)) :
            print('[',item,'top similarity ] : ',i, '\n\r---------------------------\n\r',dataset[item][result_dict[i][0]], '\n\r---------------------------\n\r', dataset[item][result_dict[i][1]],'\n')
    else :
        for i in range(len(result_dict)) :
            print('[',item,'top similarity ] : ',i, '\n\r---------------------------\n\r',dataset[item][result_dict[i]['idx'][0]], '\n\r---------------------------\n\r', dataset[item][result_dict[i]['idx'][1]],'\n')


if __name__ == "__main__":
    ######################### call this function only once ####################
    # make_clean_file() #this function is for making clean file
    ###########################################################################

    # read real dataset
    data_path = os.path.join(os.getcwd(),'Homework 1', "remove_newline_char.csv")#"remove_newline_char.csv") #original file name : [UCI] AAAI-13 Accepted Papers - Papers.csv
    dataset = pd.read_csv(data_path)

    # all possible compare
    indexes = list(itertools.combinations([i for i in range(len(dataset))], 2))
    result1 = []
    result2 = []
    result3 = []
    ############################### find keyword similarity first ##############################
    # use compare set
    k = 3
    # get the shingle from all 'keywords' 
    shingle_set = [sh.Shingling(dataset['Keywords'][i], k).shingle_set for i in range(len(dataset))]
    shingle_one_hot = []
    signatures = []
    # combine all shingles (document)
    vocabs = set().union(*shingle_set)

    nbits = 32
    minHash = minHashing(len(vocabs), nbits)

    for s in shingle_set:
        vector = [1 if x in s else 0 for x in vocabs]
        shingle_one_hot.append(vector)
        signatures.append(minHash.create_hash(vector))

    for idx in indexes :
        c1 = shingle_one_hot[idx[0]]
        c2 = shingle_one_hot[idx[1]]
        sim = CompareSets(c1, c2)
        result1.append({'idx':idx, 'similarity':sim.jaccard_sim})
        ########################## TASK 2 ################################
        signature_s1 = signatures[idx[0]]
        signature_s2 = signatures[idx[1]]
        sim_sig = CompareSignatures.compare(signature_s1, signature_s2)
        result2.append({'idx':idx, 'similarity':sim_sig})

    # 1) use shingle and calculate similarity
    # print out top 5 similar index combination of Abstracts
    temp = sorted(result1, key=itemgetter('similarity'), reverse=True)[:5]
    print(temp)
    print_results(dataset, temp, 'Keywords')
    ### save top 5 index for next section ##
    sim_idx = [temp[i]['idx'] for i in range(5)]
    sim_idx = set().union(*sim_idx)

    # 2) use min hashing with compare signature
    # print out top 5 similar index combination of Abstracts
    temp = sorted(result2, key=itemgetter('similarity'), reverse=True)[:5]
    print(temp)
    print_results(dataset, temp, 'Keywords')     
    
    # 3) use lsh 
    Threshold = 0.5
    print(f'************* Threshold {Threshold} *****************')
    lsh = LSH(band_num=8, threshold=Threshold)
    result3 = lsh.similar(np.array(signatures).T)
    print(result3)
    if len(result3) > 0 :
        print_results(dataset, result3, 'Keywords', lsh=True)
    else :
        print('No candidates pair')
    #############################################################################################

    ############################## compare REALLY similar abstract ##############################
    result1 = []
    result2 = []
    result3 = []
    indexes = list(itertools.combinations([i for i in range(len(sim_idx))], 2))
    nbits = 32
    minHash = minHashing(len(vocabs), nbits)
    # use compare set
    k = 5
    # get the shingle from all 'keywords' 
    shingle_abs_set = [sh.Shingling(dataset['Abstract'][i], k).shingle_set for i in sim_idx]
    shingle_abs_one_hot = []
    signature_abs =[]
    # combine all shingles (document)
    vocabs = set().union(*shingle_abs_set)
    for s in shingle_abs_set:
        vector = [1 if x in s else 0 for x in vocabs]
        shingle_abs_one_hot.append(vector)
        signature_abs.append(minHash.create_hash(vector))
    

    for idx in indexes :
        c1 = shingle_abs_one_hot[idx[0]]
        c2 = shingle_abs_one_hot[idx[1]]
        sim = CompareSets(c1, c2)
        result1.append({'idx':idx, 'similarity':sim.jaccard_sim})
        ################## Task 2 ###########################
        signature_s1 = signature_abs[idx[0]]
        signature_s2 = signature_abs[idx[1]]
        sim_sig = CompareSignatures.compare(signature_s1, signature_s2)
        result2.append({'idx':idx, 'similarity':sim_sig})

    # 1) use shingle and calculate similarity
    # print out top 5 similar index combination of Abstracts
    temp = sorted(result1, key=itemgetter('similarity'), reverse=True)[:5]
    print(temp)
    print_results(dataset, temp, 'Abstract')

    # 2) use min hashing with compare signature
    # print out top 5 similar index combination of Abstracts
    temp = sorted(result2, key=itemgetter('similarity'), reverse=True)[:5]
    print(temp)
    print_results(dataset, temp, 'Abstract')     

    # 3) use lsh 
    Threshold = 0.1
    print(f'************* Threshold {Threshold} *****************')
    lsh = LSH(band_num=16, threshold=Threshold)
    result3 = lsh.similar(np.array(signature_abs).T)
    print(result3)
    if len(result3) > 0 :
        print_results(dataset, result3, 'Abstract', lsh=True)
    else :
        print('No candidates pair')
