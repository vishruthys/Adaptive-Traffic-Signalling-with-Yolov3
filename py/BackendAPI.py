#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from backend_func import density_4, initial, extension
from fr import detection
import time  
from sel import VideoSampler
from sel import crop

from PyQt4.QtCore import *
from PyQt4.QtGui import *


class Backend(QThread):
   
    def __init__(self,parent = None):
        
        #Call Inherited Constructor
        super(Backend,self).__init__(parent)


    def pre_run(self,dict_front):
        self.pts = dict_front['points']
        self.vidPath = dict_front['paths']
        self.preset_time = dict_front['preset']
        self.width = dict_front['widths']

        self.img=[crop(VideoSampler(self.vidPath[0],4),self.pts[0]),
             crop(VideoSampler(self.vidPath[1],1),self.pts[1]),
             crop(VideoSampler(self.vidPath[2],6),self.pts[2]),
             crop(VideoSampler(self.vidPath[3],8),self.pts[3])]

    def construct_signal(self, lane, lane_time, ext_number = 0, ext_time = 0):
        signal = {'lane': lane, 
                  'ext_number' : ext_number,
                  'lane_time' : lane_time,
                  'ext_time' : ext_time}
        
        return signal

    def run(self):
        # =====================================================================
        # Called when the thread is started
        # =====================================================================

        while True:
            for i in range(1,5):
                den1,den2,den3,den4 = scan(self.img,self.width)
                
                #Initial Time Calculated for Lane i
                init_time = initial(den1,den2,den3,den4,i,self.preset_time)
                
                #Emits a Signal INIT
                self.emit(SIGNAL('SBS'), 
                          self.construct_signal(i-1, int(init_time)))
                
                #Change to Logger in UI
                #print('lane '+str(i)+' : '+str(int(init_time))+' secs')
                
                #Thread sleeps for init_time-7 seconds
                if init_time > 8 :
                    self.sleep((int(init_time)-10))
                
                extn_count = 1
                
                
                #Check This Line 
                den1,den2,den3,den4 = scan(self.img,self.width)
                
                etimer = extension(den1,den2,den3,den4,i,extn_count, init_time, self.preset_time)
                
                #Emits a Signal EXT1
                self.emit(SIGNAL('SBS'), 
                          self.construct_signal(i-1, int(init_time), extn_count, int(etimer))) 
                if etimer > 8 :
                    self.sleep((int(etimer)-10))
               
                #Change to Logger in UI
                #print('lane '+str(i)+' extension time 1 : '+str(int(etimer))+' secs')
                
                extn_count += 1
                if etimer != 0 :
                    #Check This Line
                    den1,den2,den3,den4 = scan(self.img, self.width)
                    
                    etimer= extension(den1,den2,den3,den4,i,extn_count, init_time, self.preset_time)
                    
                    self.emit(SIGNAL('SBS'), 
                          self.construct_signal(i-1, int(init_time), extn_count, int(etimer))) 
                    
                    if etimer > 8 :
                        self.sleep((int(etimer)-10))
                else:
                    continue
            i=0
        return 0
                    
                    #Change to Logger in UI
                    #print('lane '+str(i)+' extension time 2 : '+str(int(etimer))+' secs')    


def scan(img,width):
    den=[0,0,0,0]
    for i in range(4):
        vehicle_count = detection(img[i])
        print('c'+str(vehicle_count[0])+' m'+str(vehicle_count[1])+' b'+str(vehicle_count[2])+' t'+str(vehicle_count[3]))
        den[i] = density_4(vehicle_count, width[i])
    
    
    return den[0],den[1],den[2],den[3]


            
            
        
        
        