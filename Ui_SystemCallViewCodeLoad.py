'''
Accessible Access Control 1.0
2012-2104 Michigan Technological University
Supported in part by NSF grants: DUE-1140512, DUE-1245310 and IIS-1319363
Developer: Man Wang
Updated for PyQt6 compatibility
Advisors:Dr. Steve Carr, Dr. Jean Mayo, Dr. Ching-Kuang Shene and Dr. Chaoli Wang
'''
#-*- coding: utf-8 -*-
# Form implementation generated from reading ui file 'codeLoad.ui'
# Updated for PyQt6 compatibility

from PyQt6 import QtCore, QtWidgets

class Ui_SyscallOutputDialog(object):
    def setupUi(self, outputdlg):
        outputdlg.setObjectName("outputdlg")
        outputdlg.resize(481, 437)
        verticalLayout = QtWidgets.QVBoxLayout(outputdlg)
        verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.pushButton_Close = QtWidgets.QPushButton()
        self.textEdit_Output = QtWidgets.QPlainTextEdit()
        self.textEdit_Output.setReadOnly(True)
        verticalLayout.addWidget(self.textEdit_Output)
        verticalLayout.addWidget(self.pushButton_Close)
        
        self.retranslateUi(outputdlg)
        QtCore.QMetaObject.connectSlotsByName(outputdlg)

    def retranslateUi(self, outputdlg):
        _translate = QtCore.QCoreApplication.translate
        outputdlg.setWindowTitle(_translate("outputdlg", "Program Standard Output"))
        self.pushButton_Close.setText(_translate("outputdlg", "Close"))

class Ui_SystemCallViewCodeLoad(object):
    def setupUi(self, codeLoad):
        codeLoad.setObjectName("codeLoad")
        codeLoad.resize(481, 135)
        self.pushButton_Load = QtWidgets.QPushButton(codeLoad)
        self.pushButton_Load.setGeometry(QtCore.QRect(440, 40, 31, 31))
        self.pushButton_Load.setObjectName("pushButton_Load")
        self.pushButton_OK = QtWidgets.QPushButton(codeLoad)
        self.pushButton_OK.setGeometry(QtCore.QRect(20, 90, 94, 27))
        self.pushButton_OK.setObjectName("pushButton_OK")
        self.pushButton_Cancel = QtWidgets.QPushButton(codeLoad)
        self.pushButton_Cancel.setGeometry(QtCore.QRect(330, 90, 94, 27))
        self.pushButton_Cancel.setObjectName("pushButton_Cancel")
        self.lineEdit_Dir = QtWidgets.QLineEdit(codeLoad)
        self.lineEdit_Dir.setGeometry(QtCore.QRect(20, 40, 411, 31))
        self.lineEdit_Dir.setObjectName("lineEdit_Dir")
        self.label = QtWidgets.QLabel(codeLoad)
        self.label.setGeometry(QtCore.QRect(20, 10, 251, 17))
        self.label.setObjectName("label")

        self.retranslateUi(codeLoad)
        QtCore.QMetaObject.connectSlotsByName(codeLoad)

    def retranslateUi(self, codeLoad):
        _translate = QtCore.QCoreApplication.translate
        codeLoad.setWindowTitle(_translate("codeLoad", "Load in Program"))
        self.pushButton_Load.setText(_translate("codeLoad", "..."))
        self.pushButton_OK.setText(_translate("codeLoad", "OK"))
        self.pushButton_Cancel.setText(_translate("codeLoad", "Cancel"))
        self.label.setText(_translate("codeLoad", "Program File (*.c) :"))
