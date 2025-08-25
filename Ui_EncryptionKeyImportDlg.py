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

class Ui_EncryptionKeyImportDlg(object):
    def setupUi(self, encryptionKeyImportDlg):
        encryptionKeyImportDlg.setObjectName("encryptionKeyImportDlg")
        encryptionKeyImportDlg.resize(350, 135)
#         self.pushButton_Load = QtWidgets.QPushButton(encryptionKeyImportDlg)
#         self.pushButton_Load.setGeometry(QtCore.QRect(440, 40, 31, 31))
#         self.pushButton_Load.setObjectName("pushButton_Load")
        self.pushButton_OK = QtWidgets.QPushButton(encryptionKeyImportDlg)
        self.pushButton_OK.setGeometry(QtCore.QRect(20, 90, 94, 27))
        self.pushButton_OK.setObjectName("pushButton_OK")
        self.pushButton_Cancel = QtWidgets.QPushButton(encryptionKeyImportDlg)
        self.pushButton_Cancel.setGeometry(QtCore.QRect(250, 90, 94, 27))
        self.pushButton_Cancel.setObjectName("pushButton_Cancel")
        self.lineEdit = QtWidgets.QLineEdit(encryptionKeyImportDlg)
        self.lineEdit.setGeometry(QtCore.QRect(20, 40, 300, 31))
        self.lineEdit.setObjectName("lineEdit")
        self.label = QtWidgets.QLabel(encryptionKeyImportDlg)
        self.label.setGeometry(QtCore.QRect(20, 10, 251, 17))
        self.label.setObjectName("label")

        self.retranslateUi(encryptionKeyImportDlg)
        QtCore.QMetaObject.connectSlotsByName(encryptionKeyImportDlg)

    def retranslateUi(self, encryptionKeyImportDlg):
        _translate = QtCore.QCoreApplication.translate
        self.label.setText(_translate("encryptionKeyImportDlg", "Save Encrypted File as (*.gpg):"))
        encryptionKeyImportDlg.setWindowTitle(_translate("encryptionKeyImportDlg", "Encryption"))
#         self.pushButton_Load.setText(_translate("encryptionKeyImportDlg", "..."))
        self.pushButton_OK.setText(_translate("encryptionKeyImportDlg", "OK"))
        self.pushButton_Cancel.setText(_translate("encryptionKeyImportDlg", "Close"))
