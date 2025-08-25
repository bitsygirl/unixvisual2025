'''
Created on Jun 9, 2014

@author: mandy
'''
from PyQt4.QtGui import QDialog
from PyQt4.QtCore import Qt, QString
from Ui_SpecDialog import Ui_Dialog

class SpecDialog(QDialog):
    
    def __init__(self, main):
        QDialog.__init__(self)
        self.main = main
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.setLayout(self.ui.verticalLayout)
        flags = Qt.Dialog | Qt.WindowStaysOnTopHint
        self.setWindowFlags(flags)
        self.ui.closePushButton.clicked.connect(self.close)

    def readSpecToDialog(self, specFile):
        txt = open(specFile).read()
        self.ui.specTextEdit.setText(QString(txt))
        
    def closeEvent(self, evt):
        evt.accept()