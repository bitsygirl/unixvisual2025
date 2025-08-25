'''
Created on Sep 12, 2015

@author: manwang
Updated for PyQt6 compatibility
'''
from PyQt6.QtWidgets import *
from PyQt6.QtCore import Qt, QObject
from PyQt6.QtGui import QStandardItemModel, QStandardItem, QBrush
from collections import namedtuple
from UserNode import UserNode
from GroupNode import GroupNode
import PermissionChecker
import os

Path = namedtuple('Path', ('parent', 'name', 'children'))
 
def makePath(parent = None, name = None, children = [], parentItem = None):
    return Path(parent, name, children)

class FileBrowserViewDialog(QWidget):
    PERMS = ['Read', 'Write', 'Execute', 'Read, Write', 'Read, Execute', 'Write, Execute', 'Read, Write, Execute']
    USER_MD = 0
    GROUP_MD = 1
    NORMAL_MD = 2
    
    OR_RELATION  = 1000
    AND_RELATION = 1001
    
    def __init__(self, parent, main):
        super().__init__(parent)
        self.main = main
        self.wlayout = QVBoxLayout(self)
        self.wlayout.setContentsMargins(0, 0, 0, 0)
        self.vsplitter = QSplitter(Qt.Orientation.Horizontal)
        
        self.filterw = QWidget()
        scrollarea = QScrollArea()
        scrollarea.setWidget(self.filterw)
        scrollarea.setWidgetResizable(True)
        self.treev = QTreeView()
        self.tablev = QTableWidget()
        self.listv = QListView()
        self.viewlayout = QVBoxLayout(self.filterw)

        self.viewlayout.setContentsMargins(0, 0, 0, 0)
        self.settingBox = QGroupBox("Settings")
        self.settingBox.setAutoFillBackground(True)
        vLayout = QVBoxLayout(self.settingBox)
        vLayout.setContentsMargins(0, 0, 0, 0)
        self.logicW = QWidget()
        self.logicRadioHLayout = QHBoxLayout(self.logicW)
        self.logicRelationLabel = QLabel("Relation:")
        self.logicAndRadioBtn = QRadioButton("AND")
        self.logicOrRadioBtn = QRadioButton("OR")
        self.logicRadioHLayout.addWidget(self.logicRelationLabel)
        self.logicRadioHLayout.addWidget(self.logicOrRadioBtn)
        self.logicRadioHLayout.addWidget(self.logicAndRadioBtn)
        
        self.permW = QGroupBox("Permissions")
        self.permCheckVLayout = QVBoxLayout(self.permW)
        self.permCheckHW1 = QWidget()
        self.permCheckHLayout1 = QHBoxLayout(self.permCheckHW1)
        self.filterReadCheck = QCheckBox("Read")
        self.filterWriteCheck = QCheckBox("Write")
        self.filterExecuteCheck = QCheckBox("Execute")
        self.permCheckHLayout1.addWidget(self.filterReadCheck)
        self.permCheckHLayout1.addWidget(self.filterWriteCheck)
        self.permCheckHLayout1.addWidget(self.filterExecuteCheck)
        
        self.permCheckHW2 = QWidget()
        self.permCheckHLayout2 = QHBoxLayout(self.permCheckHW2)
        self.filterSetUidCheck = QCheckBox('Setuid')
        self.filterSetGidCheck = QCheckBox('Setgid')
        self.filterStickyBitCheck = QCheckBox('Sticky')
        self.permCheckHLayout2.addWidget(self.filterSetUidCheck)
        self.permCheckHLayout2.addWidget(self.filterSetGidCheck)
        self.permCheckHLayout2.addWidget(self.filterStickyBitCheck)
        
        self.permCheckVLayout.addWidget(self.permCheckHW1)
        self.permCheckVLayout.addWidget(self.permCheckHW2)
        
        groupboxFile = QGroupBox("Permissions for Regular File")
        groupboxVlayout = QVBoxLayout(groupboxFile)
        groupboxVlayout.setContentsMargins(0, 0, 0, 0)
        readDirLabel = QLabel("Read: View the content of a file.")
        readDirLabel.setWordWrap(True)
        writeDirLabel = QLabel("Write: Allow changes to the content of a file.")
        writeDirLabel.setWordWrap(True)
        executeDirLabel = QLabel("Execute: Allow running a file as a binary.")
        executeDirLabel.setWordWrap(True)
        groupboxVlayout.addWidget(readDirLabel)
        groupboxVlayout.addWidget(writeDirLabel)
        groupboxVlayout.addWidget(executeDirLabel)
        
        groupbox = QGroupBox("Permissions for Directory")
        groupboxVlayout = QVBoxLayout(groupbox)
        groupboxVlayout.setContentsMargins(0, 0, 0, 0)
        readDirLabel = QLabel("Read: List the content of the directory.")
        readDirLabel.setWordWrap(True)
        writeDirLabel = QLabel("Write: Allow adding/removing objects under the directory.")
        writeDirLabel.setWordWrap(True)
        executeDirLabel = QLabel("Execute: Allow 'pass-through' the directory and perform allowed operations on files/directories beneath")
        executeDirLabel.setWordWrap(True)
        groupboxVlayout.addWidget(readDirLabel)
        groupboxVlayout.addWidget(writeDirLabel)
        groupboxVlayout.addWidget(executeDirLabel)
        self.initialStateButtons()
        
        self.updateBtn = QPushButton("Refresh")
        vLayout.addWidget(self.logicW)
        vLayout.addWidget(self.permW)
        vLayout.addWidget(groupboxFile)
        vLayout.addWidget(groupbox)
        vLayout.addWidget(self.updateBtn)
        self.viewlayout.addWidget(self.settingBox)
        label = QLabel("Directory Tree")
        self.viewlayout.addWidget(label)
        label = QLabel("(Click on an object to see whether a user/group can access the object with specified permission.)")
        label.setWordWrap(True)
        self.viewlayout.addWidget(label)
        self.viewlayout.addWidget(self.treev)
        
        self.tablevW = QWidget()
        self.tablevVLayout = QVBoxLayout(self.tablevW)
        label = QLabel("Object Permissions")
        self.tablevVLayout.addWidget(label)
        label = QLabel("Access Analysis")
        self.detailTextEdit = QTextEdit()
        self.detailTextEdit.setReadOnly(True)
        self.tablevVLayout.addWidget(self.tablev)
        self.tablevVLayout.addWidget(label)
        self.tablevVLayout.addWidget(self.detailTextEdit)
        
        self.vsplitter.addWidget(scrollarea)
        self.vsplitter.addWidget(self.tablevW)
        self.vsplitter.setStyleSheet("QSplitter { background-color : #CEECF5;}")
        self.wlayout.addWidget(self.vsplitter)
        self.treev.expanded.connect(lambda index: self.generatePermHighlight(index))
        self.treev.clicked.connect(lambda index: self.showPermSelected(index))
        self.updateBtn.clicked.connect(self.updateTreeView)
        self.tablev.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.tablev.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.mode = self.NORMAL_MD
        self.user = None
        self.group = None
        
    def initialStateButtons(self):
        self.logicOrRadioBtn.setChecked(True)
        self.logicAndRadioBtn.setChecked(False) 
        self.filterReadCheck.setChecked(True)
        self.filterWriteCheck.setChecked(True)
        self.filterExecuteCheck.setChecked(True)
        self.filterSetUidCheck.setChecked(False)
        self.filterSetGidCheck.setChecked(False)
        self.filterStickyBitCheck.setChecked(False)
        self.action = set()
        self.permrelation = self.OR_RELATION
        
    def createLineSeparator(self, parent):
        line = QFrame(parent)
        line.setFrameShape(QFrame.Shape.HLine)
        line.setFrameShadow(QFrame.Shadow.Sunken)
        return line
    
    def updateTreeView(self):
        if isinstance(self.main.focusNode, UserNode):
            self.filterActionChanged(self.main.focusNode.name, None)
        elif isinstance(self.main.focusNode, GroupNode):
            self.filterActionChanged(None, self.main.focusNode.name)
        else:
            self.filterActionChanged(None, None)
            
    def showPermSelected(self, index):
        if self.user == None and self.group == None:
            self.detailTextEdit.clear()
            self.detailTextEdit.setHtml('<font color=\"Red\" size="4">%s</font>'%('Please select a(n) user/group from User/Group View to start with!'))
            return
        crawler = index.model().itemFromIndex(index)
        pathlist = [str(crawler.text())]
        pathperms = [str(crawler.accessibleDescription())]
        itemList = []
        self.message = ''
        parentSuccess = True
        while crawler.parent():
            crawler = crawler.parent()
            itemList.append(crawler.index())
            pathlist.append(crawler.text())
            pathperms.append(crawler.accessibleDescription())
        for i in reversed(itemList):
            item = i.model().itemFromIndex(i)
            success, msg = self.computePermForItem(item, set('x'), self.user, self.group, True)
            
            self.message += '<font color=\"Blue\" size="4">%s:</font> %s<br />'%(str(itemList.index(i)+2)+'. '+str(item.text()), msg)
            if not success:
                parentSuccess = False
                break
        if parentSuccess:
            item = index.model().itemFromIndex(index)
            success, msg = self.computePermForItem(item, self.action, self.user, self.group, True, False)
    #         if parentSuccess == False:
    #             item.setForeground(QBrush(Qt.GlobalColor.red))
            self.message += '<font color=\"Blue\" size="4">1. %s:</font> %s<br />'%(str(item.text()), msg)
        self.tablev.clearContents()
        self.tablev.setRowCount(len(pathlist))
        self.tablev.setColumnCount(2)
        headers = ["Directory", "Permissions"]
        self.tablev.setHorizontalHeaderLabels(headers)
        for r in range(len(pathlist)):
            newItem = QTableWidgetItem(pathlist[r])
            self.tablev.setItem(r, 0, newItem)
            newItem = QTableWidgetItem(pathperms[r])
            self.tablev.setItem(r, 1, newItem)
        self.tablev.resizeRowsToContents()
        self.detailTextEdit.clear()
        self.detailTextEdit.setHtml(self.message)
        
    def generateHierlistOneStep(self, startpath):
        dirlist = []
        if self.main.root_dir[-1] == '/':
            index = 1
        else:
            index = 0
        for l in self.main.dirSpecHier:
            for d in l:
                fullpath = d.getFullPath()
                if self.main.root_dir not in fullpath:
                    if d.dirpath:
                        d.dirpath=self.main.root_dir+d.dirpath[index:]
                    else:
                        d.name = self.main.root_dir
                if d.dirpath == startpath:
                    if d.isFile:
                        path = makePath(os.path.normpath(startpath)+'/',os.path.normpath(d.name), [])
                    else:
                        path = makePath(os.path.normpath(startpath)+'/',os.path.normpath(d.name)+'/', [])
                    dirlist.append(path)
        return dirlist
        
    def list_files(self, startpath, depth=1):
        import re
        if os.path.isdir(startpath):
            count = 0
            pathname= re.sub('/+', '/', startpath+'/')
            dirlist = [makePath(None, pathname, [])]
            filelist = []
            for root, dirs, files in os.walk(startpath):
                if ".git" in root:
                    continue
                
                if count == depth:
                    break
                for d in dirs:
                    path = makePath(re.sub('/+', '/', os.path.normpath(root)+'/'),\
                                    re.sub('/+', '/', os.path.normpath(d)+'/'),\
                                     [])
                    dirlist.append(path)
                for f in files:
                    path = makePath(re.sub('/+', '/', os.path.normpath(root)+'/'),\
                            re.sub('/+', '/', os.path.normpath(f)),\
                             [])
                    filelist.append(path)
                count+=1
            return dirlist, filelist
        return [], []
        
    def fillinFileInfo(self, root):
        dirlist, filelist = self.list_files(root)
        dirSpeclist = self.generateHierlistOneStep(root)                 
        dirlist.extend(filelist)
        dirlist.extend(dirSpeclist)
        self.newLevel = []
        self.model = QStandardItemModel(1, 1)
        firstitem = self.addItem(dirlist[0], None)
        self.model.setItem(0, 0, firstitem)
        
        for i in range(1, len(dirlist)):
            item = self.addItem(dirlist[i], firstitem)
            self.newLevel.append(item)
