'''
Created on Apr 16, 2015

@author: manwang
'''
import sys
from PyQt4.QtGui import QApplication, QDialog
from PyQt4.QtCore import QCoreApplication, Qt
from MainWindow import MainWindow
from Ui_Greeting import Ui_Greeting
from AnswerCrypto import AnswerCrypto

class GreetingWindow(QDialog):
    def __init__(self, main):
        QDialog.__init__(self)
        self.ui = Ui_Greeting()
        self.ui.setupUi(self)
        flags = Qt.Dialog | Qt.WindowStaysOnTopHint
        self.setWindowFlags(flags)
        self.ui.pushButton.clicked.connect(main.closeGreeting)
        
def main():
    app = QApplication(sys.argv)
    QCoreApplication.setApplicationName('UNIXvisual')
    QCoreApplication.setApplicationVersion('1.0')
       
    QApplication.setStyle('plastique')
    app.setStyleSheet("""QToolTip {
                        background-color:white;
                        color:black;
    }""")
    
    mainw = MainWindow()
    mainw.greetWin = GreetingWindow(mainw)
    mainw.greetWin.show()
    mainw.show()
    
    exitcode = app.exec_()
    sys.exit(exitcode)
 
if __name__ == '__main__':
    main()