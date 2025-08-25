'''
Created on Apr 16, 2015

@author: manwang
Updated for PyQt6 and Python 3.12+ compatibility
'''

from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from Ui_MainWindow import Ui_MainWindow
from DiagramScene import DiagramScene
from DiagramView import DiagramView
from SystemCallViewScene import SystemCallViewScene
from QueryWindow import QueryWindow, QueryDockWidget
from ToolBox import ToolBox, ToolBoxDockWidget, RootDirEditDialog
import os, sys
from ProcessNode import ProcessNode, Process
from UserNode import *
from GroupNode import GroupNode, GroupFrameNode
from DiagramIOHelper import DiagramIOHelper
import GenerateDirectoryTree
import PermissionChecker
from FileBrowserViewDialog import FileBrowserViewDialog
from unixpolicy import unixpolicy
from SpecDialog import SpecDialog
from PermissionCalDialog import PermissionCalDialog
from AutogradingTest import AutogradingTest
# from AnswerCrypto import AnswerCrypto
from UNIXModelAnimation import UNIXModelAnimation, TutorialAnimationScene
from ObjectViewScene import ObjectViewScene
from SelfTestScene import SelfTestScene

class MainWindow(QMainWindow):
    '''
    classdocs
    '''
    NORMAL_MODE = 0
    HIGHLIGHT_MODE = 1
    QUERY_MODE = 2
    QUIZ_MODE = 3
    currentViewId = 0
    '''interface'''
    FONT_SIZE = 18
    '''floating query widget size'''
    WIDGET_WIDTH = 265
    '''colors'''
    paleGray = QColor(215, 214, 213)
    mediumBlue = QColor(100,223,255)
    yellow = QColor(224, 195, 30)
    darkGreen =  QColor(0, 99, 37)
    mediumGreen = QColor(50, 137, 48)
    lightGreen = QColor(128, 195, 66)
    violet = QColor(100, 0, 170)
    purple = QColor(174, 50, 160)
    '''animation types'''
    ANIMA_USER = 1000
    ANIMA_GROUP = 1001
    ANIMA_TRACE = 1002
    ANIMA_SYSCALL = 1003
    '''signals'''
    continuePermissionOther = pyqtSignal()
    animationStarted = pyqtSignal()
    animationStopped = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        os.chdir(os.path.dirname(os.path.abspath(sys.argv[0])))
        self.savedFileName = None
        self.currDir = os.path.abspath('./')
        self.diagramDir = self.currDir+'/policies'
        self.specDir = self.diagramDir
        self.specFileName = ""
        self.logFile = self.diagramDir+"/UNIX_log"
        self.lastOpenedDirFile = self.currDir+"/.UNIXvisual"
        self.sysFont = QFont("Courier", 19)
        import platform
        self.sys = platform.system()
        '''central widget size'''
        self.centralWX = 0
        self.centralDeductW = 0
        self.splitterRatio = 0.25
        
        if not os.path.isdir(self.diagramDir):
            from MyFunctions import make_sure_path_exists
            make_sure_path_exists(self.diagramDir)
            
        if os.path.exists(self.lastOpenedDirFile):
            with open(self.lastOpenedDirFile, 'r') as f:
                self.currentFileDir = f.readline()
            f.close()
            self.currentFileDir = self.currentFileDir.replace('\n', '')
        else:
            self.currentFileDir = str(os.path.abspath(self.diagramDir))
            from MyFunctions import writeToFile
            writeToFile(self.lastOpenedDirFile, self.currentFileDir)
        self.windowUISetup()
        self.filebrowser = FileBrowserViewDialog(self.centralWidget(), self)
        self.filebrowser.setVisible(self.ui.actionView_User.isChecked() or self.ui.actionView_Group.isChecked())
                
        self.groupFrame = None
        self.userGeneralNode = None
        self.otherGeneralNode = None
        self.userGeneralEdge = None
        self.otherGeneralEdge = None
        self.animationTimer = None
        self.oldspec = None
        self.initParam()
        
        self.objectViewScene = ObjectViewScene(self)
        self.objectViewScene.setVisibilityOfSceneItems(self.ui.actionView_Object.isChecked())
        
        self.setupConnection()
                    
        self.ui.actionView_Process.setChecked(True)
        self.viewModeChanged(self.ui.actionView_Process)
        self.regenerateSpecInfo(None)
        
    def initUNIXModelAnimation(self):
        self.modelAnimationWin = UNIXModelAnimation(self)
        
    def initParam(self):
        self.mode = self.NORMAL_MODE
        self.anchorPointDirGraph = QGraphicsRectItem()
        if not self.groupFrame:
            self.groupFrame = GroupFrameNode(self)
            self.scene.addItem(self.groupFrame)
        self.ui.introLabel.setText("")
        
        self.focusNode = None
        self.syscallitems = set()
        self.userSysList = []
        self.groupSysList = []
        self.userSpecList = []
        self.groupSpecList = []
        self.user_group_sys_mat = {}
        '''spec'''
        self.isUNIX_flag, self.root_dir, self.user_group_mat = True, "/", {}
        self.obj_cred_mat, self.obj_perm_mat = {}, {}
        self.user_obj_perm_mat, self.group_obj_perm_mat = {}, {}
        self.specFileName = ""
        self.access_root_dir = True
        '''animation'''
        self.animationStep = 0
        self.count = 0
        self.prevCursor = None
        if self.queryWindowDockWidget.isVisible():
            self.queryWindow.changeQueryInput()
                
    def setupToolbar(self):
        self.ui.toolBar.addAction(self.ui.actionNew)
        self.ui.actionNew.setIcon(QIcon(QPixmap('./icons/NewFile.png')))
        self.ui.toolBar.addAction(self.ui.actionImport)
        self.ui.actionImport.setIcon(QIcon(QPixmap('./icons/Importfile.png')))

        self.ui.toolBar.addSeparator()
        self.ui.toolBar.addAction(self.ui.actionChangeRoot)
        self.ui.actionChangeRoot.setIcon(QIcon(QPixmap('./icons/root.png')))

        self.ui.toolBar.addAction(self.ui.actionToolBox)
        self.ui.actionToolBox.setIcon(QIcon(QPixmap('./icons/toolbox.png')))
        
        self.ui.toolBar.addAction(self.ui.actionSpecification)
        self.ui.actionSpecification.setIcon(QIcon(QPixmap('./icons/spec.png')))

        self.ui.toolBar.addAction(self.ui.actionQuery_Window)
        self.ui.actionQuery_Window.setIcon(QIcon(QPixmap('./icons/query.png')))
        self.ui.toolBar.addSeparator()
        self.ui.toolBar.addAction(self.ui.actionPermission_Calculator_Window)
        self.ui.toolBar.addSeparator()
        '''ComboBox for Nodes'''
        '''object view'''
        self.ui.toolBar.addAction(self.ui.actionView_Object)
        self.ui.toolBar.addSeparator()
        '''user view'''
        self.ui.toolBar.addAction(self.ui.actionView_User)
        self.userComboBox = QComboBox()
        self.userComboBox.setEnabled(False)
        self.ui.toolBar.addWidget(self.userComboBox)
        self.ui.toolBar.addSeparator()
        '''group view'''
        self.ui.toolBar.addAction(self.ui.actionView_Group)
        self.groupComboBox = QComboBox()
        self.groupComboBox.setEnabled(False)
        self.ui.toolBar.addWidget(self.groupComboBox)
        self.ui.toolBar.addSeparator()
        self.ui.toolBar.addAction(self.ui.actionView_ProgramTrace)
        self.ui.toolBar.addSeparator()
        self.ui.toolBar.addAction(self.ui.actionView_Process)
        self.ui.toolBar.addAction(self.ui.actionView_Permission)
        self.ui.toolBar.addSeparator()
        
        self.viewActionGroup = QActionGroup(self)
        self.viewActionGroup.addAction(self.ui.actionView_Object)
        self.viewActionGroup.addAction(self.ui.actionView_User)
        self.viewActionGroup.addAction(self.ui.actionView_Group)
        self.viewActionGroup.addAction(self.ui.actionView_ProgramTrace)
        self.viewActionGroup.addAction(self.ui.actionView_Process)
        self.viewActionGroup.addAction(self.ui.actionView_Permission)
        
        self.ui.toolBar.addSeparator()
        
        self.animationControlButton = QToolButton()
        self.animationControlButton.setIcon(QIcon(QPixmap('./icons/play.png')))
        self.animationControlButton.setDisabled(True)
        self.stopAnimationButton = QToolButton()
        self.stopAnimationButton.setIcon(QIcon(QPixmap('./icons/stop.png')))
        self.stopAnimationButton.setDisabled(True)
        
    def setupUi(self):
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.syscallViewScene = SystemCallViewScene(self)
        self.modelTutorialScene = TutorialAnimationScene(self)
        
        '''VIEW SPLITTER'''
        self.ui.viewSplitter = QSplitter(Qt.Orientation.Horizontal, self.centralWidget())
        self.scene = DiagramScene(self)
        self.view = DiagramView(self.scene, self)
        self.view.setScene(self.scene)
        self.view.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.view.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        
        self.selfTestViewScene = SelfTestScene(self.view, self)
        self.explainTextEditWidget = QWidget()
        vlayout = QVBoxLayout(self.explainTextEditWidget)
        vlayout.setContentsMargins(0, 0, 0, 0)
        self.explainTextEdit = QPlainTextEdit()
        self.explainTextEdit.setReadOnly(True)
        from MyFunctions import setFontForUI
        setFontForUI(self.explainTextEdit, 14)
        vlayout.addWidget(self.explainTextEdit)
        self.ui.viewSplitter.addWidget(self.view)
        self.ui.viewSplitter.addWidget(self.explainTextEditWidget)
        self.ui.viewSplitter.splitterMoved.connect(lambda pos, index: self.viewSplitterMoved(pos, index))
        
        self.setupToolbar()
        self.iohelper = DiagramIOHelper(self)
        self.autogradingTest = AutogradingTest(self)
        self.setupQueryWidget()
        self.setupToolBox()
        self.setupRootDirDialog()
        self.specDialog = SpecDialog(self)
        self.permissionCalDialog = PermissionCalDialog(self)
        
    def closeEvent(self, evt):
        self.animationStep = 0
        QApplication.closeAllWindows()
        
    def windowUISetup(self):
        screen = QApplication.primaryScreen().availableGeometry()
        startX = 0.5*(screen.width()-self.geometry().width())
        startY = 0.5*(screen.height()-self.geometry().height())
        self.move(QPoint(int(startX), int(startY)))
        self.setupUi()
        self.setWindowTitle(str('UNIXvisual'))
    
    '''Change root directory'''
    def changeRootDir(self):
        filedialog = QFileDialog(self)
        filedialog.setFileMode(QFileDialog.FileMode.Directory)
        filename = filedialog.getExistingDirectory(self, 'Change Root Directory',
                                             self.currentFileDir,
                                             QFileDialog.Option.ShowDirsOnly|QFileDialog.Option.DontResolveSymlinks)
        if filename:
            self.initParam()
            self.root_dir = str(filename)+'/'
            self.regenerateSpecInfo(None)
    
    '''ToolBox window'''
    def setupToolBox(self):
        self.toolBoxDockWidget = ToolBoxDockWidget(self)
        self.toolBox = ToolBox(self, self.toolBoxDockWidget)
        self.toolBoxDockWidget.setWidget(self.toolBox)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.toolBoxDockWidget)
        self.toolBoxDockWidget.setVisible(False)
        
    def toggleToolBox(self):
        toolBoxWidth = self.toolBoxDockWidget.geometry().width()+5
        if self.toolBoxDockWidget.isVisible():
            self.toolBoxDockWidget.hide()
            self.centralWX = 0
            self.centralDeductW -= toolBoxWidth
        else:
            self.toolBoxDockWidget.show()
            self.centralWX = toolBoxWidth
            self.centralDeductW += toolBoxWidth
        self.centralWidget().setGeometry(int(self.centralWX), int(self.centralWidget().geometry().y()), 
                                         int(self.geometry().width()-self.centralDeductW), int(self.centralWidget().geometry().height()))
        self.resizeViews()
    
    '''Root Edit Dialog'''
    def setupRootDirDialog(self):
        self.rootDirEditDiglog = RootDirEditDialog(self)
        
    '''Test window'''
    def showAutogradingTest(self):
        self.mode = self.QUIZ_MODE
        self.autogradingTest.questionDlg.show()
        
    def decryptAutogradingAnswer(self):
        self.answerCrypto.decryptDlg.show()
        
    '''Query window'''
    def setupQueryWidget(self):
        self.queryWindowDockWidget = QueryDockWidget(self)
        self.queryWindow = QueryWindow(self.scene, self)
        self.queryWindowDockWidget.setWidget(self.queryWindow)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.queryWindowDockWidget)
        self.queryWindowDockWidget.setVisible(False)
        
    def togglePermissionCal(self):
        if self.permissionCalDialog.isVisible():
            self.permissionCalDialog.hide()
        else:
            self.permissionCalDialog.show()
    
    def toggleQueryWindow(self):
        if self.queryWindowDockWidget.isVisible():
            self.queryWindowDockWidget.hide()
            self.mode = self.NORMAL_MODE
            self.centralDeductW -= self.WIDGET_WIDTH
        else:
            self.queryWindowDockWidget.show()
            self.mode = self.QUERY_MODE
            self.queryWindow.changeQueryInput()
            self.centralDeductW += self.WIDGET_WIDTH
        self.centralWidget().setGeometry(int(self.centralWX), int(self.centralWidget().geometry().y()), int(self.geometry().width()-self.centralDeductW), int(self.centralWidget().geometry().height()))
        self.resizeViews()
        
    def showSpecDialog(self):
        self.specDialog.show()
    
    def setupConnection(self):
        self.viewActionGroup.triggered.connect(self.viewModeChanged)
        self.ui.actionNew.triggered.connect(self.newDiagram)
        self.ui.actionImport.triggered.connect(self.importUNIXSpec)
        self.ui.actionExit.triggered.connect(self.quitApp)
        self.ui.actionChangeRoot.triggered.connect(self.changeRootDir)
        self.ui.actionToolBox.triggered.connect(self.toggleToolBox)
        self.ui.actionSpecification.triggered.connect(self.showSpecDialog)
        self.ui.actionQuery_Window.toggled.connect(self.toggleQueryWindow)
        self.ui.actionTest.triggered.connect(self.showAutogradingTest)
        self.ui.actionDecrypt.triggered.connect(self.decryptAutogradingAnswer)
        self.ui.actionPermission_Calculator_Window.triggered.connect(self.togglePermissionCal)
        '''animation'''
        self.scene.animateUser.connect(self.onAnimateUser)
        self.scene.animateGroup.connect(self.onAnimateGroup)
        self.animationStarted.connect(self.onAnimationStarted)
        self.animationStopped.connect(self.onAnimationStopped)
        
        self.userComboBox.activated.connect(lambda index: self.selectUserNode(index))
        self.groupComboBox.activated.connect(lambda index: self.selectGroupNode(index))
        self.continuePermissionOther.connect(self.checkPermissionOther)
        
    def closeGreeting(self):
        self.greetWin.close()
    
    '''Toolbar response'''   
    def viewModeChanged(self, action):
        self.currentAction = action
        self.splitterRatio = 0.25
        self.scene.resetScreen()
        self.explainTextEdit.clear()
        self.objectViewScene.setVisibilityOfSceneItems(self.ui.actionView_Object.isChecked())
        self.userComboBox.setEnabled(self.ui.actionView_User.isChecked())
        self.groupComboBox.setEnabled(self.ui.actionView_Group.isChecked())
        if action == self.ui.actionView_Object:
            self.focusNode = None
            self.scene.displaySeparate = True
            self.view.setScene(self.scene)
            self.view.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
            if self.toolBoxDockWidget.isVisible():
                self.toggleToolBox()
        elif action == self.ui.actionView_User:
            self.focusNode = None
            self.scene.displaySeparate = False
            self.view.setScene(self.scene)
            self.view.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
            if self.toolBoxDockWidget.isVisible():
                self.toggleToolBox()
        elif action == self.ui.actionView_Group:
            self.focusNode = None
            self.scene.displaySeparate = False
            self.view.setScene(self.scene)
            self.view.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
            if self.toolBoxDockWidget.isVisible():
                self.toggleToolBox()
        elif action == self.ui.actionView_ProgramTrace:
            self.scene.displaySeparate = False
            self.ui.viewSplitter.setHandleWidth(0)
            self.view.setScene(self.syscallViewScene)
            self.view.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
            if not self.toolBoxDockWidget.isVisible():
                self.toggleToolBox()
        elif action == self.ui.actionView_Process:
            self.selfTestViewScene.questionType = self.selfTestViewScene.PROCESS_QUES
            self.scene.displaySeparate = True
            self.view.setScene(self.scene)
            self.view.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
            if self.toolBoxDockWidget.isVisible():
                self.toggleToolBox()
        elif action == self.ui.actionView_Permission:
            self.selfTestViewScene.questionType = self.selfTestViewScene.PERM_QUES
            self.scene.displaySeparate = True
            self.view.setScene(self.scene)
            self.view.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
            if self.toolBoxDockWidget.isVisible():
                self.toggleToolBox()
        self.selfTestViewScene.setVisibilityOfSceneItems(self.ui.actionView_Process.isChecked() or self.ui.actionView_Permission.isChecked())
        self.groupFrame.setVisible((self.focusNode!=None) and (self.ui.actionView_User.isChecked() or self.ui.actionView_Group.isChecked()))
        self.filebrowser.setVisible(self.ui.actionView_User.isChecked() or self.ui.actionView_Group.isChecked())
        self.view.viewport().update()
        self.resizeViews()
        
    def viewSplitterMoved(self, pos, index):
        self.splitterRatio = 1-float(pos)/self.ui.viewSplitter.geometry().width()
        self.resizeViews()
        
    def newDiagram(self):
        self.removeAllItems()
        self.stopAnimationTimer()
        self.scene.message = ''
        self.initParam()
        self.ui.actionView_Object.setChecked(True)
        self.viewModeChanged(self.ui.actionView_Object)
        
    def initInterface(self):
        self.userComboBox.clear()
        self.groupComboBox.clear()

    def removeAllItems(self):
        self.initInterface()
        self.objectViewScene.resetScene()
        self.scene.removeAllItemsInScene()
        self.scene.resetScreen()
        
    def hideAllNodeItemsInScene(self, scene):
        if scene == self.scene:
            scene.resetScreen()
            self.objectViewScene.resetScene()
        else:
            for i in self.scene.items():
                i.setVisible(False)
        
    def computeSpecInfo(self):
        '''get users, groups and user assignment to groups on the real system'''
        from MyFunctions import getUserAndGroupListOnSystem
        self.userSysList, self.groupSysList, self.user_group_sys_mat = \
        getUserAndGroupListOnSystem(self.root_dir, self.currDir)
        for u in self.userSysList:
            self.createUserNode(u, 0, 0)
        for g in self.groupSysList:
            self.createGroupNode(g, 0)
        for k, v in self.user_group_sys_mat.items():
            for u in self.scene.userNodeList:
                if u.name==k:
                    for vv in v:
                        u.addToGroup(vv)
        '''create nodes for users in spec'''
        self.userSpecList = list(self.user_group_mat.keys())
        for u in self.userSpecList:
            self.createUserNode(u, 0, 0)
             
        '''create nodes for groups in spec'''
        groupSpecSet = set()
        for value in self.user_group_mat.values():
            groupSpecSet = groupSpecSet.union(value)
        self.groupSpecList = list(groupSpecSet)
        for g in self.groupSpecList:
            self.createGroupNode(g, 0)
        '''assign users to groups'''
        for k, v in self.user_group_mat.items():
            for u in self.scene.userNodeList:
                if u.name==k:
                    for vv in v:
                        u.addToGroup(vv)
        
    def regenerateSpecInfo(self, specfile):
        if specfile:
            self.specDialog.readSpecToDialog(specfile)
        self.scene.resetScreen()
        from MyFunctions import getAbsolutePath, checkDirectoryExistence
        self.root_dir = getAbsolutePath(self.root_dir)
        import re
        self.root_dir = re.sub('/+', '/', self.root_dir)
        if not checkDirectoryExistence(self.root_dir):
            self.access_root_dir = False
            QMessageBox.critical(self, 'Error', 'Specified root directory does not exist on the system!', QMessageBox.StandardButton.Ok)
            return -1
        self.access_root_dir = True
        self.removeAllItems()
        if not self.userGeneralNode:
            self.createGeneralNodes()
        self.computeSpecInfo()
        GenerateDirectoryTree.getDirHierarchy(self.root_dir, self)
        if self.access_root_dir:
            self.filebrowser.fillinFileInfo(self.scene.dirNodeList[0].getFullPath())
        if self.queryWindowDockWidget.isVisible():
            self.queryWindow.changeQueryInput()
        self.objectViewScene.addUser2ComboBox()
        self.objectViewScene.resetUserAndGroupInComboBox()
        self.objectViewScene.setVisibilityOfSceneItems(self.ui.actionView_Object.isChecked())
        self.objectViewScene.lineEditRoot.setText(self.root_dir)
        
        self.selfTestViewScene.updateUIContents()
        self.selfTestViewScene.setVisibilityOfSceneItems(self.ui.actionView_Process.isChecked() or self.ui.actionView_Permission.isChecked())
        self.selfTestViewScene.updateLayout()
        
    def showModelTutorial(self, tutorialOn, detailMode):
        print('showModelTutorial: '+str(detailMode))
        if tutorialOn:
            self.view.setScene(self.modelTutorialScene)
            self.modelTutorialScene.startAnimation(detailMode)
         
    def importUNIXSpec(self):
        filename, _ = QFileDialog.getOpenFileName(self, 'Import from UNIX Spec', directory=self.currentFileDir, filter='Specification File (*.unix)')
        if filename:
            from PyQt6.QtCore import QFileInfo
            self.specDir = QFileInfo(filename).absolutePath()
            self.initParam()
            try:
                self.isUNIX_flag, self.root_dir, self.user_group_mat, mat1, mat2 = unixpolicy(str(filename))
                if self.isUNIX_flag:
                    self.obj_cred_mat, self.obj_perm_mat = mat1, mat2
                else:
                    self.user_obj_perm_mat, self.group_obj_perm_mat = mat1, mat2
            except Exception as e:
                QMessageBox.critical(self, 'Error', str(e))
                return -1
            path = os.path.normpath(str(filename))
            self.oldspec = path
            index = path.rfind('/')
            self.specFileName = path[index+1:]
            self.specDir = path[:index]
            self.setWindowTitle(self.specFileName)
            self.regenerateSpecInfo(path)
            return 0
    
    def quitApp(self):
        QCoreApplication.quit()
        
    def setMainWindowAllGuiState(self, state):
        self.queryWindowDockWidget.setEnabled(state)
        self.toolBoxDockWidget.setEnabled(state)
        self.ui.menubar.setEnabled(state)
        self.autogradingTest.toolbarAllItems(state)
        if state and self.oldspec:
            self.iohelper.importSpec(self.oldspec)
        
    '''view update'''
    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.resizeViews()
    
    def changeViewSizeForSeparateView(self):
        ratio = self.splitterRatio
        self.view.setGeometry(0,0,int((1-ratio)*self.ui.viewSplitter.geometry().width()), self.ui.viewSplitter.geometry().height())
        self.scene.setSceneRect(QRectF(self.view.geometry()))
        currentSizes = self.ui.viewSplitter.sizes()
        currentSizes[0] = int((1-ratio)*self.ui.viewSplitter.geometry().width())
        currentSizes[1] = int(ratio*self.ui.viewSplitter.geometry().width())
        self.ui.viewSplitter.setSizes(currentSizes)

    def changeViewSizeForMainView(self):
        ratio = 0
        self.view.setGeometry(0,0,int((1-ratio)*self.ui.viewSplitter.geometry().width()), self.ui.viewSplitter.geometry().height())
        self.scene.setSceneRect(QRectF(self.view.geometry()))
        currentSizes = self.ui.viewSplitter.sizes()
        currentSizes[0] = int((1-ratio)*self.ui.viewSplitter.geometry().width())
        currentSizes[1] = int(ratio*self.ui.viewSplitter.geometry().width())
        self.ui.viewSplitter.setSizes(currentSizes)
        
    def resizeViews(self):
        self.ui.viewSplitter.setGeometry(0, 0, int(self.centralWidget().geometry().width()), int(self.centralWidget().geometry().height()))
        if self.scene.displaySeparate:
            self.changeViewSizeForSeparateView()
        else:
            self.changeViewSizeForMainView()
        self.view.centerOn(0.5*self.view.viewport().width(), 0.5*self.view.viewport().height())
        self.syscallViewScene.setSceneRect(0, 0, self.view.geometry().width(), 5000)
        self.filebrowser.setGeometry(int(0.46*self.view.geometry().width()), 0, int(0.54*self.view.geometry().width()), int(self.view.geometry().height()))
        self.updateAllItemPos()
        
    def explainTexteditHighlightLastLines(self):
        self.prevText = self.explainTextEdit.toPlainText()
        self.prevCursor = self.prevText.count('\n')
        self.resetOutputText()
        self.setOutputHighlight()
        
    def setOutputHighlight(self):
        cursor = QTextCursor(self.explainTextEdit.textCursor())
        blockFormat = QTextBlockFormat(cursor.blockFormat())
        blockFormat.setBackground(QColor(187,255,255, 10))
        blockFormat.setNonBreakableLines(True)
        blockFormat.setPageBreakPolicy(QTextFormat.PageBreakPolicy.PageBreak_AlwaysBefore)
        cursor.setBlockFormat(blockFormat)
        it = cursor.block().begin()
        while not it.atEnd():
            charFormat = QTextCharFormat(it.fragment().charFormat())
            tempCursor = QTextCursor(cursor)
            tempCursor.setPosition(it.fragment().position())
            tempCursor.setPosition(it.fragment().position() + it.fragment().length(), QTextCursor.MoveMode.KeepAnchor)
            tempCursor.setCharFormat(charFormat)
            it += 1
            
    def resetOutputText(self):
        self.explainTextEdit.clear()
        cursor = QTextCursor(self.explainTextEdit.textCursor())
        blockFormat = QTextBlockFormat(cursor.blockFormat())
        blockFormat.setBackground(QColor("white"))
        blockFormat.setNonBreakableLines(True)
        blockFormat.setPageBreakPolicy(QTextFormat.PageBreakPolicy.PageBreak_AlwaysBefore)
        cursor.setBlockFormat(blockFormat)
        it = cursor.block().begin()
        while it < self.prevCursor+1:
            charFormat = QTextCharFormat(it.fragment().charFormat())
            tempCursor = QTextCursor(cursor)
            tempCursor.setPosition(it.fragment().position())
            tempCursor.setPosition(it.fragment().position() + it.fragment().length(), QTextCursor.MoveMode.KeepAnchor)
            tempCursor.setCharFormat(charFormat)
            it += 1
        self.explainTextEdit.appendPlainText(self.prevText)
        self.cursor = cursor
        
    def updateAllItemPos(self):
        if self.ui.actionView_Object.isChecked():
            self.objectViewScene.updateLayout()
        elif self.ui.actionView_Process.isChecked():
            self.selfTestViewScene.updateLayout()
        elif self.ui.actionView_Permission.isChecked():
            self.selfTestViewScene.updateLayout()
        elif self.ui.actionView_User.isChecked() or self.ui.actionView_Group.isChecked():
            self.anchorPointDirGraph.setPos(0.5*self.scene.sceneRect().width(), 0.5*self.scene.sceneRect().height())
            for i in self.scene.items():
                if isinstance(i, UserNode) or isinstance(i, GroupNode) or isinstance(i, GeneralNode):
                    i.setPos(QPointF(i.relativeX*self.scene.sceneRect().width(), i.relativeY*self.scene.sceneRect().height()))
                elif isinstance(i, GroupFrameNode):
                    i.setPos(QPointF(i.relativeX*self.scene.sceneRect().width(), i.relativeY*self.scene.sceneRect().height()))
                    if self.focusNode:
                        if isinstance(self.focusNode, UserNode):
                            glist = list(self.focusNode.groupNodes)
                        elif isinstance(self.focusNode, GroupNode):
                            glist = [self.focusNode]
                        if glist:
                            width = glist[0].rect().width()+20
                            height = glist[-1].pos().y()+glist[-1].rect().height()-glist[0].pos().y()+20
                            self.groupFrame.setRect(0, 0, width, height)
                            self.groupFrame.setPos(glist[0].pos().x()-0.5*glist[0].rect().width()-10, glist[0].pos().y()-0.5*glist[0].rect().height()-10)
                            self.groupFrame.relativeX = self.groupFrame.pos().x()/self.scene.sceneRect().width()
                            self.groupFrame.relativeY = self.groupFrame.pos().y()/self.scene.sceneRect().height()
                        self.groupFrame.setVisible(len(glist)!=0)
                elif hasattr(i, 'setLine'):  # EdgeItem check
                    i.setLine(QLineF(i.startItem.pos(), i.endItem.pos()))
        elif self.ui.actionView_ProgramTrace.isChecked():
            for i in self.syscallViewScene.items():
                i.setVisible(True)
                if isinstance(i, ProcessNode):
                    i.setPos(QPointF(i.relativeX*self.syscallViewScene.sceneRect().width(), i.relativeY))
                elif hasattr(i, 'setLine'):  # EdgeItem check
                    i.setLine(QLineF(i.startItem.pos(), i.endItem.pos()))
                    
    '''animation'''
    def setAnimationInterval(self):
        interval, accept = QInputDialog.getInt(self, 'Set Interval(second)', '', value=self.timerInterval//1000, min=1, max=10, step=1)
        if accept:
            self.timerInterval = interval * 1000
            
    def startAnimationTimer(self):
        if self.animationTimer:
            self.animationTimer.start()
            self.animationStarted.emit() 
  
    def stopAnimationTimer(self):
        if self.animationTimer:
            self.animationTimer.stop()
            self.animationStopped.emit()

    def onAnimationStarted(self):
        self.animationControlButton.setEnabled(True)
        self.stopAnimationButton.setEnabled(True)
        self.animationControlButton.setIcon(QIcon(QPixmap('./icons/pause.png')))
    
    def onAnimationStopped(self):
        self.animationControlButton.setDisabled(True)
        self.stopAnimationButton.setDisabled(True)
        self.animationControlButton.setIcon(QIcon(QPixmap('./icons/play.png')))
        if self.animationTimer.isActive():
            self.animationStep = 0
            self.animationType = None
            self.animationTimer.setInterval(5000)
            self.scene.hint = ''
            self.animationTimer.stop()
            self.scene.update()
            
    def onAnimationButtonClicked(self):
        if self.animationTimer.interval() == 9000000:
            self.animationControlButton.setIcon(QIcon(QPixmap('./icons/pause.png')))
            self.animationTimer.setInterval(self.timerInterval)
        else:
            self.animationControlButton.setIcon(QIcon(QPixmap('./icons/play.png')))
            self.animationTimer.setInterval(9000000)
             
    '''node operation'''
    def setNodePos(self, i):
        if self.ui.actionView_ProgramTrace.isChecked():
            if isinstance(i, ProcessNode):
                i.setPos(QPointF(i.relativeX*self.view.viewport().width(),
                                  i.relativeY))
        elif self.ui.actionView_User.isChecked() or self.ui.actionView_Group.isChecked():
            if isinstance(i, UserNode) or isinstance(i, GroupNode) or isinstance(i, GeneralNode):
                i.setPos(QPointF(i.relativeX*self.scene.sceneRect().width(), i.relativeY*self.scene.sceneRect().height()))
            
    def createGeneralProcessNode(self):
        pInit = Process('init')
        self.initProcessNode = ProcessNode(self, pInit)
        self.syscallitems.add(self.initProcessNode)
        self.syscallViewScene.addItem(self.initProcessNode)
        self.initProcessNode.relativeX, self.initProcessNode.relativeY = 0.5, 100
        self.setNodePos(self.initProcessNode)
        pLogin = Process('login', 'user', 'group')
        self.loginProcessNode = ProcessNode(self, pLogin)
        self.syscallitems.add(self.loginProcessNode)
        self.syscallViewScene.addItem(self.loginProcessNode)
        self.loginProcessNode.relativeX, self.loginProcessNode.relativeY = 0.5, 100+100
        self.setNodePos(self.loginProcessNode)
        from EdgeItem import EdgeItem
        edge = EdgeItem(EdgeItem.PROCESS_CONN, self.initProcessNode, self.loginProcessNode, self)
        edge.setVisible(True)
        self.initProcessNode.edgeList.append(edge)
        self.loginProcessNode.edgeList.append(edge)
        self.syscallitems.add(edge)
        self.syscallViewScene.addItem(edge)
        
    def createGeneralNodes(self):
        self.userGeneralNode = GeneralNode(self, True, "User")
        self.otherGeneralNode = GeneralNode(self, False, "Other")
        self.scene.addItem(self.userGeneralNode)
        self.scene.addItem(self.otherGeneralNode)
    
    def createGeneralEdge(self, usernode):
        from EdgeItem import EdgeItem
        self.userGeneralEdge = EdgeItem(EdgeItem.GENERAL_CONN, usernode, self.userGeneralNode, self)
        self.otherGeneralEdge = EdgeItem(EdgeItem.GENERAL_CONN, usernode, self.otherGeneralNode, self)
        self.scene.addItem(self.userGeneralEdge)
        self.scene.addItem(self.otherGeneralEdge)
            
    def setGeneralNodeEdgeVisibility(self, isSeen):
        if self.userGeneralNode:
            self.userGeneralNode.setVisible(isSeen)
        if self.otherGeneralNode:
            self.otherGeneralNode.setVisible(isSeen)
        if self.userGeneralEdge:
            self.userGeneralEdge.setVisible(isSeen)
        if self.otherGeneralEdge:
            self.otherGeneralEdge.setVisible(isSeen)
        
    def createUserNode(self, uname, uid, gid):
        unode = UserNode(uname, uid, gid, self)
        self.scene.addItem(unode)
        self.scene.userNodeList.append(unode)
        self.userComboBox.addItem(unode.name)
    
    def removeUserNode(self, unode):
        from MyFunctions import removeItemFromCombobox
        removeItemFromCombobox(self.userComboBox, unode.name)
        self.scene.removeItem(unode)
        self.scene.userNodeList.remove(unode)
        del unode
        
    def createGroupNode(self, gname, gid):
        gnode = GroupNode(gname, gid, self)
        self.scene.addItem(gnode)
        self.scene.groupNodeList.append(gnode)
        self.groupComboBox.addItem(gnode.name)
        
    def removeGroupNode(self, gnode):
        from MyFunctions import removeItemFromCombobox
        removeItemFromCombobox(self.groupComboBox, gnode.name)
        self.scene.removeItem(gnode)
        self.scene.groupNodeList.remove(gnode)
        del gnode
    
    def setToShow(self, node):
        if isinstance(node, UserNode):
            node.relativeX, node.relativeY = 0.1, 0.5
            node.setPos(QPointF(0.1*self.scene.sceneRect().width(), 0.5*self.scene.sceneRect().height()))
        elif isinstance(node, GroupNode):
            node.relativeX, node.relativeY = 0.3, 0.5
            node.setPos(QPointF(0.3*self.scene.sceneRect().width(), 0.5*self.scene.sceneRect().height()))
        
    def arrangeGroupNodeForDisplay(self, grouplist):
        self.groupFrame.setVisible(False)
        if grouplist:
            temp = list(grouplist)
            if len(grouplist)==1:
                relativeY = 0.5
                d = 0.3
            else:
                d = 0.6/(len(grouplist)+1)
                relativeY = 0.22+d
            index = 0
            for g in grouplist:
                g.relativeY = relativeY+d*index
                g.setPos(QPointF(0.3*self.scene.sceneRect().width(), (g.relativeY)*self.scene.sceneRect().height()))
                index+=1
            g = temp[0]
            self.groupFrame.setVisible(True)
            width = g.rect().width()+20
            height = temp[-1].pos().y()+temp[-1].rect().height()-g.pos().y()+20
            self.groupFrame.setRect(0, 0, width, height)
            self.groupFrame.setPos(g.pos().x()-0.5*g.rect().width()-10, g.pos().y()-0.5*g.rect().height()-10)
            self.groupFrame.relativeX = self.groupFrame.pos().x()/self.scene.sceneRect().width()
            self.groupFrame.relativeY = self.groupFrame.pos().y()/self.scene.sceneRect().height()
            return d
        return -1
        
    def selectUserNode(self, index):
        self.animationStep = 0
        self.scene.resetScreen()
        self.groupFrame.setVisible(True)
        userNodeList = self.scene.userNodeList
        usernode = userNodeList[index]
        self.focusNode = usernode
        usernode.setVisible(True)
        usernode.highlight = True
        self.setToShow(usernode)
        for i in range(len(userNodeList)):
            if i != index:
                userNodeList[i].setVisible(False)
                for e in userNodeList[i].edgeList:
                    e.setVisible(False)
        self.scene.animateUser.emit(usernode)
        
    def checkPermissionOther(self):
        self.scene.hint = 'Other'
        PermissionChecker.checkUserPermForFileViaOther(self.scene)
        self.scene.update()
    
    def arrangeUserNodeForDisplay(self, userlist):
        if userlist:
            relativeY = 0.33
            if len(userlist)==1:
                relativeY = 0.5
            else:
                relativeY = 0.33
            d = 0.5/len(userlist)
            index = 0
            for u in userlist:
                u.setVisible(True)
                u.relativeY = relativeY+d*index
                u.setPos(QPointF(0.1*self.scene.sceneRect().width(), (relativeY+d*index)*self.scene.sceneRect().height()))
                index+=1

    def createProcessNode(self, procname):
        proc = Process(procname)
        procnode = ProcessNode(self, proc)
        procnode.procId = len(self.syscallViewScene.processNodeList)
        procnode.relativeX, procnode.relativeY = 0.5, 300
        procnode.setPos(QPointF(procnode.relativeX*self.view.viewport().width(), procnode.relativeY))
        self.syscallViewScene.addItem(procnode)
        if len(self.syscallViewScene.processNodeList) == 0:
            procnode.firstNode = True
        self.syscallViewScene.processNodeList.append(procnode)
        return proc, procnode
                    
    def selectGroupNode(self, index):
        self.animationStep = 0
        self.scene.resetScreen()
        groupNodeList = self.scene.groupNodeList
        groupnode = groupNodeList[index]
        groupnode.setVisible(True)
        self.focusNode = groupnode
        self.setToShow(groupnode)
        self.groupFrame.setVisible(True)
        width = groupnode.rect().width()+20
        height = groupnode.rect().height()+20
        self.groupFrame.setRect(0, 0, width, height)
        self.groupFrame.setPos(groupnode.pos().x()-0.5*groupnode.rect().width()-10, groupnode.pos().y()-0.5*groupnode.rect().height()-10)
        self.groupFrame.relativeX = self.groupFrame.pos().x()/self.scene.sceneRect().width()
        self.groupFrame.relativeY = self.groupFrame.pos().y()/self.scene.sceneRect().height()
        self.scene.hint = 'Group'
        self.arrangeUserNodeForDisplay(groupnode.userNodes)
        for i in range(len(groupNodeList)):
            if i != index:
                groupNodeList[i].setVisible(False)
                for e in groupNodeList[i].edgeList:
                    e.setVisible(False)
        for e in groupnode.edgeList:
            e.setVisible(True)
            e.updatePosition()
        self.scene.animateGroup.emit(groupnode)
        
    def onAnimateUser(self, usernode):
        self.arrangeGroupNodeForDisplay(usernode.groupNodes)
        self.otherGeneralNode.relativeY = 0.85
        self.setNodePos(self.otherGeneralNode)
        if not self.userGeneralEdge:
            self.createGeneralEdge(usernode)
        else:
            self.userGeneralEdge.startItem = usernode
            self.otherGeneralEdge.startItem = usernode
        for g in usernode.groupNodes:
            g.setVisible(True)
        for e in usernode.edgeList:
            e.setVisible(True)
        self.setGeneralNodeEdgeVisibility(True)
        self.scene.update()
        if self.filebrowser.isVisible():
            self.filebrowser.mode = self.filebrowser.USER_MD
            self.filebrowser.filterActionChanged(usernode.name, None)
        
    def onAnimateGroup(self, groupnode):
        if self.filebrowser.isVisible():
            self.filebrowser.mode = self.filebrowser.GROUP_MD
            self.filebrowser.filterActionChanged(None, groupnode.name)
        else:
            self.animationType = self.ANIMA_GROUP
            self.animationParameters = [groupnode]
