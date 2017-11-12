#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov  5 20:43:44 2017

@author: ravi-pc
"""
from collections import defaultdict, OrderedDict
import numpy as np
import re



# Initiallizing seed list
pos_seed_list = ["good", "nice", "love", "excellent", "fortunate", "correct", "superior"]
neg_seed_list = ["bad", "nasty", "poor", "hate", "unfortunate", "wrong", "inferior"]

def readfile(filename):
    with open(filename) as f:
        tweets = f.readlines()
        print ('The len of the ' + filename + " " + str(len(tweets)))
    tweets = [tweet.split() for tweet in tweets]
    return tweets

def count(tweets, pos_seed_list, neg_seed_list):
    word_count = defaultdict(int)
    pos_neg_count = {} 
    for word in pos_seed_list + neg_seed_list:
        pos_neg_count[word] = defaultdict(int)    
    for tweet in tweets:
        for word in set(tweet):
            word_count[word] += 1.0
            if word not in pos_seed_list or word not in neg_seed_list:
                for pos_word in pos_seed_list:
                    if pos_word in tweet:
                        pos_neg_count[pos_word][word] += 1.0
                for neg_word in neg_seed_list:
                    if neg_word in tweet:
                        pos_neg_count[neg_word][word] +=1.0
            
    return pos_neg_count, word_count

def PMI(tweets, word, pos_neg_count, word_count, alpha = 1.0):
    pos_pmi = 0
    neg_pmi = 0
    for pos_word in pos_seed_list:
        numerator = (alpha + pos_neg_count[pos_word][word])*1.0/len(tweets) # zero return 1.0
        denominator = ((alpha + word_count[word])/len(tweets))*((word_count[pos_word])/len(tweets))
        pos_pmi += np.log(numerator/denominator) 
  
    for neg_word in neg_seed_list: 
        numerator = (alpha + pos_neg_count[neg_word][word])/len(tweets) # zero return 1.0
        denominator = ((alpha + word_count[word])/len(tweets))*((word_count[neg_word])/len(tweets))
        neg_pmi += np.log(numerator/denominator)
    
    return pos_pmi - neg_pmi


def polarity(tweets, pos_neg_count, word_count, alpha):
    result = {}
    pos_seed_list = ["good", "nice", "love", "excellent", "fortunate", "correct", "superior"]
    neg_seed_list = ["bad", "nasty", "poor", "hate", "unfortunate", "wrong", "inferior"]
    for word in word_count:
        if word[0] not in ['@', '#'] and word not in pos_seed_list and word not in neg_seed_list:
            word_pmi = PMI(tweets, word, pos_neg_count, word_count, alpha)
            result[word] = word_pmi
    return result


            
                 
                
                
