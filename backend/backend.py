#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 25 13:09:40 2019

@author: sujay
"""
#import threading 
import backend_func
from fr import detection
import time  



def scan():
    v1,v2,v3,v4=backend_func.detection()
    
    den1=backend_func.density_4(v1,v2,v3,v4,w1)

    den2=backend_func.density_4(v1,v2,v3,v4,w2)
    
    den3=backend_func.density_4(v1,v2,v3,v4,w3)
    
    den4=backend_func.density_4(v1,v2,v3,v4,w4)
    
    return den1,den2,den3,den4

w1=int(input("Enter width of lane 1 "))
w2=int(input("Enter width of lane 2 "))
w3=int(input("Enter width of lane 3 "))
w4=int(input("Enter width of lane 4 "))

while True:
    for i in range(1,5):
        den1,den2,den3,den4=scan()
        init_time=backend_func.initial(den1,den2,den3,den4,i)
        
        print('lane '+str(i)+' : '+str(int(init_time))+' secs')
        time.sleep(int(init_time)-7)
        extn_count=1
        prev_time=init_time
        
        den1,den2,den3,den4=scan()
        etimer= backend_func.exten(den1,den2,den3,den4,i,extn_count,prev_time)
        print('lane '+str(i)+' extension time 1 : '+str(int(etimer))+' secs')
        extn_count=2
        den1,den2,den3,den4=scan()
        etimer= backend_func.exten(den1,den2,den3,den4,i,extn_count,prev_time)
        print('lane '+str(i)+' extension time 2 : '+str(int(etimer))+' secs')    
    i=0
        
        
        
        
        