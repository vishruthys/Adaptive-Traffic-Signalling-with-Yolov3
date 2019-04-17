#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# =============================================================================
#       Backend Thread Starting Point
#       Developers : Shashank Sharma
#                   Venkat Sai Krishna,
#                   Vishruth Y S, 
#                   Sujay Biradar, 
#                   
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

from BackendFunction import density_4, initial, extension
from Detector import detection
from Selector import VideoSampler
from Selector import crop
import random
from PyQt4.QtCore import *
from PyQt4.QtGui import *


class Backend(QThread):
   
    def __init__(self,player, parent = None):
        
        #Call Inherited Constructor
        super(Backend,self).__init__(parent)
        
        #Video Player for snapshot
        self.video_player = player
        
        #New and Better Implemetation of Timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_lcd_frontend)

    def pre_run(self,dict_front):
        # =====================================================================
        # Runs once before backend thread starts
        # =====================================================================
        self.pts = [x for x in dict_front['points'] if x != None]
        self.vidPath = [x for x in dict_front['paths'] if x != '']
        self.preset_time = dict_front['preset']
        self.width = dict_front['widths']

        self.img = list()
        for i in range(len(self.pts)):
            self.img.append(crop(VideoSampler(self.vidPath[i],random.randint(1,8)),self.pts[i]))

        # =====================================================================
        #self.img=[crop(VideoSampler(self.vidPath[0],4),self.pts[0]),
        #         crop(VideoSampler(self.vidPath[1],1),self.pts[1]),
        #         crop(VideoSampler(self.vidPath[2],6),self.pts[2]),
        #         crop(VideoSampler(self.vidPath[3],8),self.pts[3])]
        # =====================================================================
    
    def update_lcd_frontend(self):
        # =====================================================================
        # Sends signal to frontend every second to update LED Counter
        # =====================================================================
        self.start_time -= 1
        
        self.emit(SIGNAL('lcd'), self.start_time)
    
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
                
                #Stops old timer, Sets new timer timer, starts timer
                self.timer.stop()
                self.start_time = int(init_time)
                self.timer.start(1000)
                
                #Signal Emit
                self.emit(SIGNAL('SBS'), 
                          self.construct_signal(i, int(init_time)))
                
                #Thread sleeps until the timer reaches 13
                while self.start_time != 14:
                    pass
                
                extn_count = 1
                
                density = scan(self.img,self.width)
                
                etimer = extension(density,i,extn_count, init_time, self.preset_time)
                
                #Adds Extension to existing timer
                self.start_time += int(etimer)
                
                #Signal Emit 
                self.emit(SIGNAL('SBS'), 
                          self.construct_signal(i, int(init_time), extn_count, int(etimer))) 
                
                #Thread sleep until the timer reached 13
                if self.start_time > 14:
                	while self.start_time != 14:
                		pass
                
                extn_count += 1
                
                if etimer != 0 :
                    density = scan(self.img, self.width)
                    
                    etimer= extension(density, i, extn_count, init_time, self.preset_time)
                    
                    #Adds Extension2 to Existing timer
                    self.start_time += int(etimer)
                    
                    #Signal Emit
                    self.emit(SIGNAL('SBS'), 
                          self.construct_signal(i, int(init_time), extn_count, int(etimer))) 

                #End Timer
                while self.start_time != 3:
                	pass
            
            i=0
        return 0


def scan(img,width):
    # =========================================================================
    # Scans Number of Vehciles
    # =========================================================================
    density=[0,0,0,0]
    for i in range(len(img)):
        vehicle_count = detection(img[i])
        
        print('c'+str(vehicle_count[0])+' m'+str(vehicle_count[1])+' b'+str(vehicle_count[2])+' t'+str(vehicle_count[3]))
        
        #density of all lanes
        density[i] = density_4(vehicle_count, width[i])

    return density