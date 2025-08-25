'''
Created on Jul 24, 2015

@author: manwang
'''
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from Ui_SystemCallViewCodeLoad import Ui_SystemCallViewCodeLoad, Ui_SyscallOutputDialog
from SystemCallViewCodeDisplay import SystemCallViewCodeDisplay
from ProcessNodeParamDialog import ProcessNodeParamDialog
from ProcessNode import ProcessNode
from EdgeItem import EdgeItem
from SystemCallSocket import SystemCallSocket
from SystemCallQtSocket import SystemCallQtSocket
from syscalloutput import *
import os
        
class SystemCallViewCodeLoadDlg(QDialog):
    def __init__(self, main):
        QDialog.__init__(self)
        self.ui = Ui_SystemCallViewCodeLoad()
        self.ui.setupUi(self)
        self.main = main
        self.ui.pushButton_Cancel.clicked.connect(self.close)
        
    def closeEvent(self, evt):
        self.ui.lineEdit_Dir.clear()
        evt.accept()

class SystemCallOutputDialog(QDialog):
    def __init__(self, main):
        QDialog.__init__(self)
        self.ui = Ui_SyscallOutputDialog()
        self.ui.setupUi(self)
        self.main = main
        self.ui.pushButton_Close.clicked.connect(self.close)
        
    def closeEvent(self, evt):
        self.ui.textEdit_Output.clear()
        evt.accept()
        
class SystemCallViewScene(QGraphicsScene):
    def __init__(self, main):
        QGraphicsScene.__init__(self, main)
        self.main = main
        self.ruid = str(os.getuid())
        self.rgid = str(os.getgid())
        self.euid = str(os.geteuid())
        self.egid = str(os.getegid())
        self.processParamDlg = ProcessNodeParamDialog(main, self)
        self.codeLoadDlg = SystemCallViewCodeLoadDlg(main)
        self.codeDisplayDlg = SystemCallViewCodeDisplay(main, self)
        self.codeOutputDlg = SystemCallOutputDialog(main)
        self.codeLoadDlg.ui.pushButton_Load.clicked.connect(self.loadInCode)
        self.codeLoadDlg.ui.pushButton_OK.clicked.connect(self.confirmCode)
        self.initParam()
        
    def initParam(self):
        self.codeLoadDlg.ui.lineEdit_Dir.clear()
        self.codeFile = ''
        self.codeContent = None
        self.processNodeList = []
        self.syscallHier = {}
        
    def loadInCode(self):
        self.initParam()
        self.codeFile = QFileDialog.getOpenFileName(self.main, 'Import Program File', directory='./code', filter='(*.c);;All Files(*.*)')
        self.codeLoadDlg.ui.lineEdit_Dir.setText(self.codeFile)
        rect = QRect(0.3*self.main.geometry().width()+self.main.geometry().x(), 0.3*self.main.geometry().height()+self.main.geometry().y(), \
                        self.codeLoadDlg.rect().width(), self.codeLoadDlg.rect().height())
        self.codeLoadDlg.setWindowFlags(self.codeLoadDlg.windowFlags()|Qt.WindowStaysOnTopHint)
        self.codeLoadDlg.setGeometry(rect)
        self.codeLoadDlg.show()
        
    def confirmCode(self):
        if self.codeLoadDlg.ui.lineEdit_Dir.text() != '':
            self.codeLoadDlg.close()
            self.codeContent = self.codeDisplayDlg.readInCode(self.codeFile)
            self.codeDisplayDlg.show()
        else:
            QMessageBox.warning(self, '', 'Please input a file name!')
    
    def drawBackground(self, painter, rect):
        if self.main.sys == 'Linux':
            font = painter.font()
            font.setPointSize(20)
            painter.setFont(font)
        elif self.main.sys == 'Darwin':
            painter.setFont(QFont("Courier", 20))
        yStart = self.views()[0].verticalScrollBar().value()+20
        msg = "UIDs and GIDs are generated after invoking the attached system calls."
        ruid = 'Real UID: '+self.ruid
        rgid = 'Real GID: '+self.rgid
        rect = painter.fontMetrics().boundingRect(msg)
        rect.moveTo(20,yStart)
        painter.drawText(rect, Qt.AlignLeft, msg)
        yStart+=rect.height()+5
        rect = painter.fontMetrics().boundingRect(ruid)
        rect.moveTo(20,yStart)
        painter.drawText(rect, Qt.AlignLeft, ruid)
        yStart+=rect.height()+5
        rect = painter.fontMetrics().boundingRect(rgid)
        rect.moveTo(20,yStart)
        yStart+=rect.height()+5
        painter.drawText(rect, Qt.AlignLeft, rgid)
        '''draw effective ids'''
        euid = 'Effective UID: '+self.euid
        egid = 'Effective GID: '+self.egid
        rect = painter.fontMetrics().boundingRect(euid)
        rect.moveTo(20,yStart)
        yStart+=rect.height()+5
        painter.drawText(rect, Qt.AlignLeft, euid)
        rect = painter.fontMetrics().boundingRect(egid)
        rect.moveTo(20,yStart)
        painter.drawText(rect, Qt.AlignLeft, egid)
        QGraphicsScene.drawBackground(self,painter,QRectF(rect))
        self.main.view.viewport().update()
        
    '''Context menu when clicking process nodes'''
    def contextMenuEvent(self, evt):
        item = self.itemAt(evt.scenePos())
        self.rightClickedItem = item
        menu = QMenu()
        if item:
            if isinstance(item, ProcessNode):
                item.setSelected(True)
                self.viewProcessParam()
            menu.exec_(evt.screenPos())
    
    def viewProcessParam(self):
        self.processParamDlg.setParam(self.rightClickedItem.process.name, self.rightClickedItem.process.operandList)
        self.processParamDlg.show()
        
    '''Run program and visualize'''
    def findSystemCalls(self, line):
        temp = line.replace(' ', '')
        if temp == '' or temp[0] == '#' or temp.startwith('//'):
            return
        for i in xrange(len(self.main.systemCallList)):
            index = temp.find(self.main.systemCallList[i])
            if index != -1 and temp[index+1] == '(':
                self.callWrapperForSystemCall(i)
        
    def callWrapperForSystemCall(self, index):
        self.socket = SystemCallSocket(self.main)
