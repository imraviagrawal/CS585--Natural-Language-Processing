#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov  5 20:43:44 2017

@author: ravi-pc
"""
from collections import defaultdict, OrderedDict
import numpy as np
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
    pos_count = defaultdict()
    neg_count = defaultdict()
    for tweet in tweets:
        countPositive = 1 # to avoid zero in pmi calculation
        countNegative = 1 # to avoid zero in pmi calculation
        for word in tweet:
            if word in pos_seed_list:
                countPositive += 1
            if word in neg_seed_list:
                countNegative += 1
        
        for word in tweet:
            if word not in pos_count and word not in pos_seed_list:
                pos_count[word] = countPositive
            if word not in neg_count and word not in neg_seed_list:
                neg_count[word] = countNegative
            if word in pos_count and word not in pos_seed_list:
                pos_count[word] += countPositive
            if word in neg_count and word not in neg_seed_list:
                neg_count[word] += countNegative
    return pos_count, neg_count

def PMI(word, pos_count, neg_count):
    p_x_nearpos = pos_count[word]
    p_x_nearneg = neg_count[word]
    p_x = pos_count[word] + neg_count[word]
    #print word
    #print p_x
    return max(0, np.log(p_x_nearpos/p_x)), max(0, np.log(p_x_nearneg/p_x))


def polarity(tweets, pos_count, neg_count):
    result = OrderedDict()
    for tweet in tweets:
        for word in tweet:
            if (word[0] not in ['@', '#']) and (word not in pos_seed_list)\
                and (word  not in neg_seed_list):
                    pmi_word = PMI(word, pos_count, neg_count)
                    result[word] = pmi_word
    
    return result

def count_500more(tweets, pos_seed_list, neg_seed_list):
    pos_count = defaultdict()
    neg_count = defaultdict()
    for tweet in tweets:
        countPositive = 1 # to avoid zero in pmi calculation 
        countNegative = 1 # to avoid zero in pmi calculation
        for word in tweet:
            if word in pos_seed_list:
                countPositive += 1
            if word in neg_seed_list:
                countNegative += 1
        
        for word in tweet:
            if word not in pos_count and word not in pos_seed_list:
                pos_count[word] = countPositive
            if word not in neg_count and word not in neg_seed_list:
                neg_count[word] = countNegative
            if word in pos_count and word not in pos_seed_list:
                pos_count[word] += countPositive
            if word in neg_count and word not in neg_seed_list:
                neg_count[word] += countNegative
    pos_count, neg_count = {k: v for k, v in pos_count.items() if v >= 0},{k: v for k, v in neg_count.items() if v >= 0}
    return pos_count, neg_count
            
                        
                  
                
                
