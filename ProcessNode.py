'''
Created on Jun 4, 2015

@author: manwang
'''
from PyQt4.QtGui import QGraphicsItem, QGraphicsRectItem, QBrush, QPen, QColor, QFontMetrics, QPainter, QFont
from PyQt4.QtCore import Qt, QRectF, QObject

class Permission(object):
    owner = None
    ownerUID = -1
    ownerGID = -1
    group = set()
    world = set()
    sUIDFlag = False
    sGIDFlag = False
    
    def __init__(self, owner = None, oUID = -1, oGID = -1, group = set(), world = set(), sUIDFlag = False, sGIDFlag = False):
        self.owner = owner
        self.ownerUID = oUID
        self.ownerGID = oGID
        if group:
            self.group = group 
        if world:
            self.world = world
        self.sUIDFlag = sUIDFlag
        self.sGIDFlag = sGIDFlag
    
class Process(object):  
    def __init__(self, name = '', uid = '', gid = ''):
        self.name = name
        self.operandList = []
        self.euid = uid
        self.egid = gid
        self.saveduid = uid
        self.savedgid = gid
        self.pid = -1

    def setOperandValue(self, operandID, value):
        self.operandList[operandID] = value
        
    def getOperandValue(self, operandID):
        if operandID < len(self.operandList):
            return self.operandList[operandID]
        else:
            return None
    
class ProcessNode(QGraphicsRectItem):
    NODESIZE_X = 80
    NODESIZE_Y = 40
    NODE_BOUNDARY_SIZE = 20
    def __init__(self, main, process = Process()):
        QGraphicsRectItem.__init__(self)
        self.setVisible(True)
        self.setAcceptsHoverEvents(True)
        self.setFlag(QGraphicsItem.ItemIsMovable, True)
        self.setFlag(QGraphicsItem.ItemIsSelectable, True)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges, True)
        
        self.rectContent = QRectF(-0.5*self.NODESIZE_X, -0.5*self.NODESIZE_Y, self.NODESIZE_X, self.NODESIZE_Y)
        self.setRect(self.rectContent)
        
        self.main = main
        self.scene = main.syscallViewScene
        self.font = self.main.sysFont
        self.font.setPixelSize(main.FONT_SIZE)
        self.highlight = False
        
        self.blockcolor = QColor(255,215,0)
        self.color = self.blockcolor
        self.successColor = QColor(127, 255, 127)#light green
        self.failColor = Qt.red
        self.penColor = QColor(233, 171, 23)