#         for i in filelist:
#             item = self.addItem(i, firstitem)
#             self.newLevel.append(item)
#         for i in dirSpeclist:
#             item = self.addItem(i, firstitem)
#             self.newLevel
    
        self.model.setHorizontalHeaderItem( 0, QStandardItem("Directory"))
        self.treev.setModel(self.model)
        self.treev.setAnimated(True)
        self.dirlist = dirlist

    def filterActionChanged(self, username, groupname):
        self.treev.collapseAll()
        self.detailTextEdit.clear()
        self.tablev.clear()
        if username:
            self.user = username
            self.group = None
        if groupname:
            self.group = groupname
            self.user = None
        if self.logicAndRadioBtn.isChecked():
            self.permrelation = self.AND_RELATION
        else:
            self.permrelation = self.OR_RELATION
        if self.main.mode != self.main.QUERY_MODE:
            self.action = set()
            if self.filterReadCheck.isChecked():
                self.action.add('r')
            if self.filterWriteCheck.isChecked():
                self.action.add('w')
            if self.filterExecuteCheck.isChecked():
                self.action.add('x')
            if self.filterSetUidCheck.isChecked():
                self.action.add('us')
            if self.filterSetGidCheck.isChecked():
                self.action.add('gs')
            if self.filterStickyBitCheck.isChecked():
                self.action.add('t')
        self.traverseAllItemInTreeView(self.treev.model().item(0, 0), self.action, self.treev.model(), username, groupname)
            
    def getPermissionText(self):
        perms = []
        if self.filterReadCheck.isChecked():
            perms.append('read')
        if self.filterWriteCheck.isChecked():
            perms.append('write')
        if self.filterExecuteCheck.isChecked():
            perms.append('execute')
        if self.filterSetUidCheck.isChecked():
            perms.append('setuid')
        if self.filterSetGidCheck.isChecked():
            perms.append('setgid')
        if self.filterStickyBitCheck.isChecked():
            perms.append('sticky')
        if self.permrelation == self.AND_RELATION:
            return ' and '.join(perms)
        else:
            return ' or '.join(perms)
                         
    def generatePermHighlight(self, index):
        item = index.model().itemFromIndex(index)
        temp = item
        startname = ''
        while(temp):
            startname=str(temp.text())+startname
            temp = temp.parent()
        item.removeRows(0, item.rowCount())
        dirlist, filelist = self.list_files(startname)
        dirSpeclist = self.generateHierlistOneStep(startname)                 
        dirlist.extend(filelist)
        dirlist.extend(dirSpeclist)
        for d in dirlist:
            if d.parent:
                name = d.parent+d.name
            else:
                name = d.name
