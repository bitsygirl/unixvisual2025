'''
Created on Jul 26, 2015

@author: manwang
'''
from PyQt4.QtCore import Qt
from PyQt4.QtGui import QDialog, QMessageBox, QFileDialog
from Ui_CodeDialog import Ui_CodeDialog
from subprocess import call

class SystemCallViewCodeDisplay(QDialog):
    
    def __init__(self, main, scene):
        QDialog.__init__(self)
        self.main = main
        self.ui = Ui_CodeDialog()
        self.ui.setupUi(self)
        self.setLayout(self.ui.verticalLayout)
        flags = Qt.Dialog# | Qt.WindowStaysOnTopHint
        self.setWindowFlags(flags)
        self.ui.closePushButton.clicked.connect(self.close)
        self.ui.savePushButton.clicked.connect(self.saveCode)
#         self.ui.runPushButton.clicked.connect(scene.runProgram)
        self.ui.runPushButton.clicked.connect(self.openDifferentCodeFile)
        self.syscallScene = scene
        self.codeFile = None
        
    def compileCode(self, codeFile):
        exeFile = codeFile[:codeFile.rfind('.')]
#         import os.path
#         if not os.path.exists(exeFile):
        call(["gcc", "-o", exeFile, codeFile, "-L./policies/code", "-lunixvisualwrap"])
    
    def openDifferentCodeFile(self):
        codeFile = QFileDialog.getOpenFileName(self.main, 'Import Program File', directory='./code', filter='(*.c);;All Files(*.*)')
        codeFile = str(codeFile)
        import os.path
        if os.path.exists(codeFile):
            self.readInCode(codeFile)
        
    def readInCode(self, codeFile):
        self.codeFile = str(codeFile)
        index = self.codeFile.rfind('/')
        name = self.codeFile[index+1:]
        self.setWindowTitle(name)
        self.compileCode(self.codeFile)
        if codeFile[-2:]=='.c':
            self.sourceFile = self.codeFile
        else:
            self.sourceFile = self.codeFile+'.c'
        lines = [line.rstrip('\n') for line in open(self.sourceFile)]
        content = '\n'.join(lines)
        self.ui.codeEdit.setPlainText(content)
        return lines
        
    def saveCode(self):
        f = open(self.syscallScene.codeFile, 'w')
        f.write(str(self.ui.codeEdit.toPlainText()))
        f.close()
        self.compileCode(self.sourceFile)
        self.main.syscallViewScene.runProgram()
        QMessageBox.information(self, 'Information', "The changes have been saved!", buttons = QMessageBox.Ok)