# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'query_widget.ui'
#
# Updated for PyQt6 compatibility
#

from PyQt6 import QtCore, QtWidgets
import re
from UserNode import UserNode
from EdgeItem import EdgeItem
import MyFunctions

class Ui_RootInputDialog(object):

    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(468, 100)
        self.verticalLayoutWidget = QtWidgets.QWidget(Dialog)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 10, 450, 80))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label.setObjectName("label")
        self.lineEdit = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.lineEdit.setObjectName("lineEdit")
        self.verticalLayout.addWidget(self.label)
        self.verticalLayout.addWidget(self.lineEdit)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.OKPushButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.OKPushButton.setObjectName("OKPushButton")
        self.horizontalLayout.addWidget(self.OKPushButton)
        self.cancelPushButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.cancelPushButton.setObjectName("cancelPushButton")
        self.horizontalLayout.addWidget(self.cancelPushButton)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Edit Root Directory"))
        self.label.setText(_translate("Dialog", "Root Directory"))
        self.OKPushButton.setText(_translate("Dialog", "OK"))
        self.cancelPushButton.setText(_translate("Dialog", "Cancel"))
    
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
        Form.setObjectName("Form")
        Form.resize(214, 618)
        Form.setAutoFillBackground(True)
        self.tabId = 0
        self.main = main
        self.gridWidget = QtWidgets.QWidget()
        grid = QtWidgets.QGridLayout(self.gridWidget)
        grid.setVerticalSpacing(3)
        grid.addWidget(self.createProgramTraceViewExclusiveGroup(), 1, 0)
        gb = self.createSyscallListGroupBox()
        grid.addWidget(gb, 2, 0)
        grid.addItem(QtWidgets.QSpacerItem(0,300, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding), 3, 0)
        
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
        self.programTraceGroupBox = QtWidgets.QGroupBox('Program Trace View')
        vbox = QtWidgets.QVBoxLayout(self.programTraceGroupBox)
        self.importProgramFileInterface(vbox)
        self.programTraceGroupBox.setEnabled(True)
        return self.programTraceGroupBox
    
    def createLineSeparator(self, parent):
        line = QtWidgets.QFrame(parent)
        line.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        line.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        return line
    
    def importProgramFileInterface(self, vbox):
        widget = QtWidgets.QWidget(self.programTraceGroupBox)
        loadinCodeLabel = QtWidgets.QLabel('Import Program File:')
        hbox = QtWidgets.QHBoxLayout(widget)
        hbox.invalidate()
        self.strCodePath = QtWidgets.QLineEdit()
        self.btnLoadCode = QtWidgets.QPushButton('...')
        self.btnLoadCode.setSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Preferred)
#         self.btnConfirmCode = QtWidgets.QPushButton('Import')
        self.btnConfirmCode = QtWidgets.QPushButton('Run')
        hbox.addWidget(self.strCodePath)
        hbox.addWidget(self.btnLoadCode)
        hbox.setContentsMargins(0, 0, 0, 0)
        vbox.addWidget(loadinCodeLabel)
        vbox.addWidget(widget)
        vbox.addWidget(self.btnConfirmCode)

    def createSyscallListGroupBox(self):
        syscalls = ['open', 'read', 'write', 'fork']
        execalls = ['execvp', 'execv', 'execvpe', 'execlp', 'execl']
        ugidcalls = ['setuid', 'setgid', 'seteuid', 'setegid', 'setreuid', 'setregid']

        allGroupBox = QtWidgets.QGroupBox('Visualization Supported System Calls')
        allVbox = QtWidgets.QVBoxLayout()
        groupBox1 = QtWidgets.QGroupBox(allGroupBox)
        vbox1 = QtWidgets.QVBoxLayout(groupBox1)
        for i in syscalls:
            label = QtWidgets.QLabel(i)
            vbox1.addWidget(label)
        groupBox2 = QtWidgets.QGroupBox()
        vbox2 = QtWidgets.QVBoxLayout(groupBox2)
        for i in execalls:
            label = QtWidgets.QLabel(i)
            vbox2.addWidget(label)
        groupBox3 = QtWidgets.QGroupBox()
        vbox3 = QtWidgets.QVBoxLayout(groupBox3)
        for i in ugidcalls:
            label = QtWidgets.QLabel(i)
            vbox3.addWidget(label)
        allVbox.addWidget(groupBox1)
        allVbox.addWidget(groupBox2)
        allVbox.addWidget(groupBox3)
        allVbox.setContentsMargins(0, 0, 0, 0)
        allGroupBox.setLayout(allVbox)
        return allGroupBox
