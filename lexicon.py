# -*- coding: utf-8 -*-
"""
Created on Fri Aug 19 23:28:07 2016

@author: Abhishek Sharma
"""
import pickle 
import os
import sys 
    def load(self):
        d_file=open("C:\Users\Abhishek Sharma\Desktop\AN\code\subclues.tff")
        lines=d_file.readlines()[0:20]
        
        for line in lines:
            attributes=line.split()
            for index,atrb in enumerate(attributes):
                if atrb.find('word1')>-1:                
                    wordvalue=atrb.split("=")[1]
                    
    
    
    

    #def __init__(self):
        filename =  "C:\Users\Abhishek Sharma\Desktop\AN\code\lexicon.txt"
        try:
            words = pickle.load(open(filename))
        except:
            words = {}
            
            output = open(self.filename, 'wb')
            pickle.dump(self.words, output)
        
    def load(self):
        """
            The method loads the annotated corpus and extracts the structure
            with easy access for the classifiers.
        """
        dictionary_file = open("datasets/subjclueslen1-HLTEMNLP05.tff","r")
        lines = dictionary_file.readlines()[0:20]

        for line in lines:
            attributes = line.split(" ")
            for index,attr in enumerate(attributes):
                if attr.find('word1') > -1:
                    word_value = attr.split("=")[1]
                    
                    attributes[index] = []
                    break
            if word_value in words:
                for attr in attributes:
                    if attr != []:
                        arr = attr.split("=")
                        print str(arr)+"end"                     
                        key = arr[0]
                        if key == "pos1":  
                            pos = words[word_value][key]
                            print pos
                            words[word_value][key].append(arr[1])
                            break
            else:
                words[word_value] = {}
                for attr in attributes:
                    if attr != []:
                        arr = attr.split("=")
                        key = arr[0]
                        if len(arr) > 1:
                            value = arr[1]
                        if key == "pos1":
                            words[word_value][key] = [value.replace("\n", "")]
                        else:
                            words[word_value][key] = value.replace("\n", "") 
        
        self.words = dict(patch_emoticons(), **self.words)       