'''
Created on Sep 3, 2015

@author: manwang
Updated for PyQt6 compatibility
'''
from PyQt6 import QtCore, QtWidgets

class Ui_ProcessNodeParamDialog(object):

    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(468, 437)
        self.verticalLayoutWidget = QtWidgets.QWidget(Dialog)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 10, 451, 421))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)  # setMargin deprecated
        self.verticalLayout.setObjectName("verticalLayout")
        self.browser = QtWidgets.QTableWidget(15, 2, self.verticalLayoutWidget)
        headerlist = ['Property', 'Value']  # QString removed
        self.browser.setHorizontalHeaderLabels(headerlist)
        self.browser.setAlternatingRowColors(True)
        self.browser.verticalHeader().hide()
        # setResizeMode deprecated - use setSectionResizeMode
        self.browser.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)
        self.verticalLayout.addWidget(self.browser)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.closePushButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.closePushButton.setObjectName("closePushButton")
        self.horizontalLayout.addWidget(self.closePushButton)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        
    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Parameters"))
        self.closePushButton.setText(_translate("Dialog", "Close"))
