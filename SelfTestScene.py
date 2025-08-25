'''
Created on May 10, 2016

@author: manwang
'''
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from stat import *
from Ui_AutogradingTestDlg import Ui_Dialog
import MyFunctions
import PermissionChecker
import random

class FileDialog(QFileDialog):
    def __init__(self, *args):
        QFileDialog.__init__(self, *args)
        self.setOption(self.DontUseNativeDialog, True)
        self.setFileMode(self.ExistingFiles)
        btns = self.findChildren(QPushButton)
        self.openBtn = [x for x in btns if 'open' in str(x.text()).lower()][0]
        self.openBtn.clicked.disconnect()
        self.openBtn.clicked.connect(self.openClicked)
        self.tree = self.findChild(QTreeView)
        self.main = args[0]
        self.selectedFiles = []
        
    def openClicked(self):
        import os
        inds = self.tree.selectionModel().selectedIndexes()
        files = []
        for i in inds:
            if i.column() == 0:
                files.append(os.path.join(str(self.directory().absolutePath()), str(i.data().toString())))
        self.selectedFiles = files
        if self.selectedFiles:
            self.main.selfTestViewScene.setObjUI(self.selectedFiles[0])
        self.hide()
        self.main.selfTestViewScene.settingChanged()
        
    def filesSelected(self):
        return self.selectedFiles
    
class SelfTestScene(QWidget):
    PROCESS_QUES = 0
    PERM_QUES = 1
    QUES_INFO = [['Can the process access the object with the specified permission?', 'Yes', 'No'], \
                 ['What is the letter notation of the above permission?']
                ]
    FOOTNOTE = ['Assume the process has access to all directories above the object.', '']
    ANIMTESTEPS = [5, 6]
    
    def __init__(self, parent, main):
        QWidget.__init__(self, parent)
        self.main = main
        self.scene = main.scene
        self.initParam()
        self.setupWidget(parent)
        self.initQuestion()
        
    def initParam(self):
        self.spec = None
        self.interfaceQuesItems = set()
        self.interfaceTableItems = set()
        self.objDir = None
        self.info = None
        self.settingPermInfo = None
        self.settingIsChanged = False
        self.chosenAnswer = None
        self.questionType = self.PROCESS_QUES
        
    def createGraphicsTextItem(self, scene, text, fontsize=20, isQuesItem = True):
        item = QGraphicsTextItem(text)
        MyFunctions.setFontForUI(item, fontsize)
        scene.addItem(item)
        if isQuesItem:
            self.interfaceQuesItems.add(item)
        else:
            self.interfaceTableItems.add(item)
        return item
            
    def setupWidget(self, parent):
        self.setupPermissionTableView()
        self.setupProcessTableView()
        self.tableViewQuestionConf.setGeometry(0, 0, self.scene.sceneRect().width(), 0.5*self.scene.sceneRect().height())
        self.interfaceTableItems.add(self.tableViewQuestionConf)
        
