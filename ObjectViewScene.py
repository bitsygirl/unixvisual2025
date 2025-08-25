'''
Created on Mar 17, 2016

@author: manwang
Updated for PyQt6 compatibility
'''
from PyQt6.QtGui import QFont, QPainter
from PyQt6.QtWidgets import (QGraphicsTextItem, QMessageBox, QSizePolicy, 
                             QComboBox, QPushButton, QLineEdit, QGraphicsProxyWidget, 
                             QLabel, QRadioButton, QButtonGroup, QFrame, QWidget, 
                             QVBoxLayout, QScrollArea, QLayout)
from PyQt6.QtCore import QPointF, QRect, QPoint, QRectF, Qt
from FileNode import FileNode
from EdgeItem import EdgeItem
from ObjectViewNodes import FilePermNode, CheckNode, TitleNode
import PermissionChecker, MyFunctions, re
from FileDialog import FileDialog
        
class ObjectViewScene(object):
    PARENTDIRMSG = "The execute permission is needed to reach the objects under this directory."
    ALLUSERTEXT = 'All'
    ALLGROUPTEXT = 'All'
    OTHERUSERTEXT = '|others|'
    PRACTICE_QUES_CHOICES = [['User bits', 'Group bits', 'Other bits'], ['Yes', 'No']]
    PRACTICE_QUES_PERM_OPERATIONS = [['read the content of the highlighted object', 'modify the content of the highlighted object', 'execute the highlighted object as a program'], \
                                     ['list the files or directories under the highlighted object', 'add/remove files or directories under the highlighted object', 'pass through to reach the files and directories under the highlighted object']]
    '''Mac'''
    #INITROOTPATH = ''#/Users/manwang/Documents/workspace/UnixVisual/src/pseudoroot'
    #INITIALPATH = ''#code/program1'
    '''Linux'''
    INITROOTPATH = '/'#/home/manw/workspace/UNIXvisual/src/pseudoroot'
    INITIALPATH = ''#untitled folder/cod'
    msgDefault = ''#Click on a "user:permission" tuple in the last row for detailed analysis.'
    ANIMA_STOP_STEP = 1024
    
    def __init__(self, main):
        self.main = main
        self.scene = main.scene
        self.sceneClick = None
        self.isFile = True
        self.fromFileDialog = False
        self.bitsIndexList = []
        self.practiceQuestionWidgets = []
        self.practiceChoices = []
        self.practiceButtonGroups = []
        self.practiceAnswers = []
        self.practiceKeys = []
        self.checkedAnswer = False
        
        self.dirNodes = []
        self.dirEdges = []
        self.objList = []
        self.checkgridNodes = []
        self.nodeIndex = 0
        titleFont = QFont("Courier", 25)
        
        self.ownerTextItem = TitleNode('Owner bits')
        self.groupTextItem = TitleNode('Group bits')
        self.otherTextItem = TitleNode('Other bits')
        
        self.textItems = [self.ownerTextItem, self.groupTextItem, self.otherTextItem]
        self.interfaceItems = set([self.ownerTextItem, self.groupTextItem, self.otherTextItem])
        self.msg = QGraphicsTextItem(self.msgDefault)
        MyFunctions.setFontForUI(self.msg, 19)
        self.interfaceItems.add(self.msg)
        self.objPath = self.INITIALPATH
        self.userWidgets()
        self.fileDialog = FileDialog(self.main, 'Select an object', self.main.root_dir)
        self.fileDialog.fileChosen.connect(self.confirmObjPath)
        self.fileDialog.directoryEntered.connect(lambda directory: self.checkStartingDirectory(directory))
        
        
    def checkStartingDirectory(self, directory):
        if not MyFunctions.is_subdir(str(directory), self.main.root_dir): 
            self.fileDialog.setDirectory(self.main.root_dir)
        
    def resetScene(self):
        self.selectedItem = None
        for i in self.dirNodes:
            self.scene.removeItem(i)
            del i
        for i in self.dirEdges:
            self.scene.removeItem(i)
            del i
        self.dirNodes = []
        self.dirEdges = []
        self.objList = []
        self.clickableCheckNodes = []
        self.resetAnalysisNodes()

    def resetAnalysisNodes(self):
        self.previousUsers = set()
        for i in self.checkgridNodes:
            for j in i:
                for k in j:
                    k.analysisDialog.hide()
                    self.scene.removeItem(k)
                    del k
        self.checkgridNodes = [[], [], []]
        for d in self.dirNodes:
            perms = self.getPermInfo(d.dirpath)
            if perms == None:
                perms = 'None'
            self.setHighlightSec(d, perms, -1)
    
    def getRealUsrName(self):
        import pwd, os
        return pwd.getpwuid( os.getuid() )[ 0 ]
        
    def getPermInfo(self, filepath):         
        fileuser, filegroup, uid, gid = PermissionChecker.getFileUserAndGroup(filepath, None, self.scene)
        if fileuser == None and uid == -1:
            return None
        perms = PermissionChecker.getPermissionbitForFile(filepath, None, self.scene)
        permletters = PermissionChecker.convertNineBitsOctToRWX(perms)
        temp = 'User:'+str(uid)+'('+fileuser +')\nGroup:' + str(gid)+'('+filegroup+')\nPermission bits:'+perms+'('+permletters+')'
        return temp
    
    def computePermForGrid(self, username, filepath, parentDir, action = None):
        '''groupname is the name of group username belongs to'''
        if parentDir:
            action = set(['x'])
        if action == None:
            action = set(['r', 'w', 'x'])
        settingperm = ' or '.join(set(['read', 'write', 'execute']))
        msg = ''
        oldpermrelation = self.main.filebrowser.permrelation
        '''get filepath user and group and permission properties'''
        '''fileuser, filegroup, permsu, permsg, permso'''
        fileuser, filegroup, uid, gid = PermissionChecker.getFileUserAndGroup(filepath, None, self.scene)
        groups = set()
        grouptext = str(self.objectViewGroupComboBox.currentText())
        if grouptext == self.ALLGROUPTEXT:# all groups
            if username in self.main.user_group_sys_mat.keys():
                groups = self.main.user_group_sys_mat[username]
            elif username in self.main.user_group_mat.keys():
                groups = self.main.user_group_mat[username]
        else:#single group
            groups = set([grouptext])
        if fileuser == None and uid == -1:
            return None
        perms = PermissionChecker.getPermissionbitForFile(filepath, None, self.scene)
        permletters = PermissionChecker.convertNineBitsOctToRWX(perms)
        permsu = permletters[:3]
        permsg = permletters[3:6]
        permso = permletters[6:]
        self.main.filebrowser.permrelation = self.main.filebrowser.OR_RELATION
        if fileuser == username:
            prefix = 'User "%s" is the owner of the object. '%(username)
            if self.main.filebrowser.hasPerm(action, permsu, permso, 'user'):
                success = True
                if parentDir:
                    msg+=('%s%s')\
                        %(self.main.filebrowser.bitsToUseMsg('user', permsu), self.main.filebrowser.pdirMsg(success))
                else:
                    msg+=('%s%s')\
                        %(self.main.filebrowser.bitsToUseMsg('user', permsu), self.main.filebrowser.fileMsg(success, settingperm, 'user', permsu))
            else:
                success = False
                if parentDir:
                    msg+=('%s%s')\
                        %(self.main.filebrowser.bitsToUseMsg('user', permsu), self.main.filebrowser.pdirMsg(success))
                else:
                    msg+=('%s%s')\
                        %(self.main.filebrowser.bitsToUseMsg('user', permsu), self.main.filebrowser.fileMsg(success, settingperm, 'user', permsu))
        elif filegroup in groups:
            prefix = 'User "%s" is not the owner of the object. But it is a member of the object\'s group "%s". '%(username, filegroup)
            if self.main.filebrowser.hasPerm(action, permsg, permso, 'group'):
                success = True
                if parentDir:
                    msg+=('%s%s')\
                        %(self.main.filebrowser.bitsToUseMsg('group', permsg), self.main.filebrowser.pdirMsg(success))
                else:
                    msg+=('%s%s')\
                        %(self.main.filebrowser.bitsToUseMsg('group', permsg), self.main.filebrowser.fileMsg(success, settingperm, 'group', permsg))
            else:
                success = False
                if parentDir:
                    msg+=('%s%s')\
                        %(self.main.filebrowser.bitsToUseMsg('group', permsg), self.main.filebrowser.pdirMsg(success))
                else:
                    msg+=('%s%s')\
                        %(self.main.filebrowser.bitsToUseMsg('group', permsg), self.main.filebrowser.fileMsg(success, settingperm, 'group', permsg))
        else:
            prefix = 'User "%s" is neither the owner of the object nor a member of the object\'s group "%s". '%(username, filegroup)
            if self.main.filebrowser.hasPerm(action, permso, permso, 'other'):
                success = True
                if parentDir:
                    msg+=('%s%s')\
                            %(self.main.filebrowser.bitsToUseMsg('other', permso), self.main.filebrowser.pdirMsg(success))
                else:
                    msg+=('%s%s')\
                        %(self.main.filebrowser.bitsToUseMsg('other', permso), self.main.filebrowser.fileMsg(success, settingperm, 'other', permso))
            else:
                success = False
                if parentDir:
                    msg+=('%s%s')\
                            %(self.main.filebrowser.bitsToUseMsg('other', permso), self.main.filebrowser.pdirMsg(success))
                else:
                    msg += ('%s%s')\
                        %(self.main.filebrowser.bitsToUseMsg('other', permso), self.main.filebrowser.fileMsg(success, settingperm, 'other', permso))
        self.main.filebrowser.permrelation = oldpermrelation
        return success, prefix+msg, permsu, permsg, permso, groups
    
    def addUser2ComboBox(self):
        self.objectViewuserComboBox.clear()
        for u in self.main.userSysList:
            # Fixed: Handle bytes conversion
            user_str = u.decode('utf-8') if isinstance(u, bytes) else str(u)
            self.objectViewuserComboBox.addItem(user_str)
        for u in self.main.userSpecList:
            # Fixed: Handle bytes conversion
            user_str = u.decode('utf-8') if isinstance(u, bytes) else str(u)
            self.objectViewuserComboBox.addItem(user_str)
        
    def addGroup2ComboBox(self, groups):
        self.objectViewGroupComboBox.clear()
        for g in groups:
            # Fixed: Handle bytes conversion
            group_str = g.decode('utf-8') if isinstance(g, bytes) else str(g)
            self.objectViewGroupComboBox.addItem(group_str)
            
    def resetUserAndGroupInComboBox(self):
        index = self.objectViewuserComboBox.findText(self.getRealUsrName())
        self.objectViewuserComboBox.setCurrentIndex(index)
        self.setGroupForUserComboBox(index)
        
    def userWidgets(self):
        self.labelUser = QGraphicsTextItem('User:')
        MyFunctions.setFontForUI(self.labelUser, 17)
        if self.labelUser not in self.scene.items():
            self.scene.addItem(self.labelUser)
            self.objectViewuserComboBox = QComboBox()
            self.objectViewUserComboBoxWidget = QGraphicsProxyWidget()
            self.objectViewUserComboBoxWidget.setWidget(self.objectViewuserComboBox)
            self.objectViewUserComboBoxWidget.setZValue(1)
            self.scene.addItem(self.objectViewUserComboBoxWidget)
            self.objectViewuserComboBox.activated.connect(lambda index: self.selectUsername(index))
            
            self.labelGroup = QGraphicsTextItem('Group: ')
            MyFunctions.setFontForUI(self.labelGroup, 17)
            self.scene.addItem(self.labelGroup)
            self.objectViewGroupComboBox = QComboBox()
            self.objectViewGroupComboBoxWidget = QGraphicsProxyWidget()
            self.objectViewGroupComboBoxWidget.setWidget(self.objectViewGroupComboBox)
            self.objectViewGroupComboBoxWidget.setZValue(1)
            self.scene.addItem(self.objectViewGroupComboBoxWidget)
            self.objectViewGroupComboBox.activated.connect(lambda index: self.selectGroupname(index))
            
            self.labelRoot = QGraphicsTextItem('Root: ')
            MyFunctions.setFontForUI(self.labelRoot, 17)
            self.scene.addItem(self.labelRoot)
            self.lineEditRoot = QLineEdit(self.INITROOTPATH)
            self.objectViewLineEditRootWidget = QGraphicsProxyWidget()
            self.objectViewLineEditRootWidget.setWidget(self.lineEditRoot)
            self.scene.addItem(self.objectViewLineEditRootWidget)
            
            self.labelObj = QGraphicsTextItem('Object: ')
            MyFunctions.setFontForUI(self.labelObj, 17)
            self.scene.addItem(self.labelObj)
            self.lineEditObj = QLineEdit(self.INITIALPATH)
        
            self.objectViewLineEditObjWidget = QGraphicsProxyWidget()
            self.objectViewLineEditObjWidget.setWidget(self.lineEditObj)
            self.scene.addItem(self.objectViewLineEditObjWidget)
        
            self.btnupdate = QPushButton('OK')
            self.objectViewBtnupdateWidget = QGraphicsProxyWidget()
            self.objectViewBtnupdateWidget.setWidget(self.btnupdate)
            self.scene.addItem(self.objectViewBtnupdateWidget)
            
            self.btnload = QPushButton('...')
            self.objectViewBtnLoadWidget = QGraphicsProxyWidget()
            self.objectViewBtnLoadWidget.setWidget(self.btnload)
            self.scene.addItem(self.objectViewBtnLoadWidget)
 
            self.lineEditObj.textChanged.connect(self.setObjPath)
            self.btnload.clicked.connect(self.chooseObjPath)
            self.btnupdate.clicked.connect(self.confirmObjPath)
    
            self.labelViewmode = QGraphicsTextItem('View Mode:')
            MyFunctions.setFontForUI(self.labelViewmode, 17)
            self.scene.addItem(self.labelViewmode)
            self.viewmodeCombobox = QComboBox()
            self.viewmodeCombobox.addItem('Demo')
            self.viewmodeCombobox.addItem('Practice')
            self.viewmodeWidget = QGraphicsProxyWidget()
            self.viewmodeWidget.setWidget(self.viewmodeCombobox)
            self.scene.addItem(self.viewmodeWidget)
            self.viewmodeCombobox.activated.connect(lambda index: self.selectViewMode(index))
            
            self.nextPBtn = QPushButton('Explain')
            MyFunctions.setFontForUI(self.nextPBtn, 25)
            proxyWidget = QGraphicsProxyWidget()
            proxyWidget.setWidget(self.nextPBtn)
            proxyWidget.setZValue(1)
            self.scene.addItem(proxyWidget)
            self.nextPBtn.setStyleSheet("background-color: #328930")
            self.nextPBtn.clicked.connect(self.explainAnswer)
            self.interfaceItems.add(self.nextPBtn)
            self.interfaceItems.add(proxyWidget)
            
            self.detailPBtn = QPushButton('Explain')
            MyFunctions.setFontForUI(self.detailPBtn, 25)
            proxyWidget = QGraphicsProxyWidget()
            proxyWidget.setWidget(self.detailPBtn)
            proxyWidget.setZValue(1)
            self.scene.addItem(proxyWidget)
            self.detailPBtn.setStyleSheet("background-color: #328930")
            self.interfaceItems.add(self.detailPBtn)
            self.interfaceItems.add(proxyWidget)
            self.detailPBtn.clicked.connect(self.detailExplainQues)
            
            self.interfaceItems.add(self.labelRoot)
            self.interfaceItems.add(self.lineEditRoot)
            self.interfaceItems.add(self.labelObj)
            self.interfaceItems.add(self.lineEditObj)
            self.interfaceItems.add(self.btnload)
            self.interfaceItems.add(self.btnupdate)
            
            self.interfaceItems.add(self.labelGroup)
            self.interfaceItems.add(self.objectViewGroupComboBox)
            self.interfaceItems.add(self.objectViewGroupComboBoxWidget)
            self.interfaceItems.add(self.labelUser)
            self.interfaceItems.add(self.objectViewuserComboBox)
            self.interfaceItems.add(self.objectViewUserComboBoxWidget)
            self.interfaceItems.add(self.objectViewLineEditObjWidget)
            self.interfaceItems.add(self.objectViewBtnupdateWidget)
            self.interfaceItems.add(self.objectViewBtnLoadWidget)
            self.interfaceItems.add(self.objectViewLineEditRootWidget)
            self.interfaceItems.add(self.labelViewmode)
            self.interfaceItems.add(self.viewmodeWidget)
            
            startX, startY = 10, 10
            
            xinter = self.labelObj.boundingRect().width()
            ratio = 0.25
            
            self.labelViewmode.setPos(startX, startY)
            self.viewmodeCombobox.setGeometry(QRect(int(startX+self.labelViewmode.boundingRect().width()), int(startY), 
                                            self.viewmodeCombobox.geometry().width(), self.viewmodeCombobox.geometry().height()))
            startY += self.labelViewmode.boundingRect().height()
            self.labelRoot.setPos(startX, startY-ratio*self.lineEditRoot.geometry().height())
            self.lineEditRoot.setGeometry(QRect(int(startX+xinter), int(startY),
                                               self.lineEditRoot.geometry().width(), self.lineEditRoot.geometry().height()))
            startY+=self.labelRoot.boundingRect().height()
            self.labelObj.setPos(startX, startY-ratio*self.lineEditRoot.geometry().height())
            self.lineEditObj.setGeometry(QRect(int(startX+xinter), int(startY),
                                               self.lineEditObj.geometry().width(), self.lineEditObj.geometry().height()))
            self.btnload.setGeometry(QRect(int(self.lineEditObj.geometry().x()+self.lineEditObj.geometry().width()+5), int(startY),
                                       self.btnload.geometry().width(), self.lineEditObj.geometry().height()))
            self.btnupdate.setGeometry(QRect(int(self.btnload.geometry().x()+self.btnload.geometry().width()+5), int(startY),
                                       self.btnupdate.geometry().width(), self.btnload.geometry().height()))
            startY += self.labelObj.boundingRect().height()
            self.labelUser.setPos(startX, startY-ratio*self.objectViewuserComboBox.geometry().height())
            self.objectViewuserComboBox.setGeometry(QRect(int(startX+xinter), int(startY),
                            self.objectViewuserComboBox.geometry().width(), self.objectViewuserComboBox.geometry().height()))
            self.labelGroup.setPos(int(self.objectViewuserComboBox.pos().x()+
                                   self.objectViewuserComboBox.geometry().width()),
                                   int(startY-ratio*self.objectViewGroupComboBox.geometry().height()))
            self.objectViewGroupComboBox.setGeometry(QRect(int(self.labelGroup.pos().x()+
                            self.labelGroup.boundingRect().width()),
                            int(startY),
                            self.objectViewGroupComboBox.geometry().width(),
                            self.objectViewGroupComboBox.geometry().height()))
    
    def selectViewMode(self, index):
        self.main.explainTextEdit.clear()
        self.nextPBtn.setVisible(index == 0)
        if index == 0:
            self.main.ui.viewSplitter.insertWidget(1, self.main.explainTextEditWidget)
            self.practiceQuesScroll.hide()
            self.main.explainTextEditWidget.show()
        if index == 1:
            self.main.ui.viewSplitter.insertWidget(1, self.practiceQuesScroll)
            self.practiceQuesScroll.show()
            self.main.explainTextEditWidget.hide()
            self.resetAnimatedItems()
        self.main.changeViewSizeForSeparateView()
        self.explainAnswer()
                     
    def setObjPath(self):
        if self.fromFileDialog:
            self.objPath = self.fileDialog.selectedFiles
            self.lineEditObj.setText(self.objPath)
            self.fromFileDialog = False
        else:
            self.objpath = str(self.lineEditObj.text())
            
    def chooseObjPath(self):
        pattern = re.compile('^(\s)*$')
        if self.main.root_dir == "" and re.match(pattern, str(self.lineEditRoot.text())):
            QMessageBox.critical(self.main, '', 'Please import a policy file or set a root directory!')
            return
        self.fileDialog.setDirectory(self.lineEditRoot.text())
        self.fileDialog.show()
        self.fromFileDialog = True

    def confirmObjPath(self):
        self.setObjPath()
        pattern = re.compile('^(\s)*$')
        if self.main.root_dir == "" and re.match(pattern, str(self.lineEditRoot.text())):
            QMessageBox.critical(self.main, '', 'Please import a policy file or set a root directory!')
            return
        if self.main.root_dir == "":
            self.main.initParam()
            self.main.root_dir = str(self.lineEditRoot.text())
            self.main.root_dir = re.sub('/+', '/', self.main.root_dir)
            self.main.root_dir.replace('\n', '')
            self.main.root_dir.replace('\t', '')
            if self.main.root_dir[-1] == ' ':
                self.main.root_dir = self.main.root_dir[:-1]
            self.main.regenerateSpecInfo(None)
        self.objPath = str(self.lineEditObj.text())
        self.objPath.replace('\n', '')
        self.objPath.replace('\t', '')
        if re.match(pattern, self.objPath):
            QMessageBox.critical(self.main, '', 'Please set the object directory!')
            return
        self.startup(self.objPath)
        self.updateLayout()
       
    def getGroupForUser(self, username):
        groups = set()
        if self.main.user_group_sys_mat:
            if username in self.main.user_group_sys_mat.keys():
                import subprocess
                # Fixed: Handle subprocess output which returns bytes in Python 3
                groups_output = subprocess.Popen(["groups", username], 
                          stdout=subprocess.PIPE).communicate()[0]
                # Decode bytes to string and split
                groups_str = groups_output.decode('utf-8') if isinstance(groups_output, bytes) else str(groups_output)
                groups = groups_str.split()
        elif self.main.user_group_mat:
            if username in self.main.user_group_mat.keys():
                groups = self.main.user_group_mat[username]
        elif username == self.ALLUSERTEXT:
                groups = set(self.main.groupSysList) | set(self.main.groupSpecList)
        # Fixed: Handle bytes conversion in join
        txt = ','.join(g.decode('utf-8') if isinstance(g, bytes) else str(g) for g in groups)
        return txt, groups
    
    def setGroupForUserComboBox(self, index):
        username = str(self.objectViewuserComboBox.itemText(index))
        txt, groups=self.getGroupForUser(username)
        self.addGroup2ComboBox(groups)
        groupname = str(self.objectViewGroupComboBox.itemText(0))
        groups = set([groupname])
        return username, groups
    
    def practiceShowReasoning(self):
        if self.checkedAnswer:
            if self.ANIMA_STOP_STEP-1 == 0:
                self.main.explainTextEdit.appendPlainText('The meaning of permission of an object is as below:')
                self.main.explainTextEdit.appendPlainText('-'*10)
                self.main.explainTextEdit.appendPlainText('Permissions for Regular File')
                self.main.explainTextEdit.appendPlainText('-'*10)
                self.main.explainTextEdit.appendPlainText('- Read: View the content of the file.')
                self.main.explainTextEdit.appendPlainText('- Write: Allow changes to the content of the file.')
                self.main.explainTextEdit.appendPlainText('- Execute: Allow running the file as a program.')
                self.main.explainTextEdit.appendPlainText('-'*10)
                self.main.explainTextEdit.appendPlainText('Permissions for Directory')
                self.main.explainTextEdit.appendPlainText('-'*10)
                self.main.explainTextEdit.appendPlainText('- Read: List the files/directories under the directory.')
                self.main.explainTextEdit.appendPlainText('- Write: Allow creating/removing files/directories under the directory.')
                self.main.explainTextEdit.appendPlainText('- Execute: Allow "pass through" the directory and perform allowed operations on files/directories beneath.')
                self.main.explainTextEdit.appendPlainText('-'*10)
                self.main.explainTextEdit.appendPlainText('Therefore, to get to the files/directories under a directory, the execute permission is needed.')
                self.main.explainTextEdit.appendPlainText('')
            else:
                user = str(self.objectViewuserComboBox.currentText())
                group  = str(self.objectViewGroupComboBox.currentText())
                node = self.dirNodes[self.nodeIndex]
                node.highlight = True
                node.passedHiglight = False
                permnode = node.permInfo
                txt = str(permnode.toPlainText()).split('\n')
                fuser, fgroup = txt[0], txt[1]
                fuser = fuser[fuser.find('(')+1:fuser.find(')')]
                fgroup = fgroup[fgroup.find('(')+1:fgroup.find(')')]
                if self.sec == 0:
                    self.main.explainTextEdit.appendPlainText('%s. %s: user(%s), group(%s)'%((i+1), self.dirNodes[i].dirpath, fuser, fgroup))
                perms = txt[-1]
                perms = perms[perms.find('(')+1:perms.find(')')]
                uperms = perms[:3]
                gperms = perms[3:6]
                operms = perms[6:]
                usedBits = self.bitsIndexList[self.nodeIndex].index
                for i in range(3):
                    if i == 0:
                        self.main.explainTextEdit.appendPlainText('- Check user bits:')
                        if 's' in uperms or 'S' in uperms:
                            self.main.explainTextEdit.appendPlainText('  The setUID bit is on. Therefore, any user can run as the user owner of the object.')
                            self.main.explainTextEdit.appendPlainText('  That is, the effective user is "%s".'%fuser)
                            usedBits = 0
                        else:
                            self.main.explainTextEdit.appendPlainText('  The user owner of the object is "%s".'%fuser)
                            self.main.explainTextEdit.appendPlainText('  The effective user is "%s".'%user)
                        if usedBits == i:
                            self.main.explainTextEdit.appendPlainText('  The user bits "%s" are used for permission evaluation.'%uperms)
                            self.main.explainTextEdit.appendPlainText('')
                            return
                        else:
                            self.main.explainTextEdit.appendPlainText('  The effective user is not the user owner of the object...')
                            self.main.explainTextEdit.appendPlainText('-'*10)
                    elif i == 1:
                        self.main.explainTextEdit.appendPlainText('- Check group bits:')
                        if 's' in gperms or 'S' in gperms:
                            self.main.explainTextEdit.appendPlainText('  The setGID bit is on. Therefore, user from any group can run as the group owner of the object.')
                            self.main.explainTextEdit.appendPlainText('  That is, the effective group is "%s".'%fgroup)
                            usedBits = 1
                        else:
                            self.main.explainTextEdit.appendPlainText('  The group owner of the object is "%s".'%fgroup)
                            self.main.explainTextEdit.appendPlainText('  The effective group is "%s".'%group)
                        if usedBits == i:
                            self.main.explainTextEdit.appendPlainText('  The group bits "%s" are used for permission evaluation.'%gperms)
                            self.main.explainTextEdit.appendPlainText('')
                            return
                        else:
                            self.main.explainTextEdit.appendPlainText('  The effective group is not the group owner of the object...')
                            self.main.explainTextEdit.appendPlainText('-'*10)
                else:
                    self.main.explainTextEdit.appendPlainText('- Since neither the user or group bits are used, the other bits "%s" are applied:'%operms)
            self.checkedAnswer = False
               
    def detailExplainQues(self):
        for i in range(len(self.bitsIndexList)):
            node = self.bitsIndexList[i]
            dirnode = self.dirNodes[i]
            permnode = dirnode.permInfo
            if i <= (self.main.animationStep-1)/2:
                node.setVisible(True)
                self.setHighlightSec(dirnode, str(permnode.toPlainText()), node.index)
            else:
                self.bitsIndexList[i].setVisible(False)
                self.setHighlightSec(dirnode, str(permnode.toPlainText()), -1)
                
    def explainAnswer(self):
        if not self.dirNodes:
            QMessageBox.critical(self.main, '', 'Please import a policy file or set an object directory!')
            return
        if self.viewmodeCombobox.currentText() == 'Demo':
            self.totalAnimationSteps = len(self.dirNodes)+3
            if str(self.nextPBtn.text()) == 'End':
                self.main.explainTextEdit.clear()
                self.nextPBtn.setText('Explain')
                self.nextPBtn.setStyleSheet('QPushButton {background-color: #328930;}')
                return
            if str(self.nextPBtn.text()) == 'Explain':
                self.resetAnimatedItems()
                self.nextPBtn.setText('Next')
                self.nextPBtn.setStyleSheet('QPushButton {background-color: yellow;}')
            self.onAnimateObjectView_Demo(self.bitsIndexList)
            if self.main.animationStep == self.ANIMA_STOP_STEP:
                self.nextPBtn.setText('End')
                self.nextPBtn.setStyleSheet('QPushButton {background-color: red;}')
        else:
            '''practice mode'''
            if self.main.animationStep == 2*len(self.dirNodes):
                self.resetAnimatedItems()
            self.onAnimateObjectView_Practice(self.bitsIndexList)
        self.main.animationStep += 1
    
    def generateQuesKeys(self):
        numQues = 2*len(self.dirNodes)
        for i in range(numQues):
            nodeIndex = i//2
            if i % 2 == 0:
                '''The number representing the applied bits is stored as the keys, it is the index of radio buttons as well'''
                if nodeIndex < len(self.bitsIndexList):
                    self.practiceKeys.append(self.bitsIndexList[nodeIndex].index)
                else:
                    self.practiceKeys.append(-1)
            else:
                '''The number representing r w x are stored in the permset'''
                '''the key contains the correct btn to choose'''
                node = self.dirNodes[nodeIndex]
                if nodeIndex < len(self.bitsIndexList):
                    usedBits = self.bitsIndexList[nodeIndex].index
                    permnode = node.permInfo
                    txt = str(permnode.toPlainText()).split('\n')
                    perms = txt[-1]
                    perms = perms[perms.find('(')+1:perms.find(')')]
                    startP = usedBits*3
                    usedPerms = perms[startP:startP+3]
                else:
                    usedPerms = ''
                if i < numQues-2:
                    '''only check for execute'''
                    if ('x' in usedPerms) or ('s' in usedPerms) or ('t' in usedPerms):
                        self.practiceKeys.append(0)
                    else:
                        self.practiceKeys.append(1)
                else:
                    permset = set()
                    if 'r' in usedPerms:
                        permset.add(0)
                    if 'w' in usedPerms:
                        permset.add(1)
                    if ('x' in usedPerms) or ('s' in usedPerms) or ('t' in usedPerms):
                        permset.add(2)
                    if self.practicePermCheckKeys[-1] in permset:
                        self.practiceKeys.append(0)
                    else:
                        self.practiceKeys.append(1)

            

            
    def createQuestionText(self, qID):
        user = str(self.objectViewuserComboBox.currentText())
        object = self.dirNodes[qID//2].dirpath
        if qID % 2 == 0:
            qText = 'Question %s. Which bits are applied for the access of the user "%s" to the highlighted object?'%(qID+1, user)
        else:
            import random
            operation = random.randint(0,2)
            if self.isFileCheck(object):
                operationText = self.PRACTICE_QUES_PERM_OPERATIONS[0][operation]
            else:
                if qID//2 != len(self.dirNodes)-1:
                    operation = 2
                self.practicePermCheckKeys.append(operation)
                operationText = self.PRACTICE_QUES_PERM_OPERATIONS[1][operation]
            qText = 'Question %s. Will the user "%s" be able to %s?'%(qID+1, user, operationText)
        return self.createQuestionWidget(qID, qText)
        
    def createQuestionWidget(self, qID, questionText):
        question = QWidget(self.practiceQuesWidget)
        wlayout = QVBoxLayout()
        questionTextLabel = QLabel(questionText, question)
        questionTextLabel.setWordWrap(True)
        wlayout.addWidget(questionTextLabel)
        buttonGroup = QButtonGroup(question)
        buttons = []
        qType = qID%2
        if qType==0:
            numButtons = 3
        else:
            numButtons = 2
        for i in range(numButtons):
            btn = QRadioButton(self.PRACTICE_QUES_CHOICES[qType][i])
            wlayout.addWidget(btn)
            buttonGroup.addButton(btn)
            buttons.append(btn)
        self.practiceChoices.append(buttons)
        self.practiceButtonGroups.append(buttonGroup)
        buttonGroup.buttonClicked.connect(lambda clickedbtn: self.selectPracticeAnswer(clickedbtn))
        answerLabel = QLabel('test', question)
        answerLabel.setObjectName('check')
        wlayout.addWidget(answerLabel)
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setFrameShadow(QFrame.Shadow.Sunken)
        wlayout.addWidget(line)
        question.setLayout(wlayout)
        question.adjustSize()
        self.practiceQuesLayout.addWidget(question)
        return question
            
            
    def createPracticeModeInterface(self):
        self.practiceQuestionWidgets = []
        self.practiceChoices = []
        self.practiceButtonGroups = []
        self.practiceAnswers = []
        self.practiceKeys = []
        self.practicePermCheckKeys = []
        self.practiceQuesWidget = QWidget()
        self.practiceQuesScroll = QScrollArea()
        self.practiceQuesScroll.setWidget(self.practiceQuesWidget)
        self.practiceQuesScroll.setWidgetResizable(True)
        self.practiceQuesLayout = QVBoxLayout(self.practiceQuesWidget)
        for i in range(len(self.dirNodes)):
            self.practiceQuestionWidgets.append(self.createQuestionText(2*i))
            self.practiceQuestionWidgets.append(self.createQuestionText(2*i+1))
        self.practiceQuesLayout.addStretch(1)
        self.generateQuesKeys()
                    
    def uncheckPracticeRadioButtonsAndAnwserCheck(self):
        for group in self.practiceButtonGroups:
            checked = group.checkedButton()
            if checked:
                group.setExclusive(False)
                checked.setChecked(False)
                group.setExclusive(True)
        for q in self.practiceQuestionWidgets:
            label = q.findChild(QLabel, 'check')
            label.setText('')
        
    def resetAnimatedItems(self):
        username = str(self.objectViewuserComboBox.currentText())
        groupname = str(self.objectViewGroupComboBox.currentText())
        groups = set([groupname])
        self.bitsIndexList = self.reanalyze(username, groups)
        if str(self.viewmodeCombobox.currentText()) == 'Practice':
            self.main.explainTextEdit.appendPlainText('Please answer the following question (use the "Next" button to navigate):')
            self.main.explainTextEdit.appendPlainText('')
            self.totalAnimationSteps = len(self.dirNodes)+1
            self.nextPBtn.setText('Next')
            self.nextPBtn.setStyleSheet('QPushButton {background-color: yellow;}')
        self.main.animationStep = 0
        self.sec = 0
        self.nodeIndex = 0
        self.main.explainTextEdit.clear()
        self.detailPBtn.setVisible(False)
        self.uncheckPracticeRadioButtonsAndAnwserCheck()
        for i in self.dirNodes:
            i.highlight = False
            i.passedHighlight = False
        if self.bitsIndexList:
            for i in self.bitsIndexList:
                i.setVisible(False)
            

    def selectPracticeAnswer(self, clickedbtn):
        questionW = clickedbtn.parent()
        questionID = self.practiceQuestionWidgets.index(questionW)
        checklabel = questionW.findChild(QLabel, 'check')
        btnIndex = self.practiceChoices[questionID].index(clickedbtn)
        if btnIndex==self.practiceKeys[questionID]:
            checklabel.setStyleSheet("QLabel {font-weight: bold; color : green; }")
            checklabel.setText('Correct.')
        else:
            checklabel.setStyleSheet("QLabel {font-weight: bold; color : red; }")
            checklabel.setText('Incorrect.')
        self.nextPBtn.setVisible(True)  
        self.detailPBtn.setVisible(True)
        self.checkedAnswer = True      
    
    def onAnimateObjectView_Practice(self, bitsIndexList):
        for e in self.practiceQuestionWidgets:
            e.hide()
        self.practiceQuestionWidgets[0].show()
        for i in range(self.main.animationStep):
            self.practiceQuestionWidgets[i+1].show()
        self.practiceQuesWidget.adjustSize()
        self.practiceQuesScroll.ensureVisible(0,self.practiceQuesWidget.geometry().height(),0,0)
        self.nextPBtn.setVisible(False)
        self.detailPBtn.setVisible(False)
        self.checkedAnswer = False
        for i in self.dirNodes:
            i.highlight = False
        self.dirNodes[self.main.animationStep//2].highlight = True
        for i in range(len(self.bitsIndexList)):
            dirnode = self.dirNodes[i]
            permnode = dirnode.permInfo
            self.bitsIndexList[i].setVisible(False)
            self.setHighlightSec(dirnode, str(permnode.toPlainText()), -1)
            
    def onAnimateObjectView_Demo(self, bitsIndexList):
        self.main.explainTexteditHighlightLastLines()
        if self.main.animationStep == 0:
            self.main.explainTextEdit.appendPlainText('To access an object with certain permissions, the user should be able to bypass all directories along the path from the root to the object of interest. '
                                                      + 'This requires the e(x)ecute permissions of the user to the directories.')
            self.main.explainTextEdit.appendPlainText('')
        elif self.main.animationStep == 1:
            numLevel = len(self.dirNodes)
            self.main.explainTextEdit.appendPlainText('In this case, we check the following directories:')
            for i in range(numLevel-1):
                self.main.explainTextEdit.appendPlainText(self.dirNodes[i].dirpath) 
            self.main.explainTextEdit.appendPlainText('')
            self.sec = 0
            self.nodeIndex = 0
        elif self.main.animationStep<self.totalAnimationSteps-2:
            i = self.nodeIndex
            if i==0 and self.sec == 0:
                self.main.explainTextEdit.appendPlainText('Access is determined by first identifying which set of permission bits to apply: owner, group, or other. The applicable bits are determined using the effective user and group...\n')
            '''check ancestor directories'''
            user = str(self.objectViewuserComboBox.currentText())
            group  = str(self.objectViewGroupComboBox.currentText())
            node = self.dirNodes[i]
            node.highlight = True
            node.passedHiglight = False
            permnode = node.permInfo
            txt = str(permnode.toPlainText()).split('\n')
            fuser, fgroup = txt[0], txt[1]
            fuser = fuser[fuser.find('(')+1:fuser.find(')')]
            fgroup = fgroup[fgroup.find('(')+1:fgroup.find(')')]
            if self.sec == 0:
                self.main.explainTextEdit.appendPlainText('%s. %s: user(%s), group(%s)'%((i+1), self.dirNodes[i].dirpath, fuser, fgroup))
            perms = txt[-1]
            perms = perms[perms.find('(')+1:perms.find(')')]
            uperms = perms[:3]
            gperms = perms[3:6]
            operms = perms[6:]
            usedBits = bitsIndexList[i].index
            passed = False
            self.setHighlightSec(node, str(permnode.toPlainText()), self.sec)
            if self.sec==0:
                self.main.explainTextEdit.appendPlainText('- Check user bits:')
                if 's' in uperms or 'S' in uperms:
                    self.main.explainTextEdit.appendPlainText('  The setUID bit is on. Therefore, any user can run as the user owner of the object.')
                    self.main.explainTextEdit.appendPlainText('  That is, the effective user is "%s".'%fuser)
                    usedBits = 0
                else:
                    self.main.explainTextEdit.appendPlainText('  The user owner of the object is "%s".'%fuser)
                    self.main.explainTextEdit.appendPlainText('  The effective user is "%s".'%user)
                if usedBits == self.sec:
                    self.main.explainTextEdit.appendPlainText('  The user bits "%s" are used for permission evaluation.'%uperms)
                    self.main.explainTextEdit.appendPlainText('  E(x)ecute permission is required to pass through a directory.')
                    if 's' in uperms or 'x' in uperms:
                        self.main.explainTextEdit.appendPlainText('  -- User "%s" is able to pass this level of directory as the "x" permission is set.'%user)
                        passed = True
                    else:
                        self.main.explainTextEdit.appendPlainText('  -- User "%s" cannot pass this level of directory due to the lack of the "x" permission.'%user)
                else:
                    self.main.explainTextEdit.appendPlainText('  The effective user is not the user owner of the object...')
                    self.main.explainTextEdit.appendPlainText('-'*10)
            elif self.sec == 1:
                self.main.explainTextEdit.appendPlainText('- Check group bits:')
                if 's' in gperms or 'S' in gperms:
                    self.main.explainTextEdit.appendPlainText('  The setGID bit is on. Therefore, user from any group can run as the group owner of the object.')
                    self.main.explainTextEdit.appendPlainText('  That is, the effective group is "%s".'%fgroup)
                    usedBits = 1
                else:
                    self.main.explainTextEdit.appendPlainText('  The group owner of the object is "%s".'%fgroup)
                    self.main.explainTextEdit.appendPlainText('  The effective group is "%s".'%group)
                if usedBits == self.sec:
                    self.main.explainTextEdit.appendPlainText('  The group bits "%s" are used for permission evaluation.'%gperms)
                    self.main.explainTextEdit.appendPlainText('  E(x)ecute permission is required to pass through a directory.')
                    if 's' in gperms or 'x' in gperms:
                        self.main.explainTextEdit.appendPlainText('  -- User "%s" is able to pass this level of directory as the "x" permission is set.'%user)
                        passed = True
                    else:
                        self.main.explainTextEdit.appendPlainText('  -- User "%s" cannot pass this level of directory due to the lack of the "x" permission.'%user)
                else:
                    self.main.explainTextEdit.appendPlainText('  The effective group is not the group owner of the object...')
                    self.main.explainTextEdit.appendPlainText('-'*10)
            else:
                self.main.explainTextEdit.appendPlainText('- Since neither the user or group bits are used, the other bits "%s" are applied:'%operms)
                if 't' in operms or 'x' in operms:
                    self.main.explainTextEdit.appendPlainText('  -- User "%s" is able to pass this level of directory as the "x" permission is set.'%user)
                    passed = True
                else:
                    self.main.explainTextEdit.appendPlainText('  -- User "%s" cannot pass this level of directory due to the lack of the "x" permission.'%user)
            if usedBits == self.sec:
                self.nodeIndex += 1
                self.sec = 0
                bitsIndexList[i].setVisible(True)
                if not passed:
                    self.main.explainTextEdit.appendPlainText('- Conclusion:')
                    self.main.explainTextEdit.appendPlainText('  User "%s" does not have access to object "%s".'%(user, self.dirNodes[-1].dirpath))
                    self.main.explainTextEdit.appendPlainText('')
                    self.main.animationStep = self.ANIMA_STOP_STEP
                else:
                    self.main.explainTextEdit.appendPlainText('')
                    node.passedHiglight = True
                    return
            else:
                self.main.animationStep -= 1
                self.sec+=1
            ''''''
        elif self.main.animationStep == self.totalAnimationSteps-2:
            self.main.explainTextEdit.appendPlainText('Now, the user is able to reach the object of interest.')
            self.main.explainTextEdit.appendPlainText('-'*10)
            self.main.explainTextEdit.appendPlainText('Permissions for Regular File')
            self.main.explainTextEdit.appendPlainText('-'*10)
            self.main.explainTextEdit.appendPlainText('- Read: View the content of the file.')
            self.main.explainTextEdit.appendPlainText('- Write: Allow changes to the content of the file.')
            self.main.explainTextEdit.appendPlainText('- Execute: Allow running the file as a program.')
            self.main.explainTextEdit.appendPlainText('-'*10)
            self.main.explainTextEdit.appendPlainText('Permissions for Directory')
            self.main.explainTextEdit.appendPlainText('-'*10)
            self.main.explainTextEdit.appendPlainText('- Read: List the files/directories under the directory.')
            self.main.explainTextEdit.appendPlainText('- Write: Allow creating/removing files/directories under the directory.')
            self.main.explainTextEdit.appendPlainText('- Execute: Allow "pass through" the directory and perform allowed operations on files/directories beneath.')
            self.main.explainTextEdit.appendPlainText('-'*10)
            self.main.explainTextEdit.appendPlainText('')
            self.sec = 0
        elif self.main.animationStep == self.totalAnimationSteps-1:
            self.checkObjInterestPerm(bitsIndexList)
            
    def checkObjInterestPerm(self, bitsIndexList):
        user = str(self.objectViewuserComboBox.currentText())
        group  = str(self.objectViewGroupComboBox.currentText())
        node = self.dirNodes[-1]
        node.highlight = True
        node.passedHiglight = False
        permnode = node.permInfo
        txt = str(permnode.toPlainText()).split('\n')
        fuser, fgroup = txt[0], txt[1]
        fuser = fuser[fuser.find('(')+1:fuser.find(')')]
        fgroup = fgroup[fgroup.find('(')+1:fgroup.find(')')]
        if self.sec == 0:
            self.main.explainTextEdit.appendPlainText('%s. %s: user(%s), group(%s)'%(len(self.dirNodes), self.dirNodes[-1].dirpath, fuser, fgroup))
        perms = txt[-1]
        perms = perms[perms.find('(')+1:perms.find(')')]
        uperms = perms[:3]
        gperms = perms[3:6]
        operms = perms[6:]
        usedBits = bitsIndexList[-1].index
        appliedperms = None
        self.setHighlightSec(node, str(permnode.toPlainText()), self.sec)
        if self.sec==0:
            self.main.explainTextEdit.appendPlainText('- Check user bits:')
            if 's' in uperms or 'S' in uperms:
                self.main.explainTextEdit.appendPlainText('  The setUID bit is on. Therefore, any user can run as the user owner of the object.')
                self.main.explainTextEdit.appendPlainText('  That is, the effective user is "%s".'%fuser)
                usedBits = 0
            else:
                self.main.explainTextEdit.appendPlainText('  The user owner of the object is "%s".'%fuser)
                self.main.explainTextEdit.appendPlainText('  The effective user is "%s".'%user)
            if usedBits == self.sec:
                self.main.explainTextEdit.appendPlainText('  The user bits "%s" are used for permission evaluation.'%uperms)
                appliedperms = uperms
            else:
                self.main.explainTextEdit.appendPlainText('  The effective user is not the user owner of the object...')
                self.main.explainTextEdit.appendPlainText('-'*10)
        elif self.sec == 1:
            self.main.explainTextEdit.appendPlainText('- Check group bits:')
            if 's' in gperms or 'S' in gperms:
                self.main.explainTextEdit.appendPlainText('  The setGID bit is on. Therefore, user from any group can run as the group owner of the object.')
                self.main.explainTextEdit.appendPlainText('  That is, the effective group is "%s".'%fgroup)
                usedBits = 1
            else:
                self.main.explainTextEdit.appendPlainText('  The group owner of the object is "%s".'%fgroup)
                self.main.explainTextEdit.appendPlainText('  The effective group is "%s".'%group)
            if usedBits == self.sec:
                self.main.explainTextEdit.appendPlainText('  The group bits "%s" are used for permission evaluation.'%gperms)
                appliedperms = gperms
            else:
                self.main.explainTextEdit.appendPlainText('  The effective group is not the group owner of the object...')
                self.main.explainTextEdit.appendPlainText('-'*10)
        else:
            self.main.explainTextEdit.appendPlainText('- Since neither the user or group bits are used, the other bits "%s" are applied:'%operms)
            appliedperms = operms
        if appliedperms:
            bitsIndexList[-1].setVisible(True)
            self.main.explainTextEdit.appendPlainText('- Conclusion:')
            if appliedperms == '---':
                self.main.explainTextEdit.appendPlainText('  User "%s" does not have access to object "%s".'%(user, self.dirNodes[-1].dirpath))
            else:
                self.main.explainTextEdit.appendPlainText('  User "%s" has "%s" permission to object "%s".'%(user, appliedperms, self.dirNodes[-1].dirpath))
                node.passedHiglight = True
            self.main.explainTextEdit.appendPlainText('')
            self.main.animationStep = self.ANIMA_STOP_STEP
        else:
            self.main.animationStep -= 1
            self.sec+=1
            
    def reanalyze(self, username, groups):
        self.resetAnalysisNodes()
        sectionList = []
        if username == self.ALLUSERTEXT:#all users
            self.getPermForAllGrid()
        else:#single user
            dirpath = ''
            for i in self.objList:
                dirpath += i
            fileuser, filegroup, uid, gid = PermissionChecker.getFileUserAndGroup(dirpath, None, self.scene)
            if username == fileuser:#user bit applies
                section = 0
            elif filegroup in groups:#group bit applies
                section = 1
            else:#other bit applies
                section = 2
            userList = self.createInfoForOneUser(username, sectionList, section)
            if userList==[]:
                self.msg.setPlainText('No user has access to the object.')
            sectionList.append(userList)
            self.checkgridNodes = [[], [], []]
            self.checkgridNodes[section] = sectionList
        self.updateLayout()
        return userList
        
    def selectGroupname(self,index):
        username = str(self.objectViewuserComboBox.currentText())
        txt = str(self.objectViewGroupComboBox.itemText(index))
        if txt == self.ALLGROUPTEXT:
            groups = self.getGroupForUser(username)[1]
        else:
            groups = set([txt])
        self.bitsIndexList = self.reanalyze(username, groups)
        self.resetAnimatedItems()
    
    def selectUsername(self, index):
        username, groups = self.setGroupForUserComboBox(index)
        self.bitsIndexList = self.reanalyze(username, groups)
        self.resetAnimatedItems()
    
    def setHighlightPerm(self, node, colorstr='Red'):
        permstr = str(node.permInfo.toPlainText())
        permset = permstr.split('\n')
        permsHtml = ''
        indexStep = 3
        index = permset[-1].rfind('(')+1
        if permstr == 'None':
            indexStart = 0
            indexStep = 4
        for i in range(len(permset)):
            if i<len(permset)-1:
                permsHtml += ('<font color=\"%s\" size="3">%s</font><br>')%(colorstr, permset[i])
            else:
                permsHtml += ('<font color=\"%s\" size="3">%s</font>')%(colorstr, permset[i])
        node.permInfo.setHtml(permsHtml)

    def setHighlightSec(self, node, permstr, section = -1):
        permset = permstr.split('\n')
        permsHtml = ''
        indexStep = 3
        index = permset[-1].rfind('(')+1
        if section == -1:
            indexStart = -1
            indexStep = 0
        elif section == 0:#user
            indexStart = index
        elif section == 1:#group
            indexStart = index+3
        else:#other
            indexStart = index+6
        if permstr == 'None':
            indexStart = 0
            indexStep = 4
        for i in range(len(permset)):
            if i<len(permset)-1:
                if (i==0 and section==0) or (i==1 and section==1):
                    permsHtml += ('<font color=\"Blue\" size="3"><b>%s</b></font><br>')%permset[i]
                else:
                    permsHtml += ('<font color=\"Black\" size="3">%s</font><br>')%permset[i]
            else:
                permsHtml += ('<font color=\"Black\" size="3">%s</font><font color=\"Blue\" size="3"><b>%s</b></font><font color=\"Black\" size="3">%s</font>')\
                            %(permset[i][:indexStart], permset[i][indexStart:indexStart+indexStep], permset[i][indexStart+indexStep:])
        node.permInfo.setHtml(permsHtml)
    
    def isFileCheck(self, filename):
        import os
        if os.path.exists(filename):
            return os.path.isfile(filename)
        else:
            filename = filename.replace(self.main.root_dir, '')
            for k, v in self.main.obj_cred_mat.items():
                if k == filename:
                    return (not v.directory)
        return None
           
    def startup(self, objpath):
        import os
        if self.main.root_dir not in objpath:
            objpath = os.path.normpath(self.main.root_dir+'/'+objpath)
        else:
            objpath = os.path.normpath(objpath)
        self.isFile = self.isFileCheck(self.objPath)
        '''Add title nodes'''
        self.resetScene()
        if self.msg not in self.scene.items():
            self.scene.addItem(self.msg)
        for i in self.textItems:
            if i not in self.scene.items():
                self.scene.addItem(i)
        '''Add object nodes'''
        self.objList = [self.main.root_dir]
        objpath = objpath.replace('\t', '')
        objpath = objpath.replace('\n', '')
        objpath = objpath[len(self.main.root_dir):]
        temp = objpath.split('/')
        temp = [item for item in temp if item != '']
        for t in temp:
            self.objList.append('/'+t)
        dirpath = ''
        for i in range(len(self.objList)):
            dirpath += self.objList[i]
            dirpath=re.sub('/+', '/', dirpath)
            node = FileNode(dirpath, self.objList[i], False, self.main)
            perms = self.getPermInfo(dirpath)
            if perms == None:
                perms = 'None'
            node.permInfo = FilePermNode(node, self.main)
            font = QFont('LucidaGrande', 16)
            node.permInfo.setFont(font)
            self.setHighlightSec(node, perms, -1)
            if i>0:
                node.parent = self.dirNodes[-1]
                self.dirNodes[-1].children.add(node)
                edge = EdgeItem(EdgeItem.FILE_CONN, node.parent, node, self.main)
                self.dirEdges.append(edge)
                if edge not in self.scene.items():
                    self.scene.addItem(edge)
            self.dirNodes.append(node)
            if node not in self.scene.items():
                self.scene.addItem(node)
        '''generate information in grids'''
        self.resetAnimatedItems()
        self.createPracticeModeInterface()
    
    def getPermForAllGrid(self):
        allgroup = True
        currentGroup = str(self.objectViewGroupComboBox.currentText())
        usersInGroup = []
        if currentGroup != self.ALLGROUPTEXT:
            usersInGroup = list(self.getUsersInGroup(currentGroup))
            allgroup = False
        dirpath = ''
        for i in range(len(self.objList)):
            dirpath += self.objList[i]
        for j in range(3):
            sectionList = []
            userList = []
            users = set()
            if j==0:
                fileuser, filegroup, uid, gid = PermissionChecker.getFileUserAndGroup(dirpath, None, self.scene)
                if fileuser == None and uid == -1:
                    return
                if allgroup or fileuser in usersInGroup:
                    users = [fileuser]
            elif j==1:
                '''get users in group'''
                fileuser, filegroup, uid, gid = PermissionChecker.getFileUserAndGroup(dirpath, None, self.scene)
                if filegroup == None and gid == -1:
                    return
                if allgroup or filegroup == currentGroup:
                    users = list(self.getUsersInGroup(filegroup))
            elif j==2:
                '''get users that pass the 'x' requirement for all parent directories'''
                dirpatho = ''
                for k in self.objList:
                    dirpatho += k
                    fileuser, filegroup, uid, gid = PermissionChecker.getFileUserAndGroup(dirpatho, None, self.scene)
                    if fileuser == None and uid == -1:
                        continue
                    if allgroup:
                        users.add(fileuser)
                        users = users.union(self.getUsersInGroup(filegroup))
                    else:
                        if fileuser in usersInGroup:
                            users.add(fileuser)
                        if filegroup == currentGroup:
                            users = users.union(self.getUsersInGroup(filegroup))
                if allgroup:
                    users.add(self.OTHERUSERTEXT)
            usersList = list(users)
            usersList.sort()
            for u in usersList:
                if u in self.previousUsers:
                    continue
                else:
                    self.previousUsers.add(u)
                userList = self.createInfoForOneUser(u, sectionList, j)
                sectionList.append(userList)
            self.checkgridNodes[j] = sectionList
        
    def getUsersInGroup(self, groupname):
        users = set()
        for u, g in self.main.user_group_sys_mat.items():
            if groupname in g:
                users.add(u)
        #for spec
        for u, g in self.main.user_group_mat.items():
            if groupname in g:
                users.add(u)
        return users
                       
    def createInfoForOneUser(self, username, sectionList, permsec = 0):
        filepath = ''
        userList = []
        quitFlag = False
        for i in range(len(self.dirNodes)):
            filepath += self.dirNodes[i].name
            if i==len(self.dirNodes)-1:
                info = self.computePermForGrid(username, filepath, False)
                if username == self.OTHERUSERTEXT:
                    username = '<i>others</i>'
                if info[0] and (quitFlag == False):
                    if permsec == 0:#'user'
                        msg = ('%s:%s')%(username, info[2])
                        node = CheckNode(self.main, '', ('<font color=\"Green\" size="3">%s</font><br>')%(msg))
                    elif permsec == 1:#'group'
                        msg = ('%s:%s')%(username, info[3])
                        node = CheckNode(self.main, '', ('<font color=\"Green\" size="3">%s</font><br>')%(msg))
                    elif permsec == 2:#'other'
                        msg = ('%s:%s')%(username, info[4])
                        node = CheckNode(self.main, '', ('<font color=\"Green\" size="3">%s</font><br>')%(msg))
                    else:
                        msg = ('%s:None')%(username)
                        node = CheckNode(self.main, '', ('<font color=\"Red\" size="3">%s</font><br>')%(msg))
                else:
                    msg = ('%s:None')%(username)
                    node = CheckNode(self.main, '', ('<font color=\"Red\" size="3">%s</font><br>')%(msg))
                node.setTextWidth(300)
                node.setVisible(True)
                node.index = self.getColNum(info[1])
                node.indexuser = len(sectionList) #no. in the users 
                userList.append(node)
                self.clickableCheckNodes.append(node)
                if node not in self.scene.items():
                    self.scene.addItem(node)
            else:
                if not quitFlag:
                    info = self.computePermForGrid(username, filepath, True)
                    if info == None:
                        return []
                    if info[0]:
                        node = CheckNode(self.main, ('<font color=\"Black\" size="3">%s</font><br>')%info[1],
                                          '<font color=\"Green\" size="5">Y</font><br>')
                    else:
                        node = CheckNode(self.main, ('<font color=\"Red\" size="3">%s</font><br>')%info[1], 
                                            '<font color=\"Red\" size="4">N</font><br>')
                        quitFlag = True
                else:
                    node = CheckNode(self.main, '', '')
                node.permInfo = info[1]
                node.index = self.getColNum(info[1])
                node.indexuser = len(sectionList) #no. in the users 
                userList.append(node)               

                if node not in self.scene.items():
                    self.scene.addItem(node)
        return userList
                   
    def getColNum(self, info):
        if '"user" field' in info:
            return 0
        elif '"group" field' in info:
            return 1
        elif '"other" field' in info:
            return 2
          
    def updateLayout(self):
        fontSize = min(0.025*self.main.geometry().width(), 25)
        MyFunctions.setFontForUI(self.ownerTextItem, fontSize)
        MyFunctions.setFontForUI(self.groupTextItem, fontSize)
        MyFunctions.setFontForUI(self.otherTextItem, fontSize)
        
        self.msg.adjustSize()
        self.msg.setTextWidth(0.85*self.main.geometry().width())
        self.msg.setPos(20, self.scene.sceneRect().height()-self.msg.boundingRect().height()-5)
        xinter = self.nextPBtn.geometry().width()
        yinter = self.nextPBtn.geometry().height()
        self.nextPBtn.setGeometry(int(self.scene.sceneRect().width()-10-xinter), int(self.scene.sceneRect().height()-10-yinter), 
                                             xinter, yinter)
        xinter = self.nextPBtn.geometry().width()
        self.detailPBtn.setGeometry(int(self.nextPBtn.pos().x()-xinter-10), int(self.nextPBtn.pos().y()), 
                                      self.nextPBtn.geometry().width(), self.detailPBtn.geometry().height())
        self.msg.setTextWidth(self.detailPBtn.geometry().x())
        self.msg.setPos(20, self.main.scene.sceneRect().height()-self.msg.boundingRect().height()-5)
        pos = self.main.mapToGlobal(QPoint(0,0))
        if self.dirNodes:
            startY = self.objectViewuserComboBox.geometry().height() + self.objectViewuserComboBox.geometry().y() + 20
            self.ownerTextItem.setPos(0.4*self.scene.sceneRect().width(),startY)
            self.groupTextItem.setPos(0.6*self.scene.sceneRect().width(),startY)
            self.otherTextItem.setPos(0.8*self.scene.sceneRect().width(),startY)
            
            intervalY = 0.7/len(self.dirNodes)
            x, y = 0.15, float(startY)/self.scene.sceneRect().height()+0.1#0.2
            for i in range(len(self.dirNodes)):
                self.dirNodes[i].relativeX = x
                self.dirNodes[i].relativeY = y
                self.dirNodes[i].setPos(QPointF(x*self.scene.sceneRect().width(),y*self.scene.sceneRect().height()))
                self.dirNodes[i].setVisible(True)
                y += intervalY
                
            for j in range(3):
                prevk = None
                if self.checkgridNodes[j]!=[]:
                    for k in self.checkgridNodes[j]:#k - userList, self.checkgridNodes[j] - sectionList
                        if k:
                            for i in range(len(self.dirNodes)):
                                if i < len(k):
                                    k[i].relativeX = self.textItems[k[i].index].pos().x()/self.scene.sceneRect().width()
                                    k[i].relativeY = self.dirNodes[i].relativeY
                                    k[i].setPos(QPointF(k[i].relativeX*self.scene.sceneRect().width()
                                                                      ,k[i].relativeY*self.scene.sceneRect().height()))
                                    k[i].analysisDialog.move(int(pos.x()+k[i].pos().x()+100), int(pos.y()+k[i].pos().y()))
                            k[-1].relativeX = (self.textItems[k[-1].index].pos().x()-75)/self.scene.sceneRect().width()
                            if not prevk:
                                k[-1].relativeY = self.dirNodes[i].relativeY
                            else:
                                k[-1].relativeY = prevk[-1].relativeY+(prevk[-1].boundingRect().height()-5)/self.scene.sceneRect().height()
                            k[-1].setPos(QPointF(k[-1].relativeX*self.scene.sceneRect().width()
                                                ,k[-1].relativeY*self.scene.sceneRect().height()))
                            prevk = k
                        
                        
    def setVisibilityOfSceneItems(self, flag):
        if self.labelObj:
            self.labelRoot.setVisible(flag)
            self.lineEditRoot.setVisible(flag)
            self.labelObj.setVisible(flag)
            self.lineEditObj.setVisible(flag)
            self.btnupdate.setVisible(flag)
            self.btnload.setVisible(flag)
            self.labelGroup.setVisible(flag)
            self.objectViewGroupComboBox.setVisible(flag)
            self.labelUser.setVisible(flag)
            self.objectViewuserComboBox.setVisible(flag)
            self.labelViewmode.setVisible(flag)
            self.viewmodeCombobox.setVisible(flag)
            
            for i in self.interfaceItems:
                i.setVisible(flag)
            self.detailPBtn.setVisible(False)
                        
            self.msg.setVisible(flag)
            for i in self.dirNodes:
                i.setVisible(flag)
            for i in self.dirEdges:
                i.setVisible(flag)
            for i in self.textItems:
                i.setVisible(flag)
            for i in self.checkgridNodes:
                for j in i:
                    for k in range(len(j)):
                        if k < len(j)-1:
                            j[k].setVisible(False)
                            j[k].analysisDialog.setVisible(False)
                        else:
                            j[k].setVisible(flag)
