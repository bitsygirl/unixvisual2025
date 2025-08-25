'''
Created on Sep 28, 2016

@author: manw
Updated for PyQt6 compatibility
'''
import os
from PyQt6.QtCore import Qt, QObject, QPointF, QRectF, QLineF, pyqtSignal, QTimer, QRect
from PyQt6.QtWidgets import QFileDialog, QPushButton, QTreeView
from PyQt6.QtGui import QPen, QBrush, QColor, QFont, QPainter, QPixmap, QIcon, QTransform


class FileDialog(QFileDialog):
    fileChosen = pyqtSignal()
    
    def __init__(self, *args):
        super().__init__(*args)
        self.setOption(self.Option.DontUseNativeDialog, True)  # Updated enum
        self.setFileMode(self.FileMode.ExistingFiles)  # Updated enum
        btns = self.findChildren(QPushButton)
        self.openBtn = [x for x in btns if 'open' in str(x.text()).lower()][0]
        self.openBtn.clicked.disconnect()
        self.openBtn.clicked.connect(self.openClicked)
        self.tree = self.findChild(QTreeView)

    def openClicked(self):
        '''have to click the button open to emit the signal'''
        '''This means that double clicking objects will not work'''
        inds = self.tree.selectionModel().selectedIndexes()
        for i in inds:
            if i.column() == 0:
                # PyQt6: data() returns the actual data, no toString() needed
                self.selectedFiles = os.path.join(str(self.directory().absolutePath()), str(i.data()))
#                 files.append(os.path.join(str(self.directory().absolutePath()),str(i.data())))
#         self.selectedFiles = files
        self.hide()
        self.fileChosen.emit()

    def filesSelected(self):
        return self.selectedFiles
