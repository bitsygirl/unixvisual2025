'''
Accessible Access Control 1.0
2012-2104 Michigan Technological University
Supported in part by NSF grants: DUE-1140512, DUE-1245310 and IIS-1319363
Developer: Man Wang
Advisors:Dr. Steve Carr, Dr. Jean Mayo, Dr. Ching-Kuang Shene and Dr. Chaoli Wang

Updated for PyQt6 compatibility
'''
#-*- coding: utf-8 -*-
# Form implementation generated from reading ui file 'answerFileLoad.ui'
# Updated for PyQt6 compatibility

from PyQt6 import QtCore, QtWidgets

class Ui_AnswerNPrivateKeyLoad(object):
    def setupUi(self, answerFileLoad):
        answerFileLoad.setObjectName("answerFileLoad")
        answerFileLoad.resize(481, 135)
        self.pushButton_Load = QtWidgets.QPushButton(answerFileLoad)
        self.pushButton_Load.setGeometry(QtCore.QRect(440, 40, 31, 31))
        self.pushButton_Load.setObjectName("pushButton_Load")
        self.pushButton_OK = QtWidgets.QPushButton(answerFileLoad)
        self.pushButton_OK.setGeometry(QtCore.QRect(20, 90, 94, 27))
        self.pushButton_OK.setObjectName("pushButton_OK")
        self.pushButton_Cancel = QtWidgets.QPushButton(answerFileLoad)
        self.pushButton_Cancel.setGeometry(QtCore.QRect(330, 90, 94, 27))
        self.pushButton_Cancel.setObjectName("pushButton_Cancel")
        self.lineEdit_Dir = QtWidgets.QLineEdit(answerFileLoad)
        self.lineEdit_Dir.setGeometry(QtCore.QRect(20, 40, 411, 31))
        self.lineEdit_Dir.setObjectName("lineEdit_Dir")
        self.label = QtWidgets.QLabel(answerFileLoad)
        self.label.setGeometry(QtCore.QRect(20, 10, 251, 17))
        self.label.setObjectName("label")

        self.retranslateUi(answerFileLoad)
        QtCore.QMetaObject.connectSlotsByName(answerFileLoad)

    def retranslateUi(self, answerFileLoad):
        _translate = QtCore.QCoreApplication.translate
        answerFileLoad.setWindowTitle(_translate("answerFileLoad", "Load in Answer File"))
        self.pushButton_Load.setText(_translate("answerFileLoad", "..."))
        self.pushButton_OK.setText(_translate("answerFileLoad", "OK"))
        self.pushButton_Cancel.setText(_translate("answerFileLoad", "Cancel"))
        self.label.setText(_translate("answerFileLoad", "Encrypted Answer File:"))
