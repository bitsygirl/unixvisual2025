'''
Accessible Access Control 1.0
2012-2104 Michigan Technological University
Supported in part by NSF grants: DUE-1140512, DUE-1245310 and IIS-1319363
Developer: Man Wang
Advisors:Dr. Steve Carr, Dr. Jean Mayo, Dr. Ching-Kuang Shene and Dr. Chaoli Wang
'''
# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './Desktop/test.ui'
#
# Created: Sun Nov 10 11:09:48 2013
#      by: PyQt4 UI code generator 4.9.1
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
        Dialog.resize(640, 538)
        font = QtGui.QFont()
        font.setPointSize(12)
        Dialog.setFont(font)
        self.verticalLayoutWidget = QtGui.QWidget(Dialog)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(20, 10, 601, 511))
        self.verticalLayoutWidget.setObjectName(_fromUtf8("verticalLayoutWidget"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout_2.setMargin(0)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.groupBox = QtGui.QGroupBox(self.verticalLayoutWidget)
        self.groupBox.setTitle(_fromUtf8(""))
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.labQuestion1 = QtGui.QLabel(self.groupBox)
        self.labQuestion1.setGeometry(QtCore.QRect(10, 30, 421, 39))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.labQuestion1.setFont(font)
        self.labQuestion1.setText(_fromUtf8(""))
        self.labQuestion1.setWordWrap(True)
        self.labQuestion1.setObjectName(_fromUtf8("labQuestion1"))
        self.radioButton_1 = QtGui.QRadioButton(self.groupBox)
        self.radioButton_1.setGeometry(QtCore.QRect(20, 170, 21, 19))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.radioButton_1.setFont(font)
        self.radioButton_1.setText(_fromUtf8(""))
        self.radioButton_1.setObjectName(_fromUtf8("radioButton_1"))
        self.label_2 = QtGui.QLabel(self.groupBox)
        self.label_2.setGeometry(QtCore.QRect(50, 90, 179, 181))
        self.label_2.setText(_fromUtf8(""))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.radioButton_2 = QtGui.QRadioButton(self.groupBox)
        self.radioButton_2.setGeometry(QtCore.QRect(290, 170, 21, 24))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.radioButton_2.setFont(font)
        self.radioButton_2.setText(_fromUtf8(""))
        self.radioButton_2.setObjectName(_fromUtf8("radioButton_2"))
        self.radioButton_3 = QtGui.QRadioButton(self.groupBox)
        self.radioButton_3.setGeometry(QtCore.QRect(20, 350, 21, 24))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.radioButton_3.setFont(font)
        self.radioButton_3.setText(_fromUtf8(""))
        self.radioButton_3.setObjectName(_fromUtf8("radioButton_3"))
        self.radioButton_4 = QtGui.QRadioButton(self.groupBox)
        self.radioButton_4.setGeometry(QtCore.QRect(290, 350, 21, 24))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.radioButton_4.setFont(font)
        self.radioButton_4.setText(_fromUtf8(""))
        self.radioButton_4.setObjectName(_fromUtf8("radioButton_4"))
        self.label_3 = QtGui.QLabel(self.groupBox)
        self.label_3.setGeometry(QtCore.QRect(320, 90, 179, 181))
        self.label_3.setText(_fromUtf8(""))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.label_4 = QtGui.QLabel(self.groupBox)
        self.label_4.setGeometry(QtCore.QRect(50, 270, 179, 181))
        self.label_4.setText(_fromUtf8(""))
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.label_5 = QtGui.QLabel(self.groupBox)
        self.label_5.setGeometry(QtCore.QRect(320, 270, 179, 181))
        self.label_5.setText(_fromUtf8(""))
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.verticalLayout_2.addWidget(self.groupBox)
        self.pushButton = QtGui.QPushButton(self.verticalLayoutWidget)
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.verticalLayout_2.addWidget(self.pushButton)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Test", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton.setText(QtGui.QApplication.translate("Dialog", "PushButton", None, QtGui.QApplication.UnicodeUTF8))