#       self.labelChangeColor = QColor(125.0, 107, 0.0)
        self.labelChangeColor = Qt.red
        self.credentialText = None
        self.process = process
        self.adjustWidth = False
        self.edgeList = []
        self.procId = -1
        self.parent = None
        self.hierlevel = 0
        self.colum = 0
        self.firstNode = False
  
    def mousePressEvent(self, event):
        QGraphicsRectItem.mousePressEvent(self, event)
        self.scene.update()
        
    def mouseReleaseEvent(self, event):
        QGraphicsRectItem.mouseReleaseEvent(self, event)
        self.scene.update()
       
    def mouseMoveEvent(self, evt):
        QGraphicsRectItem.mouseMoveEvent(self, evt)
        for e in self.edgeList:
            e.updatePosition()
        self.scene.update()
         
    def computeTextColor(self):
        if self.parent == None:
            return Qt.black, Qt.black, Qt.black, Qt.black
        color1 = Qt.black
        color2 = Qt.black
        color3 = Qt.black
        color4 = Qt.black
        if self.parent.process.euid != self.process.euid:
            color1 = Qt.red
        if self.parent.process.saveduid != self.process.saveduid:
            color2 = Qt.red
        if self.parent.process.egid != self.process.egid:
            color3 = Qt.red
        if self.parent.process.savedgid != self.process.savedgid:
            color4 = Qt.red
        return color1, color2, color3, color4
            
    def paint(self, painter, option, widget=None):
        painter.save()
        '''
        draw outline and the inside block
        '''
        pen = QPen(Qt.black)
        pen.setWidth(3.0)
        self.setPen(pen)
        self.setBrush(QBrush(QColor(self.color)))
        painter.setRenderHint(QPainter.Antialiasing, True)
        QGraphicsRectItem.paint(self, painter, option, widget)
        '''
        display system call name
        '''
        pen.setColor(Qt.black)
        pen.setWidth(1.0)
        painter.setPen(pen)
        painter.setFont(self.font)
        painter.drawText(self.rect(), Qt.AlignCenter, self.process.name)
        '''
        display euid/saveduid and egid/savedgid
        '''
        if self.firstNode:
            text = 'effective: saved'
            utext = '<uid>'+self.process.euid+':'+self.process.saveduid
            gtext = '<gid>'+self.process.egid+':'+self.process.savedgid

            rect = painter.fontMetrics().boundingRect(text)
            x = int(self.rect().topRight().x()+5)
            y = int(0.8*self.rect().topRight().y())
            rect.moveTo(x, y-20)
            painter.drawText(rect, Qt.AlignLeft, text)
            rect = painter.fontMetrics().boundingRect(utext)
            x = int(self.rect().topRight().x()+5)
            y = int(0.8*self.rect().topRight().y())
            rect.moveTo(x, y)
            painter.drawText(rect, Qt.AlignLeft, utext)
            
            rect = painter.fontMetrics().boundingRect(gtext)
            rect.moveTo(x, y+20)
            painter.drawText(rect, Qt.AlignLeft, gtext)
            if self.process.operandList:
                error = self.process.operandList[-1]
                errortext = '<Return error> '+error
                rect = painter.fontMetrics().boundingRect(errortext)
                rect.moveTo(x, y+40)
                painter.drawText(rect, Qt.AlignLeft, errortext)
        else:
            utext = self.process.euid+':'+self.process.saveduid
            gtext = self.process.egid+':'+self.process.savedgid
            color1, color2, color3, color4 = self.computeTextColor()
            painter.save()
            '''euid'''
            painter.setPen(QPen(color1))
            rect = painter.fontMetrics().boundingRect(self.process.euid)
            x = int(self.rect().topRight().x()+5)
            prevx = x
            y = int(0.8*self.rect().topRight().y())
            rect.moveTo(x, y)
            painter.drawText(rect, Qt.AlignLeft, self.process.euid)
            '''the colon'''
            painter.setPen(QPen(Qt.black))
            x = int(rect.x()+rect.width())
            rect = painter.fontMetrics().boundingRect(': ')
            rect.moveTo(x, y)
            painter.drawText(rect, Qt.AlignLeft, ': ')
            '''saveduid'''
            painter.setPen(QPen(color2))
            x = int(rect.x()+rect.width())
            rect = painter.fontMetrics().boundingRect(self.process.saveduid)
            rect.moveTo(x, y)
            painter.drawText(rect, Qt.AlignLeft, self.process.saveduid)
            '''egid'''
            painter.setPen(QPen(color3))
            x = int(self.rect().topRight().x()+5)
            y += 20
            rect = painter.fontMetrics().boundingRect(self.process.egid)
            rect.moveTo(x, y)
            painter.drawText(rect, Qt.AlignLeft, self.process.egid)

            '''the color'''
            painter.setPen(QPen(Qt.black))
            x = int(rect.x()+rect.width())
            rect = painter.fontMetrics().boundingRect(': ')
            rect.moveTo(x, y)
            painter.drawText(rect, Qt.AlignLeft, ': ')
            '''savedgid'''
            painter.setPen(QPen(color4))
            x = int(rect.x()+rect.width())
            rect = painter.fontMetrics().boundingRect(self.process.savedgid)
            rect.moveTo(x, y)
            painter.drawText(rect, Qt.AlignLeft, self.process.savedgid)
            
            if self.process.operandList:
                errortext = self.process.operandList[-1]
                rect = painter.fontMetrics().boundingRect(errortext)
                rect.moveTo(prevx, y+20)
                painter.drawText(rect, Qt.AlignLeft, errortext)
            painter.restore()
        painter.restore()
        if self.highlight:
            MyFunctions.drawHighlightBox(self, painter)
            
    def hoverEnterEvent(self, evt):
        self.setToolTip('\n'.join(self.process.operandList))
        QGraphicsRectItem.hoverEnterEvent(self, evt)
    
    def hoverLeaveEvent(self, evt):
        QGraphicsRectItem.hoverLeaveEvent(self, evt)