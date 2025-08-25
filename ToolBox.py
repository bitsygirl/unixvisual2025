from PyQt6.QtWidgets import (QDockWidget, QWidget, QMessageBox, QScrollArea, 
                             QFileDialog, QDialog)
from PyQt6.QtGui import QTextCursor, QTextCharFormat, QTextBlock, QTextBlockFormat, QColor
from PyQt6.QtCore import Qt, pyqtSignal, QRect
from Ui_ToolBox import *

def is_binary(filename):
    """Return true if the given filename is binary.
    @raise EnvironmentError: if the file does not exist or cannot be accessed.
    """
    if filename[filename.rfind('/')+1:].find('.') != -1:
        return False
    fin = open(filename, 'rb')
    try:
        CHUNKSIZE = 1024
        while 1:
            chunk = fin.read(CHUNKSIZE)
            if b'\0' in chunk: # found null byte - fixed for Python 3
                return True
            if len(chunk) < CHUNKSIZE:
                break # done
    finally:
        fin.close()
    return False

class RootDirEditDialog(QDialog):
    def __init__(self, main):
        super().__init__()
        self.ui = Ui_RootInputDialog()
        self.ui.setupUi(self)
        flags = Qt.WindowType.Dialog | Qt.WindowType.WindowStaysOnTopHint
        self.setWindowFlags(flags)
        self.main = main
        self.ui.OKPushButton.clicked.connect(self.readinRootDir)
        self.ui.cancelPushButton.clicked.connect(self.close)
    
    def readinRootDir(self):
        self.main.root_dir = str(self.ui.lineEdit.text())
        self.main.regenerateSpecInfo()
        self.close()
        
class ToolBoxDockWidget(QDockWidget):
    def __init__(self, parent = None):
        super().__init__('Tool Box', parent)
        self.parent = parent
        self.setFeatures(QDockWidget.DockWidgetFeature.NoDockWidgetFeatures)
        self.setAllowedAreas(Qt.DockWidgetArea.LeftDockWidgetArea)
        self.setMaximumWidth(280)
        self.setMinimumWidth(280)
        
    def resizeEvent(self, event):
        self.parent.resizeViews()
  
class ToolBox(QWidget):
    def __init__(self, main, parent = None):
        super().__init__(parent)
        self.scene = main.scene
        self.syscallScene = main.syscallViewScene
        self.main = main
        self.parent = parent
        self.ui = Ui_ToolBox()
        self.ui.setupUi(self, main)
        self.scroll = QScrollArea(self)
        self.scroll.setWidget(self.ui.gridWidget)
        self.scroll.setWidgetResizable(True)
        self.ui.btnLoadCode.clicked.connect(self.loadInCode)
        self.ui.btnConfirmCode.clicked.connect(self.confirmCode)
        self.ui.strCodePath.textChanged.connect(self.setCodeToLoad)
        
    def setCodeToLoad(self):
        self.syscallScene.codeFile = str(self.ui.strCodePath.text())
        
    def loadInCode(self):
        self.ui.strCodePath.clear()
        filename, _ = QFileDialog.getOpenFileName(self.main, 'Import Program File', 
                                               directory=self.main.specDir+'/code', 
                                               filter='All Files (*)')
        self.syscallScene.codeFile = filename
        self.ui.strCodePath.setText(self.syscallScene.codeFile)
        if not self.main.ui.actionView_ProgramTrace.isChecked():
            self.main.ui.actionView_ProgramTrace.setChecked(True)
            self.main.viewModeChanged(self.main.ui.actionView_ProgramTrace)
            
    def confirmCode(self):
        self.syscallScene.codeDisplayDlg.hide()
        OTHER_TYPE = -1
        CFILE_TYPE = 0
        BINARY_TYPE = 1
        if self.ui.strCodePath.text() != '':
            typefile = OTHER_TYPE
            if is_binary(self.syscallScene.codeFile):
                typefile = BINARY_TYPE
            elif self.syscallScene.codeFile[-2:] == '.c':
                typefile = CFILE_TYPE
            if typefile == OTHER_TYPE:
                QMessageBox.warning(self, '', 'Please select a c program source or binary file!')
                return
            elif typefile == BINARY_TYPE:
                self.syscallScene.codeContent = self.syscallScene.codeDisplayDlg.readInCode(self.syscallScene.codeFile)
                self.syscallScene.codeDisplayDlg.show()
                self.syscallScene.runProgram()
            elif typefile == CFILE_TYPE:
                self.syscallScene.codeContent = self.syscallScene.codeDisplayDlg.readInCode(self.syscallScene.codeFile)
                self.syscallScene.codeDisplayDlg.show()
                self.syscallScene.runProgram()
        else:
            QMessageBox.warning(self, '', 'Please input a file name!')
            
    def resizeEvent(self, event):
        self.scroll.setGeometry(0, 0, self.geometry().width(), self.geometry().height())
