# -*- coding: utf-8 -*-
"""
Created on Wed Aug 17 17:24:36 2016

@author: Abhishek Sharma
"""

# -*- coding: utf-8 -*-
"""
Created on Fri Aug 12 17:58:08 2016

@author: Abhishek Sharma
"""

import itertools
import openpyxl
import gensim,logging,bz2
import re
from gensim import corpora,models,similarities
import pandas as pd 
import numpy as np
import collections
from collections import defaultdict,OrderedDict
import math
frequency=defaultdict(int)
import classifiers
from nltk.classify import NaiveBayesClassifier as nbc
from sklearn.naive_bayes import GaussianNB

from nltk.sentiment.vader import SentimentIntensityAnalyzer
df = pd.read_csv('C:\Users\Abhishek Sharma\Desktop\medhelp_csv.csv',nrows=50,usecols=['Sl_no', 'reply_by', 'reply_to','label', 'text'])
test1=df.text[1:50]
modals=['can', 'could', 'may', 'might', 'must', 'will', 'would', 'should',"i'd"]
pronouns=['you','they','he','she','it']
advise_list=['recommend','advise','need','require']
q_words=['anybody','question','wonder']
neg_words=['worse','irritation','pain','bad']
nl=df.reply_to[0]

nl='NaN'
featuresets=[]  

def lexical_features(txt):
    m_count=p_count=advs_count=q_count=neg_count=0 
    count=0
    count+=1
    print count
    features = {}
    ####Count Pronouns
    
    ####Count modals
    for word in txt.split():
        if word in modals:
            m_count += 1
        if word in pronouns:
            p_count+=1
        if word in advise_list:
            advs_count+=1
        if word in q_words:
            q_count+=1
#        if word in neg_words:
#            neg_count+=1
    
    features["modal_count"]=m_count
    features["pronoun_count"]=p_count
    features["advise_count"]=advs_count
    features["question_count"]=q_count
#    features["neg_count"]=neg_count
    
    return features

def basic_features(reply_by,reply_to,text,Sl_no):
        
    bfeatures={}
    if Sl_no!=0:
        bfeatures["sl"]="N"
    else:
        bfeatures["sl"]="Y"
    
    bfeatures["length"]=len(text.split())
    if type(reply_to)==float:    
        print type(reply_to)        
        bfeatures["reply"]="N" 
    else:
        bfeatures["reply"]="Y"
        
    return bfeatures

def senti_features(text):
    sfeatures={}#OrderedDict()
    #remove non-ascii    
    text=re.sub(r'[^\x00-\x7f]',r'', text)     
    hps=HpSubj()
    ss=SentimentScore()
    a,b=ss.classify(text)
    sfeatures["sub_count"]=hps.classify(text)   
    sfeatures["pos_freq"]=a
    sfeatures["neg_freq"]=b
     
    return sfeatures
    
