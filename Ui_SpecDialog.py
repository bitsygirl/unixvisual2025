# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'spec_dialog.ui'
#
# Updated for PyQt6 compatibility
#

from PyQt6 import QtCore, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(468, 437)
        self.verticalLayoutWidget = QtWidgets.QWidget(Dialog)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 10, 451, 421))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.specTextEdit = QtWidgets.QTextEdit(self.verticalLayoutWidget)
        self.specTextEdit.setReadOnly(True)
        self.specTextEdit.setObjectName("specTextEdit")
        self.verticalLayout.addWidget(self.specTextEdit)
        self.closePushButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.closePushButton.setObjectName("closePushButton")
        self.verticalLayout.addWidget(self.closePushButton)
        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Specification"))
        self.closePushButton.setText(_translate("Dialog", "Close"))