#             for c in dirlist:
#                 if name == c.parent:
#                     d.children.append(c)
            if name != startname:
                self.addItem(d, item)
        for i in range(item.rowCount()):
            item.child(i).removeRows(0, item.child(i).rowCount())
            dirlist, filelist = self.list_files(startname+str(item.child(i).text()))
            dirSpeclist = self.generateHierlistOneStep(startname+str(item.child(i).text()))
            dirlist.extend(filelist)
            dirlist.extend(dirSpeclist)
            for d in dirlist:
                if d.parent:
                    name = d.parent+d.name
                else:
                    name = d.name
#                 for c in dirlist:
#                     if name == c.parent:
#                         d.children.append(c)
                if name != startname+str(item.child(i).text()):
                    self.addItem(d, item.child(i))
        for i in range(item.rowCount()):
            c = item.child(i)
            self.traverseAllItemInTreeView(c, self.action, self.treev.model(), self.user, self.group)
               
    def traverseAllItemInTreeView(self, item, action, model, username = None, groupname = None):
        index = item.index()
        crawler = index.model().itemFromIndex(index)
        pathlist = [str(crawler.text())]
        pathperms = [str(crawler.accessibleDescription())]
        itemList = []
        parentSuccess = True
        while crawler.parent():
            crawler = crawler.parent()
            itemList.append(crawler.index())
            pathlist.append(crawler.text())
            pathperms.append(crawler.accessibleDescription())
        for i in reversed(itemList):
            item = i.model().itemFromIndex(i)
            success, msg = self.computePermForItem(item, set('x'), username, groupname, True)
            if not success:
                parentSuccess = False
        item = index.model().itemFromIndex(index)
        self.computePermForItem(item, action, username, groupname)
        if parentSuccess == False:
            item.setForeground(QBrush(Qt.GlobalColor.red))
        if model.hasChildren(index) and self.treev.isExpanded(index):
            for i in range(item.rowCount()):
                c = item.child(i)
                self.traverseAllItemInTreeView(c, action, model)
                    
    def hasPerm(self, action, permStr, permso, bits):
        if self.permrelation == self.OR_RELATION:
            for a in action:
                if a == 't' and (permso[-1] == 't' or permso == 'T'):
                    return True
                if a in permStr:
                    return True
                if bits == 'other':
                    if a == 'x' and ('t' in permStr or 'x' in permStr):
                        return True
                else:
                    if a == 'x' and ('s' in permStr or 'x' in permStr):
                        return True
                    if ('s' in permStr or 'S' in permStr):
                        if (bits == 'user' and a == 'us') or \
                           (bits == 'group' and a == 'gs'):
                            return True
            return False
        elif self.permrelation == self.AND_RELATION:
            for a in action:
                if a == 't' and (permso[-1] == 't' or permso == 'T'):
                    continue
                if bits == 'other':
                    if a == 'x' and ('t' in permStr or 'x' in permStr):
                        continue
                else:
                    if a == 'x' and ('s' in permStr or 'x' in permStr):
                        continue
                    if ('s' in permStr or 'S' in permStr):
                        if (bits == 'user' and a == 'us') or \
                           (bits == 'group' and a == 'gs'):
                            continue
                if a not in permStr:
                    return False
            return True
            
    def bitsToUseMsg(self, whichbits, perms):
        return 'Bits in the "%s" field are applied for this access. The %s bits are %s.'%(whichbits, whichbits, perms)
    
    def pdirMsg(self, havePerm):
        if havePerm:
            return "The 'x' bit allows passing through the directory."
        else:
            return "'x' is required to pass through this directory to files and directories beneath but this bit is not set."
        
    def fileMsg(self, havePerm, requestPerm, subject, bitsPerm):
        if havePerm:
            return 'This satisfies the requested access of "%s".'%(requestPerm)
        else:
            return 'This is not sufficient for the requested access of "%s".'%(requestPerm)
        
    def computePermForItem(self,item, action, username, groupname, msgOn = False, parentDir = True):
        msg = ''
        success = False
        index1 = str(item.accessibleText()).find(':')
        index2 = str(item.accessibleText()).rfind(':')
        fileuser = str(item.accessibleText())[:index1]
        filegroup = str(item.accessibleText())[index1+1:index2]
        perms = str(item.accessibleText())[index2+1:]
        permsu = perms[:3]
        permsg = perms[3:6]
        permso = perms[6:]
        settingperm = self.getPermissionText()
        if self.mode == self.USER_MD:
            #self.userModeComputePermForItem(item, action, username, groupname, msgOn, parentDir)
            node = None
            gnode = None
            for u in self.main.scene.userNodeList:
                if u.name == username:
                    node = u
            for g in self.main.scene.groupNodeList:
                if g.name == filegroup:
                    gnode = g
            if fileuser == username:
                if self.hasPerm(action, permsu, permso, 'user'):
                    if msgOn:
                        success = True
                        if parentDir:
                            msg+=('<font color=\"Black\" size="4">%s%s</font><br>')\
                                %(self.bitsToUseMsg('user', permsu), self.pdirMsg(success))
                        else:
                            msg+=('<font color=\"Black\" size="4">%s%s</font><br>')\
                                %(self.bitsToUseMsg('user', permsu), self.fileMsg(success, settingperm, 'user', permsu))
                    else:
                        item.setForeground(QBrush(Qt.GlobalColor.black))
                else:
                    if msgOn:
                        success = False
                        if parentDir:
                            msg+=('<font color=\"Red\" size="4">%s%s</font><br>')\
                                %(self.bitsToUseMsg('user', permsu), self.pdirMsg(success))
                        else:
                            msg+=('<font color=\"Red\" size="4">%s%s</font><br>')\
                                %(self.bitsToUseMsg('user', permsu), self.fileMsg(success, settingperm, 'user', permsu))
                    else:
                        item.setForeground(QBrush(Qt.GlobalColor.red))
            
            elif node and (gnode in node.groupNodes):
                if self.hasPerm(action, permsg, permso, 'group'):
                    if msgOn:
                        success = True
                        if parentDir:
                            msg+=('<font color=\"Black\" size="4">%s%s</font><br>')\
                                %(self.bitsToUseMsg('group', permsg), self.pdirMsg(success))
                        else:
                            msg+=('<font color=\"Black\" size="4">%s%s</font><br>')\
                                %(self.bitsToUseMsg('group', permsg), self.fileMsg(success, settingperm, 'group', permsg))
                    else:
                        item.setForeground(QBrush(Qt.GlobalColor.black))
                else:
                    if msgOn:
                        success = False
                        if parentDir:
                            msg+=('<font color=\"Red\" size="4">%s%s</font><br>')\
                                %(self.bitsToUseMsg('group', permsg), self.pdirMsg(success))
                        else:
                            msg+=('<font color=\"Red\" size="4">%s%s</font><br>')\
                                %(self.bitsToUseMsg('group', permsg), self.fileMsg(success, settingperm, 'group', permsg))
                    else:
                        item.setForeground(QBrush(Qt.GlobalColor.red))
            else:
                if self.hasPerm(action, permso, permso, 'other'):
                    if msgOn: 
                        success = True
                        if parentDir:
                            msg+=('<font color=\"Black\" size="4">%s%s</font><br>')\
                                    %(self.bitsToUseMsg('other', permso), self.pdirMsg(success))
                        else:
                            msg+=('<font color=\"Black\" size="4">%s%s</font><br>')\
                                %(self.bitsToUseMsg('other', permso), self.fileMsg(success, settingperm, 'other', permso))
                    else:
                        item.setForeground(QBrush(Qt.GlobalColor.black))
                else:
                    if msgOn:
                        success = False
                        if parentDir:
                            msg+=('<font color=\"Red\" size="4">%s%s</font><br>')\
                                    %(self.bitsToUseMsg('other', permso), self.pdirMsg(success))
                        else:
                            msg += ('<font color=\"Red\" size="4">%s%s</font><br>')\
                                %(self.bitsToUseMsg('other', permso), self.fileMsg(success, settingperm, 'other', permso))
                    else:
                        item.setForeground(QBrush(Qt.GlobalColor.red))
        elif self.mode == self.GROUP_MD:
            if filegroup == groupname:
                if self.hasPerm(action, permsg, permso, 'group'):
                    if msgOn:
                        success = True
                        if parentDir:
                            msg+=('<font color=\"Black\" size="4">%s%s</font><br>')\
                                %(self.bitsToUseMsg('group', permsg), self.pdirMsg(success))
                        else:
                            msg+=('<font color=\"Black\" size="4">%s%s</font><br>')\
                                %(self.bitsToUseMsg('group', permsg), self.fileMsg(success, settingperm, 'group', permsg))
                    else:
                        item.setForeground(QBrush(Qt.GlobalColor.black))
                else:
                    if msgOn:
                        success = False
                        if parentDir:
                            msg+=('<font color=\"Red\" size="4">%s%s</font><br>')\
                                %(self.bitsToUseMsg('group', permsg), self.pdirMsg(success))
                        else:
                            msg+=('<font color=\"Red\" size="4">%s%s</font><br>')\
                                %(self.bitsToUseMsg('group', permsg), self.fileMsg(success, settingperm, 'group', permsg))
                    else:
                        item.setForeground(QBrush(Qt.GlobalColor.red))
            else:
                if msgOn:
                    success = False
                    if parentDir:
                        msg+='<font color=\"Red\" size="4">The group is not the group of the object so there is no access to the object.\n'\
                            + "%s.<\font><br>"%self.pdirMsg(success)

                    else:
                        msg+='<font color=\"Red\" size="4">The group is not the group of the object so there is no access to the object.<\font><br>'
                else:
                    item.setForeground(QBrush(Qt.GlobalColor.red))
        return success, msg
    
    def addItem(self, diritem, prevStandItem):
        item = QStandardItem(diritem.name)
        item.setEditable(False)
        if diritem.parent:
            filepath = diritem.parent+ diritem.name
        else:
            filepath = diritem.name
        fileuser, filegroup, uid, gid = PermissionChecker.getFileUserAndGroup(filepath, None, self.main.scene)
        if fileuser == None and uid == -1:
            return
        perms = PermissionChecker.getPermissionbitForFile(filepath, None, self.main.scene)
        permletters = PermissionChecker.convertNineBitsOctToRWX(perms)
        temp = 'User:'+str(uid)+'('+fileuser +')\nGroup:' + str(gid)+'('+filegroup+')\nPermission bits:\n'+perms+'('+permletters+')'
        item.setAccessibleDescription(temp)
        item.setAccessibleText(fileuser+':'+filegroup+':'+permletters)
        if prevStandItem: 
            prevStandItem.appendRow(item)
        return item