#         self.questionType = QComboBox()
#         self.questionType.addItem('Process')
#         self.questionType.addItem('Permission')
#         MyFunctions.setFontForUI(self.questionType, 20)
#         self.createUIInScene(self.questionType)
#         self.questionType.activated.connect(self.questionTypeChanged)

    def setCellText(self, table, r, c, text, font = QFont('Courier', 18), isBold = False):
        item = QTableWidgetItem(QString(text))
        font.setBold(isBold)
        item.setFont(font)
        item.setTextAlignment(Qt.AlignCenter)
        table.setItem(r, c, item)
        return item
        
    def createLineEditAndButtonCombo(self, r, c, btnText='Random', isLineEdit = False):
        widget = QWidget()
        hlayout = QHBoxLayout(widget)
        if isLineEdit:
            lineEdit = QLineEdit()
        else:
            lineEdit = QComboBox()
            lineEdit.setSizeAdjustPolicy(QComboBox.AdjustToContents)
            lineEdit.setEditable(True)
            lineEdit.completer().setCompletionMode(QCompleter.PopupCompletion)

        button = QPushButton(btnText)
        hlayout.addWidget(lineEdit)
        hlayout.addWidget(button)
        hlayout.setContentsMargins(0, 0, 0, 0)
        widget.setLayout(hlayout)
        self.tableViewQuestionConf.setCellWidget(r,c,widget)
        return lineEdit, button
    
    def setupPermissionTableView(self):
        self.tablePermissionViewQuestionConf = QTableWidget(self.main.view)
        self.tablePermissionViewQuestionConf.setRowCount(3)
        self.tablePermissionViewQuestionConf.setColumnCount(3)
        self.tablePermissionViewQuestionConf.verticalHeader().setVisible(False)
        self.tablePermissionViewQuestionConf.horizontalHeader().setVisible(False)

        item = self.setCellText(self.tablePermissionViewQuestionConf, 0, 1, 'Permission', QFont('Courier', 20))
        item.setFlags(item.flags() &~Qt.ItemIsEditable)
        item = self.setCellText(self.tablePermissionViewQuestionConf, 0, 0, '', QFont('Courier', 20))
        item.setFlags(item.flags() &~Qt.ItemIsEditable)
        item = self.setCellText(self.tablePermissionViewQuestionConf, 0, 2, '', QFont('Courier', 20))
        item.setFlags(item.flags() &~Qt.ItemIsEditable)
        item = self.setCellText(self.tablePermissionViewQuestionConf, 1, 0, 'Octal Notation', QFont('Courier', 20))
        item.setFlags(item.flags() &~Qt.ItemIsEditable)
        
        chosenPerm = self.generateRandomPermissionInOctal()
        item = self.setCellText(self.tablePermissionViewQuestionConf, 1, 1, chosenPerm, QFont('Courier', 20))
        
        item.setFlags(item.flags() &~Qt.ItemIsEditable)
        item = self.setCellText(self.tablePermissionViewQuestionConf, 1, 2, '', QFont('Courier', 20))
        item.setFlags(item.flags() &~Qt.ItemIsEditable)
        item = self.setCellText(self.tablePermissionViewQuestionConf, 2, 0, '', QFont('Courier', 20))
        item.setFlags(item.flags() &~Qt.ItemIsEditable)
        
        widget = QWidget()
        layout = QHBoxLayout(widget)
        self.updatePermBtn = QPushButton('Obtain a New Permission')
        layout.addWidget(self.updatePermBtn)
        layout.setContentsMargins(0, 0, 0, 0)
        widget.setLayout(layout)
        self.tablePermissionViewQuestionConf.setCellWidget(2,1,widget)
        self.updatePermBtn.clicked.connect(self.generateChoicesForPermQues)
        item = self.setCellText(self.tablePermissionViewQuestionConf, 2, 1, '', QFont('Courier', 20))
        item.setFlags(item.flags() &~Qt.ItemIsEditable)
        item = self.setCellText(self.tablePermissionViewQuestionConf, 2, 2, '', QFont('Courier', 20))
        item.setFlags(item.flags() &~Qt.ItemIsEditable)
        self.setPermTableBackgroundColor()
        self.tablePermissionViewQuestionConf.verticalHeader().setResizeMode(QHeaderView.Stretch)
        self.tablePermissionViewQuestionConf.horizontalHeader().setResizeMode(QHeaderView.Stretch)
        
    def setupProcessTableView(self):
        self.tableViewQuestionConf = QTableWidget(self.main.view)
        self.tableViewQuestionConf.setRowCount(5)
        self.tableViewQuestionConf.setColumnCount(5)
        self.tableViewQuestionConf.verticalHeader().setVisible(False)
        self.tableViewQuestionConf.horizontalHeader().setVisible(False)
 
        item = self.setCellText(self.tableViewQuestionConf, 1, 0, 'Real UID', QFont('Courier', 20))
        item.setFlags(item.flags() &~Qt.ItemIsEditable)
        item = self.setCellText(self.tableViewQuestionConf, 2, 0, 'Real GID', QFont('Courier', 20))
        item.setFlags(item.flags() &~Qt.ItemIsEditable)
        item = self.setCellText(self.tableViewQuestionConf, 3, 0, 'Effective UID', QFont('Courier', 20))
        item.setFlags(item.flags() &~Qt.ItemIsEditable)
        item = self.setCellText(self.tableViewQuestionConf, 4, 0, 'Effective GID', QFont('Courier', 20))
        item.setFlags(item.flags() &~Qt.ItemIsEditable)
        
        widget = QWidget()
        procLabel = QLabel('Process')
        procLabel.setFont(QFont('Courier', 20))
        procLabel.setAlignment(Qt.AlignCenter)
        self.procAllRandomPBtn = QPushButton('Random All')
        hlayout = QHBoxLayout(widget)
        hlayout.addWidget(procLabel)
        hlayout.addWidget(self.procAllRandomPBtn)
        hlayout.setContentsMargins(0, 0, 0, 0)
        widget.setLayout(hlayout)
        self.tableViewQuestionConf.setCellWidget(0,1,widget)
        
        self.procRUIDLineEdit, self.procRUIDRandomPBtn = self.createLineEditAndButtonCombo(1,1)
        self.procRGIDLineEdit, self.procRGIDRandomPBtn = self.createLineEditAndButtonCombo(2,1)
        self.procEUIDLineEdit, self.procEUIDRandomPBtn = self.createLineEditAndButtonCombo(3,1)
        self.procEGIDLineEdit, self.procEGIDRandomPBtn = self.createLineEditAndButtonCombo(4,1)
        '''cell 1,3'''
        widget = QWidget()
        glayout = QGridLayout(widget)
        self.objDirLineEdit = QComboBox()
        self.objDirLineEdit.setSizeAdjustPolicy(QComboBox.AdjustToContents)
        self.objDirLineEdit.setEditable(True)
        self.objDirLineEdit.completer().setCompletionMode(QCompleter.PopupCompletion)
        self.objDirLoadPBtn = QPushButton('...')
        self.objPermRefresh = QPushButton('Refresh')
        glayout.addWidget(self.objDirLineEdit,0,0)
        glayout.addWidget(self.objDirLoadPBtn,0,1)
        glayout.addWidget(self.objPermRefresh,1,0,1,2)
        glayout.setContentsMargins(0, 0, 0, 0)
        widget.setLayout(glayout)
        self.tableViewQuestionConf.setCellWidget(1,3,widget)
        '''cell 1,3'''
        
        self.permLineEdit, self.permRandomPBtn = self.createLineEditAndButtonCombo(1,4)
        for i in xrange(1, 8):
            self.permLineEdit.addItem(PermissionChecker.convertOctToRWXString(i))
        
        self.settingPermLabel = QLabel('')
        self.settingPermLabel.setMargin(0)
        self.settingPermLabel.setTextFormat(Qt.RichText)
        self.settingPermLabel.setWordWrap(True)
        self.settingPermLabel.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.settingPermLabel.setFont(QFont('Courier', 19))
        self.tableViewQuestionConf.setCellWidget(4,3,self.settingPermLabel)
        
        item = self.setCellText(self.tableViewQuestionConf, 0, 3, 'Object', QFont('Courier', 20))
        item.setFlags(item.flags() &~Qt.ItemIsEditable)
        item = self.setCellText(self.tableViewQuestionConf, 0, 4, 'Permission(Letter)', QFont('Courier', 20))
        item.setFlags(item.flags() &~Qt.ItemIsEditable)
         
        item = self.setCellText(self.tableViewQuestionConf, 1, 2, 'Directory', QFont('Courier', 20))
        item.setFlags(item.flags() &~Qt.ItemIsEditable)
        item = self.setCellText(self.tableViewQuestionConf, 2, 2, 'User Owner', QFont('Courier', 20))
        item.setFlags(item.flags() &~Qt.ItemIsEditable)
        item = self.setCellText(self.tableViewQuestionConf, 3, 2, 'Group Owner', QFont('Courier', 20))
        item.setFlags(item.flags() &~Qt.ItemIsEditable)
        item = self.setCellText(self.tableViewQuestionConf, 4, 2, 'Permissions', QFont('Courier', 20))
        item.setFlags(item.flags() &~Qt.ItemIsEditable)
        
        for c in xrange(self.tableViewQuestionConf.columnCount()):
            for r in xrange(self.tableViewQuestionConf.rowCount()): 
                if self.tableViewQuestionConf.item(r, c) == None:
                    self.setCellText(self.tableViewQuestionConf, r, c, '')
                if c < 2:
                    color = QColor(234, 250, 241)
                elif c < 4:
                    color = QColor(252, 243, 207)
                else:
                    color = QColor(250, 219, 216)
                self.tableViewQuestionConf.item(r, c).setData(Qt.BackgroundRole, QVariant(QBrush(color)))
        self.tableViewQuestionConf.verticalHeader().setResizeMode(QHeaderView.Stretch)
        self.tableViewQuestionConf.horizontalHeader().setResizeMode(QHeaderView.Stretch)
        
        self.objDirLoadPBtn.clicked.connect(self.setObjPath)
        self.objDirLineEdit.highlighted.connect(lambda dirIndex: self.showWholePathAsHint(dirIndex))
        self.objPermRefresh.clicked.connect(self.updateFileInfo)
        self.procAllRandomPBtn.clicked.connect(self.randomProc)
        self.procRUIDRandomPBtn.clicked.connect(self.randomGetRUID)
        self.procRGIDRandomPBtn.clicked.connect(self.randomGetRGID)
        self.procEUIDRandomPBtn.clicked.connect(self.randomGetEUID)
        self.procEGIDRandomPBtn.clicked.connect(self.randomGetEGID)
        self.permRandomPBtn.clicked.connect(self.randomGetPerm)
        
        self.procRUIDLineEdit.currentIndexChanged.connect(self.settingChanged)
        self.procEUIDLineEdit.currentIndexChanged.connect(self.settingChanged)
        self.procRGIDLineEdit.currentIndexChanged.connect(self.settingChanged)
        self.procEGIDLineEdit.currentIndexChanged.connect(self.settingChanged)
        self.permLineEdit.currentIndexChanged.connect(self.settingChanged)
        self.objDirLineEdit.editTextChanged.connect(self.updateFileInfo)
        
        
    def createUIInScene(self, widget, isQuesItem = True):
        proxyWidget = QGraphicsProxyWidget()
        proxyWidget.setWidget(widget)
        proxyWidget.setZValue(1)
        self.scene.addItem(proxyWidget)
        if isQuesItem:
            self.interfaceQuesItems.add(proxyWidget)
            self.interfaceQuesItems.add(widget)
        else:
            self.interfaceTableItems.add(proxyWidget)
            self.interfaceTableItems.add(widget)
        return proxyWidget
    
    def initQuestion(self):        
        self.labelQuestionText = QGraphicsTextItem(self.QUES_INFO[self.PROCESS_QUES][0])
        MyFunctions.setFontForUI(self.labelQuestionText, 25)
