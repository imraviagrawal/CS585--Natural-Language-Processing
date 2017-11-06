#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov  5 20:43:44 2017

@author: ravi-pc
"""
from collections import defaultdict

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
        countPositive = 0
        countNegative = 0
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

def count_500more(tweets, pos_seed_list, neg_seed_list):
    pos_count = defaultdict()
    neg_count = defaultdict()
    for tweet in tweets:
        countPositive = 0
        countNegative = 0
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
            
                        
                  
                
                