# generate lda mdoel with given dataset
def lda_topic_gen(text):
    stoplist=["anxiety","i","im","im'","it","a","like","going", "about", "above", "above", "across", "after", "afterwards", "again", "against", "all", "almost", "alone", "along", "already", "also","although","always","am","among", "amongst", "amoungst", "amount",  "an", "and", "another", "any","anyhow","anyone","anything","anyway", "anywhere", "are", "around", "as",  "at", "back","be","became", "because","become","becomes", "becoming", "been", "before", "beforehand", "behind", "being", "below", "beside", "besides", "between", "beyond", "bill", "both", "bottom","but", "by", "call", "can", "cannot", "cant", "co", "con", "could", "couldnt", "cry", "de", "describe", "detail", "do", "done", "down", "due", "during", "each", "eg", "eight", "either", "eleven","else", "elsewhere", "empty", "enough", "etc", "even", "ever", "every", "everyone", "everything", "everywhere",  "fifteen", "fify", "fill", "find", "fire", "first", "five", "for", "former", "formerly", "forty", "found", "four", "from", "front", "full", "further", "get", "give", "go", "had", "has", "hasnt", "have", "he", "her", "here", "hereafter", "hereby", "herein", "hereupon", "hers", "herself", "him", "himself", "his", "how", "however", "hundred", "ie", "if", "in", "inc", "interest", "into", "is", "it", "its", "itself", "keep", "last", "latter", "latterly", "least", "less", "ltd", "made", "many", "me", "meanwhile", "mill", "mine", "more", "most", "mostly", "move", "much", "must", "my", "myself", "name", "namely", "never", "next", "nine", "no", "nobody", "none", "noone", "nor", "not", "nothing", "now", "nowhere", "of", "off", "often", "on", "once", "one", "only", "onto", "or", "other", "others", "our", "ours", "ourselves", "out", "over", "own","part", "per", "put", "rather", "re", "same", "see", "seem", "seemed", "seeming", "seems", "several", "she","show", "side", "since", "sincere", "six", "sixty", "so", "some", "someone", "something", "sometime", "sometimes", "somewhere", "such", "system", "take", "ten", "that", "the", "their", "them", "themselves", "then", "thence", "there", "thereafter", "thereby", "therein", "thereupon", "these", "they", "thickv", "thin", "third", "this", "those", "three", "through", "throughout", "thru", "thus", "to", "together", "too", "top", "toward", "towards", "twelve", "twenty", "two", "un", "under", "until", "up", "upon", "us", "very", "via", "was", "we", "well", "were", "what", "whatever", "when", "whence", "whenever", "where", "whereafter", "whereas", "whereby", "wherein", "whereupon", "wherever", "whether",  "whither", "who", "whoever", "whole", "whose", "why", "will", "with", "within", "without", "yet", "you", "your", "yours", "yourself", "yourselves", "the"]
    txt= [[word for word in document.split() if word not in stoplist]
        for document in text]
    dictionary = gensim.corpora.Dictionary(txt)
    corpus = [dictionary.doc2bow(text) for text in txt]    
    lda = gensim.models.ldamodel.LdaModel(corpus,id2word=dictionary, num_topics=10,iterations=50)  # train model
    return lda,dictionary,corpus
    #was msg_pair before

#############################################
#getkey used in sorted_t_list,sorting by max %
def getKey(item):
     return item[1]
def lda_topic_features(text):
        lda_t_f={}    
        vec = dictionary.doc2bow(text.split())
        topic_list = lda[vec]
        print topic_list        
        sorted_t_list=sorted(topic_list, key=getKey,reverse=True)
        lda_t_f['top1']= sorted_t_list[0][0]
        #lda_t_f['top2']= sorted_t_list[1][0]
        
        return lda_t_f
def just_return_label(text):
    l={}#OrderedDict()    
    l['label']=text
    return text
#############################3

    



lda,dictionary,corpus=lda_topic_gen(test1)

#make a dictionary of features
featuresets = [(dict(lexical_features(df.text[k]).items() \
                +basic_features(df.reply_by[k],df.reply_to[k],df.text[k],df.Sl_no[k]).items() \
                +senti_features(df.text[k]).items() \
                +lda_topic_features(df.text[k]).items())\
                ,just_return_label(df.label[k]))\
                for k in range(0, len(df[1:50]))]

colnames=['adv_cnt','mdl_cnt','prnn_cnt','q_cnt','reply','lngth','sl','neg_cnt','subj_cnt',\
'pos_freq','top1','label']

featuresets_pd=pd.DataFrame(featuresets)
featuresets_pd.columns=(colnames)

train_set, test_set = featuresets[:50], featuresets[26:50]

classifier = nbc.train(train_set)
classified_label = classifier.classify(dict(lexical_features(df.text[k]).items() \
                +basic_features(df.reply_by[k],df.reply_to[k],df.text[k],df.Sl_no[k]).items() \
                +senti_features(df.text[k]).items() \
                +lda_topic_features(df.text[k]).items())\
                for k in range(50, 100))





