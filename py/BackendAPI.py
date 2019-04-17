#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from backend_func import density_4, initial, extension
from fr import detection
import time  
from sel import VideoSampler
from sel import crop

from PyQt4.QtCore import *
from PyQt4.QtGui import *
import random


class Backend(QThread):
   
    def __init__(self,parent = None):
        
        #Call Inherited Constructor
        super(Backend,self).__init__(parent)


    def pre_run(self,dict_front):

        self.pts = [x for x in dict_front['points'] if x != None]
        self.vidPath = [x for x in dict_front['paths'] if x != '']
        self.preset_time = dict_front['preset']
        self.width = dict_front['widths']
   
# =============================================================================
# giving UMat cv2 error     
# =============================================================================
        print(self.pts,self.vidPath,self.width)
        
        self.img = list()
        for i in range(len(self.vidPath)):
            self.img.append(crop(VideoSampler(self.vidPath[i],random.randint(1,8)),self.pts[i]))
#            self.img.append(VideoSampler(self.vidPath[i],random.randint(1,8)))

#        self.img=[crop(VideoSampler(self.vidPath[0],4),self.pts[0]),
#                  crop(VideoSampler(self.vidPath[1],1),self.pts[1]),
#                  crop(VideoSampler(self.vidPath[2],6),self.pts[2]),
#                  crop(VideoSampler(self.vidPath[3],8),self.pts[3])]
        print('crop',type(crop(VideoSampler(self.vidPath[0],4),self.pts[0])))
        print('img',type(self.img[0]))
        


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
            for i in range(len(self.img)):
                density = scan(self.img,self.width)
                
                #Initial Time Calculated for Lane i
                init_time = initial(density,i,self.preset_time)
                
                #Emits a Signal INIT
                self.emit(SIGNAL('SBS'), 
                          self.construct_signal(i, int(init_time)))
                
                #Change to Logger in UI
                #print('lane '+str(i)+' : '+str(int(init_time))+' secs')
                
                #Thread sleeps for init_time-7 seconds
            
                self.sleep((int(init_time)-10))
                
                extn_count = 1
                
                
                #Check This Line 
                density = scan(self.img,self.width)
                
                etimer = extension(density,i,extn_count, init_time, self.preset_time)
                
                #Emits a Signal EXT1
                self.emit(SIGNAL('SBS'), 
                          self.construct_signal(i, int(init_time), extn_count, int(etimer))) 
               
                self.sleep((int(etimer)-10))
               
                #Change to Logger in UI
                #print('lane '+str(i)+' extension time 1 : '+str(int(etimer))+' secs')
                
                extn_count += 1
                if etimer != 0 :
                    #Check This Line
                    density = scan(self.img, self.width)
                    
                    etimer= extension(density,i,extn_count, init_time, self.preset_time)
                    
                    self.emit(SIGNAL('SBS'), 
                          self.construct_signal(i, int(init_time), extn_count, int(etimer))) 
                    
                    self.sleep((int(etimer)-10))
                else:
                    continue
#                self.sleep(3)
            i=0
        return 0
                    
                    #Change to Logger in UI
                    #print('lane '+str(i)+' extension time 2 : '+str(int(etimer))+' secs')    


def scan(img,width):
    density=[0,0,0,0]
    for i in range(len(img)):
        vehicle_count = detection(img[i])
        print('c'+str(vehicle_count[0])+' m'+str(vehicle_count[1])+' b'+str(vehicle_count[2])+' t'+str(vehicle_count[3]))
        density[i] = density_4(vehicle_count, width[i])
    #density of all lanes
    
    return density

            
            
        
        
        