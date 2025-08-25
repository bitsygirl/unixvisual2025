'''
Accessible Access Control 1.0
2012-2104 Michigan Technological University
Supported in part by NSF grants: DUE-1140512, DUE-1245310 and IIS-1319363
Developer: Yifei Li
Updated for PyQt6 compatibility
Advisors:Dr. Steve Carr, Dr. Jean Mayo, Dr. Ching-Kuang Shene and Dr. Chaoli Wang
'''
'''
Created on Dec 20, 2011

@author: yifli
'''

from PyQt6.QtWidgets import (QGraphicsLineItem, QMessageBox, QInputDialog, 
                             QGraphicsItem)
from PyQt6.QtGui import (QPen, QBrush, QPolygonF, QPainter, QPainterPath, 
                         QColor, QFontMetricsF, QTransform)
from PyQt6.QtCore import Qt, QLineF, QPointF, QRectF, QPropertyAnimation, pyqtProperty, QBasicTimer, QObject
import MyFunctions
import math, time
import PermissionChecker
from ProcessNode import ProcessNode

class EdgeObjectType(QObject):
    def __init__(self, edgeItem):
        super().__init__()
        self.edgeItem = edgeItem
        self.startItem = edgeItem.startItem
        self.endItem = edgeItem.endItem
        
    @pyqtProperty(QPointF)
    def endPoint(self):
        l = self.edgeItem.line()
        return l.p2()
         
    @endPoint.setter
    def endPoint(self, pt):
        l = self.edgeItem.line()
        l.setP2(pt)
        self.edgeItem.setLine(l)
            
class EdgeItem(QGraphicsLineItem):

    USERFUNC_CONN = 0
    FUNCFILE_CONN  =1
    FILE_CONN = 2
    USERGRP_CONN = 3
    GRPFILE_CONN = 4
    GENERAL_CONN = 5
    PROCESS_CONN = 6
    FILESEL_CONN = 7
    
    EDGE_WIDTH = 2
    
    def __init__(self, linetype, start, end, main):
        super().__init__()
        self.main = main
        self.scene = main.scene
        self.selectionOffset = 20
        self.arrowSize = 20
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable)
        self.type = linetype
        self.startItem = start
        self.endItem = end
        self.description = ''
        self.setZValue((-1000.0))
        self.highlight = False   
        self.selectionPolygon = None
        
        if self.type == self.FILE_CONN or self.type == self.PROCESS_CONN:
            self.setVisible(True)
            self.eObjType = None
        elif self.type == self.USERGRP_CONN or self.type == self.GRPFILE_CONN:
            self.eObjType = EdgeObjectType(self)
            self.setVisible(False)
            
    def startAnimation(self):
        if self.eObjType:
            if self.main.ui.actionView_User.isChecked():
                if self.type == self.USERGRP_CONN:
                    self.scene.groupFileConnToShowID = 0
                    self.scene.hint = 'Group'
                self.setLine(QLineF(self.startItem.pos(), self.endItem.pos()))
                # Note: Animation functionality would need QPropertyAnimation setup
                # self.eObjType.animation.setStartValue(self.startItem.pos())
                # self.eObjType.animation.setEndValue(self.endItem.pos())
                # self.eObjType.animation.start()
    
    def stopAnimation(self):
        if self.eObjType:
            # self.eObjType.animation.stop()
            pass
        
    def animationFinished(self):
        if self.type == self.USERGRP_CONN and self.scene.groupFileConnToShowID == 0:
            self.scene.prevUserGroupNodeList = list(self.startItem.groupNodes)
            gnode = self.scene.prevUserGroupNodeList[self.scene.groupFileConnToShowID]
            gnode.setVisible(True)
            for e in gnode.edgeList:
                if e.type == self.GRPFILE_CONN:
                    e.setVisible(True)
                    e.startAnimation()
            self.scene.groupFileConnToShowID += 1
        elif self.type == self.GRPFILE_CONN and self.scene.groupFileConnToShowID<len(self.scene.prevUserGroupNodeList):
            PermissionChecker.checkUserPermForFileViaGroup(self.scene.prevUserGroupNodeList[self.scene.groupFileConnToShowID-1], self.scene)
            self.scene.update()
            gnode = self.scene.prevUserGroupNodeList[self.scene.groupFileConnToShowID]
            gnode.setVisible(True)
            for e in gnode.edgeList:
                if e.type == self.GRPFILE_CONN:
                    e.setVisible(True)
                    e.startAnimation()
            self.scene.groupFileConnToShowID += 1
        elif self.type == self.GRPFILE_CONN and self.scene.groupFileConnToShowID==len(self.scene.prevUserGroupNodeList):
            PermissionChecker.checkUserPermForFileViaGroup(self.scene.prevUserGroupNodeList[self.scene.groupFileConnToShowID-1], self.scene)
            self.scene.update()
            time.sleep(2)
            self.main.continuePermissionOther.emit()
            
    def createSelectionPolygon(self):
        pi = 3.141592653589793238463
        angle = self.line().angle()
        radAngle = angle*pi/180
        dx = self.selectionOffset * math.sin(radAngle)
        dy = self.selectionOffset * math.cos(radAngle)
        halfoffset = 0.5*self.selectionOffset
        if dx == 0 or dy == 0:
            dx, dy = halfoffset, halfoffset 
        offset1 = QPointF(dx, dy)
        offset2 = QPointF(-dx, -dy)
        nPolygon = QPolygonF([self.line().p1() + offset1, self.line().p1() + offset2,
                             self.line().p2() + offset2, self.line().p2() + offset1])
        self.selectionPolygon = nPolygon
        self.update()

    def shape(self):  
        c1, c2 = MyFunctions.computeControlPointForBezierCurve(self.startItem, self.endItem, self.type == self.FILE_CONN)
        myPath = QPainterPath()
        myPath.moveTo(self.startItem.pos())
        myPath.cubicTo(c1, c2, self.endItem.pos())
        return myPath
    
    def paint(self, painter, option, widget=None):
        if self.startItem.collidesWithItem(self.endItem):
            return
         
        if not self.startItem.isVisible() or not self.endItem.isVisible():
            return 
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        pen = QPen(Qt.PenStyle.SolidLine)
        pen.setWidth(2)  # FIXED: Changed from 2.0 to 2 (PyQt6 requires int)
        pen.setColor(Qt.GlobalColor.lightGray)
        painter.setPen(pen)
        if self.main.ui.actionView_Object.isChecked():
            self.setLine(QLineF(self.startItem.pos(), self.endItem.pos()))
            painter.drawLine(self.line())
        else:
            painter.drawPath(self.shape()) #for beizercurve    

    def updatePosition(self):
        line = QLineF(self.mapFromItem(self.startItem, QPointF(0, 0)), self.mapFromItem(self.endItem, QPointF(0, 0)))
        self.setLine(line)
