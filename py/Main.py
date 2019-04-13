#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from Application import Ui_MainWindow
from VidSelect import Ui_Dialog
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.phonon import Phonon
import sys,time,os,shutil,logging
import cv2
import numpy as np
import matplotlib.pyplot as plt


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
        
        #Plots the Image on the Plot
        ax.imshow(cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB))
        
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
        
        self.path_edit = [self.ui.videdit0, self.ui.videdit1, self.ui.videdit2, self.ui.videdit3]
        self.width_edit = [self.ui.width0, self.ui.width1, self.ui.width2, self.ui.width3]

        #Configure Buttons
        self.upload_button_config()
        self.button_box_config()
        self.crop_button_config()
        
        #Temporary Paths
        self.video_paths = [None, None, None, None]
        
        #Temporary ROI
        self.roi_point_list = [None, None, None, None]
        
    def upload_button_config(self):
        # =====================================================================
        # Configure Upload Buttons
        # =====================================================================
        
        self.ui.vid0.pressed.connect(lambda: self.file_select(0))
        self.ui.vid1.pressed.connect(lambda: self.file_select(1))
        self.ui.vid2.pressed.connect(lambda: self.file_select(2))
        self.ui.vid3.pressed.connect(lambda: self.file_select(3))
    
    def crop_button_config(self):
        self.crop_buttons = [self.ui.crop0, self.ui.crop1, self.ui.crop2, self.ui.crop3]
        
        self.ui.crop0.pressed.connect(lambda : self.select_roi(0))
        self.ui.crop1.pressed.connect(lambda : self.select_roi(1))
        self.ui.crop2.pressed.connect(lambda : self.select_roi(2))
        self.ui.crop3.pressed.connect(lambda : self.select_roi(3))
    
    def select_roi(self,index):
        video_file = self.path_edit[index].text()
        
        if video_file:
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
        preset, yes = QInputDialog.getInt(self,'Enter Preset','Preset : ', 150, 0, 999)
        
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
        if path :
            self.path_edit[q_id].setText(path)
            self.crop_buttons[q_id].click()
        
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
        self.backend = Backend()
        
        #Connect Backend Thread to UI via signal SBS
        self.connect(self.backend, SIGNAL('SBS'), self.SBS_frontend_update)
        
        
        #Create a Timer
        self.timer = QTimer()
    
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
            self.create_lcd_timer(signal['lane_time'], signal['lane'])
        elif signal['ext_number'] == 1:
            self.timer.stop()
            self.create_lcd_timer(self.start_time + signal['ext_time'], signal['lane'])
        else:
            self.timer.stop()
            self.create_lcd_timer(self.start_time + signal['ext_time'], signal['lane'])
    
        #Write Log
    
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
        
        #Add Player to Layouts
        for index in range(len(self.player)):
            self.video_layouts[index].addWidget(self.player[index])
            
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
            
            self.backend.start() 
           #Starts Backend Thread
           
    
        #Set Paths for Video Player
        finally:
            self.video_paths = self.data['paths']
            
            #Load Video
            self.show_status('Loading...', 1500)
            for index in range(len(self.video_paths)):
                if self.video_paths[index]:
                    self.stream_video(index)
            
            #Least Delayed Play
            for x in self.player:
                x.play()
        
       
                
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
        
        #Set Start time
        self.start_time = countdown
        
        #For every second update LCD
        self.timer.timeout.connect(lambda: self.update_lcd_timer_value(index))
       
        #Start Timer
        self.timer.start(1000)

    def update_lcd_timer_value(self,index):
        # =====================================================================
        # Called Every second when timer is running : Updates LCD
        # =====================================================================
        
        self.start_time -= 1
        if self.start_time >= 0 :
            self.lcd_timers[index].display(self.start_time)
            self.lcd_timers[(index+1)%4].display(self.start_time)
        
        if self.start_time == 0:
            self.timer.stop()
            self.log('DONE')
        
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
        
