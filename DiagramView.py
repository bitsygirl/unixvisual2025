'''
Created on Apr 20, 2015

@author: manwang
'''
from PyQt4.QtGui import QGraphicsView, QPainter
from EdgeItem import EdgeItem

class DiagramView(QGraphicsView):
    
    def __init__(self, scene, parent = None):
        QGraphicsView.__init__(self, scene, parent)
        self.setRenderHint(QPainter.HighQualityAntialiasing, True)
        
    def scrollContentsBy(self, dx, dy):
        QGraphicsView.scrollContentsBy(self, dx, dy)
        for i in self.scene().items():
            if isinstance(i, EdgeItem):
                i.setVisible(True)
                i.updatePosition()
        self.update()