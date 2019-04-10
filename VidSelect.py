# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/VidSelect.ui'
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

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(739, 276)
        Dialog.setMinimumSize(QtCore.QSize(739, 276))
        Dialog.setMaximumSize(QtCore.QSize(739, 276))
        self.vid0 = QtGui.QPushButton(Dialog)
        self.vid0.setGeometry(QtCore.QRect(670, 20, 51, 41))
        self.vid0.setText(_fromUtf8(""))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/img/upload_icon.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.vid0.setIcon(icon)
        self.vid0.setIconSize(QtCore.QSize(25, 25))
        self.vid0.setObjectName(_fromUtf8("vid0"))
        self.videdit0 = QtGui.QLineEdit(Dialog)
        self.videdit0.setGeometry(QtCore.QRect(20, 20, 631, 41))
        self.videdit0.setObjectName(_fromUtf8("videdit0"))
        self.vid1 = QtGui.QPushButton(Dialog)
        self.vid1.setGeometry(QtCore.QRect(670, 70, 51, 41))
        self.vid1.setText(_fromUtf8(""))
        self.vid1.setIcon(icon)
        self.vid1.setIconSize(QtCore.QSize(25, 25))
        self.vid1.setObjectName(_fromUtf8("vid1"))
        self.vid2 = QtGui.QPushButton(Dialog)
        self.vid2.setGeometry(QtCore.QRect(670, 120, 51, 41))
        self.vid2.setText(_fromUtf8(""))
        self.vid2.setIcon(icon)
        self.vid2.setIconSize(QtCore.QSize(25, 25))
        self.vid2.setObjectName(_fromUtf8("vid2"))
        self.vid3 = QtGui.QPushButton(Dialog)
        self.vid3.setGeometry(QtCore.QRect(670, 170, 51, 41))
        self.vid3.setText(_fromUtf8(""))
        self.vid3.setIcon(icon)
        self.vid3.setIconSize(QtCore.QSize(25, 25))
        self.vid3.setObjectName(_fromUtf8("vid3"))
        self.videdit1 = QtGui.QLineEdit(Dialog)
        self.videdit1.setGeometry(QtCore.QRect(20, 70, 631, 41))
        self.videdit1.setObjectName(_fromUtf8("videdit1"))
        self.videdit2 = QtGui.QLineEdit(Dialog)
        self.videdit2.setGeometry(QtCore.QRect(20, 120, 631, 41))
        self.videdit2.setObjectName(_fromUtf8("videdit2"))
        self.videdit3 = QtGui.QLineEdit(Dialog)
        self.videdit3.setGeometry(QtCore.QRect(20, 170, 631, 41))
        self.videdit3.setObjectName(_fromUtf8("videdit3"))
        self.ok = QtGui.QPushButton(Dialog)
        self.ok.setGeometry(QtCore.QRect(625, 230, 97, 27))
        self.ok.setDefault(True)
        self.ok.setObjectName(_fromUtf8("ok"))
        self.cancel = QtGui.QPushButton(Dialog)
        self.cancel.setGeometry(QtCore.QRect(520, 230, 97, 27))
        self.cancel.setDefault(False)
        self.cancel.setObjectName(_fromUtf8("cancel"))

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Select Streams", None))
        self.ok.setText(_translate("Dialog", "OK", None))
        self.cancel.setText(_translate("Dialog", "Cancel", None))

import AppResources_rc
