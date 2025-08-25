'''
Created on Sep 28, 2016

@author: manw
'''
from PyQt4 import QtGui
from PyQt4.QtCore import pyqtSignal
import os


class FileDialog(QtGui.QFileDialog):
    fileChosen = pyqtSignal()
    def __init__(self, *args):
        QtGui.QFileDialog.__init__(self, *args)
        self.setOption(self.DontUseNativeDialog, True)
        self.setFileMode(self.ExistingFiles)
        btns = self.findChildren(QtGui.QPushButton)
        self.openBtn = [x for x in btns if 'open' in str(x.text()).lower()][0]
        self.openBtn.clicked.disconnect()
        self.openBtn.clicked.connect(self.openClicked)
        self.tree = self.findChild(QtGui.QTreeView)

    def openClicked(self):
        'have to click the button open to emit the signal'
        'This means that double clicking objects will not work'
        inds = self.tree.selectionModel().selectedIndexes()
        for i in inds:
            if i.column() == 0:
                self.selectedFiles = os.path.join(str(self.directory().absolutePath()),str(i.data().toString()))
#                 files.append(os.path.join(str(self.directory().absolutePath()),str(i.data().toString())))
#         self.selectedFiles = files
        self.hide()
        self.fileChosen.emit()

    def filesSelected(self):
        return self.selectedFiles