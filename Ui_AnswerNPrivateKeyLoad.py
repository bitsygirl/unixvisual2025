'''
Accessible Access Control 1.0
2012-2104 Michigan Technological University
Supported in part by NSF grants: DUE-1140512, DUE-1245310 and IIS-1319363
Developer: Man Wang
Advisors:Dr. Steve Carr, Dr. Jean Mayo, Dr. Ching-Kuang Shene and Dr. Chaoli Wang
'''
#-*- coding: utf-8 -*-
# Form implementation generated from reading ui file 'answerFileLoad.ui'
#
# Created: Tue Feb 25 10:55:33 2014
#      by: PyQt4 UI code generator 4.9.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_AnswerNPrivateKeyLoad(object):
    def setupUi(self, answerFileLoad):
        answerFileLoad.setObjectName(_fromUtf8("answerFileLoad"))
        answerFileLoad.resize(481, 135)
        self.pushButton_Load = QtGui.QPushButton(answerFileLoad)
        self.pushButton_Load.setGeometry(QtCore.QRect(440, 40, 31, 31))
        self.pushButton_Load.setObjectName(_fromUtf8("pushButton_Load"))
        self.pushButton_OK = QtGui.QPushButton(answerFileLoad)
        self.pushButton_OK.setGeometry(QtCore.QRect(20, 90, 94, 27))
        self.pushButton_OK.setObjectName(_fromUtf8("pushButton_OK"))
        self.pushButton_Cancel = QtGui.QPushButton(answerFileLoad)
        self.pushButton_Cancel.setGeometry(QtCore.QRect(330, 90, 94, 27))
        self.pushButton_Cancel.setObjectName(_fromUtf8("pushButton_Cancel"))
        self.lineEdit_Dir = QtGui.QLineEdit(answerFileLoad)
        self.lineEdit_Dir.setGeometry(QtCore.QRect(20, 40, 411, 31))
        self.lineEdit_Dir.setObjectName(_fromUtf8("lineEdit_Dir"))
        self.label = QtGui.QLabel(answerFileLoad)
        self.label.setGeometry(QtCore.QRect(20, 10, 251, 17))
        self.label.setObjectName(_fromUtf8("label"))

        self.retranslateUi(answerFileLoad)
        QtCore.QMetaObject.connectSlotsByName(answerFileLoad)

    def retranslateUi(self, answerFileLoad):
        answerFileLoad.setWindowTitle(QtGui.QApplication.translate("answerFileLoad", "Load in Answer File", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_Load.setText(QtGui.QApplication.translate("answerFileLoad", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_OK.setText(QtGui.QApplication.translate("answerFileLoad", "OK", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_Cancel.setText(QtGui.QApplication.translate("answerFileLoad", "Cancel", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("answerFileLoad", "Encrypted Answer File:", None, QtGui.QApplication.UnicodeUTF8))

