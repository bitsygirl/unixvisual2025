# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'spec_dialog.ui'
#
# Created: Tue Feb 21 15:40:52 2012
#      by: PyQt4 UI code generator 4.9
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(468, 437)
        self.verticalLayoutWidget = QtGui.QWidget(Dialog)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 10, 451, 421))
        self.verticalLayoutWidget.setObjectName(_fromUtf8("verticalLayoutWidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.specTextEdit = QtGui.QTextEdit(self.verticalLayoutWidget)
        self.specTextEdit.setReadOnly(True)
        self.specTextEdit.setObjectName(_fromUtf8("specTextEdit"))
        self.verticalLayout.addWidget(self.specTextEdit)
        self.closePushButton = QtGui.QPushButton(self.verticalLayoutWidget)
        self.closePushButton.setObjectName(_fromUtf8("closePushButton"))
        self.verticalLayout.addWidget(self.closePushButton)
        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Specification", None, QtGui.QApplication.UnicodeUTF8))
        self.closePushButton.setText(QtGui.QApplication.translate("Dialog", "Close", None, QtGui.QApplication.UnicodeUTF8))

