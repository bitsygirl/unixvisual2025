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

class Ui_EncryptionKeyImportDlg(object):
    def setupUi(self, encryptionKeyImportDlg):
        encryptionKeyImportDlg.setObjectName(_fromUtf8("encryptionKeyImportDlg"))
        encryptionKeyImportDlg.resize(350, 135)
#         self.pushButton_Load = QtGui.QPushButton(encryptionKeyImportDlg)
#         self.pushButton_Load.setGeometry(QtCore.QRect(440, 40, 31, 31))
#         self.pushButton_Load.setObjectName(_fromUtf8("pushButton_Load"))
        self.pushButton_OK = QtGui.QPushButton(encryptionKeyImportDlg)
        self.pushButton_OK.setGeometry(QtCore.QRect(20, 90, 94, 27))
        self.pushButton_OK.setObjectName(_fromUtf8("pushButton_OK"))
        self.pushButton_Cancel = QtGui.QPushButton(encryptionKeyImportDlg)
        self.pushButton_Cancel.setGeometry(QtCore.QRect(250, 90, 94, 27))
        self.pushButton_Cancel.setObjectName(_fromUtf8("pushButton_Cancel"))
        self.lineEdit = QtGui.QLineEdit(encryptionKeyImportDlg)
        self.lineEdit.setGeometry(QtCore.QRect(20, 40, 300, 31))
        self.lineEdit.setObjectName(_fromUtf8("lineEdit"))
        self.label = QtGui.QLabel(encryptionKeyImportDlg)
        self.label.setGeometry(QtCore.QRect(20, 10, 251, 17))
        self.label.setObjectName(_fromUtf8("label"))

        self.retranslateUi(encryptionKeyImportDlg)
        QtCore.QMetaObject.connectSlotsByName(encryptionKeyImportDlg)

    def retranslateUi(self, encryptionKeyImportDlg):
        self.label.setText(QtGui.QApplication.translate("encryptionKeyImportDlg", "Save Encrypted File as (*.gpg):", None, QtGui.QApplication.UnicodeUTF8))
        encryptionKeyImportDlg.setWindowTitle(QtGui.QApplication.translate("encryptionKeyImportDlg", "Encryption", None, QtGui.QApplication.UnicodeUTF8))
#         self.pushButton_Load.setText(QtGui.QApplication.translate("encryptionKeyImportDlg", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_OK.setText(QtGui.QApplication.translate("encryptionKeyImportDlg", "OK", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_Cancel.setText(QtGui.QApplication.translate("encryptionKeyImportDlg", "Close", None, QtGui.QApplication.UnicodeUTF8))

