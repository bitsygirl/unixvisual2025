'''
Created on Jun 22, 2015

@author: manwang
'''
from PyQt4.QtGui import QGraphicsItem, QGraphicsEllipseItem, QBrush, QPen, QColor, QFontMetrics, QPainter, QFont
from PyQt4.QtCore import Qt, QRectF, QObject, QPointF
from EdgeItem import EdgeItem
import MyFunctions

class GeneralNode(QGraphicsEllipseItem):
    def __init__(self, main, isUserG, name):
        QGraphicsEllipseItem.__init__(self, QRectF(-40,-20,80,40))
        self.isUserG = isUserG
        self.setVisible(False)
        self.setFlag(QGraphicsItem.ItemIsMovable, False)
        self.setFlag(QGraphicsItem.ItemIsSelectable, True)
        self.relativeX, self.relativeY = 0.3, 0.2
        self.main = main
        self.scene = main.scene
        self.edgeList = []
        self.highlight = False
        self.name = name
        if self.isUserG:
            self.color = Qt.magenta
        else:
            self.color = self.main.mediumBlue
        self.setPos(QPointF(self.relativeX*self.scene.sceneRect().width(), self.relativeY*self.scene.sceneRect().height()))
        
    def paint(self, painter, option, widget=None):
        painter.setFont(self.main.sysFont)
        brush = QBrush(self.color)
        self.setBrush(brush)
        pen = QPen(QColor(0, 0, 0))
        pen.setWidth(1.0)
        self.setPen(pen)
        QGraphicsEllipseItem.paint(self, painter, option, widget)
        painter.drawText(self.rect(), Qt.AlignCenter, self.name)
#         if self.highlight:
#             MyFunctions.drawHighlightBox(self, painter, Qt.red)
         
    def mousePressEvent(self, evt):
        QGraphicsEllipseItem.mousePressEvent(self, evt)
             
    def mouseMoveEvent(self, evt):
        QGraphicsEllipseItem.mouseMoveEvent(self, evt)
        for e in self.edgeList:
            e.updatePosition()
               
class UserNode(QGraphicsEllipseItem):
    
    def __init__(self, name, uid, gid, main):
        QGraphicsEllipseItem.__init__(self, QRectF(-40,-20,80,40))
        self.setVisible(False)
        self.setFlag(QGraphicsItem.ItemIsMovable, False)
        self.setFlag(QGraphicsItem.ItemIsSelectable, True)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges, True)
        self.normal = QColor(230, 230, 230)
        self.color = QColor(230, 230, 230)
        self.colorForOther = main.mediumBlue
        self.highlightColor = Qt.red
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
        pen.setWidth(1.0)
        self.setPen(pen)
        QGraphicsEllipseItem.paint(self, painter, option, widget)
        rect = QRectF(self.rect().x()-2*self.rect().width(), self.rect().y(), 5*self.rect().width(), self.rect().height())
        painter.drawText(rect, Qt.AlignCenter, self.name)
#         if self.highlight:
#             MyFunctions.drawHighlightBox(self, painter, Qt.red)
            
    def mousePressEvent(self, evt):
        QGraphicsEllipseItem.mousePressEvent(self, evt)
             
    def mouseMoveEvent(self, evt):
        QGraphicsEllipseItem.mouseMoveEvent(self, evt)
        for e in self.edgeList:
            e.updatePosition()