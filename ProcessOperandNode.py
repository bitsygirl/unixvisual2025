'''
Created on Jun 22, 2015

@author: manwang
'''
from PyQt4.QtGui import QGraphicsItem, QGraphicsRectItem, QBrush, QPen, QColor, QFontMetrics, QPainter, QFont
from PyQt4.QtCore import Qt, QRectF, QObject

class ProcessOperandNode(QGraphicsRectItem):

    def __init__(self, processNode, operandList, scene):
        self.processNode = processNode
        self.operandList = operandList
        self.scene = scene
        
    def setOperandValue(self, operandID, value):
        self.operandList[operandID] = value