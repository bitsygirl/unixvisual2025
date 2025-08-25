'''
Created on Jun 22, 2015

@author: manwang
Updated for PyQt6 compatibility
'''
from PyQt6.QtWidgets import QGraphicsItem, QGraphicsRectItem
from PyQt6.QtGui import QBrush, QPen, QColor, QPainter, QFont
from PyQt6.QtCore import Qt, QRectF, QObject, QPointF
import MyFunctions

class GroupFrameNode(QGraphicsRectItem):
    
    def __init__(self, main):
        super().__init__(QRectF(-40,-20,200,200))
        self.setVisible(False)
        self.setBrush(Qt.GlobalColor.lightGray)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable, False)
        self.relativeX, self.relativeY = 0, 0
        self.main = main
        
    def paint(self, painter, option, widget=None):
        painter.setFont(self.main.sysFont)
        pen = QPen(Qt.GlobalColor.lightGray)
        pen.setWidth(1.0)
        self.setPen(pen)
        super().paint(painter, option, widget)
        rect = QRectF(self.rect().x(), self.rect().y()-0.5*self.rect().height()-10, self.rect().width(), self.rect().height())
        painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, "Groups")
        
class GroupNode(QGraphicsRectItem):
    
    def __init__(self, name, gid, main):
        super().__init__(QRectF(-40,-20,80,40))
        self.setVisible(False)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable, False)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable, True)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemSendsGeometryChanges, True)
        brush = QBrush(QColor(255, 255, 0))
        self.setBrush(brush)
        self.edgeList = [] 
        self.main = main
        self.scene = main.scene
        self.name = name
        self.gid = gid
        self.highlight = False
        self.userNodes = set()
        self.relativeX, self.relativeY = 0.3, 0.5
        self.setPos(QPointF(self.relativeX*self.scene.sceneRect().width(), self.relativeY*self.scene.sceneRect().height()))
        
    def addUser(self, user):
        self.userNodes.add(user)

    def removeUser(self, user):
        self.userNodes.remove(user)
        
    def checkUserNode(self, user):
        return user in self.userNodes
    
    def checkUserName(self, uname):
        for u in self.userNodes:
            if u.name == uname:
                return True
        return False
    
    def setGID(self, gid):
        self.gid = gid
        
    def getGID(self):
        return self.gid
        
    def paint(self, painter, option, widget=None):
        painter.setFont(self.main.sysFont)
        pen = QPen(QColor(0, 0, 0))
        pen.setWidth(1.0)
        self.setPen(pen)
        super().paint(painter, option, widget)
        rect = QRectF(self.rect().x()-2*self.rect().width(), self.rect().y(), 5*self.rect().width(), self.rect().height())
        painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, self.name)
        
    def mouseMoveEvent(self, evt):
        super().mouseMoveEvent(evt)
        for e in self.edgeList:
            e.updatePosition()
