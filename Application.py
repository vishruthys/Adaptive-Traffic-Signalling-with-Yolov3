# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/Application.ui'
#
# Created by: PyQt4 UI code generator 4.12.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(1920, 1080)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.vid_bg0 = QtGui.QColumnView(self.centralwidget)
        self.vid_bg0.setGeometry(QtCore.QRect(10, 10, 651, 501))
        self.vid_bg0.setObjectName(_fromUtf8("vid_bg0"))
        self.vid_bg2 = QtGui.QColumnView(self.centralwidget)
        self.vid_bg2.setGeometry(QtCore.QRect(10, 520, 651, 501))
        self.vid_bg2.setObjectName(_fromUtf8("vid_bg2"))
        self.vid_bg1 = QtGui.QColumnView(self.centralwidget)
        self.vid_bg1.setGeometry(QtCore.QRect(670, 10, 651, 501))
        self.vid_bg1.setObjectName(_fromUtf8("vid_bg1"))
        self.verticalLayoutWidget_2 = QtGui.QWidget(self.centralwidget)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(680, 20, 631, 481))
        self.verticalLayoutWidget_2.setObjectName(_fromUtf8("verticalLayoutWidget_2"))
        self.video_layout1 = QtGui.QVBoxLayout(self.verticalLayoutWidget_2)
        self.video_layout1.setMargin(0)
        self.video_layout1.setObjectName(_fromUtf8("video_layout1"))
        self.verticalLayoutWidget_3 = QtGui.QWidget(self.centralwidget)
        self.verticalLayoutWidget_3.setGeometry(QtCore.QRect(680, 530, 631, 481))
        self.verticalLayoutWidget_3.setObjectName(_fromUtf8("verticalLayoutWidget_3"))
        self.video_layout3 = QtGui.QVBoxLayout(self.verticalLayoutWidget_3)
        self.video_layout3.setMargin(0)
        self.video_layout3.setObjectName(_fromUtf8("video_layout3"))
        self.vid_bg3 = QtGui.QColumnView(self.centralwidget)
        self.vid_bg3.setGeometry(QtCore.QRect(670, 520, 651, 501))
        self.vid_bg3.setObjectName(_fromUtf8("vid_bg3"))
        self.line = QtGui.QFrame(self.centralwidget)
        self.line.setGeometry(QtCore.QRect(1330, 10, 20, 1011))
        self.line.setFrameShape(QtGui.QFrame.VLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.verticalLayoutWidget_4 = QtGui.QWidget(self.centralwidget)
        self.verticalLayoutWidget_4.setGeometry(QtCore.QRect(20, 530, 631, 481))
        self.verticalLayoutWidget_4.setObjectName(_fromUtf8("verticalLayoutWidget_4"))
        self.video_layout2 = QtGui.QVBoxLayout(self.verticalLayoutWidget_4)
        self.video_layout2.setMargin(0)
        self.video_layout2.setObjectName(_fromUtf8("video_layout2"))
        self.verticalLayoutWidget_5 = QtGui.QWidget(self.centralwidget)
        self.verticalLayoutWidget_5.setGeometry(QtCore.QRect(20, 20, 631, 481))
        self.verticalLayoutWidget_5.setObjectName(_fromUtf8("verticalLayoutWidget_5"))
        self.video_layout0 = QtGui.QVBoxLayout(self.verticalLayoutWidget_5)
        self.video_layout0.setMargin(0)
        self.video_layout0.setObjectName(_fromUtf8("video_layout0"))
        self.textBrowser = QtGui.QTextBrowser(self.centralwidget)
        self.textBrowser.setGeometry(QtCore.QRect(1360, 10, 551, 1011))
        self.textBrowser.setStyleSheet(_fromUtf8("background-color: rgb(48, 10, 36);\n"
"color: rgb(255, 255, 255);"))
        self.textBrowser.setObjectName(_fromUtf8("textBrowser"))
        self.vid_bg0.raise_()
        self.vid_bg3.raise_()
        self.vid_bg2.raise_()
        self.vid_bg1.raise_()
        self.verticalLayoutWidget_2.raise_()
        self.verticalLayoutWidget_3.raise_()
        self.line.raise_()
        self.verticalLayoutWidget_4.raise_()
        self.verticalLayoutWidget_5.raise_()
        self.textBrowser.raise_()
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1920, 25))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setObjectName(_fromUtf8("menuFile"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.actionSelect_Stream = QtGui.QAction(MainWindow)
        self.actionSelect_Stream.setObjectName(_fromUtf8("actionSelect_Stream"))
        self.actionExit = QtGui.QAction(MainWindow)
        self.actionExit.setObjectName(_fromUtf8("actionExit"))
        self.actionMinimize = QtGui.QAction(MainWindow)
        self.actionMinimize.setObjectName(_fromUtf8("actionMinimize"))
        self.menuFile.addAction(self.actionSelect_Stream)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionMinimize)
        self.menuFile.addAction(self.actionExit)
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.textBrowser.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Ubuntu\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Hello World]</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">ighdof</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">ofhgpdf</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">hfh\\</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">gh</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">]fgig</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">oigh</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">fsgg]g</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">s</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">]\'gg[go</p></body></html>", None))
        self.menuFile.setTitle(_translate("MainWindow", "File", None))
        self.actionSelect_Stream.setText(_translate("MainWindow", "Select Stream", None))
        self.actionSelect_Stream.setShortcut(_translate("MainWindow", "Ctrl+O", None))
        self.actionExit.setText(_translate("MainWindow", "Exit", None))
        self.actionExit.setShortcut(_translate("MainWindow", "Ctrl+Q", None))
        self.actionMinimize.setText(_translate("MainWindow", "Minimize", None))

