import re


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


class QueryOutput(QPlainTextEdit):
 
    def __init__(self, scene, parent):
        QPlainTextEdit.__init__(self, parent)
        self.scene = scene
        self.queryWindow = parent
        self.setReadOnly(True)
    
#    def mouseDoubleClickEvent(self, evt):
#        if self.queryWindow.animationEnabled:
#            if self.scene.animationTimer.isActive():
#                QMessageBox.warning(None, 'Warnning', 'Stop current animation first')
#                return
#            
#        if self.queryWindow.animationEnabled:
#            text = str(self.cursorForPosition(evt.pos()).block().text())
#            
#            if re.search('query 0', text) is not None:
#                filename = re.findall('\(.*\)' ,text)[0]
#                filename = filename[1:-1]
#                self.queryWindow.runQuery0(filename)
#            elif re.search('query 1', text) is not None:
#                filename = re.findall('\(.*\)' ,text)[0]
#                filename = filename[1:-1]
#                self.queryWindow.runQuery1(filename)
#            elif re.search('query 2', text) is not None:
#                patterns = re.findall('\([^\)]*\)', text)
#                filename = patterns[0][1:-1]
#                mode = 'd'#patterns[1][1:-1]
#                self.queryWindow.runQuery2(filename, mode)
#            elif re.search('query 3', text) is not None:
#                patterns = re.findall('\([^\)]*\)', text)
#                mode = patterns[0][1:-1]
#                domain = patterns[1][1:-1]
#                self.queryWindow.runQuery3(domain, mode)
#            elif re.search('query 4', text) is not None:
#                patterns = re.findall('\([^\)]*\)', text)
#                filename1 = patterns[0][1:-1]
#                filename2 = patterns[1][1:-1]
#                mode = patterns[2][1:-1]
#                self.queryWindow.runQuery4(filename1, filename2, mode)
#            elif re.search('query 5', text) is not None:
#                filename = re.findall('\(.*\)' ,text)[0]
#                filename = filename[1:-1]
#                self.queryWindow.runQuery5(filename)
#            elif re.search('query 6', text) is not None:
#                patterns = re.findall('\([^\)]*\)', text)
#                filename = patterns[0][1:-1]
#                mode = patterns[1][1:-1]
#                self.queryWindow.runQuery6(filename, mode)
#            elif re.search('query 7', text) is not None:
#                self.queryWindow.runQuery7()
#            elif re.search('query 8', text) is not None:
#                mode = re.findall('\(.*\)' ,text)[0][1:-1]
#                self.queryWindow.runQuery8(mode)
#            elif re.search('query 9', text) is not None:
#                patterns = re.findall('\([^\)]*\)', text)
#                filename = patterns[0][1:-1]
#                domain = patterns[1][1:-1]
#                self.queryWindow.runQuery9(filename, domain)
#            elif re.search('query 10', text) is not None:
#                patterns = re.findall('\([^\)]*\)', text)
#                filename = patterns[0][1:-1]
#                domain = patterns[1][1:-1]
#                self.queryWindow.runQuery10(filename, domain)
 
                


                        
            
             