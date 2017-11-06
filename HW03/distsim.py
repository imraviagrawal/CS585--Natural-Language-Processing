from __future__ import division
import sys,json,math
import os
import numpy as np

def load_word2vec(filename):
    # Returns a dict containing a {word: numpy array for a dense word vector} mapping.
    # It loads everything into memory.
    
    w2vec={}
    with open(filename,"r") as f_in:
        for line in f_in:
            line_split=line.replace("\n","").split()
            w=line_split[0]
            vec=np.array([float(x) for x in line_split[1:]])
            w2vec[w]=vec
    return w2vec

def load_contexts(filename):
    # Returns a dict containing a {word: contextcount} mapping.
    # It loads everything into memory.

    data = {}
    for word,ccdict in stream_contexts(filename):
        data[word] = ccdict
    print "file %s has contexts for %s words" % (filename, len(data))
    return data

def stream_contexts(filename):
    # Streams through (word, countextcount) pairs.
    # Does NOT load everything at once.
    # This is a Python generator, not a normal function.
    for line in open(filename):
        word, n, ccdict = line.split("\t")
        n = int(n)
        ccdict = json.loads(ccdict)
        yield word, ccdict

def cosine_similarity(word1, word2):
    length1 = len(word1)
    length2 = len(word2)
    d1 = np.sqrt(sum([word1[key]**2 for key in word1]))
    d2 = np.sqrt(sum([word2[key]**2 for key in word2]))
    num = 0
    if length1 < length2:
        for key in word1:
            num += word1[key]*word2.get(key, 0)
    else:
        for key in word2:
            num += word2[key]*word1.get(key, 0)
    return num/(d1*d2)

def nearest_word(word2vec):
    result = {}
    for key1 in word2vec:
        for key2 in word2vec:
            if key1 != key2:
                if key1 not in result:
                    result[key1] = [[key2, cosine_similarity(word2vec[key1], word2vec[key2])]]
                else:
                    result[key1].append([key2, cosine_similarity(word2vec[key1], word2vec[key2])])
    return result

def cos_sim(v1, v2):
    dot_product = np.dot(v1, v2)
    norm1 = np.linalg.norm(v1)
    norm2 = np.linalg.norm(v2)
    return dot_product/(norm1*norm2)
        