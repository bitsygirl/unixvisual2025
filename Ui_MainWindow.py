# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MainWindow.ui'
#
# Created: Apr 16, 2015
#      by: PyQt4 UI code generator 4.9.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(697, 574)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.centralwidget.setGeometry(QtCore.QRect(0,0,697,574))
        '''MENUBAR'''
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 697, 25))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menu_File = QtGui.QMenu(self.menubar)
        self.menu_File.setObjectName(_fromUtf8("menu_File"))
        self.menu_View = QtGui.QMenu(self.menubar)
        self.menu_View.setObjectName(_fromUtf8("menu_View"))
        self.menu_Settings = QtGui.QMenu(self.menubar)
        self.menu_Settings.setObjectName(_fromUtf8("menu_Settings"))
        self.menu_Practice = QtGui.QMenu(self.menubar)
        self.menu_Practice.setObjectName(_fromUtf8("menu_Practice"))
        self.menu_Help = QtGui.QMenu(self.menubar)
        self.menu_Help.setObjectName(_fromUtf8("menu_Help"))
        MainWindow.setMenuBar(self.menubar)
        '''STATUSBAR'''
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        self.introLabel = QtGui.QLabel(self.statusbar)
        self.introLabel.setGeometry(QtCore.QRect(2,0,2000,20))
        self.introLabel.setObjectName(_fromUtf8("introLabel"))
        self.introLabel.setText('')
        MainWindow.setStatusBar(self.statusbar)
        
        '''TOOLBAR'''
        self.toolBar = QtGui.QToolBar(MainWindow)
        self.toolBar.setObjectName(_fromUtf8("toolBar"))
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        
        '''IO'''
        self.actionNew = QtGui.QAction(MainWindow)
        self.actionNew.setObjectName(_fromUtf8("actionNew"))
        self.actionNew.setToolTip("Create a blank graph")
        
        self.actionImport = QtGui.QAction(MainWindow)
        self.actionImport.setObjectName(_fromUtf8("actionImport"))
        self.actionImport.setToolTip("Import a unix specification file")
        
        self.actionExport = QtGui.QAction(MainWindow)
        self.actionExport.setObjectName(_fromUtf8("actionExport"))
        self.actionExport.setToolTip("Export as a unix specification file")

        '''MALLECIOUS'''
        self.actionExit = QtGui.QAction(MainWindow)
        self.actionExit.setObjectName(_fromUtf8("actionExit"))
        
        self.actionHelp_Contents = QtGui.QAction(MainWindow)
        self.actionHelp_Contents.setObjectName(_fromUtf8("actionHelp_Contents"))
        
        '''VIEWS and GRAPHS'''
        self.actionView_Object = QtGui.QAction(MainWindow)
        self.actionView_Object.setCheckable(True)
        self.actionView_Object.setChecked(True)
        self.actionView_Object.setObjectName(_fromUtf8("actionView_Object"))
        self.actionView_Object.setToolTip("Show permissions of a specified object")
        
        self.actionView_User = QtGui.QAction(MainWindow)
        self.actionView_User.setCheckable(True)
        self.actionView_User.setObjectName(_fromUtf8("actionView_User"))
        self.actionView_User.setToolTip("Show permissions of users")
 
        self.actionView_Group = QtGui.QAction(MainWindow)
        self.actionView_Group.setCheckable(True)
        self.actionView_Group.setObjectName(_fromUtf8("actionView_Group"))
        self.actionView_Group.setToolTip("Show permissions of groups")
        
        self.actionView_ProgramTrace = QtGui.QAction(MainWindow)
        self.actionView_ProgramTrace.setCheckable(True)
        self.actionView_ProgramTrace.setObjectName(_fromUtf8("actionView_ProgramTrace"))
        self.actionView_ProgramTrace.setToolTip("Show the program execution with permission details")
        
#         self.actionView_AccessControlList = QtGui.QAction(MainWindow)
#         self.actionView_AccessControlList.setCheckable(True)
#         self.actionView_AccessControlList.setObjectName(_fromUtf8("actionView_AccessControlList"))
#         self.actionView_AccessControlList.setToolTip("Show the access control list from Unix permission settings")

        '''animation'''
        self.actionAnimation = QtGui.QAction(MainWindow)
        self.actionAnimation.setCheckable(True)
