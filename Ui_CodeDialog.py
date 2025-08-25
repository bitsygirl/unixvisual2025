# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'spec_dialog.ui'
# Updated for PyQt6 compatibility

from PyQt6 import QtCore, QtWidgets
from CodeEditor import CodeEditor

class Ui_CodeDialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(468, 437)
        self.verticalLayoutWidget = QtWidgets.QWidget(Dialog)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 10, 451, 421))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.codeEdit = CodeEditor(self.verticalLayoutWidget)
        self.codeEdit.setObjectName("codeEdit")
        self.verticalLayout.addWidget(self.codeEdit)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.runPushButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.runPushButton.setObjectName("runPushButton")
        self.horizontalLayout.addWidget(self.runPushButton)
        self.savePushButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.savePushButton.setObjectName("savePushButton")
        self.horizontalLayout.addWidget(self.savePushButton)
        self.closePushButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.closePushButton.setObjectName("closePushButton")
        self.horizontalLayout.addWidget(self.closePushButton)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Program"))
        self.runPushButton.setText(_translate("Dialog", "Different source file for display"))
        self.savePushButton.setText(_translate("Dialog", "Save and Run"))
        self.closePushButton.setText(_translate("Dialog", "Close"))
