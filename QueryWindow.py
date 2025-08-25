from PyQt6.QtWidgets import (QDockWidget, QWidget, QMessageBox)
from PyQt6.QtGui import (QTextCursor, QTextCharFormat, QTextBlock, 
                         QTextBlockFormat, QColor)
from PyQt6.QtCore import Qt, pyqtSignal
from Ui_QueryWindow import Ui_QueryWindow
from QueryOutput import QueryOutput
import PermissionChecker
import os, stat, re

class QueryDockWidget(QDockWidget):
    def __init__(self, parent = None):
        super().__init__('Query Window', parent)
        self.main = parent
        self.setFeatures(QDockWidget.DockWidgetFeature.DockWidgetMovable|QDockWidget.DockWidgetFeature.DockWidgetFloatable)
        self.setAllowedAreas(Qt.DockWidgetArea.RightDockWidgetArea)
        
    def resizeEvent(self, event):
        self.main.resizeViews()
  
class QueryWindow(QWidget):
    QUESTIONS = [
                'List all users',#0
                'List all groups',#1
                'List user members in group',#2
                'List groups that user is assigned to',#3
                'Which objects can user read/write/execute',#4
                'Which objects can group read/write/execute',
                'Which users can read/write/execute the specified object',#6
                'Which groups can read/write/execute the specified object',
                'Which objects have setuid bit on',#8
                'Which objects have setgid bit on',
                'Which objects have sticky bit on']#10
    
    animateQuery0 = pyqtSignal()
    animateQuery1 = pyqtSignal()
    # group name
    animateQuery2 = pyqtSignal(str)
    # user name
    animateQuery3 = pyqtSignal(str)
    # user name, permission
    animateQuery4 = pyqtSignal(str, str)
    # group name, permission
    animateQuery5 = pyqtSignal(str, str)
    # object name, permission
    animateQuery6 = pyqtSignal(str, str)
    # object name , permission
    animateQuery7 = pyqtSignal(str, str)
    
    def __init__(self, scene, parent = None):
        super().__init__(parent)
        
        self.scene = scene
        self.main = parent
        self.ui = Ui_QueryWindow()
        self.ui.setupUi(self)
        self.queryResultTextEdit = QueryOutput(scene,self)
        self.ui.runQueryLayout.addWidget(self.queryResultTextEdit)
        self.setLayout(self.ui.verticalLayout)
        self.ui.queryTypeGroupBox.setLayout(self.ui.queryTypeLayout)
        self.ui.queryInputGroupBox.setLayout(self.ui.queryInputLayout)
        self.ui.runQueryGroupBox.setLayout(self.ui.runQueryLayout)
     
        for i in range(len(self.QUESTIONS)):  # xrange → range for Python 3
            self.ui.queryListWidget.addItem(self.QUESTIONS[i])
                 
        self.setQueryForQuestion(0)
         
        self.ui.queryListWidget.currentRowChanged.connect(self.changeQueryInput)
        self.ui.runQueryButton.clicked.connect(self.runQuery)
        self.ui.clearButton.clicked.connect(self.queryResultClear)
         
        self.animationEnabled = False
         
        self.count = 0
        self.prevCursor = None
        
    def setQueryForQuestion(self, questionId):
        self.ui.queryListWidget.setCurrentRow(questionId)
        self.changeQueryInput()
        
    def queryResultClear(self):
        self.queryResultTextEdit.clear()
        
    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Enter:  # Updated enum
            self.runQuery()
    
    def clearAllInputspace(self):
        self.ui.file1ComboBox.clear()
        self.ui.file2ComboBox.clear()
        self.ui.file3ComboBox.clear()
    
    def setVisibilityOfField1(self, visibility):
        self.ui.file1Label.setVisible(visibility)
        self.ui.file1ComboBox.setVisible(visibility)
        
    def setVisibilityOfField2(self, visibility):
        self.ui.file2Label.setVisible(visibility)
        self.ui.file2ComboBox.setVisible(visibility)
        
    def setVisibilityOfField3(self, visibility):
        self.ui.file3Label.setVisible(visibility)
        self.ui.file3ComboBox.setVisible(visibility)
        
    def setVisibilityOfLineEdit(self, visibility):
        self.ui.lineEditLabel.setVisible(visibility)
        self.ui.lineEdit.setVisible(visibility)
        
    def setContentOfComboBox(self, comboBox, content):
        comboBox.clear()
        for i in content:
            comboBox.addItem(i)
            
    def changeQueryInput(self):
        self.clearAllInputspace()
        current = self.ui.queryListWidget.currentRow()
        if current == 0:
            '''the input None'''
            self.ui.queryInputGroupBox.setVisible(False)
        elif current == 1:
            '''the input - None'''
            self.ui.queryInputGroupBox.setVisible(False)
        elif current == 2:
            '''input - group name'''
            self.ui.queryInputGroupBox.setVisible(True)
            self.setVisibilityOfField1(True)
            self.ui.file1Label.setText('Group:')
            self.ui.file1Label.adjustSize()
            temp = self.main.groupSysList + self.main.groupSpecList
            self.setContentOfComboBox(self.ui.file1ComboBox, temp)
            self.setVisibilityOfField2(False)
            self.setVisibilityOfField3(False)
            self.setVisibilityOfLineEdit(False)
        elif current == 3:
            '''input - user name'''
            self.ui.queryInputGroupBox.setVisible(True)
            self.setVisibilityOfField1(True)
            self.ui.file1Label.setText('User:')
            self.ui.file1Label.adjustSize()
            temp = self.main.userSysList + self.main.userSpecList
            self.setContentOfComboBox(self.ui.file1ComboBox, temp)
            self.setVisibilityOfField2(False)
            self.setVisibilityOfLineEdit(False)
        elif current == 4:
            '''input - user name, permission'''
            self.ui.queryInputGroupBox.setVisible(True)
            self.setVisibilityOfField1(True)
            self.ui.file1Label.setText('User:')
            self.ui.file1Label.adjustSize()
            temp = self.main.userSysList + self.main.userSpecList
            self.setContentOfComboBox(self.ui.file1ComboBox, temp)
            self.setVisibilityOfField2(True)
            self.ui.file2Label.setText('Permissions:')
            self.ui.file2Label.adjustSize()
            self.setContentOfComboBox(self.ui.file2ComboBox, ['read', 'write', 'execute'])
            self.setVisibilityOfField3(False)
            self.setVisibilityOfLineEdit(False)
        elif current == 5:
            '''input - group name, permission'''
            self.ui.queryInputGroupBox.setVisible(True)
            self.setVisibilityOfField1(True)
            self.ui.file1Label.setText('Group:')
            self.ui.file1Label.adjustSize()
            temp = self.main.groupSysList + self.main.groupSpecList
            self.setContentOfComboBox(self.ui.file1ComboBox, temp)
            self.setVisibilityOfField2(True)
            self.ui.file2Label.setText('Permissions:')
            self.ui.file2Label.adjustSize()
            self.setContentOfComboBox(self.ui.file2ComboBox, ['read', 'write', 'execute'])
            self.setVisibilityOfField3(False)
            self.setVisibilityOfLineEdit(False)
        elif current == 6 or current == 7:
            '''input - object name, permission'''
            self.ui.queryInputGroupBox.setVisible(True)
            self.setVisibilityOfField1(True)
            self.ui.file1Label.setText('Permissions:')
            self.ui.file1Label.adjustSize()
            self.setContentOfComboBox(self.ui.file1ComboBox, ['read', 'write', 'execute'])
            self.setVisibilityOfField2(False)
            self.setVisibilityOfField3(False)
            self.setVisibilityOfLineEdit(True)
            self.ui.lineEditLabel.setText('Object:')
            self.ui.lineEditLabel.adjustSize()
        elif current > 7:
            '''input - None'''
            self.ui.queryInputGroupBox.setVisible(False)
            
    def setOutputHighlight(self):
        lineCnt = self.queryResultTextEdit.toPlainText().count('\n')
        cursor = QTextCursor(self.queryResultTextEdit.textCursor())
        blockFormat = QTextBlockFormat(cursor.blockFormat())
        blockFormat.setBackground(QColor(187, 255, 255, 10))  # qRgba removed in PyQt6
        blockFormat.setNonBreakableLines(True)
        blockFormat.setPageBreakPolicy(QTextFormat.PageBreakPolicy.PageBreak_AlwaysBefore)  # Updated enum
        cursor.setBlockFormat(blockFormat)
        it = cursor.block().begin()
        while not it.atEnd():
            charFormat = QTextCharFormat(it.fragment().charFormat())
            tempCursor = QTextCursor(cursor)
            tempCursor.setPosition(it.fragment().position())
            tempCursor.setPosition(it.fragment().position() + it.fragment().length(), QTextCursor.MoveMode.KeepAnchor)  # Updated enum
            tempCursor.setCharFormat(charFormat)
            self.count+=1
            
    def resetOutputText(self):
        self.queryResultTextEdit.clear()
        cursor = QTextCursor(self.queryResultTextEdit.textCursor())
        blockFormat = QTextBlockFormat(cursor.blockFormat())
        blockFormat.setBackground(QColor("white"))
        blockFormat.setNonBreakableLines(True)
        blockFormat.setPageBreakPolicy(QTextFormat.PageBreakPolicy.PageBreak_AlwaysBefore)  # Updated enum
        cursor.setBlockFormat(blockFormat)
        it = cursor.block().begin()
        while it < self.prevCursor+1:
            charFormat = QTextCharFormat(it.fragment().charFormat())
            tempCursor = QTextCursor(cursor)
            tempCursor.setPosition(it.fragment().position())
            tempCursor.setPosition(it.fragment().position() + it.fragment().length(), QTextCursor.MoveMode.KeepAnchor)  # Updated enum
            tempCursor.setCharFormat(charFormat)
            it+=1
        self.queryResultTextEdit.appendPlainText(self.prevText)
        self.cursor = cursor
        
    def runQuery0(self):
        temp = []
        for u in self.main.userSysList:
            temp.append(u)
        for u in self.main.userSpecList:
            temp.append(u)
        if len(temp) == 0:
            output = 'There is no user'
        else:
            output = 'The users are: ' + ', '.join(temp)
        output+='.\n'
        self.queryResultTextEdit.appendPlainText('[query 0] %s.' % self.QUESTIONS[0])
        self.queryResultTextEdit.appendPlainText(output)
    
    def runQuery1(self):
        temp = []
        for u in self.main.groupSysList:
            temp.append(u)
        for u in self.main.groupSpecList:
            temp.append(u)
        if len(temp) == 0:
            output = 'There is no group'
        else:
            output = 'The groups are: ' + ', '.join(temp)
        output+='.\n'
        self.queryResultTextEdit.appendPlainText('[query 1] %s.' % self.QUESTIONS[1])
        self.queryResultTextEdit.appendPlainText(output)
        
    def runQuery2(self, groupname):
        output=''
        users = set()
        #for system
        for u, g in self.main.user_group_sys_mat.items():
            if groupname in g:
                users.add(u)
        #for spec
        for u, g in self.main.user_group_mat.items():
            if groupname in g:
                users.add(u)
        if len(users) == 0:
            output += 'There is no user as a member of this group.'
        elif len(users) == 1:
            output+= 'The user in group '+groupname+ ' is:\n'
            output+= ', '.join(users)
        else:
            output+= 'The users in group '+groupname+ ' are:\n'
            output+= ', '.join(users)
        output+='\n'
        self.queryResultTextEdit.appendPlainText('[query 2] List user members in group '+ groupname+ '.')
        self.queryResultTextEdit.appendPlainText(output)
        
    def runQuery3(self, username):
        output=''
        if username in self.main.user_group_sys_mat.keys():
            groups = self.main.user_group_sys_mat[username]
            if len(groups) == 1:
                output+= 'The group user '+username+ ' assigned to is:\n'
                output+= ', '.join(groups)
            else:
                output+= 'The groups user '+username+ ' assigned to are:\n'
                output+= ', '.join(groups)
        elif username in self.main.user_group_mat.keys():
            groups = self.main.user_group_mat[username]
            if len(groups) == 1:
                output+= 'The group user '+username+ ' assigned to is:\n'
                output+= ', '.join(groups)
            else:
                output+= 'The groups user '+username+ ' assigned to are:\n'
                output+= ', '.join(groups)
        else:
            output += 'User '+username+' is not assigned to any group.'
        output+='\n'
        self.queryResultTextEdit.appendPlainText('[query 3] List groups that user '+ username+ ' is assigned to.')
        self.queryResultTextEdit.appendPlainText(output)
  
    def filterPermForFileNodes(self, permset):
        accessibleObjs = []
        for d in self.scene.dirNodeList:
            if permset.issubset(d.permset):
                    d.accessible = 0
                    d.drawCross = False
                    if d.fullpath != '/':
                        accessibleObjs.append(d.fullpath)
            else:
                d.accessible = -1
                d.drawCross = True
        accessibleObjs.sort()
        return accessibleObjs
                
    def queryUserAccessObjWithPerm(self, username, permtype):
        '''What objects can user read/write/execute'''
        output = ''
        if permtype == 'read':
            p = set(['r'])
        elif permtype == 'write':
            p = set(['w'])
        elif permtype == 'execute':
            p = set(['x'])
        for r in self.main.scene.userNodeList:
            if r.name == username:
                unode = r
        groupNum = len(unode.groupNodes)
        groupList = list(unode.groupNodes)
        PermissionChecker.checkUserPermForFileViaUser(unode, self.scene, p)
        for i in range(groupNum):  # xrange → range for Python 3
            PermissionChecker.checkUserPermForFileViaGroup(groupList[i], self.scene, p)
        PermissionChecker.checkUserPermForFileViaOther(self.scene, p)
        obj = self.filterPermForFileNodes(p)
        numobj = len(obj)
        if numobj==0:
            output += 'User '+username+' can not '+permtype+' any object.'
        elif numobj == 1:
            output +=  'The object that user '+username+' can '+permtype+' is:\n'
        else:
            output +=  'The objects that user '+username+' can '+permtype+' are:\n'
        output+='\n'.join(obj)
        output+= '\n'
        return output
    
    def runQuery4(self, username, permtype):
        '''Which objects can user read/write/execute'''
        output = 'The result is shown in the directory tree on the right side of the canvas. \
                    Inaccessible objects are in red. More objects can be displayed by expanding existing objects.\n'
        self.main.ui.actionView_User.setChecked(True)
        self.main.viewModeChanged(self.main.ui.actionView_User)
        self.main.selectUserNode(self.main.userComboBox.findText(username))
        self.main.filebrowser.filterReadCheck.setChecked(permtype == 'read')
        self.main.filebrowser.filterWriteCheck.setChecked(permtype == 'write')
        self.main.filebrowser.filterExecuteCheck.setChecked(permtype == 'execute')
        self.main.filebrowser.filterSetUidCheck.setChecked(False)
        self.main.filebrowser.filterSetGidCheck.setChecked(False)
        self.main.filebrowser.filterStickyBitCheck.setChecked(False)
        self.main.filebrowser.updateTreeView()
        self.queryResultTextEdit.appendPlainText('[query 4] Which objects can user %s %s.' % (username, permtype))
        self.queryResultTextEdit.appendPlainText(output)
                   
    def runQuery5(self, name, permtype):
        '''Which objects can group read/write/execute'''
        output = 'The result is shown in the directory tree on the right side of the canvas. \
                    Inaccessible objects are in red. More objects can be displayed by expanding existing objects.\n'
        self.main.ui.actionView_Group.setChecked(True)
        self.main.viewModeChanged(self.main.ui.actionView_Group)
        self.main.selectGroupNode(self.main.groupComboBox.findText(name))
        self.main.filebrowser.filterReadCheck.setChecked(permtype == 'read')
        self.main.filebrowser.filterWriteCheck.setChecked(permtype == 'write')
        self.main.filebrowser.filterExecuteCheck.setChecked(permtype == 'execute')
        self.main.filebrowser.filterSetUidCheck.setChecked(False)
        self.main.filebrowser.filterSetGidCheck.setChecked(False)
        self.main.filebrowser.filterStickyBitCheck.setChecked(False)
        self.main.filebrowser.updateTreeView()
        self.queryResultTextEdit.appendPlainText('[query 5] Which objects can group %s %s.' % (name, permtype))
        self.queryResultTextEdit.appendPlainText(output)

    def queryUsersAccessAnObjWithPerm(self, objname, permtype):
        accessibleUsers = set()
        if permtype == 'read':
            p = set(['r'])
        elif permtype == 'write':
            p = set(['w'])
        elif permtype == 'execute':
            p = set(['x'])
        objList = []
        objname = objname.replace(self.main.root_dir, '')
        temp = objname.split('/')
        temp = [item for item in temp if item != '']  # filter → list comprehension for Python 3
        for t in temp:
            objList.append('/'+t)
        for u in self.main.scene.userNodeList:
            username = u.name
            filepath = ''
            for i in range(len(objList)):  # xrange → range for Python 3
                filepath += objList[i]
                if i==len(objList)-1:
                    info = self.main.objectViewScene.computePermForGrid(username, filepath, False, p)
                    if info[0]:
                        accessibleUsers.add(u)
                else:
                    info = self.main.objectViewScene.computePermForGrid(username, filepath, True)
                    if info[0]:
                        continue
                    else:
                        break
        return accessibleUsers
        
    def runQuery6(self, objname, permtype):
        '''Which users can read/write/execute the specified object''' 
        '''Check the format and existence of the object'''
        self.main.ui.actionView_Object.setChecked(True)
        self.main.viewModeChanged(self.main.ui.actionView_Object)
        self.main.objectViewScene.lineEditObj.setText(objname)
        self.main.objectViewScene.startup(objname)
        self.main.objectViewScene.updateLayout()
        output = '\n'
        accessibleUsers = self.queryUsersAccessAnObjWithPerm(objname, permtype)
        if len(accessibleUsers) > 0:
            output+='The users can %s the object are:\n'%permtype
            output+=','.join(a.name for a in accessibleUsers)
        else:
            output+='No user can %s the object.'%permtype
        output += '\n'
        self.queryResultTextEdit.appendPlainText('[query 6] Which users can read/write/execute the specified object?')
        self.queryResultTextEdit.appendPlainText(output)
            
    def queryGroupsAccessAnObjWithPerm(self, objname, permtype):
        accessibleGroups = set()
        if permtype == 'read':
            p = set(['r'])
        elif permtype == 'write':
            p = set(['w'])
        elif permtype == 'execute':
            p = set(['x'])
        objList = []
        objname = objname.replace(self.main.root_dir, '')
        temp = objname.split('/')
        temp = [item for item in temp if item != '']  # filter → list comprehension for Python 3
        for t in temp:
            objList.append('/'+t)
        for g in self.main.scene.groupNodeList:
            users = self.main.objectViewScene.getUsersInGroup(g.name)
            for u in users:
                fileuser, filegroup, uid, gid = PermissionChecker.getFileUserAndGroup(objname, None, self.scene)
                if filegroup == None and gid == -1:
                    continue
                if fileuser == u:
                    continue
                filepath = ''
                for i in range(len(objList)):  # xrange → range for Python 3
                    filepath += objList[i]
                    if i==len(objList)-1:
                        info = self.main.objectViewScene.computePermForGrid(u, filepath, False, p)
                        if info[0]:
                            accessibleGroups.add(g)
                    else:
                        info = self.main.objectViewScene.computePermForGrid(u, filepath, True)
                        if info[0]:
                            continue
                        else:
                            break
        return accessibleGroups
      
    def runQuery7(self, objname, permtype):
        '''Which groups can read/write/execute the specified object'''
        '''Check the format and existence of the object'''
        self.main.ui.actionView_Object.setChecked(True)
        self.main.viewModeChanged(self.main.ui.actionView_Object)
        self.main.objectViewScene.lineEditObj.setText(objname)
        self.main.objectViewScene.startup(objname)
        self.main.objectViewScene.updateLayout()
        output = '\n'
        accessibleGroups = self.queryGroupsAccessAnObjWithPerm(objname, permtype)
        if len(accessibleGroups) > 0:
            output+='The groups can %s the object are:\n'%permtype
            output+=','.join(a.name for a in accessibleGroups)
        else:
            output+='No group can %s the object.'%permtype
        output += '\n'
        self.queryResultTextEdit.appendPlainText('[query 7] Which groups can read/write/execute the specified object?')
        self.queryResultTextEdit.appendPlainText(output)
            
    def runQuery8(self):
        '''Which objects have setuid bit on'''
        self.main.ui.actionView_User.setChecked(True)
        self.main.viewModeChanged(self.main.ui.actionView_User)
        self.main.filebrowser.filterReadCheck.setChecked(False)
        self.main.filebrowser.filterWriteCheck.setChecked(False)
        self.main.filebrowser.filterExecuteCheck.setChecked(False)
        self.main.filebrowser.filterSetUidCheck.setChecked(True)
        self.main.filebrowser.filterSetGidCheck.setChecked(False)
        self.main.filebrowser.filterStickyBitCheck.setChecked(False)
        self.main.filebrowser.updateTreeView()
        output = '\n'
        objs = []
        for o in self.scene.dirNodeList:
            opath = o.getFullPath()
            if os.path.exists(opath):
                stat_info = os.stat(opath)
                if stat_info.st_mode & stat.S_ISUID:
                    objs.append(o.name)
            else:
                opath = re.sub(self.scene.main.root_dir, '', opath)
                if opath[-1] == '/' and opath!= '/':
                    opath=opath[:-1]
                perm = self.scene.main.obj_perm_mat[opath].userperm
                if ('s' in perm) or ('S' in perm):
                    objs.append(opath[1:])
        if objs == []:
            output += 'No object has setuid bit on.\n'
        else:
            objs.sort()
            output += 'The objects that have setuid on are: (under directory "%s")\n'%self.scene.main.root_dir
            output += '\n'.join(objs)
            output += '\n'
        self.queryResultTextEdit.appendPlainText('[query 8] Which objects have setuid bit on?')
        self.queryResultTextEdit.appendPlainText(output)
        
    def runQuery9(self):
        '''Which objects have setgid bit on'''
        self.main.ui.actionView_User.setChecked(True)
        self.main.viewModeChanged(self.main.ui.actionView_User)
        output = '\n'
        objs = []
        for o in self.scene.dirNodeList:
            opath = o.getFullPath()
            if os.path.exists(opath):
                stat_info = os.stat(opath)
                if stat_info.st_mode & stat.S_ISGID:
                    objs.append(o.name)
            else:
                opath = re.sub(self.scene.main.root_dir, '', opath)
                if opath[-1] == '/' and opath!= '/':
                    opath=opath[:-1]
                perm = self.scene.main.obj_perm_mat[opath].groupperm
                if ('s' in perm) or ('S' in perm):
                    objs.append(opath[1:])
        if objs == []:
            output += 'No object has setgid bit on.\n'
        else:
            output += 'The objects that have setgid on are: (under directory "%s")\n'%self.scene.main.root_dir
            output += '\n'.join(objs)
            output += '\n'
        self.queryResultTextEdit.appendPlainText('[query 9] Which objects have setgid bit on?')
        self.queryResultTextEdit.appendPlainText(output)
        
    def runQuery10(self):
        'Which objects have sticky bit on'
        self.main.ui.actionView_User.setChecked(True)
        self.main.viewModeChanged(self.main.ui.actionView_User)
        output = '\n'
        objs = []
        for o in self.scene.dirNodeList:
            opath = o.getFullPath()
            if os.path.exists(opath):
                stat_info = os.stat(opath)
                if stat_info.st_mode & 0o1000 == 0o1000:  # Updated octal syntax for Python 3
                    objs.append(o.name)
            else:
                opath = re.sub(self.scene.main.root_dir, '', opath)
                if opath[-1] == '/' and opath!= '/':
                    opath=opath[:-1]
                perm = self.scene.main.obj_perm_mat[opath].otherperm
                if ('t' in perm) or ('T' in perm):
                    objs.append(opath[1:])
        if objs == []:
            output += 'No object has sticky bit on.\n'
        else:
            output += 'The objects that have sticky on are: (under directory "%s")\n'%self.scene.main.root_dir
            output += '\n'.join(objs)
            output += '\n'
        self.queryResultTextEdit.appendPlainText('[query 10] Which objects have sticky bit on?')
        self.queryResultTextEdit.appendPlainText(output)
        
    def getQueryResult(self, queryId):
        paras = []
        if queryId == 0:
            self.runQuery0()
        elif queryId == 1:
            self.runQuery1()
        elif queryId == 2:
            username = str(self.ui.file1ComboBox.currentText())
            paras = [username]
            self.runQuery2(username)
        elif queryId == 3:
            username = str(self.ui.file1ComboBox.currentText())
            paras = [username]
            self.runQuery3(username)
        elif queryId == 4:
            username = str(self.ui.file1ComboBox.currentText())
            permtype = str(self.ui.file2ComboBox.currentText())
            paras = [username, permtype]
            self.runQuery4(username, permtype)
        elif queryId == 5:
            name = str(self.ui.file1ComboBox.currentText())
            permtype = str(self.ui.file2ComboBox.currentText())
            paras = [name, permtype]
            self.runQuery5(name, permtype)
        elif queryId == 6:
            permtype = str(self.ui.file1ComboBox.currentText())
            objname = str(self.ui.lineEdit.text())
            paras = [permtype, objname]
            self.runQuery6(objname, permtype)
        elif queryId == 7:
            permtype = str(self.ui.file1ComboBox.currentText())
            objname = str(self.ui.lineEdit.text())
            paras = [permtype, objname]
            self.runQuery7(objname, permtype)
        elif queryId == 8:
            paras = ['suid']
            self.runQuery8()
        elif queryId == 9:
            paras = ['sgid']
            self.runQuery9()
        elif queryId == 10:
            paras = ['sticky']
            self.runQuery10()
           
    def runQuery(self, paras=None):
        if not self.main.root_dir:  # Changed from access_root_dir to root_dir based on error message
            QMessageBox.critical(self.main, 'Error', 'Please specify a root directory to start with!', QMessageBox.StandardButton.Ok)  # Updated enum
            return
            
        self.main.hideAllNodeItemsInScene(self.scene)
        self.prevText = self.queryResultTextEdit.toPlainText()
        self.prevCursor = self.prevText.count('\n')
        self.resetOutputText()
        self.setOutputHighlight()
        current = self.ui.queryListWidget.currentRow()
        self.getQueryResult(current)
