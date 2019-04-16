#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# =============================================================================
#       Backend Thread Starting Point
#       Developers : Venkat Sai Krishna,
#                   Vishruth Y S, 
#                   Sujay Biradar, 
#                   Shashank Sharma
# =============================================================================
#       Copyright (C) 2019  *Developers* 
# 
#       This program is free software: you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation, either version 3 of the License, or
#       (at your option) any later version.
# 
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
# 
#       You should have received a copy of the GNU General Public License
#       along with this program.  If not, see <https://www.gnu.org/licenses/>.
# =============================================================================

# =============================================================================
#       Removing the above copyright notice from the code is a direct breach 
#       of GNU's GPL v3.0 . If you have modified this code or developed 
#       any feature, feel free to append your name to the copyright name list.
#
#       This code is part of the repo https://github.com/vishruthys/VidGUI
# =============================================================================

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
        self.video_player = player

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
        # =====================================================================
        # Constructs a signal to integrate with UI
        # =====================================================================
        signal = {'lane': lane, 
                  'ext_number' : ext_number,
                  'lane_time' : lane_time,
                  'ext_time' : ext_time}
        
        return signal

    def get_current_frame(self):
        # =====================================================================
        # Returns an array of 4 QImage
        # =====================================================================
        imgs = list()
        for player in self.video_player:
            imgs.append(player.videoWidget().snapshot())
        return imgs

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
                
                #Thread sleeps for init_time-7 seconds
                if init_time > 8 :
                    self.sleep((int(init_time)-7)+3)
                
                extn_count = 1
                
                #Check This Line 
                den1,den2,den3,den4 = scan(self.img,self.width)
                
                etimer = extension(den1,den2,den3,den4,i,extn_count, init_time, self.preset_time)
                
                #Emits a Signal EXT1
                self.emit(SIGNAL('SBS'), 
                          self.construct_signal(i-1, int(init_time), extn_count, int(etimer))) 
                
                extn_count += 1
                if etimer != 0 :
                    #Check This Line
                    den1,den2,den3,den4 = scan(self.img, self.width)
                    
                    etimer= extension(den1,den2,den3,den4,i,extn_count, init_time, self.preset_time)
                    
                    self.emit(SIGNAL('SBS'), 
                          self.construct_signal(i-1, int(init_time), extn_count, int(etimer))) 
                else:
                    continue
            i=0
        return 0


def scan(img,width):
    vehicle_count = detection(img[0])
    print('c'+str(vehicle_count[0])+' m'+str(vehicle_count[1])+' b'+str(vehicle_count[2])+' t'+str(vehicle_count[3]))
    den1 = density_4(vehicle_count, width[0])
    
    vehicle_count = detection(img[1])
    print('c'+str(vehicle_count[0])+' m'+str(vehicle_count[1])+' b'+str(vehicle_count[2])+' t'+str(vehicle_count[3]))
    den2 = density_4(vehicle_count, width[1])

    vehicle_count = detection(img[2])  
    print('c'+str(vehicle_count[0])+' m'+str(vehicle_count[1])+' b'+str(vehicle_count[2])+' t'+str(vehicle_count[3]))
    den3 = density_4(vehicle_count, width[2])
    
    vehicle_count = detection(img[3])
    print('c'+str(vehicle_count[0])+' m'+str(vehicle_count[1])+' b'+str(vehicle_count[2])+' t'+str(vehicle_count[3]))
    den4 = density_4(vehicle_count, width[3])
    
    return den1,den2,den3,den4


            
            
        
        
        