'''
Created on Jun 16, 2015

@author: manwang
Updated for PyQt6 compatibility
'''
from PyQt6.QtGui import QTransform, QPen, QColor, QFontMetrics, QPainterPath, QBrush, QFont
from PyQt6.QtWidgets import QGraphicsItem, QGraphicsEllipseItem, QGraphicsTextItem
from PyQt6.QtCore import Qt, QRectF, QObject, QSize, QRect, QPoint
import os, math
import MyFunctions, PermissionChecker

def setFontForUI(widget, size=20):
        import platform
        operSys = platform.system()
        if operSys == 'Linux':
            font = widget.font()
            font.setPointSize(size)
            widget.setFont(font)
        elif operSys == 'Darwin':
            font = QFont('Lucida Grande', size)
            widget.setFont(font)
        
class FileNodeTextItem(QGraphicsTextItem):
    def __init__(self, name, parent, main):
        super().__init__(name, parent)
        self.parent = parent
        setFontForUI(self, 19)
        self.setAcceptHoverEvents(True)
        
    def hoverEnterEvent(self, evt):
        self.setToolTip("<font size=\"5\">%s</font>"%self.parent.getFullPath())
        super().hoverEnterEvent(evt)
        
    def hoverLeaveEvent(self, evt):
        super().hoverLeaveEvent(evt)
        
class FileNode(QGraphicsEllipseItem):
    DIST_NODE_TEXT = 5
    LEN_SHORTFILENAME = 20
    FOREST_GREEN = QColor(34,139,34)
    
    def __init__(self, dirpath, name, isFile, main = None, specNode = False):
        super().__init__()
        self.setRect(-5,-5,10,10)
        self.isFile = isFile
        if isFile:
            self.color = QColor(255, 127, 127)
        else:
            self.color = QColor(127, 255, 127)
        self.pen = QPen(Qt.GlobalColor.black)
        self.pen.setWidth(2)  # Fixed: changed from 2.0 to 2
        self.pen.setCosmetic(True)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable, True)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable, False)
        self.setAcceptHoverEvents(True)
        self.main = main
        self.scene = main.scene
        self.dirpath = dirpath
        self.name = name
        self.displayName = self.getDisplayName()
        self.parent = None
        self.children = set()
        self.wedgeAngle = 0.0
        self.angle = 0.0
        self.leaves = 0
        self.visited = False
        self.accessible = -1 #-2 means denied
        self.edgeList = []
        self.setVisible(False)
        self.relativeX, self.relativeY = 0.85, 0.5
        self.fullpath = self.getFullPath()
        self.groupAccessibleColor = QColor(255, 255, 0)#1
        self.userAccessibleColor = Qt.GlobalColor.magenta#0
        self.otherAccessibleColor = self.main.mediumBlue#2
        self.permAccessibleColor = MyFunctions.EMERALD#3
        self.permset = set()
        self.highlight = False
        self.passedHiglight = False
        self.specNode = specNode
        self.specChildren = set()
        self.permInfo = None
        
    def setParent(self, p):
        self.parent = p
        
    def addChild(self, child):
        self.children.add(child)
        
    def addChildSet(self, childset):
        self.children = self.children.union(childset)
        
    def getDisplayName(self):
        if len(self.name)>self.LEN_SHORTFILENAME:
            displayName = self.name[:self.LEN_SHORTFILENAME]+'..'
        else:
            displayName = self.name
        return displayName
        
    def getFullPath(self):
        import re
        if self.isFile:
            sign = ''
        else:
            sign = '/'
        if self.dirpath:
            return re.sub('/+', '/', os.path.join(self.dirpath, self.name)+sign)
        else:
            return re.sub('/+', '/', self.name)
        
    def paint(self, painter, option, widget=None):
        if self.accessible == 0:
            self.setBrush(self.userAccessibleColor)
        elif self.accessible == 1:
            self.setBrush(self.groupAccessibleColor)
        elif self.accessible == 2:
            self.setBrush(self.otherAccessibleColor)
        elif self.accessible == 3:
            self.setBrush(self.permAccessibleColor)
        else:
            self.setBrush(self.color)
        
        setFontForUI(painter, 19)
        if self.highlight:
            if self.passedHiglight:
                self.setPen(QPen(self.FOREST_GREEN))
            else:
                self.setPen(QPen(Qt.GlobalColor.red))
        else:
            self.setPen(QPen(Qt.GlobalColor.black))
        name = self.displayName
        super().paint(painter, option, widget)
        
        if self.parent:
            rect = painter.fontMetrics().boundingRect(name)
            rect = QRectF(rect.x(), rect.y(), rect.width()+5, rect.height())
            angle = self.angle*180/math.pi
            halfview = 0.5*self.scene.sceneRect().width()
            if self.relativeX >=halfview and self.relativeY >= 0:
                x = self.rect().x()+3*self.DIST_NODE_TEXT
                y =  self.rect().y()
                rect.moveTo(x,y)
                painter.rotate(-angle)
                painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, name)
                painter.rotate(angle)
            elif self.relativeX < halfview and self.relativeY > 0:
                x = self.rect().x()-rect.width()-self.DIST_NODE_TEXT
                y =  self.rect().y()
                angle +=180
                rect.moveTo(x,y)
                painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, name)
            elif self.relativeX > halfview and self.relativeY < 0:
                x = self.rect().x()+3*self.DIST_NODE_TEXT
                y =  self.rect().y()
                rect.moveTo(x,y)
                painter.rotate(-angle)
                painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, name)
                painter.rotate(angle)
            else:
                x = self.rect().x()-rect.width()-self.DIST_NODE_TEXT
                y =  self.rect().y()
                angle +=180
                rect.moveTo(x,y)
                painter.rotate(-angle)
                painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, name)
                painter.rotate(angle)
        else:
            rect = painter.fontMetrics().boundingRect('Root')
            x = int(self.rect().topLeft().x())
            y = int(self.rect().topLeft().y()-20)
            rect.moveTo(x, y)
            painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, 'Root')
        
        if self.highlight:
            if self.passedHiglight:
                MyFunctions.drawHighlightBox(self, painter, self.FOREST_GREEN)
            else:
                MyFunctions.drawHighlightBox(self, painter, Qt.GlobalColor.red)
            
    def hoverEnterEvent(self, evt):
        if self.permset:
            self.setToolTip("<font size=\"5\">%s</font>"%('Permissions: '+','.join(self.permset)+'\n'+self.getFullPath()))
        else:
            self.setToolTip("<font size=\"5\">%s</font>"%self.getFullPath())
        super().hoverEnterEvent(evt)
        
    def hoverLeaveEvent(self, evt):
        super().hoverLeaveEvent(evt)
        
    def itemChange(self, change, value):
        if change == QGraphicsItem.GraphicsItemChange.ItemPositionChange:
            for edge in self.edgeList:
                edge.updatePosition()
        return value
