'''
Created on Apr 20, 2015

@author: manwang
Updated for PyQt6 compatibility
'''
from PyQt6.QtWidgets import QGraphicsView
from PyQt6.QtGui import QPainter
from EdgeItem import EdgeItem

class DiagramView(QGraphicsView):
    
    def __init__(self, scene, parent = None):
        super().__init__(scene, parent)
        self.setRenderHint(QPainter.RenderHint.Antialiasing, True)
        
    def scrollContentsBy(self, dx, dy):
        super().scrollContentsBy(dx, dy)
        for i in self.scene().items():
            if isinstance(i, EdgeItem):
                i.setVisible(True)
                i.updatePosition()
        self.update()
