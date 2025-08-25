'''
Created on Apr 20, 2015

@author: manwang
Updated for PyQt6 compatibility
'''

from PyQt6.QtCore import QRect, QRectF, Qt, QPointF, QLineF, pyqtSignal, QTimer
from PyQt6.QtWidgets import QGraphicsScene, QGraphicsView, QGraphicsEllipseItem, QGraphicsItem, QMenu
from PyQt6.QtGui import QPainter, QPen, QBrush, QColor, QTransform, QPainterPath, QFont
from GroupNode import GroupFrameNode
from UserNode import GeneralNode
import os, socket, datetime

class DiagramScene(QGraphicsScene):
    DIRNODESIZE = 30
    FILENODESIZE = 30
    
    animateUser = pyqtSignal(QGraphicsItem)
    animateGroup = pyqtSignal(QGraphicsItem)
    animateProcess = pyqtSignal(QGraphicsItem)
    animateSelfTest_Object = pyqtSignal()
    animateSelfTest_Command = pyqtSignal(QGraphicsItem)
    animateSelfTest_Program = pyqtSignal(QGraphicsItem)
    
    def __init__(self, mainWindow):
        super().__init__(mainWindow)
        self.hostname = socket.gethostname() 
        self.pid = os.getpid()
        self.date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.stuInfo = self.hostname+'.'+str(self.pid)+'.'+self.date
        self.main = mainWindow
        
        self.message = ''
        self.groupFileConnToShowID = 0
        self.prevUserGroupNodeList = None
        self.hint = ''
        self.initParam()
        
    def initParam(self):
        self.displaySeparate = True
        self.dirHier = []
        self.dirNodeList = []
        self.userNodeList = []
        self.groupNodeList = []
        self.leftClickedItem = None
        self.permClickedItem = None
        self.clickedfilen = None
        self.tempUserGeneralEdge = []
        self.tempUserOtherGeneralEdge = []
    
    def resetScreen(self):
        self.main.permissionCalDialog.tabWidget.setTabEnabled(0, True)
        self.main.setGeneralNodeEdgeVisibility(False)
        self.main.groupFrame.setVisible(False)
        for u in self.userNodeList:
            u.color = u.normal
            u.setVisible(False)
            for e in u.edgeList:
                e.setVisible(False)
        for g in self.groupNodeList:
            g.setVisible(False)
            for e in g.edgeList:
                e.setVisible(False)
        for item in self.items():
            item.highlight = False
        
    def resetTempEdgeForFileNodeSel(self):
        for e in self.tempUserGeneralEdge:
            self.removeItem(e)
            del e
        for e in self.tempUserOtherGeneralEdge:
            self.removeItem(e)
            del e
        self.tempUserGeneralEdge = []
        self.tempUserOtherGeneralEdge = []
            
    def resetNodesFrameHighlight(self):
        for i in self.userNodeList:
            i.highlight = False
        for i in self.groupNodeList:
            i.highlight = False
        if self.main.userGeneralNode:
            self.main.userGeneralNode.highlight = False
        if self.main.otherGeneralNode:
            self.main.otherGeneralNode.highlight = False
        
    def removeAllItemsInScene(self):
        self.main.setGeneralNodeEdgeVisibility(False)
        self.main.groupFrame.setVisible(False)
        for item in self.items():
            if (item not in self.main.objectViewScene.interfaceItems) and (not isinstance(item, GroupFrameNode)) and\
            (not isinstance(item, GeneralNode)) and (item!=self.main.userGeneralEdge) and (item!=self.main.otherGeneralEdge)\
            and ((item not in self.main.selfTestViewScene.interfaceQuesItems) and \
                 (item not in self.main.selfTestViewScene.interfaceTableItems)):
                self.removeItem(item)
                del item
        self.dirHier = []
        self.dirNodeList = []
        self.userNodeList = []
        self.groupNodeList = []
        
    def mousePressEvent(self, evt):
        super().mousePressEvent(evt)
            
    def mouseReleaseEvent(self, evt):
        super().mouseReleaseEvent(evt)
        self.update()
        
    def mouseMoveEvent(self, evt):
        super().mouseMoveEvent(evt)
        self.update()
        
    def drawBackground(self, painter, rect):
        if self.main.ui.actionView_User.isChecked() or self.main.ui.actionView_Group.isChecked():
            if self.dirHier:
                if self.main.sys == 'Linux':
                    font = painter.font()
                    font.setPointSize(20)
                    painter.setFont(font)
                elif self.main.sys == 'Darwin':
                    painter.setFont(QFont("Courier", 20))
                rootdir = 'Root: '+self.dirHier[0][0].getFullPath()
                self.drawListRow(rootdir, painter, 10, 20, 0.4*self.main.geometry().width())

    def wrap(self, text, width, painter):
        result = []
        if text == None or text == '':
            return result
        hasMore = True
        #The current index of the cursor
        current = 0
        #The next line break index
        lineBreak = -1
        #The space after line break
        nextSpace = -1
        while hasMore:
            while True:
                lineBreak = nextSpace
                if lineBreak == len(text) - 1:
                    hasMore = False
                    break
                else:
                    nextSpace = text[lineBreak+1:].find('/')
                    if nextSpace == -1:
                        nextSpace = len(text)-1
                    else:
                        nextSpace += lineBreak+1
                    linewidth = painter.fontMetrics().boundingRect(text[current:nextSpace]).width()
                    if linewidth > width:
                        nextSpace = lineBreak
                        break
            line = text[current: lineBreak + 1]
            result.append(line)
            current = lineBreak + 1
        return result
    
    def drawListRow(self, text, g, x, y, width):
        lines = self.wrap(text, width, g)
        for i in range(len(lines)):
            liney = y + (i * g.fontMetrics().boundingRect(text).height())
            g.drawText(x,liney, lines[i])
