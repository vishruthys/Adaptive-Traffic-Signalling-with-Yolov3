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
from sel import VideoSampler
from sel import crop


#    
#img0=Selector(VideoSampler('/home/vishruthys/Project/video/t1.mp4',4))
#img1=Selector(VideoSampler('/home/vishruthys/Project/video/t1.mp4',1))
#img2=Selector(VideoSampler('/home/vishruthys/Project/video/t1.mp4',6))
#img3=Selector(VideoSampler('/home/vishruthys/Project/video/t1.mp4',8))



def scan(img,w1,w2,w3,w4):
    v1,v2,v3,v4=detection(img[0])
    print('c'+str(v1)+' m'+str(v2)+' b'+str(v3)+' t'+str(v4))
    den1=backend_func.density_4(v1,v2,v3,v4,w1)
    
    v1,v2,v3,v4=detection(img[1])
    print('c'+str(v1)+' m'+str(v2)+' b'+str(v3)+' t'+str(v4))
    den2=backend_func.density_4(v1,v2,v3,v4,w2)

    v1,v2,v3,v4=detection(img[2])  
    print('c'+str(v1)+' m'+str(v2)+' b'+str(v3)+' t'+str(v4))
    den3=backend_func.density_4(v1,v2,v3,v4,w3)
    
    v1,v2,v3,v4=detection(img[3])
    print('c'+str(v1)+' m'+str(v2)+' b'+str(v3)+' t'+str(v4))
    den4=backend_func.density_4(v1,v2,v3,v4,w4)
    
    return den1,den2,den3,den4

def compute(dict_front):
    pts = dict_front['points']
    vidPath = dict_front['paths']
    preset_time = dict_front['preset']
    w = dict_front['widths']
    
    img=[crop(VideoSampler(vidPath[0],4),pts[0]),
         crop(VideoSampler(vidPath[1],1),pts[1]),
         crop(VideoSampler(vidPath[2],6),pts[2]),
         crop(VideoSampler(vidPath[3],8),pts[3])]
    
    
    
#    w1=int(input("Enter width of lane 1 "))
#    w2=int(input("Enter width of lane 2 "))
#    w3=int(input("Enter width of lane 3 "))
#    w4=int(input("Enter width of lane 4 "))
    
    while True:
        for i in range(1,5):
            den1,den2,den3,den4=scan(img,w[0],w[1],w[2],w[3])
            init_time=backend_func.initial(den1,den2,den3,den4,i,preset_time)
            
            #EMIT  SIGNAL - Lane Number , time [Lane num turns green, lane+1 turns red (same time) ]
            
            print('lane '+str(i)+' : '+str(int(init_time))+' secs')
            if init_time > 8:    
                time.sleep(int(init_time)-7)
            extn_count=1
            prev_time=init_time
            
            den1,den2,den3,den4=scan()
            
            etimer= backend_func.exten(den1,den2,den3,den4,i,extn_count,prev_time,preset_time)
            
            #EMIT  SIGNAL - Lane Number ,etime [Lane num remains green(prev+etimer), lane+1 remains red (same time) ]
            
            print('lane '+str(i)+' extension time 1 : '+str(int(etimer))+' secs')
            
            extn_count=2
            if(etimer!=0):
                den1,den2,den3,den4=scan()
                etimer= backend_func.exten(den1,den2,den3,den4,i,extn_count,prev_time,preset_time)
                
                #EMIT  SIGNAL - Lane Number ,etime [Lane num remains green(prev+etimer), lane+1 remains red (same time) ]
                print('lane '+str(i)+' extension time 2 : '+str(int(etimer))+' secs')    
            else:
                continue
        i=0
    return 0
            
            
        
        
        