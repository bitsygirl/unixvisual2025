'''
Created on Apr 16, 2015

@author: manwang
Updated for PyQt6 and Python 3.12+ compatibility
'''
import sys
from PyQt6.QtWidgets import QApplication, QDialog
from PyQt6.QtCore import QCoreApplication, Qt
from MainWindow import MainWindow
from Ui_Greeting import Ui_Greeting
from AnswerCrypto import AnswerCrypto

class GreetingWindow(QDialog):
    def __init__(self, main):
        super().__init__()
        self.ui = Ui_Greeting()
        self.ui.setupUi(self)
        flags = Qt.WindowType.Dialog | Qt.WindowType.WindowStaysOnTopHint
        self.setWindowFlags(flags)
        self.ui.pushButton.clicked.connect(main.closeGreeting)
        
def main():
    app = QApplication(sys.argv)
    QCoreApplication.setApplicationName('UNIXvisual')
    QCoreApplication.setApplicationVersion('1.0')
    
    # Note: 'plastique' style is deprecated, using default or 'Fusion'
    # QApplication.setStyle('Fusion')  # Modern alternative to plastique
    
    app.setStyleSheet("""QToolTip {
                        background-color: white;
                        color: black;
    }""")
    
    mainw = MainWindow()
    mainw.greetWin = GreetingWindow(mainw)
    mainw.greetWin.show()
    mainw.show()
    
    exitcode = app.exec()  # Removed underscore - deprecated in PyQt6
    sys.exit(exitcode)
 
if __name__ == '__main__':
    main()
