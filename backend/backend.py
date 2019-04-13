#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 25 13:09:40 2019

@author: sujay
"""
#import threading 
from backend_func import density_4,initial,extension
from fr import detection
import time  
from sel import VideoSampler,crop



   
#img0=Selector(VideoSampler('/home/vishruthys/Project/video/t1.mp4',4))
#img1=Selector(VideoSampler('/home/vishruthys/Project/video/t1.mp4',1))
#img2=Selector(VideoSampler('/home/vishruthys/Project/video/t1.mp4',6))
#img3=Selector(VideoSampler('/home/vishruthys/Project/video/t1.mp4',8))



def scan(img,width):
    v1,v2,v3,v4=detection(img[0])
    print('c'+str(v1)+' m'+str(v2)+' b'+str(v3)+' t'+str(v4))
    den1=density_4(v1,v2,v3,v4,width[0])
    
    v1,v2,v3,v4=detection(img[1])
    print('c'+str(v1)+' m'+str(v2)+' b'+str(v3)+' t'+str(v4))
    den2=density_4(v1,v2,v3,v4,width[1])

    v1,v2,v3,v4=detection(img[2])  
    print('c'+str(v1)+' m'+str(v2)+' b'+str(v3)+' t'+str(v4))
    den3=density_4(v1,v2,v3,v4,width[2])
    
    v1,v2,v3,v4=detection(img[3])
    print('c'+str(v1)+' m'+str(v2)+' b'+str(v3)+' t'+str(v4))
    den4=density_4(v1,v2,v3,v4,width[3])
    
    return den1,den2,den3,den4

def compute(dict_front):
    pts = dict_front['points']
    vidPath = dict_front['paths']
    preset_time = dict_front['preset']
    width = dict_front['widths']
    
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
            den1,den2,den3,den4=scan(img,width)
            init_time=initial(den1,den2,den3,den4,i,preset_time)
            
            print('lane '+str(i)+' : '+str(int(init_time))+' secs')
            if init_time > 8:    
                time.sleep(int(init_time)-7)
            extn_count=1
            prev_time=init_time
            
            den1,den2,den3,den4=scan(img,width)
            
            etimer= extension(den1,den2,den3,den4,i,extn_count,prev_time,preset_time)
            if(etimer!=0):
                print('lane '+str(i)+' extension time 1 : '+str(int(etimer))+' secs')
                extn_count=2
                den1,den2,den3,den4=scan(img,width)
                etimer= extension(den1,den2,den3,den4,i,extn_count,prev_time,preset_time)
                print('lane '+str(i)+' extension time 2 : '+str(int(etimer))+' secs')    
            else:
                continue
        i=0
    return 0
            
            
        
        
        