#         self.actionAnimation.setChecked(True)
        self.actionAnimation.setObjectName(_fromUtf8("actionAnimation"))
        self.actionAnimation.setToolTip("Toggle Animation for Query")
        
        self.actionAnimation_SetInterval = QtGui.QAction(MainWindow)
        self.actionAnimation_SetInterval.setObjectName(_fromUtf8("actionAnimation_SetInterval"))
        '''SPEC'''
        self.actionSpecification = QtGui.QAction(MainWindow)
        self.actionSpecification.setObjectName(_fromUtf8("actionSpecification"))
        self.actionSpecification.setToolTip("Show the specification file")
        '''ToolBox'''
        self.actionToolBox = QtGui.QAction(MainWindow)
        self.actionToolBox.setObjectName(_fromUtf8("actionToolBox"))
        self.actionToolBox.setCheckable(True)
        '''Change Root Directory'''
        self.actionChangeRoot= QtGui.QAction(MainWindow)
        self.actionChangeRoot.setObjectName(_fromUtf8("actionChangeRoot"))
        self.actionChangeRoot.setToolTip("Change the root directory")
        '''QUERY'''
        self.actionQuery_Window = QtGui.QAction(MainWindow)
        self.actionQuery_Window.setObjectName(_fromUtf8("actionQuery_Window"))
        self.actionQuery_Window.setCheckable(True)
        '''Numeric-letter presentation of permission'''
        self.actionPermission_Calculator_Window = QtGui.QAction(MainWindow)
        self.actionPermission_Calculator_Window.setObjectName(_fromUtf8("actionPermission_Calculator_Window"))
        self.actionPermission_Calculator_Window.setCheckable(True)
        '''Process view'''
        self.actionView_Process = QtGui.QAction(MainWindow)
        self.actionView_Process.setObjectName(_fromUtf8("actionView_Process"))
        self.actionView_Process.setCheckable(True)
        '''Permission view'''
        self.actionView_Permission = QtGui.QAction(MainWindow)
        self.actionView_Permission.setObjectName(_fromUtf8("actionView_Permission"))
        self.actionView_Permission.setCheckable(True)
        '''Test'''
        self.actionTest = QtGui.QAction(MainWindow)
        self.actionTest.setObjectName(_fromUtf8("actionTest"))
        self.actionTest.setCheckable(True)
        '''Decrypt'''
        self.actionDecrypt = QtGui.QAction(MainWindow)
        self.actionDecrypt.setObjectName(_fromUtf8("actionDecrypt"))
        self.actionDecrypt.setCheckable(True)
        
        '''add actions to menubar'''
        self.menu_File.addAction(self.actionNew)
        self.menu_File.addAction(self.actionImport)
        self.menu_File.addAction(self.actionExit)
        
        self.menu_View.addAction(self.actionView_Object)
        self.menu_View.addAction(self.actionView_User)
        self.menu_View.addAction(self.actionView_Group)

        self.menu_View.addAction(self.actionView_ProgramTrace)
#         self.menu_View.addAction(self.actionView_AccessControlList)
        self.menu_View.addSeparator()
        self.menu_View.addAction(self.actionToolBox)
        self.menu_View.addAction(self.actionSpecification)
        self.menu_View.addAction(self.actionQuery_Window)
        self.menu_View.addSeparator()
        self.menu_Practice.addAction(self.actionTest)
