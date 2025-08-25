'''
Created on Feb 25, 2016

@author: manwang
'''
from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import QDialog, QGraphicsScene, QFont, QGraphicsView
from PyQt4.QtCore import Qt, QRectF

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s
    
class Ui_UNIXModelAnimation(object):
    def setupUi(self, UNIXModelAnimation):
        UNIXModelAnimation.setObjectName(_fromUtf8("UNIXModelAnimation"))
        UNIXModelAnimation.resize(481, 300)
        
        vLayout = QtGui.QVBoxLayout(UNIXModelAnimation)
        groupbox1 = QtGui.QGroupBox()
        vLayout1 = QtGui.QVBoxLayout(groupbox1)
        label1 = QtGui.QLabel()
        label1.setObjectName(_fromUtf8("label1"))
        label1.setText("Would you like an introduction to UNIX Permission Model?")

        hLayout1 = QtGui.QHBoxLayout()
        self.rbtnYes1 = QtGui.QRadioButton("Yes")
        self.rbtnYes1.setChecked(True)
        self.rbtnNo1 = QtGui.QRadioButton("No")
        hLayout1.addWidget(self.rbtnYes1)
        hLayout1.addWidget(self.rbtnNo1)
        vLayout1.addWidget(label1)
        vLayout1.addLayout(hLayout1)


        groupbox2 = QtGui.QGroupBox()
        vLayout2 = QtGui.QVBoxLayout(groupbox2)
        label2 = QtGui.QLabel()
        label2.setObjectName(_fromUtf8("label2"))
        label2.setText("Would you like the basic model introduction or details with system mechanism included?")
        hLayout2 = QtGui.QHBoxLayout()
        self.rbtnYes2 = QtGui.QRadioButton("Yes")
        self.rbtnNo2 = QtGui.QRadioButton("No")
        self.rbtnNo2.setChecked(True)
        hLayout2.addWidget(self.rbtnYes2)
        hLayout2.addWidget(self.rbtnNo2)
        vLayout2.addWidget(label2)
        vLayout2.addLayout(hLayout2)
        
        hLayout3 = QtGui.QHBoxLayout()
        self.pushButton_OK = QtGui.QPushButton()
        self.pushButton_OK.setObjectName(_fromUtf8("pushButton_OK"))
        self.pushButton_Cancel = QtGui.QPushButton()
        self.pushButton_Cancel.setObjectName(_fromUtf8("pushButton_Cancel"))
        hLayout3.addWidget(self.pushButton_OK)
        hLayout3.addWidget(self.pushButton_Cancel)
        
        vLayout.addWidget(groupbox1)
        vLayout.addWidget(groupbox2)
        vLayout.addLayout(hLayout3)
        self.retranslateUi(UNIXModelAnimation)
        QtCore.QMetaObject.connectSlotsByName(UNIXModelAnimation)

    def retranslateUi(self, UNIXModelAnimation):
        UNIXModelAnimation.setWindowTitle(QtGui.QApplication.translate("UNIXModelAnimation", "UNIX Model Tutorial", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_OK.setText(QtGui.QApplication.translate("UNIXModelAnimation", "OK", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_Cancel.setText(QtGui.QApplication.translate("UNIXModelAnimation", "Cancel", None, QtGui.QApplication.UnicodeUTF8))
        
class UNIXModelAnimation(QDialog):

    def __init__(self, main):
        QDialog.__init__(self)
        self.setVisible(False)
        self.ui = Ui_UNIXModelAnimation()
        self.ui.setupUi(self)
        flags = Qt.Dialog | Qt.WindowStaysOnTopHint
        self.setWindowFlags(flags)
        self.main = main
        self.tutorialOn = True
        self.tutorialDetail = False
        self.ui.pushButton_OK.clicked.connect(self.readTutorialSettings)
        self.ui.pushButton_Cancel.clicked.connect(self.close)
        
    def readTutorialSettings(self):
        if self.ui.rbtnYes1.isChecked():
            self.tutorialOn = True
        else:
            self.tutorialOn = False
        if self.ui.rbtnYes2.isChecked():
            self.tutorialDetail = True
        else:
            self.tutorialDetail = False
        self.main.showModelTutorial(self.tutorialOn, self.tutorialDetail)
        self.close()


class TutorialAnimationView(QGraphicsView):

    def __init__(self, main):
        QGraphicsView.__init__(self, main)
        self.main = main
  
class TutorialAnimationScene(QGraphicsScene):
    
    def __init__(self, main):
        QGraphicsScene.__init__(self, main)
        self.main = main
        self.font = QFont("Courier", 30, QFont.Bold)
#         self.view = TutorialAnimationView(self, self.centralWidget())
#         self.view.setScene(self.scene)
#         self.view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
#         self.view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.initParam()
        
    def resize(self):
        pass
    
    def clearScreen(self):
        self.message = ''
        self.clear()
        
    def drawBackground(self, painter, rect):
        painter.setFont(self.main.scene.rootfont)
        yStart = self.views()[0].verticalScrollBar().value()+20
        rect = painter.fontMetrics().boundingRect(self.message)
        rect.moveTo(20,yStart)
        painter.drawText(rect, Qt.AlignLeft, self.message)
        QGraphicsScene.drawBackground(self,painter,QRectF(rect))
        self.update()
        
    def initParam(self):
        self.message = 'testing this view'
    
    def startAnimation(self, detailMode):
        self.initParam()