# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'query_widget.ui'
#
# Created: Mon Feb 27 21:37:40 2012
#      by: PyQt4 UI code generator 4.9
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui
import re
from UserNode import UserNode
from EdgeItem import EdgeItem
import MyFunctions

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_RootInputDialog(object):

    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(468, 100)
        self.verticalLayoutWidget = QtGui.QWidget(Dialog)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 10, 450, 80))
        self.verticalLayoutWidget.setObjectName(_fromUtf8("verticalLayoutWidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.label = QtGui.QLabel(self.verticalLayoutWidget)
        self.label.setObjectName(_fromUtf8("label"))
        self.lineEdit = QtGui.QLineEdit(self.verticalLayoutWidget)
        self.lineEdit.setObjectName(_fromUtf8("lineEdit"))
        self.verticalLayout.addWidget(self.label)
        self.verticalLayout.addWidget(self.lineEdit)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.OKPushButton = QtGui.QPushButton(self.verticalLayoutWidget)
        self.OKPushButton.setObjectName(_fromUtf8("OKPushButton"))
        self.horizontalLayout.addWidget(self.OKPushButton)
        self.cancelPushButton = QtGui.QPushButton(self.verticalLayoutWidget)
        self.cancelPushButton.setObjectName(_fromUtf8("cancelPushButton"))
        self.horizontalLayout.addWidget(self.cancelPushButton)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Edit Root Directory", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Dialog", "Root Directory", None, QtGui.QApplication.UnicodeUTF8))
        self.OKPushButton.setText(QtGui.QApplication.translate("Dialog", "OK", None, QtGui.QApplication.UnicodeUTF8))
        self.cancelPushButton.setText(QtGui.QApplication.translate("Dialog", "Cancel", None, QtGui.QApplication.UnicodeUTF8))
    
class Ui_ToolBox(object):
    NUM_GROUPBOX = 3
    '''ids for tabs'''
    MODIFY_TAB = 0
    ADD_TAB = 1
    DELETE_TAB = 2
    '''none item in combobox'''
    NONE_ITEM = 'None'
    
    openFlags = ['O_RDONLY', 'O_WRONLY','O_RDWR', 'O_CREAT', 'O_TRUNC']
    openMode = ['S_IRWXU', 'S_IRUSR', 'S_IWUSR', 'S_IXUSR', 'S_IRWXG', 'S_IRGRP',\
            'S_IWGRP', 'S_IXGRP', 'S_IRWXO', 'S_IROTH', 'S_IWOTH', 'S_IXOTH']
    
    def setupUi(self, Form, main):
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(214, 618)
        Form.setAutoFillBackground(True)
        self.tabId = 0
        self.main = main
        self.gridWidget = QtGui.QWidget()
        grid = QtGui.QGridLayout(self.gridWidget)
        grid.setVerticalSpacing(3)
        grid.addWidget(self.createProgramTraceViewExclusiveGroup(), 1, 0)
        gb = self.createSyscallListGroupBox()
        grid.addWidget(gb, 2, 0)
        grid.addItem(QtGui.QSpacerItem(0,300, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding), 3, 0)
        
    def isNameEmpty(self, name):
        p = re.compile('^(\s)*$')
        if p.match(name):
            return True
        else:
            return False
        
    def nameHasSpace(self, name):
        if (re.search('\s', name)):
            return True
        else:
            return False
             
    def createProgramTraceViewExclusiveGroup(self):
        self.programTraceGroupBox = QtGui.QGroupBox('Program Trace View')
        vbox = QtGui.QVBoxLayout(self.programTraceGroupBox)
        self.importProgramFileInterface(vbox)
        self.programTraceGroupBox.setEnabled(True)
        return self.programTraceGroupBox
    
    def createLineSeparator(self, parent):
        line = QtGui.QFrame(parent)
        line.setFrameShape(QtGui.QFrame.HLine)
        line.setFrameShadow(QtGui.QFrame.Sunken)
        return line
    
    def importProgramFileInterface(self, vbox):
        widget = QtGui.QWidget(self.programTraceGroupBox)
        loadinCodeLabel = QtGui.QLabel('Import Program File:')
        hbox = QtGui.QHBoxLayout(widget)
        hbox.invalidate()
        self.strCodePath = QtGui.QLineEdit()
        self.btnLoadCode = QtGui.QPushButton('...')
        self.btnLoadCode.setSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Preferred)
#         self.btnConfirmCode = QtGui.QPushButton('Import')
        self.btnConfirmCode = QtGui.QPushButton('Run')
        hbox.addWidget(self.strCodePath)
        hbox.addWidget(self.btnLoadCode)
        hbox.setMargin(0)
        vbox.addWidget(loadinCodeLabel)
        vbox.addWidget(widget)
        vbox.addWidget(self.btnConfirmCode)

    def createSyscallListGroupBox(self):
        syscalls = ['open', 'read', 'write', 'fork']
        execalls = ['execvp', 'execv', 'execvpe', 'execlp', 'execl']
        ugidcalls = ['setuid', 'setgid', 'seteuid', 'setegid', 'setreuid', 'setregid']

        allGroupBox = QtGui.QGroupBox('Visualization Supported System Calls')
        allVbox = QtGui.QVBoxLayout()
        groupBox1 = QtGui.QGroupBox(allGroupBox)
        vbox1 = QtGui.QVBoxLayout(groupBox1)
        for i in syscalls:
            label = QtGui.QLabel(i)
            vbox1.addWidget(label)
        groupBox2 = QtGui.QGroupBox()
        vbox2 = QtGui.QVBoxLayout(groupBox2)
        for i in execalls:
            label = QtGui.QLabel(i)
            vbox2.addWidget(label)
        groupBox3 = QtGui.QGroupBox()
        vbox3 = QtGui.QVBoxLayout(groupBox3)
        for i in ugidcalls:
            label = QtGui.QLabel(i)
            vbox3.addWidget(label)
        allVbox.addWidget(groupBox1)
        allVbox.addWidget(groupBox2)
        allVbox.addWidget(groupBox3)
        allVbox.setMargin(0)
        allGroupBox.setLayout(allVbox)
        return allGroupBox


            