'''

# PyQt4/PyQt6 Compatibility Shim
try:
    from PyQt6.QtCore import Qt, QObject, QPointF, QRectF, QLineF, pyqtSignal, QTimer, QRect
    from PyQt6.QtWidgets import *
    from PyQt6.QtGui import QPen, QBrush, QColor, QFont, QPainter, QPixmap, QIcon, QTransform
    USING_PYQT6 = True
except ImportError:
    from PyQt4.QtCore import Qt, QObject, QPointF, QRectF, QLineF, pyqtSignal, QTimer, QRect
    from PyQt4.QtGui import *
    USING_PYQT6 = False


Created on Jun 16, 2015

@author: manwang
'''
'''
Created on Jun 16, 2015

@author: manwang
'''
import os

class FileNode(QGraphicsPixmapItem):
    def __init__(self, dirpath, name, isFile, scene = None):
        pixmap = QPixmap()
        if isFile:
            pixmap.load("./icons/filenode.png")
            pixmap = pixmap.scaled(QSize(scene.FILENODESIZE,scene.FILENODESIZE))
        else:
            pixmap.load("./icons/OpenFile.png")
            pixmap = pixmap.scaled(QSize(scene.DIRNODESIZE,scene.DIRNODESIZE))
        QGraphicsPixmapItem.__init__(self, pixmap)
        self.setFlag(QGraphicsItem.ItemIsMovable, True)
        self.setFlag(QGraphicsItem.ItemIsSelectable, True)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges, True)
        self.scene = scene
        self.dirpath = dirpath
        self.name = name
        self.parent = None
        self.children = set()
        self.wedgeAngle = 0.0
        self.leaves = 0
        self.visited = False
        self.edgeList = []
        self.setVisible(True)
        self.relativeX, self.relativeY = 0.85, 0.5
        
    def setParent(self, p):
        self.parent = p
        
    def addChild(self, child):
        self.children.add(child)
        
    def addChildSet(self, childset):
        self.children = self.children.union(childset)
        
    def getFullPath(self):
        if self.dirpath:
            return os.path.join(self.dirpath, self.name)
        else:
            return self.name
        
    def paint(self, painter, option, widget=None):
        pen = QPen(QColor(0, 0, 0))
        pen.setWidth(1.0)
        painter.setPen(pen)
        rect = painter.fontMetrics().boundingRect(self.name)
        rect = QRect(rect.x(), rect.y(), rect.width(), rect.height()*1.2)
        x = int(rect.topLeft().x())
        y = int(rect.topLeft().y()-0.6*rect.height())
        rect.moveTo(x, y)
        painter.drawText(rect, Qt.AlignLeft, self.name)
        QGraphicsPixmapItem.paint(self, painter, option, widget)
        
    def itemChange(self, change, value):
        if change == QGraphicsItem.ItemPositionChange:
            for edge in self.edgeList:
                edge.updatePosition()
        return value 