#         self.menu_Practice.addAction(self.actionDecrypt)
        
        self.menu_Help.addAction(self.actionHelp_Contents)
        
        self.menubar.addAction(self.menu_File.menuAction())
        self.menubar.addAction(self.menu_View.menuAction())
        self.menubar.addAction(self.menu_Practice.menuAction())
        self.menubar.addAction(self.menu_Help.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QObject.connect(self.actionExit, QtCore.SIGNAL(_fromUtf8("activated()")), MainWindow.close)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "MainWindow", None, QtGui.QApplication.UnicodeUTF8))
        self.menu_File.setTitle(QtGui.QApplication.translate("MainWindow", "&File", None, QtGui.QApplication.UnicodeUTF8))
        self.menu_View.setTitle(QtGui.QApplication.translate("MainWindow", "&View", None, QtGui.QApplication.UnicodeUTF8))
        self.menu_Practice.setTitle(QtGui.QApplication.translate("MainWindow", "&Practice", None, QtGui.QApplication.UnicodeUTF8))
        self.menu_Help.setTitle(QtGui.QApplication.translate("MainWindow", "&Help", None, QtGui.QApplication.UnicodeUTF8))
        
        self.toolBar.setWindowTitle(QtGui.QApplication.translate("MainWindow", "toolBar", None, QtGui.QApplication.UnicodeUTF8))
        self.actionHelp_Contents.setText(QtGui.QApplication.translate("MainWindow", "Help Contents", None, QtGui.QApplication.UnicodeUTF8))
        self.actionHelp_Contents.setShortcut(QtGui.QApplication.translate("MainWindow", "F1", None, QtGui.QApplication.UnicodeUTF8))
        self.actionNew.setText(QtGui.QApplication.translate("MainWindow", "New", None, QtGui.QApplication.UnicodeUTF8))
        self.actionNew.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+N", None, QtGui.QApplication.UnicodeUTF8))
        
        self.actionExit.setText(QtGui.QApplication.translate("MainWindow", "Exit", None, QtGui.QApplication.UnicodeUTF8))
        self.actionExit.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+Q", None, QtGui.QApplication.UnicodeUTF8))
        
        self.actionImport.setText(QtGui.QApplication.translate("MainWindow", "Import", None, QtGui.QApplication.UnicodeUTF8))
        self.actionExport.setText(QtGui.QApplication.translate("MainWindow", "Export", None, QtGui.QApplication.UnicodeUTF8))
        
        self.actionView_Object.setText(QtGui.QApplication.translate("MainWindow", "Object View", None, QtGui.QApplication.UnicodeUTF8))
        self.actionView_User.setText(QtGui.QApplication.translate("MainWindow", "User View", None, QtGui.QApplication.UnicodeUTF8))
        self.actionView_Group.setText(QtGui.QApplication.translate("MainWindow", "Group View", None, QtGui.QApplication.UnicodeUTF8))
        self.actionView_ProgramTrace.setText(QtGui.QApplication.translate("MainWindow", "Program Trace View", None, QtGui.QApplication.UnicodeUTF8))
        self.actionView_Process.setText(QtGui.QApplication.translate("MainWindow", "Process View", None, QtGui.QApplication.UnicodeUTF8))
        self.actionView_Permission.setText(QtGui.QApplication.translate("MainWindow", "Permission View", None, QtGui.QApplication.UnicodeUTF8))
        self.actionAnimation.setText(QtGui.QApplication.translate("MainWindow", "Toggle Animation for Views", None, QtGui.QApplication.UnicodeUTF8))
        self.actionAnimation_SetInterval.setText(QtGui.QApplication.translate("MainWindow", "Set Animation Interval", None, QtGui.QApplication.UnicodeUTF8))
        self.actionToolBox.setText(QtGui.QApplication.translate("MainWindow", "Tool Box", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSpecification.setText(QtGui.QApplication.translate("MainWindow", "Specification", None, QtGui.QApplication.UnicodeUTF8))
        self.actionQuery_Window.setText(QtGui.QApplication.translate("MainWindow", "Query Window", None, QtGui.QApplication.UnicodeUTF8))
        self.actionChangeRoot.setText(QtGui.QApplication.translate("MainWindow", "Change Root Directory", None, QtGui.QApplication.UnicodeUTF8))
        self.actionTest.setText(QtGui.QApplication.translate("MainWindow", "Quiz Mode", None, QtGui.QApplication.UnicodeUTF8))
        self.actionDecrypt.setText(QtGui.QApplication.translate("MainWindow", "Decrypt Answer File", None, QtGui.QApplication.UnicodeUTF8))
        self.actionPermission_Calculator_Window.setText(QtGui.QApplication.translate("MainWindow", "Permission Calculator", None, QtGui.QApplication.UnicodeUTF8))