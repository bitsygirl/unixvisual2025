'''
Accessible Access Control 1.0
2012-2104 Michigan Technological University
Supported in part by NSF grants: DUE-1140512, DUE-1245310 and IIS-1319363
Developer: Man Wang
Advisors:Dr. Steve Carr, Dr. Jean Mayo, Dr. Ching-Kuang Shene and Dr. Chaoli Wang

Updated for PyQt6 compatibility
'''
#-*- coding: utf-8 -*-
# Form implementation generated from reading ui file 'answerRenameDlg.ui'
# Updated for PyQt6 compatibility

from PyQt6 import QtCore, QtWidgets

class Ui_DecryptionDlg(object):
    def setupUi(self, decryptionDlg):
        decryptionDlg.setObjectName("decryptionDlg")
        decryptionDlg.resize(350, 135)
        self.pushButton_LoadKey = QtWidgets.QPushButton(decryptionDlg)
        self.pushButton_LoadKey.setGeometry(QtCore.QRect(440, 40, 31, 31))
        self.pushButton_LoadKey.setObjectName("pushButton_LoadKey")
        
        self.pushButton_LoadAnswer = QtWidgets.QPushButton(decryptionDlg)
        self.pushButton_LoadAnswer.setGeometry(QtCore.QRect(440, 40, 31, 31))
        self.pushButton_LoadAnswer.setObjectName("pushButton_LoadAnswer")
        
        self.pushButton_OK = QtWidgets.QPushButton(decryptionDlg)
        self.pushButton_OK.setGeometry(QtCore.QRect(20, 90, 94, 27))
        self.pushButton_OK.setObjectName("pushButton_OK")
        self.pushButton_Cancel = QtWidgets.QPushButton(decryptionDlg)
        self.pushButton_Cancel.setGeometry(QtCore.QRect(250, 90, 94, 27))
        self.pushButton_Cancel.setObjectName("pushButton_Cancel")
        self.lineEdit = QtWidgets.QLineEdit(decryptionDlg)
        self.lineEdit.setGeometry(QtCore.QRect(20, 40, 300, 31))
        self.lineEdit.setObjectName("lineEdit")
        self.keylabel = QtWidgets.QLabel(decryptionDlg)
        self.keylabel.setGeometry(QtCore.QRect(20, 10, 251, 17))
        self.keylabel.setObjectName("keylabel")
        self.answerlabel = QtWidgets.QLabel(decryptionDlg)
        self.answerlabel.setGeometry(QtCore.QRect(20, 10, 251, 17))
        self.answerlabel.setObjectName("answerlabel")

        self.retranslateUi(decryptionDlg)
        QtCore.QMetaObject.connectSlotsByName(decryptionDlg)

    def retranslateUi(self, decryptionDlg):
        _translate = QtCore.QCoreApplication.translate
        self.keylabel.setText(_translate("decryptionDlg", "Decryption Key"))
        decryptionDlg.setWindowTitle(_translate("decryptionDlg", "Decryption"))
        self.pushButton_LoadKey.setText(_translate("encryptionKeyImportDlg", "..."))
        self.pushButton_OK.setText(_translate("decryptionDlg", "OK"))
        self.pushButton_Cancel.setText(_translate("decryptionDlg", "Close"))
