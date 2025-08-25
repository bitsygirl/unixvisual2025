'''
Created on Jun 9, 2014

@author: mandy
Updated for PyQt6 compatibility
'''
from PyQt6.QtWidgets import QDialog
from PyQt6.QtCore import Qt
from Ui_SpecDialog import Ui_Dialog

class SpecDialog(QDialog):
    
    def __init__(self, main):
        super().__init__()
        self.main = main
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.setLayout(self.ui.verticalLayout)
        flags = Qt.WindowType.Dialog | Qt.WindowType.WindowStaysOnTopHint
        self.setWindowFlags(flags)
        self.ui.closePushButton.clicked.connect(self.close)

    def readSpecToDialog(self, specFile):
        txt = open(specFile).read()
        self.ui.specTextEdit.setText(txt)
        
    def closeEvent(self, evt):
        evt.accept()
