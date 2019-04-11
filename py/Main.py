#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from Application import Ui_MainWindow
from VidSelect import Ui_Dialog
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.phonon import Phonon
import sys,time,os,shutil

class SelectStream(QDialog):
    def __init__(self, *args,**kwargs):
        QWidget.__init__(self, parent = kwargs.get('parent'))
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.parent = kwargs.get('parent')
        
        self.path_edit = [self.ui.videdit0, self.ui.videdit1, self.ui.videdit2, self.ui.videdit3]

        #Configure Buttons
        self.upload_button_config()
        self.button_box_config()
        
        #Temporary Paths
        self.video_paths = [None, None, None, None]
        
    def upload_button_config(self):
        # =====================================================================
        # Configure Upload Buttons
        # =====================================================================
        
        self.ui.vid0.pressed.connect(lambda: self.file_select(0))
        self.ui.vid1.pressed.connect(lambda: self.file_select(1))
        self.ui.vid2.pressed.connect(lambda: self.file_select(2))
        self.ui.vid3.pressed.connect(lambda: self.file_select(3))
    
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
        for q_id in range(len(self.path_edit)):
            self.video_paths[q_id] = self.path_edit[q_id].text()
        
        # Add Video Paths
        self.parent.video_paths = self.video_paths
        
        #Close Dialog Box
        self.reject()
    
    def file_select(self, q_id):
        # =====================================================================
        # Select File When Upload Button is clicked
        # =====================================================================
        path = QFileDialog.getOpenFileName(self)
        self.path_edit[q_id].setText(path)
        

class MyApp(QMainWindow):
    def __init__(self,*args,**kwargs):
        QMainWindow.__init__(self,parent = None)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        #Full Screen
        self.showFullScreen()
        
        #Configure Video Players
        self.video_player_config()
        
        #Array of Paths (None Indicates Path Unknown)
        self.video_paths = [None,None,None,None]
        
        #Configure Menu Bar Actions
        self.action_config()
        
        #Status bar
        self.statusbar = QStatusBar()
        self.setStatusBar(self.statusbar)
        
        #Needed Below lines for future releases
        #scrollbar = self.ui.terminal.verticalScrollBar()
        #scrollbar.setValue(scrollbar.maximum())
        
    def video_player_config(self):
        # =====================================================================
        # Configure Video Player related Config
        # =====================================================================
        
        #Array of Players and Layouts
        self.player = [Phonon.VideoPlayer(Phonon.VideoCategory,self),
                      Phonon.VideoPlayer(Phonon.VideoCategory,self),
                      Phonon.VideoPlayer(Phonon.VideoCategory,self),
                      Phonon.VideoPlayer(Phonon.VideoCategory,self)]
        
        
        self.video_layouts = [self.ui.video_layout0,
                              self.ui.video_layout1,
                              self.ui.video_layout2,
                              self.ui.video_layout3]
    
    
    def showStatus(self,msg,t=2500):
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
        
        
    def vid_select(self):
        # =====================================================================
        # Handler for Select Stream Action
        # =====================================================================
        vid_select_dialog = SelectStream(parent = self)
        vid_select_dialog.exec()
        
        for index in range(len(self.video_paths)):
            if self.video_paths[index]:
                self.stream_video(index)
        
        for x in self.player:
            x.play()
                
    def stream_video(self, q_id):
        # =====================================================================
        # Stream Video of Quadrant identified by q_id
        # =====================================================================
        
        self.player[q_id].load(Phonon.MediaSource(self.video_paths[q_id]))
        self.video_layouts[q_id].addWidget(self.player[q_id])
        time.sleep(0.1)        

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
        
