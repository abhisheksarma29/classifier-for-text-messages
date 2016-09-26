# -*- coding: utf-8 -*-
"""
Created on Wed Aug 24 17:30:11 2016

@author: Abhishek Sharma
"""

from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
from nltk.stem import *
from subclues import SubClues

#from subclues import SubClues
file_pos="C:\Users\Abhishek Sharma\Desktop\AN\code\positive-words.txt"
file_neg=r"C:\Users\Abhishek Sharma\Desktop\AN\code\negative-words.txt"
pos= open(file_pos, 'r')
neg= open(file_neg, 'r')


pos_list = [line.rstrip()for line in pos.readlines()]
pos_list =pos_list[35:] 

neg_list = [line.rstrip() for line in neg.readlines()] 
neg_list=neg_list[35:]

class HpSubj:
    def __init__(self):
           
        subjdic=SubClues()
        self.dic= subjdic.dic 
        self.stemr=PorterStemmer()
    def classify(self,text):
        
        
        subjective_count=0.0
        subjective_score=0.0
        for sentence in  sent_tokenize(text):
            
            strong_subjective_words_count = 0
            subjective = False            
            words=word_tokenize(sentence)
                        
            for word in words:
                word=word.lower()
#                word_stem=[word,stemr.stem(word)] NEED TO CHANGE THE IF LINE FOR TYPE condition
                if (self.dic.has_key(word) or self.dic.has_key(self.stemr.stem(word))):
                    if self.dic.has_key(word):
                        dic_word=word
                    else:
                        dic_word=self.stemr.stem(word)
                    if self.dic[dic_word]['type']=='strongsubj':
                        strong_subjective_words_count +=1
                    #print strong_subjective_words_count
                        if strong_subjective_words_count>2:
                            subjective=True
                        #print word
                
            if subjective==True:
                subjective_count+=1
        subjective_score=subjective_count/len(sent_tokenize(text))
        print subjective_count
        print len(sent_tokenize(text))
        return subjective_score
            
class SentimentScore:
    def classify(self,text):
        sent_score={}        
        pos_count=neg_count=0
#        for sentence in  sent_tokenize(text):
        words=word_tokenize(text)
        print pos_list[2]        
        for word in words:
            word=word.lower()
            if word in pos_list:
                pos_count+=1
            if word in neg_list:
                neg_count+=1
        sent_score["positive"]=pos_count
        sent_score["negative"]=neg_count
        return pos_count,neg_count
    
    
#hps=HpSubj()    


                
            