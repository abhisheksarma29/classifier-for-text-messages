# -*- coding: utf-8 -*-
"""
Created on Thu Aug 25 02:32:08 2016

@author: Abhishek Sharma
"""
# subjective dictionary :subjdic
class SubClues:
    def __init__(self, sc_path="C:\Users\Abhishek Sharma\Desktop\AN\code\subclues.tff"):
        self.d_file=open(sc_path)
        self.lines=self.d_file.readlines()[0:5549]
        
        sub_clues = [c.strip().split() for c in self.lines]
        
        
               
        self.dic={}        
        for rows in sub_clues:
            for attr in rows:
                arr=(attr.split('='))
                                
                if arr[0]=='type':
                    temp=arr[1]                    
                    self.dic[temp]={}
                    
                
                else:
                    self.dic[temp][arr[0]]=arr[1]
            
            temp_word=self.dic[temp]['word1']
            self.dic[temp_word]=self.dic.pop(temp)
        
            self.dic[temp_word]['type']=self.dic[temp_word].pop('word1') #replacing word1 in dictionary of dictionary by type
            self.dic[temp_word]['type']=temp
            
subjdic=SubClues()
