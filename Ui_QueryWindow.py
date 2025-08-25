# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'query_widget.ui'
#
# Created: Mon Feb 27 21:37:40 2012
#      by: PyQt4 UI code generator 4.9
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui
try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_QueryWindow(object):
    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(214, 618)
        Form.setAutoFillBackground(True)
        self.horizontalLayoutWidget = QtGui.QWidget(Form)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(0, 0, 211, 611))
        self.horizontalLayoutWidget.setObjectName(_fromUtf8("horizontalLayoutWidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.horizontalLayoutWidget)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.createQueryPanel()
        #self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def createQueryPanel(self):
        self.queryTypeGroupBox = QtGui.QGroupBox(self.horizontalLayoutWidget)
        self.queryTypeGroupBox.setObjectName(_fromUtf8("queryTypeGroupBox"))
        self.verticalLayoutWidget_2 = QtGui.QWidget(self.queryTypeGroupBox)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(0, 20, 201, 191))
        self.verticalLayoutWidget_2.setObjectName(_fromUtf8("verticalLayoutWidget_2"))
        self.queryTypeLayout = QtGui.QVBoxLayout(self.verticalLayoutWidget_2)
        self.queryTypeLayout.setMargin(0)
        self.queryTypeLayout.setObjectName(_fromUtf8("queryTypeLayout"))
        self.queryListWidget = QtGui.QListWidget(self.verticalLayoutWidget_2)
        self.queryListWidget.setObjectName(_fromUtf8("queryListWidget"))
        self.queryTypeLayout.addWidget(self.queryListWidget)
        self.verticalLayout.addWidget(self.queryTypeGroupBox)
        self.createQueryInputInterface()
        self.runQueryGroupBox = QtGui.QGroupBox(self.horizontalLayoutWidget)
        self.runQueryGroupBox.setObjectName(_fromUtf8("runQueryGroupBox"))
        self.verticalLayoutWidget = QtGui.QWidget(self.runQueryGroupBox)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(0, 20, 201, 201))
        self.verticalLayoutWidget.setObjectName(_fromUtf8("verticalLayoutWidget"))
        self.runQueryLayout = QtGui.QVBoxLayout(self.verticalLayoutWidget)
        self.runQueryLayout.setMargin(0)
        self.runQueryLayout.setObjectName(_fromUtf8("runQueryLayout"))
        self.runQueryButton = QtGui.QPushButton(self.verticalLayoutWidget)
        self.runQueryButton.setText('Run Query')
        self.runQueryButton.setObjectName(_fromUtf8("runQueryButton"))
        self.runQueryLayout.addWidget(self.runQueryButton)
        self.clearButton = QtGui.QPushButton(self.verticalLayoutWidget)
        self.clearButton.setText('Clear Output')
        self.clearButton.setObjectName(_fromUtf8("clearButton"))
        self.runQueryLayout.addWidget(self.clearButton)
        self.verticalLayout.addWidget(self.runQueryGroupBox)
        
    def createQueryInputInterface(self):
        self.queryInputGroupBox = QtGui.QGroupBox(self.horizontalLayoutWidget)
        self.queryInputGroupBox.setObjectName(_fromUtf8("queryInputGroupBox"))
        self.gridLayoutWidget = QtGui.QWidget(self.queryInputGroupBox)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(0, 20, 300, 191))
        self.gridLayoutWidget.setObjectName(_fromUtf8("gridLayoutWidget"))
        self.queryInputLayout = QtGui.QGridLayout(self.gridLayoutWidget)
        self.queryInputLayout.setMargin(0)
        self.queryInputLayout.setObjectName(_fromUtf8("queryInputLayout"))
        self.file1Label = QtGui.QLabel(self.gridLayoutWidget)
        self.file1Label.setObjectName(_fromUtf8("file1Label"))
        self.queryInputLayout.addWidget(self.file1Label, 1, 0, 1, 1)
        self.file1ComboBox = QtGui.QComboBox(self.gridLayoutWidget)
        self.file1ComboBox.setObjectName(_fromUtf8("file1ComboBox"))
        self.queryInputLayout.addWidget(self.file1ComboBox, 1, 1, 1, 1)
        self.lineEditLabel = QtGui.QLabel(self.gridLayoutWidget)
        self.lineEditLabel.setObjectName(_fromUtf8("lineEditLabel"))
        self.queryInputLayout.addWidget(self.lineEditLabel, 0, 0, 1, 1)
        self.lineEdit = QtGui.QLineEdit(self.gridLayoutWidget)
        self.lineEdit.setObjectName(_fromUtf8("lineEdit"))
        self.queryInputLayout.addWidget(self.lineEdit, 0, 1, 1, 1)
        self.file2Label = QtGui.QLabel(self.gridLayoutWidget)
        self.file2Label.setObjectName(_fromUtf8("file2Label"))
        self.queryInputLayout.addWidget(self.file2Label, 2, 0, 1, 1)
        self.file2ComboBox = QtGui.QComboBox(self.gridLayoutWidget)
        self.file2ComboBox.setObjectName(_fromUtf8("file2ComboBox"))
        self.queryInputLayout.addWidget(self.file2ComboBox, 2, 1, 1, 1)
        self.file3Label = QtGui.QLabel(self.gridLayoutWidget)
        self.file3Label.setObjectName(_fromUtf8("file3Label"))
        self.queryInputLayout.addWidget(self.file3Label, 3, 0, 1, 1)
        self.file3ComboBox = QtGui.QComboBox(self.gridLayoutWidget)
        self.file3ComboBox.setObjectName(_fromUtf8("file3ComboBox"))
        self.queryInputLayout.addWidget(self.file3ComboBox, 3, 1, 1, 1)
        self.verticalLayout.addWidget(self.queryInputGroupBox)