#         self.labelQuestion = QGraphicsTextItem('Question Type: ')
#         MyFunctions.setFontForUI(self.labelQuestion, 25)
        if self.labelQuestionText not in self.scene.items():
#             self.scene.addItem(self.labelQuestion)
#             self.interfaceQuesItems.add(self.labelQuestion)
#             self.labelQuestionText = self.createGraphicsTextItem(self.scene, self.QUES_INFO[self.PROCESS_QUES][0], 25)
            self.scene.addItem(self.labelQuestionText)
            self.interfaceQuesItems.add(self.labelQuestionText)
            self.quesTextWidth = self.labelQuestionText.boundingRect().width()
            
            self.answerWidget = QWidget()
            self.answerWidget.setStyleSheet("background-color: white")
            answerLayout = QVBoxLayout()
            answerLayout.setMargin(0)
            self.answerRadioBtn1 = QRadioButton('Yes')
            self.answerRadioBtn1.setStyleSheet("background-color: white")
            MyFunctions.setFontForUI(self.answerRadioBtn1, 25)
            self.answerRadioBtn2 = QRadioButton('No')
            self.answerRadioBtn2.setStyleSheet("background-color: white")
            MyFunctions.setFontForUI(self.answerRadioBtn2, 25)
            self.answerRadioBtn3 = QRadioButton()
            self.answerRadioBtn3.setStyleSheet("background-color: white")
            MyFunctions.setFontForUI(self.answerRadioBtn3, 25)
            self.answerRadioBtn4 = QRadioButton()
            self.answerRadioBtn4.setStyleSheet("background-color: white")
            MyFunctions.setFontForUI(self.answerRadioBtn4, 25)
            answerLayout.addWidget(self.answerRadioBtn1)
            answerLayout.addWidget(self.answerRadioBtn2)
            answerLayout.addWidget(self.answerRadioBtn3)
            answerLayout.addWidget(self.answerRadioBtn4)
            self.answerWidget.setLayout(answerLayout)
            self.createUIInScene(self.answerWidget)
            self.interfaceQuesItems.add(self.answerRadioBtn1)
            self.interfaceQuesItems.add(self.answerRadioBtn2)
            self.interfaceQuesItems.add(self.answerRadioBtn3)
            self.interfaceQuesItems.add(self.answerRadioBtn4)
            
            self.nextExplainPBtn = QPushButton('Explain')
            MyFunctions.setFontForUI(self.nextExplainPBtn, 25)
            self.createUIInScene(self.nextExplainPBtn)
            self.nextExplainPBtn.setStyleSheet("background-color: #328930")

            self.nextSkipPBtn = QPushButton('Check')
            MyFunctions.setFontForUI(self.nextSkipPBtn, 25)
            self.createUIInScene(self.nextSkipPBtn)
            
            self.correctnessTextItem = self.createGraphicsTextItem(self.scene,'', 25)
                
            self.footnoteTextItem = self.createGraphicsTextItem(self.scene,self.FOOTNOTE[self.PROCESS_QUES], 25)
            self.footnoteTextWidth = self.footnoteTextItem.boundingRect().width()

            self.answerRadioBtn1.clicked.connect(self.rBtn1Clicked)
            self.answerRadioBtn2.clicked.connect(self.rBtn2Clicked)
            self.answerRadioBtn3.clicked.connect(self.rBtn3Clicked)
            self.answerRadioBtn4.clicked.connect(self.rBtn4Clicked)
        
            self.nextSkipPBtn.clicked.connect(self.checkAnswer)
            self.nextExplainPBtn.clicked.connect(self.explainAnswer)
        
    def updateLayout(self):
        self.tableViewQuestionConf.setGeometry(0, 0, self.scene.sceneRect().width(), 0.5*self.scene.sceneRect().height())
        self.tablePermissionViewQuestionConf.setGeometry(0, 0, self.scene.sceneRect().width(), 0.5*self.scene.sceneRect().height())

        if self.quesTextWidth > self.scene.sceneRect().width(): 
            self.labelQuestionText.setTextWidth(self.scene.sceneRect().width())
        else:
            self.labelQuestionText.setTextWidth(self.quesTextWidth)
        if self.footnoteTextWidth > self.scene.sceneRect().width():   
            self.footnoteTextItem.setTextWidth(self.scene.sceneRect().width())
        else:
            self.footnoteTextItem.setTextWidth(self.footnoteTextWidth)
        
        xinter = self.labelQuestionText.boundingRect().width()
        xinter1 = self.footnoteTextItem.boundingRect().width()
        xinter = max(xinter, xinter1)
        self.footnoteTextItem.setPos(0.5*(self.scene.sceneRect().width()-xinter), 0.51*self.scene.sceneRect().height())
        self.labelQuestionText.setPos(self.footnoteTextItem.pos().x(), self.footnoteTextItem.pos().y()+self.footnoteTextItem.boundingRect().height()+5)
        self.answerWidget.setGeometry(self.labelQuestionText.pos().x()+10, self.labelQuestionText.pos().y()+self.labelQuestionText.boundingRect().height()+5, \
                                           self.answerWidget.geometry().width(), self.answerWidget.geometry().height())
        xinter = self.nextExplainPBtn.geometry().width()
        yinter = self.nextExplainPBtn.geometry().height()
        self.nextExplainPBtn.setGeometry(self.scene.sceneRect().width()-10-xinter, self.scene.sceneRect().height()-10-yinter, \
                                         xinter, yinter)
        xinter = self.nextSkipPBtn.geometry().width()
        self.nextSkipPBtn.setGeometry(self.nextExplainPBtn.pos().x()-xinter-10, self.nextExplainPBtn.pos().y(), \
                                         self.nextExplainPBtn.geometry().width(), self.nextSkipPBtn.geometry().height())
        self.correctnessTextItem.setPos(self.nextSkipPBtn.geometry().x(), self.nextSkipPBtn.geometry().y()-self.nextSkipPBtn.geometry().height()-5)
        if self.questionType == self.PROCESS_QUES:
            self.answerRadioBtn3.setVisible(False)
            self.answerRadioBtn4.setVisible(False)
        else:
            self.answerRadioBtn3.setVisible(True)
            self.answerRadioBtn4.setVisible(True)
        
    def setVisibilityOfSceneItems(self, flag):
        for i in self.interfaceQuesItems:
            i.setVisible(flag)
        flagQuesType = (self.questionType == self.PROCESS_QUES)
        allflag = flag and flagQuesType
        for i in self.interfaceTableItems:
                i.setVisible(allflag)
        if flag:
            if self.questionType == self.PROCESS_QUES:
                self.labelQuestionText.setPlainText(self.QUES_INFO[self.PROCESS_QUES][0])
                self.quesTextWidth = self.labelQuestionText.boundingRect().width()
                self.answerRadioBtn1.setText(self.QUES_INFO[self.PROCESS_QUES][1])
                self.answerRadioBtn2.setText(self.QUES_INFO[self.PROCESS_QUES][2])
                self.processUIsetting()
            elif self.questionType == self.PERM_QUES:
                self.labelQuestionText.setPlainText(self.QUES_INFO[self.PERM_QUES][0])
                self.permissionUIsetting()
            self.settingChanged()
            self.updateLayout()
        
    def setTableBackgroundColor(self, endr, endc, isEnabled):
        for c in xrange(endc):
            for r in xrange(endr): 
                item = self.tableViewQuestionConf.item(r, c)
                if isEnabled:
                    if c < 2:
                        color = QColor(234, 250, 241)
                    elif c < 4:
                        color = QColor(252, 243, 207)
                    else:
                        color = QColor(250, 219, 216)
                else:
                    color = Qt.lightGray
                item.setData(Qt.BackgroundRole, QVariant(QBrush(color)))
                
    def setPermTableBackgroundColor(self):
        for r in xrange(self.tablePermissionViewQuestionConf.rowCount()):
            for c in xrange(self.tablePermissionViewQuestionConf.columnCount()):
                item = self.tablePermissionViewQuestionConf.item(r,c)
                item.setData(Qt.BackgroundRole, QVariant(QBrush(QColor(252, 243, 207))))
                             
    def processUIsetting(self):
        self.tableViewQuestionConf.setVisible(True)
        self.tablePermissionViewQuestionConf.setVisible(False)
        self.footnoteTextItem.setVisible(True)
        
    def permissionUIsetting(self):
        self.tableViewQuestionConf.setVisible(False)
        self.tablePermissionViewQuestionConf.setVisible(True)
        self.generateChoicesForPermQues()
        self.footnoteTextItem.setVisible(False)
        
    def convertOctStringToRWXSet(self, permOctString):
        permRWXSet = set(PermissionChecker.convertOctToRWXString(int(permOctString)))
        permRWXSet.discard('-') 
        return permRWXSet
        
    def convertNineBitsOctToRWX(self, perm):
        perms = ''
        start = 3
        otherp = int(perm[start], 8)
        groupp = int(perm[start-1], 8)
        userp = int(perm[start-2], 8)
        perms+=PermissionChecker.convertOctToRWXString(userp, int(perm, 8) & S_ISUID)
        perms+=PermissionChecker.convertOctToRWXString(groupp, int(perm, 8) & S_ISGID)
        other=PermissionChecker.convertOctToRWXString(otherp, False, True, int(perm, 8) & S_ISVTX)
        if other[-2:] == 'xt':
            perms+=other[:-2]
            perms+='t'
        elif other[-2:] == '-t':
            perms+=other[:-2]
            perms+='T'
        else:
            perms+=other[:-1]
        return perms
        
    def generateRandomPermissionInOctal(self):
        special = [0, 1, 2, 4, 3, 6, 7]
        specialNum = random.choice(special)
        usernum = random.randrange(0, 8)
        groupnum = random.randrange(0, 8)
        othernum = random.randrange(0, 8)
        permstr = str(specialNum)+str(usernum)+str(groupnum)+str(othernum)
        return permstr
    
    def generateChoicesForPermQues(self):
        '''random permission in question'''
        choices = ['']*4
        index = [0,1,2,3]
        chosenPerm = self.generateRandomPermissionInOctal()
        tableItem = self.tablePermissionViewQuestionConf.item(1,1)
        tableItem.setText(chosenPerm)
        chosenPerm = self.convertNineBitsOctToRWX(chosenPerm)
        i = random.choice(index)
        choices[i] = chosenPerm
        index.remove(i)
        while index:
            choiceStr = self.generateRandomPermissionInOctal()
            choiceStr = self.convertNineBitsOctToRWX(choiceStr)
            if choiceStr not in choices:
                i = random.choice(index)
                choices[i] = choiceStr
                index.remove(i)
        self.answerRadioBtn1.setText(choices[0])
        self.answerRadioBtn2.setText(choices[1])
        self.answerRadioBtn3.setText(choices[2])
        self.answerRadioBtn4.setText(choices[3])

    def resetAnimatedItems(self):
        for r in xrange(self.tableViewQuestionConf.rowCount()):
            for c in xrange(self.tableViewQuestionConf.columnCount()):
                self.tableViewQuestionConf.item(r,c).setSelected(False)
        '''disable all highlight in text as well'''
        self.higlightPermSection(-1, False)
                
    def higlightPermSection(self, section=0, isHighlight = True):
        text = self.settingPermInfo
        if isHighlight:
            colonIndex = text.find(':')
            letterStart = 1+section*3
            numberStart = colonIndex+3+section
            colorStr = '<font color=black size=3>%s</font>'%text[:letterStart]
            colorStr += '<font color="red" size="3">%s</font>'%text[letterStart:letterStart+3]
            colorStr += '<font color="black" size="3">%s</font>'%text[letterStart+3:numberStart]
            colorStr += '<font color="red" size="3">%s</font>'%text[numberStart:numberStart+1]
            colorStr += '<font color="black" size="3">%s</font>'%text[numberStart+1:]
        else:
            colorStr = '<font color="black" size="3">%s</font>'%text
        self.settingPermLabel.setText(colorStr)
        if isHighlight:
            return text[letterStart:letterStart+3]
        else:
            return None
        
    def onAnimateSelfTest(self):
        if self.questionType == self.PROCESS_QUES:
            self.onAnimateSelfTest_Process()
        else:
            self.onAnimateSelfTest_Permission()
            
    def onAnimateSelfTest_Permission(self):
        self.resetAnimatedItems()
        self.main.explainTexteditHighlightLastLines()
        correctPerm = str(self.tablePermissionViewQuestionConf.item(1,1).text())
        if self.main.animationStep == 0:
            self.updateExplainText('- The permission in octal notation is: '+str(correctPerm))
            self.updateExplainText('- Each octal digit in order represents:')
            self.updateExplainText('  Special bits, user bits, group bits and other bits.\n')
        elif self.main.animationStep == 1:
            self.updateExplainText('- The representation in user, group and other permission bits means: ')
            self.updateExplainText('  (R)ead (W)rite E(x)ecute')
            self.updateExplainText('   1\t  1\t   1')
            self.updateExplainText('  "1" means having the permission')
            self.updateExplainText('  "0" means not having the permission')
            self.updateExplainText('  Weight for each bit')
            self.updateExplainText('   4\t  2\t   1')
            self.updateExplainText('   For example, 3 means having write and execute permissions.')
            self.updateExplainText('   In letter notation, it writes as "-wx".\n')
        elif self.main.animationStep == 2:
            userbit = correctPerm[1]
            self.updateExplainText('- Checking user bits (The second digit):')
            self.updateExplainText('  The octal is: %s'%userbit)
            userLetter = PermissionChecker.convertOctToRWXString(int(userbit))
            self.updateExplainText('  Its letter notation is: %s\n'%userLetter)
        elif self.main.animationStep == 3:
            octalbit = correctPerm[2]
            self.updateExplainText('- Checking group bits (The third digit):')
            self.updateExplainText('  The octal is: %s'%octalbit)
            letter = PermissionChecker.convertOctToRWXString(int(octalbit))
            self.updateExplainText('  Its letter notation is: %s\n'%letter)
        elif self.main.animationStep == 4:
            octalbit = correctPerm[3]
            self.updateExplainText('- Checking other bits (The fourth digit):')
            self.updateExplainText('  The octal is: %s'%octalbit)
            letter = PermissionChecker.convertOctToRWXString(int(octalbit))
            self.updateExplainText('  Its letter notation is: %s\n'%letter)
        elif self.main.animationStep == 5:
            octalbit = correctPerm[0]
            self.updateExplainText('- Checking special bits (The first digit):')
            self.updateExplainText('  SUID SGID Sticky')
            self.updateExplainText('  1\t1\t1')
            self.updateExplainText('  "1" means having the permission')
            self.updateExplainText('  "0" means not having the permission')
            self.updateExplainText('  Weight for each bit')
            self.updateExplainText('  4\t2\t1')
            self.updateExplainText('  The octal is: %s\n'%octalbit)
            if int(octalbit, 8) & S_ISUID:
                self.updateExplainText('  SUID bit is set. "x" bit in user bits should be "s" if "x" is set; "x" bit in user bits should be "S" if "x" is not set.\n')
            if int(octalbit, 8) & S_ISGID:
                self.updateExplainText('  SGID bit is set. "x" bit in group bits should be "s" if "x" is set; "x" bit in group bits should be "S" if "x" is not set.\n')
            if int(octalbit, 8) & S_ISVTX:
                self.updateExplainText('  Sticky bit is set. "x" bit in other bits should be "t" if "x" is set; "x" bit in other bits should be "T" if "x" is not set.\n')
        elif self.main.animationStep == 6:
            self.updateExplainText('- Conclusion:')
            self.updateExplainText('  "%s" means having permission of %s.\n'%(\
                                    correctPerm, self.convertNineBitsOctToRWX(correctPerm)))
        
    def onAnimateSelfTest_Process(self):
        '''
        0 |     1   | 2 |  3  |     4
        0 | process | 2 | obj | perm(binary)
        1 | ruid    |   | dir | p
        2 | rgid    |   | user | 
        3 | euid    |   | group|
        4 | egid    |   | perm | 
        '''
        self.resetAnimatedItems()
        self.main.explainTexteditHighlightLastLines()
        if self.main.animationStep == 0:
            self.updateExplainText('Access is determined by first identifying which set of permission bits to apply: owner, group, or world. The applicable bits are determined using the effective UID and GID...\n')
        elif self.main.animationStep == 1:
            self.updateExplainText('- Check effective UID:')
            self.tableViewQuestionConf.item(3,1).setSelected(True)
            self.tableViewQuestionConf.item(2,3).setSelected(True)
            highlightedPerm = self.higlightPermSection(0)
            if 's' in highlightedPerm or 'S' in highlightedPerm:
                self.updateExplainText('  The setUID bit is on. Therefore, the process runs as the user owner of the object.')
                self.updateExplainText('  So the effective user of the process is "%s".'%self.info_fileuser)
                self.updateExplainText('  The user owner of the object is "%s".'%self.info_fileuser)
            else:
                self.updateExplainText('  The user owner of the object is "%s".'%self.info_fileuser)
                self.updateExplainText('  The effective user of the process is "%s".'%self.info_procuser)
            if self.info_section != 0:
                self.updateExplainText('  The effective UID of the process is not the user owner of the object.')
            else:
                self.main.animationStep = 4
                self.getProcessQuestionHighlightAndConcludSpec()
            self.updateExplainText('')
        elif self.main.animationStep == 2:
            self.updateExplainText('- Check effective GID:')
            self.tableViewQuestionConf.item(4,1).setSelected(True)
            self.tableViewQuestionConf.item(3,3).setSelected(True)
            highlightedPerm = self.higlightPermSection(1)
            if 's' in highlightedPerm or 'S' in highlightedPerm:
                self.updateExplainText('  The setGID bit is on. Therefore, the process runs as the group owner of the object.')
                self.updateExplainText('  So the effective group of the process is "%s".'%self.info_filegroup)
                self.updateExplainText('  The group owner of the object is "%s".'%self.info_filegroup)
            else:
                self.updateExplainText('  The group owner of the object is "%s".'%self.info_filegroup)
                self.updateExplainText('  The effective group of the process is "%s".'%self.info_procgroup)
            if self.info_section == 1:
                self.main.animationStep = 4
                self.updateExplainText('  The effective GID of the process is the group owner of the object.')
                self.getProcessQuestionHighlightAndConcludSpec()
            else:
                self.updateExplainText('  The effective GID of the process is not the group owner of the object.')
            self.updateExplainText('')
        elif self.main.animationStep == 3:
            self.updateExplainText('- Since neither the owner or group bits are used, the other bits are applied:')
            self.main.animationStep = 4
            self.getProcessQuestionHighlightAndConcludSpec()
            self.updateExplainText('')
        elif self.main.animationStep == 5:
            self.updateExplainText('- Conclusion:')
            if self.info_success:
                if self.info_section == 0:
                    bits = 'user'
                elif self.info_section == 1:
                    bits = 'group'
                else:
                    bits = 'other'
                self.updateExplainText('  The process can access the object with the chosen permission through "%s" field.'%bits)
            else:
                self.updateExplainText('  The process does not have the specified permission to the object.')
    
    def getProcessQuestionHighlightAndConcludSpec(self):
        self.tableViewQuestionConf.item(4,3).setSelected(True)
        self.higlightPermSection(self.info_section)
        infomsgs = self.info_msg.split('.')
        infomsgs.remove('')
        self.updateExplainText('  '+infomsgs[0]+'.')
        for i in xrange(len(infomsgs)):
            number = 2
            if infomsgs[i][0] == ' ':
                number = 1
            spaces = number*' '
            self.updateExplainText(spaces+infomsgs[i]+'.')
            if i == 0:
                self.updateExplainText('  Once the applicable set of bits is determined, their values are compared to the requested access.')
  
    def setObjUI(self, objDir):
        self.objDir = objDir
        self.objDirLineEdit.lineEdit().setText(objDir)
        
    def getPermInfo(self, filepath):   
        fileuser, filegroup, uid, gid = PermissionChecker.getFileUserAndGroup(filepath, None, self.scene)
        if fileuser == None and uid == -1:
            return None
        perms = PermissionChecker.getPermissionbitForFile(filepath, None, self.scene)
        permletters = PermissionChecker.convertNineBitsOctToRWX(perms)
        return fileuser, str(uid), filegroup, str(gid), permletters, perms
    
    def updateFileInfo(self):
        '''file type'''
        self.objDir = str(self.objDirLineEdit.currentText())
        if self.objDir:
            if self.objDir[-1] == '/' and self.objDir != '/':
                self.objDir = self.objDir[:-1]
            itemUser = self.tableViewQuestionConf.item(2,3)
            itemGroup = self.tableViewQuestionConf.item(3,3)
            permInfo = self.getPermInfo(self.objDir)
            import os
            if permInfo:
                itemUser.setText(permInfo[0]+':'+permInfo[1])
                itemGroup.setText(permInfo[2]+':'+permInfo[3])
                if os.path.isfile(self.objDir):
                    self.settingPermLabel.setText('-'+permInfo[4]+':'+permInfo[5])
                    self.settingPermInfo = '-'+permInfo[4]+':'+permInfo[5]
                else:
                    self.settingPermLabel.setText('d'+permInfo[4]+':'+permInfo[5])
                    self.settingPermInfo = 'd'+permInfo[4]+':'+permInfo[5]
            else:
                itemUser.setText('None')
                itemGroup.setText('None')
                self.settingPermLabel.setText('-----------:----')
                self.settingPermInfo = '-----------:----'
        self.settingChanged()
        
    def addUsersToUI(self):
        self.procRUIDLineEdit.clear()
        self.procEUIDLineEdit.clear()
        for u in self.main.userSysList:
            self.procRUIDLineEdit.addItem(u)
            self.procEUIDLineEdit.addItem(u)
        for u in self.main.userSpecList:
            self.procRUIDLineEdit.addItem(u)
            self.procEUIDLineEdit.addItem(u)
            
    def addGroupsToUI(self):
        self.procRGIDLineEdit.clear()
        self.procEGIDLineEdit.clear()
        for u in self.main.groupSysList:
            self.procRGIDLineEdit.addItem(u)
            self.procEGIDLineEdit.addItem(u)
        for u in self.main.groupSpecList:
            self.procRGIDLineEdit.addItem(u)
            self.procEGIDLineEdit.addItem(u)
    
    def addSpecObjToUI(self):
        self.objDirLineEdit.clear()
        for d in self.scene.dirNodeList:
            self.objDirLineEdit.addItem(d.getFullPath())
        self.objDir = str(self.objDirLineEdit.itemText(0))
        
    def updateUIContents(self):
        if self.main.root_dir:
            self.addUsersToUI()
            self.addGroupsToUI()
            self.addSpecObjToUI()
            self.w = FileDialog(self.main, 'Select an object', self.main.root_dir)
    
    '''handlers'''
    def noRootdirWarning(self):
        if not self.main.root_dir:
            QMessageBox.critical(self.main, '', 'Please import a policy file or set a root directory!')
            return
        
    def setObjPath(self):
        if not self.main.root_dir:
            QMessageBox.critical(self.main, '', 'Please import a policy file or set a root directory!')
            return
        self.w.show()
