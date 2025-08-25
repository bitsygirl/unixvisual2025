# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MainWindow.ui'
# Updated for PyQt6 compatibility

from PyQt6 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(697, 574)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.centralwidget.setGeometry(QtCore.QRect(0,0,697,574))
        '''MENUBAR'''
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 697, 25))
        self.menubar.setObjectName("menubar")
        self.menu_File = QtWidgets.QMenu(self.menubar)
        self.menu_File.setObjectName("menu_File")
        self.menu_View = QtWidgets.QMenu(self.menubar)
        self.menu_View.setObjectName("menu_View")
        self.menu_Settings = QtWidgets.QMenu(self.menubar)
        self.menu_Settings.setObjectName("menu_Settings")
        self.menu_Practice = QtWidgets.QMenu(self.menubar)
        self.menu_Practice.setObjectName("menu_Practice")
        self.menu_Help = QtWidgets.QMenu(self.menubar)
        self.menu_Help.setObjectName("menu_Help")
        MainWindow.setMenuBar(self.menubar)
        '''STATUSBAR'''
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        self.introLabel = QtWidgets.QLabel(self.statusbar)
        self.introLabel.setGeometry(QtCore.QRect(2,0,2000,20))
        self.introLabel.setObjectName("introLabel")
        self.introLabel.setText('')
        MainWindow.setStatusBar(self.statusbar)
        
        '''TOOLBAR'''
        self.toolBar = QtWidgets.QToolBar(MainWindow)
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(QtCore.Qt.ToolBarArea.TopToolBarArea, self.toolBar)
        
        '''IO'''
        self.actionNew = QtGui.QAction(MainWindow)
        self.actionNew.setObjectName("actionNew")
        self.actionNew.setToolTip("Create a blank graph")
        
        self.actionImport = QtGui.QAction(MainWindow)
        self.actionImport.setObjectName("actionImport")
        self.actionImport.setToolTip("Import a unix specification file")
        
        self.actionExport = QtGui.QAction(MainWindow)
        self.actionExport.setObjectName("actionExport")
        self.actionExport.setToolTip("Export as a unix specification file")

        '''MISCELLANEOUS'''
        self.actionExit = QtGui.QAction(MainWindow)
        self.actionExit.setObjectName("actionExit")
        
        self.actionHelp_Contents = QtGui.QAction(MainWindow)
        self.actionHelp_Contents.setObjectName("actionHelp_Contents")
        
        '''VIEWS and GRAPHS'''
        self.actionView_Object = QtGui.QAction(MainWindow)
        self.actionView_Object.setCheckable(True)
        self.actionView_Object.setChecked(True)
        self.actionView_Object.setObjectName("actionView_Object")
        self.actionView_Object.setToolTip("Show permissions of a specified object")
        
        self.actionView_User = QtGui.QAction(MainWindow)
        self.actionView_User.setCheckable(True)
        self.actionView_User.setObjectName("actionView_User")
        self.actionView_User.setToolTip("Show permissions of users")
 
        self.actionView_Group = QtGui.QAction(MainWindow)
        self.actionView_Group.setCheckable(True)
        self.actionView_Group.setObjectName("actionView_Group")
        self.actionView_Group.setToolTip("Show permissions of groups")
        
        self.actionView_ProgramTrace = QtGui.QAction(MainWindow)
        self.actionView_ProgramTrace.setCheckable(True)
        self.actionView_ProgramTrace.setObjectName("actionView_ProgramTrace")
        self.actionView_ProgramTrace.setToolTip("Show the program execution with permission details")

        '''animation'''
        self.actionAnimation = QtGui.QAction(MainWindow)
        self.actionAnimation.setCheckable(True)
        self.actionAnimation.setObjectName("actionAnimation")
        self.actionAnimation.setToolTip("Toggle Animation for Query")
        
        self.actionAnimation_SetInterval = QtGui.QAction(MainWindow)
        self.actionAnimation_SetInterval.setObjectName("actionAnimation_SetInterval")
        '''SPEC'''
        self.actionSpecification = QtGui.QAction(MainWindow)
        self.actionSpecification.setObjectName("actionSpecification")
        self.actionSpecification.setToolTip("Show the specification file")
        '''ToolBox'''
        self.actionToolBox = QtGui.QAction(MainWindow)
        self.actionToolBox.setObjectName("actionToolBox")
        self.actionToolBox.setCheckable(True)
        '''Change Root Directory'''
        self.actionChangeRoot= QtGui.QAction(MainWindow)
        self.actionChangeRoot.setObjectName("actionChangeRoot")
        self.actionChangeRoot.setToolTip("Change the root directory")
        '''QUERY'''
        self.actionQuery_Window = QtGui.QAction(MainWindow)
        self.actionQuery_Window.setObjectName("actionQuery_Window")
        self.actionQuery_Window.setCheckable(True)
        '''Numeric-letter presentation of permission'''
        self.actionPermission_Calculator_Window = QtGui.QAction(MainWindow)
        self.actionPermission_Calculator_Window.setObjectName("actionPermission_Calculator_Window")
        self.actionPermission_Calculator_Window.setCheckable(True)
        '''Process view'''
        self.actionView_Process = QtGui.QAction(MainWindow)
        self.actionView_Process.setObjectName("actionView_Process")
        self.actionView_Process.setCheckable(True)
        '''Permission view'''
        self.actionView_Permission = QtGui.QAction(MainWindow)
        self.actionView_Permission.setObjectName("actionView_Permission")
        self.actionView_Permission.setCheckable(True)
        '''Test'''
        self.actionTest = QtGui.QAction(MainWindow)
        self.actionTest.setObjectName("actionTest")
        self.actionTest.setCheckable(True)
        '''Decrypt'''
        self.actionDecrypt = QtGui.QAction(MainWindow)
        self.actionDecrypt.setObjectName("actionDecrypt")
        self.actionDecrypt.setCheckable(True)
        
        '''add actions to menubar'''
        self.menu_File.addAction(self.actionNew)
        self.menu_File.addAction(self.actionImport)
        self.menu_File.addAction(self.actionExit)
        
        self.menu_View.addAction(self.actionView_Object)
        self.menu_View.addAction(self.actionView_User)
        self.menu_View.addAction(self.actionView_Group)
        self.menu_View.addAction(self.actionView_ProgramTrace)
        self.menu_View.addSeparator()
        self.menu_View.addAction(self.actionToolBox)
        self.menu_View.addAction(self.actionSpecification)
        self.menu_View.addAction(self.actionQuery_Window)
        self.menu_View.addSeparator()
        self.menu_Practice.addAction(self.actionTest)
        
        self.menu_Help.addAction(self.actionHelp_Contents)
        
        self.menubar.addAction(self.menu_File.menuAction())
        self.menubar.addAction(self.menu_View.menuAction())
        self.menubar.addAction(self.menu_Practice.menuAction())
        self.menubar.addAction(self.menu_Help.menuAction())

        self.retranslateUi(MainWindow)
        self.actionExit.triggered.connect(MainWindow.close)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.menu_File.setTitle(_translate("MainWindow", "&File"))
        self.menu_View.setTitle(_translate("MainWindow", "&View"))
        self.menu_Practice.setTitle(_translate("MainWindow", "&Practice"))
        self.menu_Help.setTitle(_translate("MainWindow", "&Help"))
        
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar"))
        self.actionHelp_Contents.setText(_translate("MainWindow", "Help Contents"))
        self.actionHelp_Contents.setShortcut(_translate("MainWindow", "F1"))
        self.actionNew.setText(_translate("MainWindow", "New"))
        self.actionNew.setShortcut(_translate("MainWindow", "Ctrl+N"))
        
        self.actionExit.setText(_translate("MainWindow", "Exit"))
        self.actionExit.setShortcut(_translate("MainWindow", "Ctrl+Q"))
        
        self.actionImport.setText(_translate("MainWindow", "Import"))
        self.actionExport.setText(_translate("MainWindow", "Export"))
        
        self.actionView_Object.setText(_translate("MainWindow", "Object View"))
        self.actionView_User.setText(_translate("MainWindow", "User View"))
        self.actionView_Group.setText(_translate("MainWindow", "Group View"))
        self.actionView_ProgramTrace.setText(_translate("MainWindow", "Program Trace View"))
        self.actionView_Process.setText(_translate("MainWindow", "Process View"))
        self.actionView_Permission.setText(_translate("MainWindow", "Permission View"))
        self.actionAnimation.setText(_translate("MainWindow", "Toggle Animation for Views"))
        self.actionAnimation_SetInterval.setText(_translate("MainWindow", "Set Animation Interval"))
        self.actionToolBox.setText(_translate("MainWindow", "Tool Box"))
        self.actionSpecification.setText(_translate("MainWindow", "Specification"))
        self.actionQuery_Window.setText(_translate("MainWindow", "Query Window"))
        self.actionChangeRoot.setText(_translate("MainWindow", "Change Root Directory"))
        self.actionTest.setText(_translate("MainWindow", "Quiz Mode"))
        self.actionDecrypt.setText(_translate("MainWindow", "Decrypt Answer File"))
        self.actionPermission_Calculator_Window.setText(_translate("MainWindow", "Permission Calculator"))
