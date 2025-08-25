# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'spec_dialog.ui'
#
# Created: Tue Feb 21 15:40:52 2012
#      by: PyQt4 UI code generator 4.9
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui
from CodeEditor import CodeEditor

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_CodeDialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(468, 437)
        self.verticalLayoutWidget = QtGui.QWidget(Dialog)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 10, 451, 421))
        self.verticalLayoutWidget.setObjectName(_fromUtf8("verticalLayoutWidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.codeEdit = CodeEditor(self.verticalLayoutWidget)
#         self.codeEdit.setReadOnly(True)
        self.codeEdit.setObjectName(_fromUtf8("codeEdit"))
        self.verticalLayout.addWidget(self.codeEdit)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.runPushButton = QtGui.QPushButton(self.verticalLayoutWidget)
        self.runPushButton.setObjectName(_fromUtf8("runPushButton"))
        self.horizontalLayout.addWidget(self.runPushButton)
        self.savePushButton = QtGui.QPushButton(self.verticalLayoutWidget)
        self.savePushButton.setObjectName(_fromUtf8("savePushButton"))
        self.horizontalLayout.addWidget(self.savePushButton)
        self.closePushButton = QtGui.QPushButton(self.verticalLayoutWidget)
        self.closePushButton.setObjectName(_fromUtf8("closePushButton"))
        self.horizontalLayout.addWidget(self.closePushButton)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Program", None, QtGui.QApplication.UnicodeUTF8))
#         self.runPushButton.setText(QtGui.QApplication.translate("Dialog", "Run", None, QtGui.QApplication.UnicodeUTF8))
        self.runPushButton.setText(QtGui.QApplication.translate("Dialog", "Different source file for display", None, QtGui.QApplication.UnicodeUTF8))
        self.savePushButton.setText(QtGui.QApplication.translate("Dialog", "Save and Run", None, QtGui.QApplication.UnicodeUTF8))
        self.closePushButton.setText(QtGui.QApplication.translate("Dialog", "Close", None, QtGui.QApplication.UnicodeUTF8))

