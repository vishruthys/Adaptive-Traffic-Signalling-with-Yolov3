#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# =============================================================================
#       Main Application Executable
#       Developer : Shashank Sharma
# =============================================================================
#       Copyright (C) 2019  Shashank Sharma, 
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

from Application import Ui_MainWindow
from VidSelect import Ui_Dialog
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.phonon import Phonon
import sys,time,os,shutil,logging
import cv2
import numpy as np
import matplotlib.pyplot as plt
import UiEssentials as uie
from BackendAPI import Backend

class ROI():
    
    def __init__(self, video_file):
        self.video = video_file
        
        self.logger = logging.getLogger('my-logger')
        self.logger.propagate = False
        
        #Video Sampler
        cap = cv2.VideoCapture(self.video)
        cap.set(cv2.CAP_PROP_POS_FRAMES, 120-1)
        res, self.frame = cap.read()

    def select_points(self):
        # =====================================================================
        # Select 4 Points in CW
        # =====================================================================
        fig, ax = plt.subplots(figsize = (20, 10))
        fig.canvas.set_window_title('Region Selector')
        
        #Plots the Image on the Plot
        ax.imshow(cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB))
        
        #Title of Image
        ax.set_title('Select Region of Interest')
        
        #Select 4 Points on the image
        co_ords = plt.ginput(4)
        
        #Close Plot
        plt.close()
        
        #Returns 4 Points
        return co_ords