#        self.socket = SystemCallQtSocket(self.main)
#        programFile = self.codeDisplayDlg.codeFile
        programFile = self.codeFile
        lastSlashIdx = programFile.rfind('/')
        lastDotIdx = programFile.rfind('.')
        if (lastDotIdx!= -1) and (lastSlashIdx < lastDotIdx):
            programFile = programFile[:programFile.rfind('.')]
        self.socket.createServerSocket(programFile)
        
    def runProgram(self):
        self.clear()
        self.syscallHier = {}
        self.callWrapperForSystemCall(0)
        
    '''visualization for system calls'''
    def updateSyscallLayout(self):
        intervalY = min(self.sceneRect().height()/len(self.syscallHier), 100)
        x, y = 0.5, 50
        for key, value in self.syscallHier.items():
            y += intervalY
            if len(value) > 1:
                intervalX = self.sceneRect().width()/(len(value)+1)
                for i in xrange(len(value)):
                    value[i].relativeX = intervalX*(i+1)/self.sceneRect().width()
                    value[i].relativeY = y
                    value[i].setPos(QPointF(value[i].relativeX*self.sceneRect().width(), value[i].relativeY))
            else:
                value[0].relativeX = 0.5
                value[0].relativeY = y
                value[0].setPos(QPointF(value[0].relativeX*self.sceneRect().width(), value[0].relativeY))
    
    def createEdgeWithParentNode(self, procnode, parent=None): 
        if not parent:    
            level = len(self.syscallHier)-1
            while level > -1:
                for n in self.syscallHier[level]:
                    if n.process.pid == procnode.process.pid:
                        parent = n
                        procnode.parent = n
                        procnode.hierlevel = level+1
                        procnode.colum = n.colum
                        level = -1
                        break
                level -= 1
        if parent:
            procnode.hierlevel = parent.hierlevel+1
            edge = EdgeItem(EdgeItem.PROCESS_CONN, parent, procnode, self.main)
            edge.setVisible(True)
            edge.startItem.edgeList.append(edge)
            edge.endItem.edgeList.append(edge)
            self.addItem(edge)
    
    def checkReturnStatus(self, syscall, status, procnode):
        #'open', 'read', 'write', 'fork', 'wait'\
        #'execl', 'execlp', 'execle', 'execv', 'execvp', 'execvpe',\
        #'setuid', 'setgid', 'seteuid', 'setegid', 'setreuid', 'setregid'
        if syscall == 'open':
            if status == '-1':
                procnode.color = procnode.failColor
            else:
                procnode.color = procnode.successColor
        elif syscall == 'read':
            if status == '-1':
                procnode.color = procnode.failColor
            else:
                procnode.color = procnode.successColor
        elif syscall == 'write':
            if status == '-1':
                procnode.color = procnode.failColor
            else:
                procnode.color = procnode.successColor
        elif syscall in ['execvp', 'execv', 'execvpe', 'execl', 'execlp']:
            if status == '-1':
                procnode.color = procnode.failColor
            else:
                procnode.color = procnode.successColor
        elif syscall in ['seteuid', 'setegid', 'setuid', 'setgid', 'setreuid', 'setregid']:
            if status == '-1':
                procnode.color = procnode.failColor
            else:
                procnode.color = procnode.successColor
        elif syscall in ['fork', 'wait']:
            if status == '-1':
                procnode.color = procnode.failColor
            else:
                procnode.color = procnode.successColor 
            
    def pass2visual(self, data):
        callinfo = syscalloutput(data)
        parentpid = callinfo[0]
        self.euid = callinfo[1]
        self.egid = callinfo[2]
        calls = callinfo[3:]
        for onecall in calls:
            syscall = onecall[0]
            ids = onecall[1]
            param = onecall[2]
            status = None
            error = 'No error'
            if len(onecall)>3:
                status = onecall[3]
            error = onecall[len(onecall)-1]
            proc, procnode = self.main.createProcessNode(syscall)
            proc.euid = ids[0]
            proc.saveduid = ids[1]
            proc.egid = ids[2]
            proc.savedgid = ids[3]
            proc.pid = param[0]
            proc.operandList = param[1:]
            proc.operandList.append(error)
            if procnode.procId > 0:
                self.createEdgeWithParentNode(procnode)
            if procnode.hierlevel<len(self.syscallHier):
                self.syscallHier[procnode.hierlevel].append(procnode)
                numElem = procnode.hierlevel
                if numElem > 0:
                    temp = []
                    for pp in self.syscallHier[numElem-1]:
                        for p in self.syscallHier[numElem]:
                            if pp == p.parent:
                                temp.append(p)
                    self.syscallHier[numElem] = temp
            else:
                self.syscallHier[len(self.syscallHier)] = [procnode]
                    
            if syscall == 'fork':
                if status != '-1':
                    proc1, procnode1 = self.main.createProcessNode('Parent')
                    proc1.euid = ids[0]
                    proc1.saveduid = ids[1]
                    proc1.egid = ids[2]
                    proc1.savedgid = ids[3]
                    proc1.pid = param[0]
                    self.createEdgeWithParentNode(procnode1, procnode)
                    
                    proc2, procnode2 = self.main.createProcessNode('Child')
                    proc2.euid = ids[0]
                    proc2.saveduid = ids[1]
                    proc2.egid = ids[2]
                    proc2.savedgid = ids[3]
                    proc2.pid = param[1]
                    self.createEdgeWithParentNode(procnode2, procnode)
                    level = len(self.syscallHier)
                    if procnode1.hierlevel == level:
                        self.syscallHier[level] = []
                    self.syscallHier[level].append(procnode1)
                    self.syscallHier[level].append(procnode2)
            self.checkReturnStatus(syscall, status, procnode)
            self.updateSyscallLayout()
            self.update()
        