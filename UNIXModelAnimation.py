'''
Created on Feb 25, 2016

@author: manwang
Updated for PyQt6 compatibility
'''

from PyQt6 import QtCore, QtWidgets
from PyQt6.QtWidgets import QDialog, QGraphicsView, QGraphicsScene
from PyQt6.QtCore import Qt, QRectF
from PyQt6.QtGui import QFont
    
class Ui_UNIXModelAnimation(object):
    def setupUi(self, UNIXModelAnimation):
        UNIXModelAnimation.setObjectName("UNIXModelAnimation")
        UNIXModelAnimation.resize(481, 300)
        
        vLayout = QtWidgets.QVBoxLayout(UNIXModelAnimation)
        groupbox1 = QtWidgets.QGroupBox()
        vLayout1 = QtWidgets.QVBoxLayout(groupbox1)
        label1 = QtWidgets.QLabel()
        label1.setObjectName("label1")
        label1.setText("Would you like an introduction to UNIX Permission Model?")

        hLayout1 = QtWidgets.QHBoxLayout()
        self.rbtnYes1 = QtWidgets.QRadioButton("Yes")
        self.rbtnYes1.setChecked(True)
        self.rbtnNo1 = QtWidgets.QRadioButton("No")
        hLayout1.addWidget(self.rbtnYes1)
        hLayout1.addWidget(self.rbtnNo1)
        vLayout1.addWidget(label1)
        vLayout1.addLayout(hLayout1)

        groupbox2 = QtWidgets.QGroupBox()
        vLayout2 = QtWidgets.QVBoxLayout(groupbox2)
        label2 = QtWidgets.QLabel()
        label2.setObjectName("label2")
        label2.setText("Would you like the basic model introduction or details with system mechanism included?")
        hLayout2 = QtWidgets.QHBoxLayout()
        self.rbtnYes2 = QtWidgets.QRadioButton("Yes")
        self.rbtnNo2 = QtWidgets.QRadioButton("No")
        self.rbtnNo2.setChecked(True)
        hLayout2.addWidget(self.rbtnYes2)
        hLayout2.addWidget(self.rbtnNo2)
        vLayout2.addWidget(label2)
        vLayout2.addLayout(hLayout2)
        
        hLayout3 = QtWidgets.QHBoxLayout()
        self.pushButton_OK = QtWidgets.QPushButton()
        self.pushButton_OK.setObjectName("pushButton_OK")
        self.pushButton_Cancel = QtWidgets.QPushButton()
        self.pushButton_Cancel.setObjectName("pushButton_Cancel")
        hLayout3.addWidget(self.pushButton_OK)
        hLayout3.addWidget(self.pushButton_Cancel)
        
        vLayout.addWidget(groupbox1)
        vLayout.addWidget(groupbox2)
        vLayout.addLayout(hLayout3)
        self.retranslateUi(UNIXModelAnimation)
        QtCore.QMetaObject.connectSlotsByName(UNIXModelAnimation)

    def retranslateUi(self, UNIXModelAnimation):
        _translate = QtCore.QCoreApplication.translate
        UNIXModelAnimation.setWindowTitle(_translate("UNIXModelAnimation", "UNIX Model Tutorial"))
        self.pushButton_OK.setText(_translate("UNIXModelAnimation", "OK"))
        self.pushButton_Cancel.setText(_translate("UNIXModelAnimation", "Cancel"))
        
class UNIXModelAnimation(QDialog):

    def __init__(self, main):
        super().__init__()
        self.setVisible(False)
        self.ui = Ui_UNIXModelAnimation()
        self.ui.setupUi(self)
        flags = Qt.WindowType.Dialog | Qt.WindowType.WindowStaysOnTopHint
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
        super().__init__(main)
        self.main = main
  
class TutorialAnimationScene(QGraphicsScene):
    
    def __init__(self, main):
        super().__init__(main)
        self.main = main
        self.font = QFont("Courier", 30, QFont.Weight.Bold)
#         self.view = TutorialAnimationView(self, self.centralWidget())
#         self.view.setScene(self.scene)
#         self.view.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
#         self.view.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
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
        painter.drawText(rect, Qt.AlignmentFlag.AlignLeft, self.message)
        super().drawBackground(painter, QRectF(rect))
        self.update()
        
    def initParam(self):
        self.message = 'testing this view'
    
    def startAnimation(self, detailMode):
        self.initParam()
