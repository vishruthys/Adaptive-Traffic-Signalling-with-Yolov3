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
import random


class Backend(QThread):
   
    def __init__(self,parent = None):
        
        #Call Inherited Constructor
        super(Backend,self).__init__(parent)
        self.video_player = player

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
        for i in range(len(self.pts)):
            self.img.append(crop(VideoSampler(self.vidPath[i],random.randint(1,8)),self.pts[i]))
        print(self.img)



# =============================================================================
# 
#         self.img=[crop(VideoSampler(self.vidPath[0],4),self.pts[0]),
#              crop(VideoSampler(self.vidPath[1],1),self.pts[1]),
#              crop(VideoSampler(self.vidPath[2],6),self.pts[2]),
#              crop(VideoSampler(self.vidPath[3],8),self.pts[3])]
# 
# =============================================================================
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
            for i in range(len(self.img)):
                density = scan(self.img,self.width)
                
                #Initial Time Calculated for Lane i
                init_time = initial(density,i,self.preset_time)
                
                #Emits a Signal INIT
                self.emit(SIGNAL('SBS'), 
                          self.construct_signal(i, int(init_time)))

                self.sleep((int(init_time)-10))
                
                extn_count = 1
                
                #Check This Line 
                density = scan(self.img,self.width)
                
                etimer = extension(density,i,extn_count, init_time, self.preset_time)
                
                #Emits a Signal EXT1
                self.emit(SIGNAL('SBS'), 
                          self.construct_signal(i, int(init_time), extn_count, int(etimer))) 

               
                self.sleep((int(etimer)-10))

                
                extn_count += 1
                
                if etimer != 0 :
                    #Check This Line
                    density = scan(self.img, self.width)
                    
                    etimer= extension(density,i,extn_count, init_time, self.preset_time)
                    
                    self.emit(SIGNAL('SBS'), 
                          self.construct_signal(i, int(init_time), extn_count, int(etimer))) 

                else:
                    continue
            i=0
        return 0


def scan(img,width):
    density=[0,0,0,0]
    for i in range(len(img)):
        vehicle_count = detection(img[i])
        print('c'+str(vehicle_count[0])+' m'+str(vehicle_count[1])+' b'+str(vehicle_count[2])+' t'+str(vehicle_count[3]))
        density[i] = density_4(vehicle_count, width[i])
    #density of all lanes
    
    return density

            
            
        
        
        