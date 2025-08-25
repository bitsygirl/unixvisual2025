'''
Accessible Access Control 1.0
2012-2104 Michigan Technological University
Supported in part by NSF grants: DUE-1140512, DUE-1245310 and IIS-1319363
Developer: Man Wang
Advisors:Dr. Steve Carr, Dr. Jean Mayo, Dr. Ching-Kuang Shene and Dr. Chaoli Wang
'''
#-*- coding: utf-8 -*-
# Form implementation generated from reading ui file 'answerRenameDlg.ui'
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

class Ui_DecryptionDlg(object):
    def setupUi(self, decryptionDlg):
        decryptionDlg.setObjectName(_fromUtf8("decryptionDlg"))
        decryptionDlg.resize(350, 135)
        self.pushButton_LoadKey = QtGui.QPushButton(decryptionDlg)
        self.pushButton_LoadKey.setGeometry(QtCore.QRect(440, 40, 31, 31))
        self.pushButton_LoadKey.setObjectName(_fromUtf8("pushButton_LoadKey"))
        
        self.pushButton_LoadAnswer = QtGui.QPushButton(decryptionDlg)
        self.pushButton_LoadAnswer.setGeometry(QtCore.QRect(440, 40, 31, 31))
        self.pushButton_LoadAnswer.setObjectName(_fromUtf8("pushButton_LoadAnswer"))
        
        self.pushButton_OK = QtGui.QPushButton(decryptionDlg)
        self.pushButton_OK.setGeometry(QtCore.QRect(20, 90, 94, 27))
        self.pushButton_OK.setObjectName(_fromUtf8("pushButton_OK"))
        self.pushButton_Cancel = QtGui.QPushButton(decryptionDlg)
        self.pushButton_Cancel.setGeometry(QtCore.QRect(250, 90, 94, 27))
        self.pushButton_Cancel.setObjectName(_fromUtf8("pushButton_Cancel"))
        self.lineEdit = QtGui.QLineEdit(decryptionDlg)
        self.lineEdit.setGeometry(QtCore.QRect(20, 40, 300, 31))
        self.lineEdit.setObjectName(_fromUtf8("lineEdit"))
        self.keylabel = QtGui.QLabel(decryptionDlg)
        self.keylabel.setGeometry(QtCore.QRect(20, 10, 251, 17))
        self.keylabel.setObjectName(_fromUtf8("keylabel"))
        self.answerlabel = QtGui.QLabel(decryptionDlg)
        self.answerlabel.setGeometry(QtCore.QRect(20, 10, 251, 17))
        self.answerlabel.setObjectName(_fromUtf8("answerlabel"))

        self.retranslateUi(decryptionDlg)
        QtCore.QMetaObject.connectSlotsByName(decryptionDlg)

    def retranslateUi(self, decryptionDlg):
        self.keylabel.setText(QtGui.QApplication.translate("decryptionDlg", "Decryption Key", None, QtGui.QApplication.UnicodeUTF8))
        decryptionDlg.setWindowTitle(QtGui.QApplication.translate("decryptionDlg", "Decryption", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_LoadKey.setText(QtGui.QApplication.translate("encryptionKeyImportDlg", "...", None, QtGui.QApplication.UnicodeUTF8))
        
        self.pushButton_OK.setText(QtGui.QApplication.translate("decryptionDlg", "OK", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_Cancel.setText(QtGui.QApplication.translate("decryptionDlg", "Close", None, QtGui.QApplication.UnicodeUTF8))

