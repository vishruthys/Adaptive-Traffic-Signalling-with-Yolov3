#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 10 11:01:56 2019

@author: vishruthys
"""

from Application import Ui_MainWindow
from VidSelect import Ui_Dialog
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.phonon import Phonon
import sys
import time

class SelectStream(QDialog):
    def __init__(self, *args,**kwargs):
        QWidget.__init__(self, parent = kwargs.get('parent'))
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        
        self.parent = kwargs.get('parent')
        
        self.upload_button_config()
        self.button_box_config()
        
        self.path_edit = [self.ui.videdit0, self.ui.videdit1, self.ui.videdit2, self.ui.videdit3]
        
        
        self.video_paths = [None, None, None, None]
        
    def upload_button_config(self):
        self.ui.vid0.pressed.connect(lambda : self.file_select(0))
        self.ui.vid1.pressed.connect(lambda : self.file_select(1))
        self.ui.vid2.pressed.connect(lambda : self.file_select(2))
        self.ui.vid3.pressed.connect(lambda : self.file_select(3))
    
    def button_box_config(self):
        self.ui.ok.pressed.connect(self.ok)
        self.ui.cancel.pressed.connect(lambda : self.reject())

    def ok(self):
        for q_id in range(len(self.path_edit)):
            self.video_paths[q_id] = self.path_edit[q_id].text()
        self.parent.video_paths = self.video_paths
        self.reject()
    
    def file_select(self, q_id):
        path = QFileDialog.getOpenFileName(self)
        self.path_edit[q_id].setText(path)
        
        

class MyApp(QMainWindow):
    def __init__(self,*args,**kwargs):
        QMainWindow.__init__(self,parent = None)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        self.showFullScreen()

        self.player = [Phonon.VideoPlayer(Phonon.VideoCategory,self),
                      Phonon.VideoPlayer(Phonon.VideoCategory,self),
                      Phonon.VideoPlayer(Phonon.VideoCategory,self),
                      Phonon.VideoPlayer(Phonon.VideoCategory,self)]
        
        self.video_paths = [None,None,None,None]
        
        self.video_layouts = [self.ui.video_layout0,self.ui.video_layout1,self.ui.video_layout2,self.ui.video_layout3]
        
        #self.player2 = Phonon.VideoPlayer(Phonon.VideoCategory,self)
        #self.player2.load(Phonon.MediaSource(self.videopath2))
        #self.ui.video_layout2.addWidget(self.player2)
        #self.player2.play()
        
        self.action_config()
        
        #status bar
        self.statusbar = QStatusBar()
        self.setStatusBar(self.statusbar)
        
    def showStatus(self,msg,t=2500):
        self.statusbar.showMessage(msg,t)
        self.ui_update()
        
    @classmethod
    def ui_update(self):
        qApp.processEvents()
    
    def action_config(self):
        self.ui.actionSelect_Stream.triggered.connect(self.vid_select)
        
        self.ui.actionMinimize.triggered.connect(lambda : self.showMinimized())
        self.ui.actionExit.triggered.connect(lambda : self.close())
        
    def vid_select(self):
        vid_select_dialog = SelectStream(parent = self)
        vid_select_dialog.exec()
        
        for index in range(len(self.video_paths)):
            if self.video_paths[index]:
                self.stream_video(index)
                
    def stream_video(self, q_id):
        self.player[q_id].load(Phonon.MediaSource(self.video_paths[q_id]))
        self.video_layouts[q_id].addWidget(self.player[q_id])
        self.player[q_id].play()
  
        
if __name__ == "__main__":
    App = QApplication(sys.argv)
    myapp = MyApp()
    myapp.show()
    sys.exit(App.exec_())
        