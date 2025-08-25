'''
Created on Sep 3, 2015

@author: manwang
'''
from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s
    
class Ui_ProcessNodeParamDialog(object):

    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(468, 437)
        self.verticalLayoutWidget = QtGui.QWidget(Dialog)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 10, 451, 421))
        self.verticalLayoutWidget.setObjectName(_fromUtf8("verticalLayoutWidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.browser = QtGui.QTableWidget(15, 2, self.verticalLayoutWidget)
        headerlist = [QtCore.QString('Property'), QtCore.QString('Value')]
        self.browser.setHorizontalHeaderLabels(headerlist)
        self.browser.setAlternatingRowColors(True)
        self.browser.verticalHeader().hide()
        self.browser.horizontalHeader().setResizeMode(QtGui.QHeaderView.Stretch)
        self.verticalLayout.addWidget(self.browser)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.closePushButton = QtGui.QPushButton(self.verticalLayoutWidget)
        self.closePushButton.setObjectName(_fromUtf8("closePushButton"))
        self.horizontalLayout.addWidget(self.closePushButton)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        
    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Parameters", None, QtGui.QApplication.UnicodeUTF8))
#         self.runPushButton.setText(QtGui.QApplication.translate("Dialog", "Run", None, QtGui.QApplication.UnicodeUTF8))
#         self.savePushButton.setText(QtGui.QApplication.translate("Dialog", "Save", None, QtGui.QApplication.UnicodeUTF8))
        self.closePushButton.setText(QtGui.QApplication.translate("Dialog", "Close", None, QtGui.QApplication.UnicodeUTF8))