'''
Created on Jun 22, 2015

@author: manwang
Updated for PyQt6 compatibility
'''
from PyQt6.QtWidgets import QGraphicsItem, QGraphicsEllipseItem
from PyQt6.QtGui import QBrush, QPen, QColor, QPainter, QFont
from PyQt6.QtCore import Qt, QRectF, QObject, QPointF
from EdgeItem import EdgeItem
import MyFunctions

class GeneralNode(QGraphicsEllipseItem):
    def __init__(self, main, isUserG, name):
        super().__init__(QRectF(-40,-20,80,40))
        self.isUserG = isUserG
        self.setVisible(False)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable, False)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable, True)
        self.relativeX, self.relativeY = 0.3, 0.2
        self.main = main
        self.scene = main.scene
        self.edgeList = []
        self.highlight = False
        self.name = name
        if self.isUserG:
            self.color = Qt.GlobalColor.magenta
        else:
            self.color = self.main.mediumBlue
        self.setPos(QPointF(self.relativeX*self.scene.sceneRect().width(), self.relativeY*self.scene.sceneRect().height()))
        
    def paint(self, painter, option, widget=None):
        painter.setFont(self.main.sysFont)
        brush = QBrush(self.color)
        self.setBrush(brush)
        pen = QPen(QColor(0, 0, 0))
        pen.setWidth(1)
        self.setPen(pen)
        super().paint(painter, option, widget)
        painter.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, self.name)
         
    def mousePressEvent(self, evt):
        super().mousePressEvent(evt)
             
    def mouseMoveEvent(self, evt):
        super().mouseMoveEvent(evt)
        for e in self.edgeList:
            e.updatePosition()
               
class UserNode(QGraphicsEllipseItem):
    
    def __init__(self, name, uid, gid, main):
        super().__init__(QRectF(-40,-20,80,40))
        self.setVisible(False)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable, False)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable, True)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemSendsGeometryChanges, True)
        self.normal = QColor(230, 230, 230)
        self.color = QColor(230, 230, 230)
        self.colorForOther = main.mediumBlue
        self.highlightColor = Qt.GlobalColor.red
        self.highlight = False
        self.main = main
        self.scene = main.scene
        self.name = name
        self.uid = uid
        self.gid = gid
        self.groupNodes = set()
        self.edgeList = []
        self.relativeX, self.relativeY = 0.1, 0.5
        self.setPos(QPointF(self.relativeX*self.scene.sceneRect().width(), self.relativeY*self.scene.sceneRect().height()))
        
    def addToGroup(self, group):
        groupnode = MyFunctions.getNodeFromListByName(group, self.scene.groupNodeList)
        if groupnode:
            self.groupNodes.add(groupnode)
            groupnode.addUser(self)
            e = EdgeItem(EdgeItem.USERGRP_CONN, self, groupnode, self.main)
            self.edgeList.append(e)
            groupnode.edgeList.append(e)
            self.scene.addItem(e)
        
    def removeFromGroup(self, group):
        groupnode = MyFunctions.getNodeFromListByName(group, self.scene.groupNodeList)
        if groupnode:
            self.groupNodes.remove(groupnode)
            groupnode.removeUser(self)
        
    def isMemberOfGroup(self, groupnode):
        return groupnode in self.groupNodes

    def setUID(self, uid):
        self.uid = uid
    
    def getUID(self):
        return self.uid
    
    def setGID(self, gid):
        self.gid = gid
        
    def getGID(self):
        return self.gid
        
    def paint(self, painter, option, widget=None):
        painter.setFont(self.main.sysFont)
        brush = QBrush(self.color)
        self.setBrush(brush)
        pen = QPen(QColor(0, 0, 0))
        pen.setWidth(1)
        self.setPen(pen)
        super().paint(painter, option, widget)
        rect = QRectF(self.rect().x()-2*self.rect().width(), self.rect().y(), 5*self.rect().width(), self.rect().height())
        painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, self.name)
            
    def mousePressEvent(self, evt):
        super().mousePressEvent(evt)
             
    def mouseMoveEvent(self, evt):
        super().mouseMoveEvent(evt)
        for e in self.edgeList:
            e.updatePosition()
