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


Created on Jun 4, 2015

@author: manwang
'''
from unixpolicy import unixpolicy

class DiagramIOHelper(object):
    def __init__(self, main):
        self.main = main
        
    def importSpec(self, filename):
        self.main.initParam()
        try:
            self.main.isUNIX_flag, self.main.root_dir, self.main.user_group_mat, mat1, mat2 = unixpolicy(str(filename))
            if self.main.isUNIX_flag:
                self.main.obj_cred_mat, self.main.obj_perm_mat = mat1, mat2
            else:
                self.main.user_obj_perm_mat, self.main.group_obj_perm_mat = mat1, mat2
        except Exception as e:
            QMessageBox.critical(self.main, 'Error', str(e))
            return -1
        import os
        path = os.path.normpath(str(filename))
        index = path.rfind('/')
        self.main.specFileName = path[index+1:]
        self.main.specDir = path[:index]
        self.main.regenerateSpecInfo(path)
        return 0
    
    def exportSpec(self, filename):
        pass
    
    def readVis(self):
        pass
    
    def writeVis(self):
        pass