class SelectStream(QDialog):
    def __init__(self, *args,**kwargs):
        self.parent = kwargs.get('parent')
        
        QWidget.__init__(self, parent = self.parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        
        self.edit_box_config()

        #Configure Buttons
        self.upload_button_config()
        self.button_box_config()
        self.crop_button_config()
        
        #Temporary Paths
        self.video_paths = [None, None, None, None]
        
        #Temporary ROI
        self.roi_point_list = [None, None, None, None]
    
    def edit_box_config(self):
        # =====================================================================
        # Configure Text Boxes and Spin Box
        # =====================================================================
        self.path_edit = [self.ui.videdit0, self.ui.videdit1, self.ui.videdit2, self.ui.videdit3]
        self.width_edit = [self.ui.width0, self.ui.width1, self.ui.width2, self.ui.width3]

        #Crop Activates when there is an active video file
        self.path_edit[0].textChanged.connect(lambda: self.paths_changed(0))
        self.path_edit[1].textChanged.connect(lambda: self.paths_changed(1))
        self.path_edit[2].textChanged.connect(lambda: self.paths_changed(2))
        self.path_edit[3].textChanged.connect(lambda: self.paths_changed(3))
    
    def paths_changed(self, q_id):
        # =====================================================================
        # Runs whenever path is a valid video path
        # =====================================================================
        path = self.path_edit[q_id].text()
        if uie.isVideoFile(path):
            self.crop_buttons[q_id].click()
    
    def upload_button_config(self):
        # =====================================================================
        # Configure Upload Buttons
        # =====================================================================
        
        self.ui.vid0.pressed.connect(lambda: self.file_select(0))
        self.ui.vid1.pressed.connect(lambda: self.file_select(1))
        self.ui.vid2.pressed.connect(lambda: self.file_select(2))
        self.ui.vid3.pressed.connect(lambda: self.file_select(3))
    
    def crop_button_config(self):
        # =====================================================================
        # Configure Crop Buttons
        # =====================================================================
        self.crop_buttons = [self.ui.crop0, self.ui.crop1, self.ui.crop2, self.ui.crop3]
        
        self.ui.crop0.pressed.connect(lambda : self.select_roi(0))
        self.ui.crop1.pressed.connect(lambda : self.select_roi(1))
        self.ui.crop2.pressed.connect(lambda : self.select_roi(2))
        self.ui.crop3.pressed.connect(lambda : self.select_roi(3))
    
    def select_roi(self,index):
        # =====================================================================
        # Selecting Region of Interest
        # =====================================================================
        video_file = self.path_edit[index].text()
        
        #Also checks if the file is a valid video file
        if video_file and uie.isVideoFile(video_file):
            roi_selector = ROI(video_file)
            self.roi_point_list[index] = roi_selector.select_points()
            
    def button_box_config(self):
        # =====================================================================
        # Configure Ok and Cancel Button
        # =====================================================================
        self.ui.ok.pressed.connect(self.ok)
        self.ui.cancel.pressed.connect(lambda : self.reject())

    def ok(self):
        # =====================================================================
        # Handler when Ok Button is clicked
        # =====================================================================
        video_paths = list()
        width = list()
        
        for q_id in range(len(self.path_edit)):
            video_paths.append(self.path_edit[q_id].text())
            width.append(self.width_edit[q_id].value())

        #Entering Preset
        preset, yes = QInputDialog.getInt(self,'Enter Preset','Preset (in sec): ', 150, 0, 999)
        
        #If Clicked Ok
        packed_data = dict()
        if yes:
            packed_data['preset'] = preset
            packed_data['points'] = self.roi_point_list
            packed_data['paths'] = video_paths
            packed_data['widths'] = width

            self.parent.data = packed_data

            #Close Dialog Box
            self.reject()
    
    def file_select(self, q_id):
        # =====================================================================
        # Select File When Upload Button is clicked
        # =====================================================================
        path = QFileDialog.getOpenFileName(self)
        if path and uie.isVideoFile(path):
            self.path_edit[q_id].setText(path)
            
        
class MyApp(QMainWindow):
    
    def __init__(self,*args,**kwargs):
        QMainWindow.__init__(self,parent = None)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        #Configure Video Players
        self.video_player_config()

        #Configure Menu Bar Actions and Shortcuts
        self.action_config()
        self.shortcut_config()
        
        #Status bar
        self.statusbar = QStatusBar()
        self.setStatusBar(self.statusbar)
        
        #Needed Below lines for future releases
        self.terminal_scrollbar = self.ui.terminal.verticalScrollBar()
        
        #Configure Close and Minimize Buttons
        self.right_menu_bar_config()
        
        #Full Screen (This should be at last of constructor)
        #Because UI needs to buildup without full screen flag turned on
        self.showFullScreen()
        
        #Create a Backend Thread
        self.backend = Backend(player = self.player)
        
        #Connect Backend Thread to UI via signal SBS
        self.connect(self.backend, SIGNAL('SBS'), self.SBS_frontend_update)
        
        self.traffic_index = -1
        
        #Create a Timer
        self.timer = QTimer()
        self.timer.start(1000)
        
        #For every second update LCD
        self.timer.timeout.connect(lambda: self.update_lcd_timer_value(self.traffic_index))
        
    
    def SBS_frontend_update(self, signal):
        # =====================================================================
        # Updates Frontend Whenever tje signal SBS is emitted
        # =====================================================================
        self.log('''
                 Lane : {}
                 Initial Time Calculated : {}
                 Extenstion Number : {}
                 Extension Time : {}
                 '''.format(
                 signal['lane'],
                 signal['lane_time'],
                 signal['ext_number'],
                 signal['ext_time']))
        
        if signal['ext_number'] == 0:
            self.traffic_index = signal['lane']
            self.create_lcd_timer(signal['lane_time'], signal['lane'])
            for index in range(len(self.video_bg)):
                if index == signal['lane']:
                    self.video_bg[index].setStyleSheet('background-color:green')
                else:
                    self.video_bg[index].setStyleSheet('background-color:red')
        elif signal['ext_number'] == 1:
            self.start_time += signal['ext_time']
        else:
            self.start_time += signal['ext_time']
    
    
    def video_player_config(self):
        # =====================================================================
        # Configure Video Player related Config
        # =====================================================================
        
        #Array of Paths (None Indicates Path Unknown)
        self.video_paths = [None,None,None,None]
        
        #Array of Players and Layouts
        self.player = [Phonon.VideoPlayer(Phonon.VideoCategory,self),
                      Phonon.VideoPlayer(Phonon.VideoCategory,self),
                      Phonon.VideoPlayer(Phonon.VideoCategory,self),
                      Phonon.VideoPlayer(Phonon.VideoCategory,self)]
        
        
        self.video_layouts = [self.ui.video_layout0,
                              self.ui.video_layout1,
                              self.ui.video_layout2,
                              self.ui.video_layout3]
        
        self.video_bg = [self.ui.vid_bg0,
                         self.ui.vid_bg1,
                         self.ui.vid_bg2,
                         self.ui.vid_bg3]
        
        #Add Player to Layouts
        for index in range(len(self.player)):
            self.video_layouts[index].addWidget(self.player[index])
            self.player[index].load(Phonon.MediaSource('/'))
            self.player[index].installEventFilter(self)

        #Plays Video in Infinite Repeat Mode
        self.player[0].mediaObject().aboutToFinish.connect(lambda: self.player[0].seek(0))
        self.player[1].mediaObject().aboutToFinish.connect(lambda: self.player[1].seek(0))
        self.player[2].mediaObject().aboutToFinish.connect(lambda: self.player[2].seek(0))
        self.player[3].mediaObject().aboutToFinish.connect(lambda: self.player[3].seek(0))
        
        #Full Screen Handlers
        self.ui.full_screen0.pressed.connect(lambda: self.show_full_screen_video(0))
        self.ui.full_screen1.pressed.connect(lambda: self.show_full_screen_video(1))
        self.ui.full_screen2.pressed.connect(lambda: self.show_full_screen_video(2))
        self.ui.full_screen3.pressed.connect(lambda: self.show_full_screen_video(3))
        
        #Full Screen Exit Handler
        close_full_screenSC = QShortcut(self)
        close_full_screenSC.setKey(QKeySequence('Esc'))
        close_full_screenSC.setContext(Qt.ApplicationShortcut)
        close_full_screenSC.activated.connect(self.close_full_screen_video)
    
        #LCD Timer Configuration
        self.lcd_timers = [self.ui.lcd_timer0, self.ui.lcd_timer1, self.ui.lcd_timer2, self.ui.lcd_timer3]

    
    def eventFilter(self, obj, event):
        # =====================================================================
        # Enables Double Click Full screen for video Player
        # =====================================================================
        if event.type() == QEvent.MouseButtonDblClick:
            index = self.player.index(obj)
            self.show_full_screen_video(index)    
        return True

    def show_full_screen_video(self,index):
        # =====================================================================
        # Sets Full Screen of particular quadrant
        # =====================================================================
        self.player[index].videoWidget().setFullScreen(True)
    
    def close_full_screen_video(self):
        # =====================================================================
        # Closes Full Screen Video
        # =====================================================================
        for x in self.player:
            vid_widget_x = x.videoWidget()
            if vid_widget_x.isFullScreen():
                vid_widget_x.exitFullScreen()
   
    
    def vid_select(self):
        # =====================================================================
        # Handler for Select Stream Action
        # =====================================================================
        
        vid_select_dialog = SelectStream(parent = self)
        vid_select_dialog.exec()
        
        #Written in Try-Except Block to handle Cancel Button Click
       
        try:
            self.backend.pre_run(self.data)
            
            #Starts Backend Thread
            self.backend.start() 
            pass
        except:
            #If Cancel Button is Clicked
            pass
        finally:
            try:
                #Set Paths for Video Player
                self.video_paths = self.data['paths']
                
                #Load Video
                self.show_status('Loading...', 1500)
                for index in range(len(self.video_paths)):
                    if self.video_paths[index]:
                        self.stream_video(index)

                #Least Delayed Play
                for x in self.player:
                    x.play()

            except:
                # If cancel Button is clicked
                pass

    def stream_video(self, q_id):
        # =====================================================================
        # Stream Video of Quadrant identified by q_id
        # =====================================================================
        self.player[q_id].load(Phonon.MediaSource(self.video_paths[q_id]))
        
        #Delay to Load Video
        time.sleep(0.1)        

    def create_lcd_timer(self, countdown, index):
        # =====================================================================
        # Start LCD Timer
        # =====================================================================
        
        #Same Timer for Index and Index+1 (Traffic Color Change)
        self.lcd_timers[index].display(countdown)
        self.lcd_timers[(index+1)%4].display(countdown)
        
        self.lcd_timers[(index+2)%4].display(0)
        self.lcd_timers[(index+3)%4].display(0)
        
        #Set Start time
        self.start_time = countdown
        
    def update_lcd_timer_value(self,index):
        # =====================================================================
        # Called Every second when timer is running : Updates LCD
        # =====================================================================
        if index != -1:
            self.start_time -= 1
            if self.start_time >= 0 :
                self.lcd_timers[index].display(self.start_time)
                self.lcd_timers[(index+1)%4].display(self.start_time)
     
            if self.start_time == 0:
                self.timer.stop()
            
        
    def log(self, msg):
        # =====================================================================
        # Log on the application Terminal
        self.ui.terminal.append('>> {}'.format(msg))
        self.terminal_scrollbar.setValue(self.terminal_scrollbar.maximum())
    
    def show_status(self,msg,t=2500):
        # =====================================================================
        # Show Status Messages for t milliseconds
        # =====================================================================
        self.statusbar.showMessage(msg,t)
        self.ui_update()
        
    @classmethod
    def ui_update(self):
        qApp.processEvents()

    def action_config(self):
        # =====================================================================
        # Configures all Actions
        # =====================================================================
        self.ui.actionSelect_Stream.triggered.connect(self.vid_select)
        self.ui.actionMinimize.triggered.connect(lambda : self.showMinimized())
        self.ui.actionExit.triggered.connect(lambda : self.close())
        
    def shortcut_config(self):
        #Pressing F5 will clear the Application Terminal
        clear_logSC = QShortcut(self)
        clear_logSC.setKey(QKeySequence('F5'))
        clear_logSC.setContext(Qt.ApplicationShortcut)
        clear_logSC.activated.connect(lambda : self.ui.terminal.clear())
        
    def right_menu_bar_config(self):
        # =====================================================================
        # Configure Quit and Minimize Buttons
        # =====================================================================
        right_menubar = QMenuBar(self.menuBar())
        
        #Quit
        action0 = QAction(QIcon('{}/img/close.png'.format(os.environ['APPDIR'])),'', self)
        action0.triggered.connect(lambda : self.close())
        
        #Minimize
        action1 = QAction(QIcon('{}/img/minimize.png'.format(os.environ['APPDIR'])),'', self)
        action1.triggered.connect(lambda : self.showMinimized())
        
        #Add actins to Menu Bar
        right_menubar.addAction(action1)
        right_menubar.addAction(action0)
        
        #Add Menubar to Window
        self.menuBar().setCornerWidget(right_menubar)
    
    def closeEvent(self, event):
        # =====================================================================
        # Runs when close button is pressed
        # =====================================================================
        
        #Should stop all videos before exit (Else Segmentation Fault)
        for video_player in self.player:
            video_player.stop()

if __name__ == "__main__":
    App = QApplication(sys.argv)
    myapp = MyApp()
    myapp.show()
    
    shutil.rmtree('./__pycache__',ignore_errors=True)
    sys.exit(App.exec_())
        