#         
    def showWholePathAsHint(self, dirIndex):
        self.objDirLineEdit.setItemData(dirIndex, str(self.objDirLineEdit.itemText(dirIndex)), Qt.ToolTipRole)
        
    def randomProc(self):
        if not self.main.root_dir:
            QMessageBox.critical(self.main, '', 'Please import a policy file or set a root directory!')
            return
        self.randomGetRUID()
        self.randomGetRGID()
        self.randomGetEUID()
        self.randomGetEGID()
        
    def randomGetRUID(self):
        if not self.main.root_dir:
            QMessageBox.critical(self.main, '', 'Please import a policy file or set a root directory!')
            return
        index = random.randrange(self.procRUIDLineEdit.count())
        self.procRUIDLineEdit.setCurrentIndex(index)
        self.settingChanged()
        
    def randomGetRGID(self):
        if not self.main.root_dir:
            QMessageBox.critical(self.main, '', 'Please import a policy file or set a root directory!')
            return
        index = random.randrange(self.procRGIDLineEdit.count())
        self.procRGIDLineEdit.setCurrentIndex(index)
        self.settingChanged()
    
    def randomGetEUID(self):
        if not self.main.root_dir:
            QMessageBox.critical(self.main, '', 'Please import a policy file or set a root directory!')
            return
        index = random.randrange(self.procEUIDLineEdit.count())
        self.procEUIDLineEdit.setCurrentIndex(index)
        self.settingChanged()
    
    def randomGetEGID(self):
        if not self.main.root_dir:
            QMessageBox.critical(self.main, '', 'Please import a policy file or set a root directory!')
            return
        index = random.randrange(self.procEGIDLineEdit.count())
        self.procEGIDLineEdit.setCurrentIndex(index)
        self.settingChanged()
    
    def randomGetPerm(self):
        if not self.main.root_dir:
            QMessageBox.critical(self.main, '', 'Please import a policy file or set a root directory!')
            return
        perm = random.randrange(1, 8)
        self.permLineEdit.setCurrentIndex(perm-1)
        self.settingChanged()
        
    def radioButtonSetChecked(self, rbtn, flag):
        rbtn.setAutoExclusive(False)
        rbtn.setChecked(flag)
        rbtn.setAutoExclusive(True)
        
    def rBtn1Clicked(self):
        self.chosenAnswer = self.answerRadioBtn1
        self.radioButtonSetChecked(self.answerRadioBtn2, False)
        self.radioButtonSetChecked(self.answerRadioBtn3, False)
        self.radioButtonSetChecked(self.answerRadioBtn4, False)
        
    def rBtn2Clicked(self):
        self.chosenAnswer = self.answerRadioBtn2
        self.radioButtonSetChecked(self.answerRadioBtn1, False)
        self.radioButtonSetChecked(self.answerRadioBtn3, False)
        self.radioButtonSetChecked(self.answerRadioBtn4, False)

    def rBtn3Clicked(self):
        self.chosenAnswer = self.answerRadioBtn3
        self.radioButtonSetChecked(self.answerRadioBtn1, False)
        self.radioButtonSetChecked(self.answerRadioBtn2, False)
        self.radioButtonSetChecked(self.answerRadioBtn4, False)
        
    def rBtn4Clicked(self):
        self.chosenAnswer = self.answerRadioBtn4
        self.radioButtonSetChecked(self.answerRadioBtn1, False)
        self.radioButtonSetChecked(self.answerRadioBtn2, False)
        self.radioButtonSetChecked(self.answerRadioBtn3, False)
        
    def settingChanged(self):
        self.correctnessTextItem.setHtml("")
        self.resetAnimatedItems()
        self.main.animationStep = 0
        self.main.explainTextEdit.clear()
        self.nextExplainPBtn.setText('Explain')
        self.nextExplainPBtn.setStyleSheet('QPushButton {background-color: #328930;}')
        self.settingIsChanged = True
        if self.questionType == self.PERM_QUES:
            self.generateChoicesForPermQues()
        
    def computePermForEachBit(self, username, filepath, parentDir, action):
        '''groupname is name of any group'''
        actionOrdered = sorted(list(action))
        settingperm = ' and '.join(actionOrdered)
        msg = ''
        oldpermrelation = self.main.filebrowser.permrelation
        fileuser = str(self.tableViewQuestionConf.item(2,3).text())
        fileuser = fileuser[:fileuser.find(':')]
        filegroup = str(self.tableViewQuestionConf.item(3,3).text())
        filegroup = filegroup[:filegroup.find(':')]
        filePerm = str(self.tableViewQuestionConf.item(4,3).text())
        filePerm = filePerm[:filePerm.find(':')]
        
        grouptext = str(self.procEGIDLineEdit.currentText())
        groups = set([grouptext])
        if fileuser == None:
            return None
        perms = PermissionChecker.getPermissionbitForFile(filepath, None, self.scene)
        permletters = PermissionChecker.convertNineBitsOctToRWX(perms)
        permsu = permletters[:3]
        permsg = permletters[3:6]
        permso = permletters[6:]
        self.main.filebrowser.permrelation = self.main.filebrowser.AND_RELATION
        if (fileuser == username) or ('s' in permsu or 'S' in permsu):
            section = 0
            if self.main.filebrowser.hasPerm(action, permsu, permso, 'user'):
                success = True
                msg+=('%s%s')\
                    %(self.main.filebrowser.bitsToUseMsg('user', permsu), self.main.filebrowser.fileMsg(success, settingperm, 'user', permsu))
            else:
                success = False
                msg+=('%s%s')\
                    %(self.main.filebrowser.bitsToUseMsg('user', permsu), self.main.filebrowser.fileMsg(success, settingperm, 'user', permsu))
        elif (filegroup in groups) or ('s' in permsg or 'S' in permsg):
            section = 1
            if self.main.filebrowser.hasPerm(action, permsg, permso, 'group'):
                success = True
                msg+=('%s%s')\
                    %(self.main.filebrowser.bitsToUseMsg('group', permsg), self.main.filebrowser.fileMsg(success, settingperm, 'group', permsg))
            else:
                success = False
                msg+=('%s%s')\
                    %(self.main.filebrowser.bitsToUseMsg('group', permsg), self.main.filebrowser.fileMsg(success, settingperm, 'group', permsg))
        else:
            section = 2
            if self.main.filebrowser.hasPerm(action, permso, permso, 'other'):
                success = True
                msg+=('%s%s')\
                    %(self.main.filebrowser.bitsToUseMsg('other', permso), self.main.filebrowser.fileMsg(success, settingperm, 'other', permso))
            else:
                success = False
                msg += ('%s%s')\
                    %(self.main.filebrowser.bitsToUseMsg('other', permso), self.main.filebrowser.fileMsg(success, settingperm, 'other', permso))
        self.main.filebrowser.permrelation = oldpermrelation
        return success, section, username, fileuser, grouptext, filegroup, msg
    
    def reanalyze(self):
        actionText = str(self.permLineEdit.currentText())
        action = set(actionText)
        action.discard("-")
        username = str(self.procEUIDLineEdit.currentText())
        return self.computePermForEachBit(username, self.objDir, False, action)             
            
    def checkAnswer(self):
        if self.chosenAnswer == None:
            QMessageBox.critical(self.main, '', 'Please choose an answer!')
            return
        if self.questionType == self.PROCESS_QUES:
            if not self.main.root_dir:
                QMessageBox.critical(self.main, '', 'Please import a policy file or set a root directory!')
                return
            self.procruid = str(self.procRUIDLineEdit.currentText())
            self.procrgid = str(self.procRGIDLineEdit.currentText())
            self.proceuid = str(self.procEUIDLineEdit.currentText())
            self.procegid = str(self.procEGIDLineEdit.currentText())
    
            self.objDir = str(self.objDirLineEdit.currentText())
            if self.info == None or self.settingIsChanged:
                self.info = self.reanalyze()
                self.settingIsChanged = False
            if self.info[0] == self.answerRadioBtn1.isChecked():
                self.correctnessTextItem.setHtml('<font color="green" size="3">Correct</font>')
            else:
                self.correctnessTextItem.setHtml('<font color="red" size="3">Incorrect</font>')
        else:
            correctPerm = str(self.main.permissionCalDialog.octal2Letter.octalDisplayLab.displayText())
            correctPermLetter = self.convertNineBitsOctToRWX(correctPerm)
            chosenPerm = str(self.chosenAnswer.text())
            if correctPermLetter != chosenPerm:
                self.correctnessTextItem.setHtml('<font color="red" size="3">Incorrect</font>')
            else:
                self.correctnessTextItem.setHtml('<font color="green" size="3">Correct</font>')
            
    def updateExplainText(self, text):
        self.msg += text
        self.main.explainTextEdit.appendPlainText(text)
        
    def explainAnswer(self):
        if str(self.nextExplainPBtn.text()) == 'End':
            self.main.explainTextEdit.clear()
            self.nextExplainPBtn.setText('Explain')
            self.nextExplainPBtn.setStyleSheet('QPushButton {background-color: #328930;}')
            return
        if self.questionType == self.PROCESS_QUES:
            if str(self.nextExplainPBtn.text()) == 'Explain':
                self.nextExplainPBtn.setText('Next')
                self.nextExplainPBtn.setStyleSheet('QPushButton {background-color: yellow;}')
                if not self.main.root_dir:
                    QMessageBox.critical(self.main, '', 'Please import a policy file or set a root directory!')
                    return
                self.msg = ''
                if self.info == None or self.settingIsChanged:
                    self.info = self.reanalyze()
                    self.settingIsChanged = False
                self.info_success = self.info[0]
                self.info_section = self.info[1]
                self.info_procuser = self.info[2]
                self.info_fileuser = self.info[3]
                self.info_procgroup = self.info[4]
                self.info_filegroup = self.info[5]
                self.info_msg = self.info[6]
                self.main.animationStep = 0
            self.onAnimateSelfTest_Process()
            if self.main.animationStep == self.ANIMTESTEPS[self.PROCESS_QUES]:
                self.nextExplainPBtn.setText('End')
                self.nextExplainPBtn.setStyleSheet('QPushButton {background-color: red;}')
        else:
            if str(self.nextExplainPBtn.text()) == 'Explain':
                self.nextExplainPBtn.setText('Next')
                self.nextExplainPBtn.setStyleSheet('QPushButton {background-color: yellow;}')
                self.msg = ''
                self.main.animationStep = 0
            self.onAnimateSelfTest_Permission()
            if self.main.animationStep == self.ANIMTESTEPS[self.PERM_QUES]:
                self.nextExplainPBtn.setText('End')
                self.nextExplainPBtn.setStyleSheet('QPushButton {background-color: red;}')
        self.main.animationStep += 1