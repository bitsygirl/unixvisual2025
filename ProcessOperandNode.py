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


Created on Jun 22, 2015

@author: manwang
'''

class ProcessOperandNode(QGraphicsRectItem):

    def __init__(self, processNode, operandList, scene):
        self.processNode = processNode
        self.operandList = operandList
        self.scene = scene
        
    def setOperandValue(self, operandID, value):
        self.operandList[operandID] = value