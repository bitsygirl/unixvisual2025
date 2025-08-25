from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import QWidget, QCheckBox, QVBoxLayout, QGroupBox, QDialog, QTabWidget, QPushButton, \
                        QHBoxLayout, QLabel, QFont, QLineEdit, QSizePolicy
from PyQt4.QtCore import QString, Qt
import MyFunctions
        
class PermissionCalDialog(QDialog):
    
    def __init__(self, parent = None):
        QDialog.__init__(self, parent)
        self.main = parent
        flags = Qt.Dialog | Qt.WindowStaysOnTopHint
        self.setWindowFlags(flags)
        self.resize(400, 400)
#         self.tabId = 0
        self.tabWidget = QTabWidget()
        self.octal2Letter = Octal2LetterTab()
        self.tabWidget.addTab(Letter2OctalTab(), QString('Convert to Octal'))
        self.tabWidget.addTab(self.octal2Letter, QString('Decode Octal'))
        
        closePB = QPushButton('Close')
        
        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.tabWidget)
        mainLayout.addWidget(closePB)
        self.setLayout(mainLayout)
        closePB.clicked.connect(self.close)
    
    def closeEvent(self, evt):
        self.main.ui.actionPermission_Calculator_Window.setChecked(False)
        QDialog.closeEvent(self, evt)
        
class Letter2OctalTab(QWidget):
    def __init__(self, parent = None):
        QWidget.__init__(self, parent)
        self.specOctal = 0
        self.userOctal = 0
        self.groupOctal = 0
        self.otherOctal = 0
        self.userLetter = '---'
        self.groupLetter = '---'
        self.otherLetter = '---'
        
        vbox0 = QVBoxLayout(self)
        
        hwidget1 = QWidget(self)
        hbox1 = QHBoxLayout(hwidget1)
        hwidget1.setLayout(hbox1)
        
        specialGroupBox = QGroupBox('Special')
        vbox1 = QVBoxLayout(specialGroupBox)
        self.setuidCB = QCheckBox('setuid')
        self.setgidCB = QCheckBox('setgid')
        self.stickyCB = QCheckBox('Sticky bit')
        vbox1.addWidget(self.setuidCB)
        vbox1.addWidget(self.setgidCB)
        vbox1.addWidget(self.stickyCB)
        specialGroupBox.setLayout(vbox1)
        hbox1.addWidget(specialGroupBox)
        
        userGroupBox = QGroupBox('User')
        vbox2 = QVBoxLayout(userGroupBox)
        self.ureadCB = QCheckBox('Read')
        self.uwriteCB = QCheckBox('Write')
        self.uexecCB = QCheckBox('Execute')
        vbox2.addWidget(self.ureadCB)
        vbox2.addWidget(self.uwriteCB)
        vbox2.addWidget(self.uexecCB)
        userGroupBox.setLayout(vbox2)
        hbox1.addWidget(userGroupBox)
        
        groupGroupBox = QGroupBox('Group')
        vbox3 = QVBoxLayout(groupGroupBox)
        self.greadCB = QCheckBox('Read')
        self.gwriteCB = QCheckBox('Write')
        self.gexecCB = QCheckBox('Execute')
        vbox3.addWidget(self.greadCB)
        vbox3.addWidget(self.gwriteCB)
        vbox3.addWidget(self.gexecCB)
        groupGroupBox.setLayout(vbox3)
        hbox1.addWidget(groupGroupBox)
        
        otherGroupBox = QGroupBox('Other')
        vbox4 = QVBoxLayout(otherGroupBox)
        self.oreadCB = QCheckBox('Read')
        self.owriteCB = QCheckBox('Write')
        self.oexecCB = QCheckBox('Execute')
        vbox4.addWidget(self.oreadCB)
        vbox4.addWidget(self.owriteCB)
        vbox4.addWidget(self.oexecCB)
        otherGroupBox.setLayout(vbox4)
        hbox1.addWidget(otherGroupBox)
        vbox0.addWidget(hwidget1)
        
        
        octalGB = QGroupBox('Octal and Letter Notations')
        MyFunctions.setFontForUI(octalGB, 20)
        vbox5 = QVBoxLayout(octalGB)
        vbox5.setContentsMargins(0, 0, 0, 0)
        self.octalDisplayLab = QLabel('0000')
        self.octalDisplayLab.setContentsMargins(0, 0, 0, 0)
        MyFunctions.setFontForUI(self.octalDisplayLab, 30)
        self.octalDisplayLab.setStyleSheet("qproperty-alignment: AlignCenter;")
        self.octalDisplayLab.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Preferred)
        vbox5.addWidget(self.octalDisplayLab)
        
        self.letterDisplayLab = QLabel('%s%s%s'%(self.userLetter, self.groupLetter, self.otherLetter))
        self.letterDisplayLab.setContentsMargins(0, 0, 0, 0)
        MyFunctions.setFontForUI(self.letterDisplayLab, 30)
        self.letterDisplayLab.setStyleSheet("qproperty-alignment: AlignCenter;")
        self.letterDisplayLab.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Preferred)
        vbox5.addWidget(self.letterDisplayLab)
        
        vbox0.addWidget(octalGB)
        self.setLayout(vbox0)
        self.setupConnections()
        
    def setupConnections(self):
        self.setuidCB.stateChanged.connect(self.updateSpecUidBit)
        self.setgidCB.stateChanged.connect(self.updateSpecGidBit)
        self.stickyCB.stateChanged.connect(self.updateSpecStickyBit)
        self.ureadCB.stateChanged.connect(self.updateUserReadBit)
        self.uwriteCB.stateChanged.connect(self.updateUserWriteBit)
        self.uexecCB.stateChanged.connect(self.updateUserExecBit)
        self.greadCB.stateChanged.connect(self.updateGroupReadBit)
        self.gwriteCB.stateChanged.connect(self.updateGroupWriteBit)
        self.gexecCB.stateChanged.connect(self.updateGroupExecBit)
        self.oreadCB.stateChanged.connect(self.updateOtherReadBit)
        self.owriteCB.stateChanged.connect(self.updateOtherWriteBit)
        self.oexecCB.stateChanged.connect(self.updateOtherExecBit)
            
    def changeCharacterInString(self, letter, index, inputStr):
        return inputStr[:index]+letter+inputStr[index+1:]
        
    def updateSpecUidBit(self):
        if self.setuidCB.isChecked():
            self.specOctal+=4
            if self.uexecCB.isChecked():
                self.userLetter = self.changeCharacterInString('s', 2, self.userLetter)
            else:
                self.userLetter = self.changeCharacterInString('S', 2, self.userLetter)
        else:
            self.specOctal-=4
            if self.uexecCB.isChecked():
                self.userLetter = self.changeCharacterInString('x', 2, self.userLetter)
            else:
                self.userLetter = self.changeCharacterInString('-', 2, self.userLetter)
        self.octalDisplayLab.setText('%s%s%s%s'%(self.specOctal, self.userOctal, self.groupOctal, self.otherOctal))
        self.letterDisplayLab.setText('%s%s%s'%(self.userLetter, self.groupLetter, self.otherLetter))

    def updateSpecGidBit(self):
        if self.setgidCB.isChecked():
            self.specOctal+=2
            if self.gexecCB.isChecked():
                self.groupLetter = self.changeCharacterInString('s', 2, self.groupLetter)
            else:
                self.groupLetter = self.changeCharacterInString('S', 2, self.groupLetter)
        else:
            self.specOctal-=2
            if self.gexecCB.isChecked():
                self.groupLetter = self.changeCharacterInString('x', 2, self.groupLetter)
            else:
                self.groupLetter = self.changeCharacterInString('-', 2, self.groupLetter)
        self.octalDisplayLab.setText('%s%s%s%s'%(self.specOctal, self.userOctal, self.groupOctal, self.otherOctal))
        self.letterDisplayLab.setText('%s%s%s'%(self.userLetter, self.groupLetter, self.otherLetter))

    def updateSpecStickyBit(self):
        if self.stickyCB.isChecked():
            self.specOctal+=1
            if self.oexecCB.isChecked():
                self.otherLetter = self.changeCharacterInString('t', 2, self.otherLetter)
            else:
                self.otherLetter = self.changeCharacterInString('T', 2, self.otherLetter)
        else:
            self.specOctal-=1
            if self.oexecCB.isChecked():
                self.otherLetter = self.changeCharacterInString('x', 2, self.otherLetter)
            else:
                self.otherLetter = self.changeCharacterInString('-', 2, self.otherLetter)
        self.octalDisplayLab.setText('%s%s%s%s'%(self.specOctal, self.userOctal, self.groupOctal, self.otherOctal))
        self.letterDisplayLab.setText('%s%s%s'%(self.userLetter, self.groupLetter, self.otherLetter))

    def updateUserReadBit(self):
        if self.ureadCB.isChecked():
            self.userOctal+=4
            self.userLetter = self.changeCharacterInString('r', 0, self.userLetter)
        else:
            self.userOctal-=4
            self.userLetter = self.changeCharacterInString('-', 0, self.userLetter)
        self.octalDisplayLab.setText('%s%s%s%s'%(self.specOctal, self.userOctal, self.groupOctal, self.otherOctal))
        self.letterDisplayLab.setText('%s%s%s'%(self.userLetter, self.groupLetter, self.otherLetter))

    def updateUserWriteBit(self):
        if self.uwriteCB.isChecked():
            self.userOctal+=2
            self.userLetter = self.changeCharacterInString('w', 1, self.userLetter)
        else:
            self.userOctal-=2
            self.userLetter = self.changeCharacterInString('-', 1, self.userLetter)
        self.octalDisplayLab.setText('%s%s%s%s'%(self.specOctal, self.userOctal, self.groupOctal, self.otherOctal))
        self.letterDisplayLab.setText('%s%s%s'%(self.userLetter, self.groupLetter, self.otherLetter))

    def updateUserExecBit(self):
        if self.uexecCB.isChecked():
            self.userOctal+=1
            if self.setuidCB.isChecked():
                self.userLetter = self.changeCharacterInString('s', 2, self.userLetter)
            else:
                self.userLetter = self.changeCharacterInString('x', 2, self.userLetter)
        else:
            self.userOctal-=1
            if self.setuidCB.isChecked():
                self.userLetter = self.changeCharacterInString('S', 2, self.userLetter)
            else:
                self.userLetter = self.changeCharacterInString('-', 2, self.userLetter)
        self.octalDisplayLab.setText('%s%s%s%s'%(self.specOctal, self.userOctal, self.groupOctal, self.otherOctal))
        self.letterDisplayLab.setText('%s%s%s'%(self.userLetter, self.groupLetter, self.otherLetter))

    def updateGroupReadBit(self):
        if self.greadCB.isChecked():
            self.groupOctal+=4
            self.groupLetter = self.changeCharacterInString('r', 0, self.groupLetter)
        else:
            self.groupOctal-=4
            self.groupLetter = self.changeCharacterInString('-', 0, self.groupLetter)
        self.octalDisplayLab.setText('%s%s%s%s'%(self.specOctal, self.userOctal, self.groupOctal, self.otherOctal))
        self.letterDisplayLab.setText('%s%s%s'%(self.userLetter, self.groupLetter, self.otherLetter))

    def updateGroupWriteBit(self):
        if self.gwriteCB.isChecked():
            self.groupOctal+=2
            self.groupLetter = self.changeCharacterInString('w', 1, self.groupLetter)
        else:
            self.groupOctal-=2
            self.groupLetter = self.changeCharacterInString('-', 1, self.groupLetter)
        self.octalDisplayLab.setText('%s%s%s%s'%(self.specOctal, self.userOctal, self.groupOctal, self.otherOctal))
        self.letterDisplayLab.setText('%s%s%s'%(self.userLetter, self.groupLetter, self.otherLetter))

    def updateGroupExecBit(self):
        if self.gexecCB.isChecked():
            self.groupOctal+=1
            if self.setgidCB.isChecked():
                self.groupLetter = self.changeCharacterInString('s', 2, self.groupLetter)
            else:
                self.groupLetter = self.changeCharacterInString('x', 2, self.groupLetter)
        else:
            self.groupOctal-=1
            if self.setgidCB.isChecked():
                self.groupLetter = self.changeCharacterInString('S', 2, self.groupLetter)
            else:
                self.groupLetter = self.changeCharacterInString('-', 2, self.groupLetter)
        self.octalDisplayLab.setText('%s%s%s%s'%(self.specOctal, self.userOctal, self.groupOctal, self.otherOctal))
        self.letterDisplayLab.setText('%s%s%s'%(self.userLetter, self.groupLetter, self.otherLetter))

    def updateOtherReadBit(self):
        if self.oreadCB.isChecked():
            self.otherOctal+=4
            self.otherLetter = self.changeCharacterInString('r', 0, self.otherLetter)
        else:
            self.otherOctal-=4
            self.otherLetter = self.changeCharacterInString('-', 0, self.otherLetter)
        self.octalDisplayLab.setText('%s%s%s%s'%(self.specOctal, self.userOctal, self.groupOctal, self.otherOctal))
        self.letterDisplayLab.setText('%s%s%s'%(self.userLetter, self.groupLetter, self.otherLetter))

    def updateOtherWriteBit(self):
        if self.owriteCB.isChecked():
            self.otherOctal+=2
            self.otherLetter = self.changeCharacterInString('w', 1, self.otherLetter)
        else:
            self.otherOctal-=2
            self.otherLetter = self.changeCharacterInString('-', 1, self.otherLetter)
        self.octalDisplayLab.setText('%s%s%s%s'%(self.specOctal, self.userOctal, self.groupOctal, self.otherOctal))
        self.letterDisplayLab.setText('%s%s%s'%(self.userLetter, self.groupLetter, self.otherLetter))

    def updateOtherExecBit(self):
        if self.oexecCB.isChecked():
            self.otherOctal+=1
            if self.stickyCB.isChecked():
                self.otherLetter = self.changeCharacterInString('t', 2, self.otherLetter)
            else:
                self.otherLetter = self.changeCharacterInString('x', 2, self.otherLetter)
        else:
            self.otherOctal-=1
            if self.stickyCB.isChecked():
                self.otherLetter = self.changeCharacterInString('T', 2, self.otherLetter)
            else:
                self.otherLetter = self.changeCharacterInString('-', 2, self.otherLetter)
        self.octalDisplayLab.setText('%s%s%s%s'%(self.specOctal, self.userOctal, self.groupOctal, self.otherOctal))
        self.letterDisplayLab.setText('%s%s%s'%(self.userLetter, self.groupLetter, self.otherLetter))

class Octal2LetterTab(QWidget):

    def __init__(self, parent = None):
        QWidget.__init__(self, parent)
        
        self.userLetter, self.groupLetter, self.otherLetter = '---', '---', '---'
        
        vbox0 = QVBoxLayout(self)
        
        hwidget1 = QWidget(self)
        hbox1 = QHBoxLayout(hwidget1)
        hwidget1.setLayout(hbox1)
        
        specialGroupBox = QGroupBox('Special')
        vbox1 = QVBoxLayout(specialGroupBox)
        self.setuidCB = CustomReadCheckBox('Setuid')
        self.setgidCB = CustomReadCheckBox('Setgid')
        self.stickyCB = CustomReadCheckBox('Sticky bit')
        vbox1.addWidget(self.setuidCB)
        vbox1.addWidget(self.setgidCB)
        vbox1.addWidget(self.stickyCB)
        specialGroupBox.setLayout(vbox1)
        hbox1.addWidget(specialGroupBox)
        
        userGroupBox = QGroupBox('User')
        vbox2 = QVBoxLayout(userGroupBox)
        self.ureadCB = CustomReadCheckBox('Read')
        self.uwriteCB = CustomReadCheckBox('Write')
        self.uexecCB = CustomReadCheckBox('Execute')
        vbox2.addWidget(self.ureadCB)
        vbox2.addWidget(self.uwriteCB)
        vbox2.addWidget(self.uexecCB)
        userGroupBox.setLayout(vbox2)
        hbox1.addWidget(userGroupBox)
        
        groupGroupBox = QGroupBox('Group')
        vbox3 = QVBoxLayout(groupGroupBox)
        self.greadCB = CustomReadCheckBox('Read')
        self.gwriteCB = CustomReadCheckBox('Write')
        self.gexecCB = CustomReadCheckBox('Execute')
        vbox3.addWidget(self.greadCB)
        vbox3.addWidget(self.gwriteCB)
        vbox3.addWidget(self.gexecCB)
        groupGroupBox.setLayout(vbox3)
        hbox1.addWidget(groupGroupBox)
        
        otherGroupBox = QGroupBox('Other')
        vbox4 = QVBoxLayout(otherGroupBox)
        self.oreadCB = CustomReadCheckBox('Read')
        self.owriteCB = CustomReadCheckBox('Write')
        self.oexecCB = CustomReadCheckBox('Execute')
        vbox4.addWidget(self.oreadCB)
        vbox4.addWidget(self.owriteCB)
        vbox4.addWidget(self.oexecCB)
        otherGroupBox.setLayout(vbox4)
        hbox1.addWidget(otherGroupBox)
        
        octalGB = QGroupBox('Octal and Letter Notations')
        MyFunctions.setFontForUI(octalGB, 20)
        vbox5 = QVBoxLayout(octalGB)
        vbox5.setContentsMargins(0, 0, 0, 0)
        self.octalDisplayLab = QLineEdit('0000')
        self.octalDisplayLab.setContentsMargins(0, 0, 0, 0)
        MyFunctions.setFontForUI(self.octalDisplayLab, 30)
        self.octalDisplayLab.setStyleSheet("qproperty-alignment: AlignCenter;")
        self.octalDisplayLab.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Preferred)
        self.submitBtn = QPushButton('update')
        self.errorLab = QLabel('')
        self.errorLab.setStyleSheet("QLabel {color : red; }")
        
        self.letterDisplayLab = QLabel('%s%s%s'%(self.userLetter, self.groupLetter, self.otherLetter))
        MyFunctions.setFontForUI(self.letterDisplayLab, 30)
        self.letterDisplayLab.setContentsMargins(0, 0, 0, 0)
        self.letterDisplayLab.setStyleSheet("qproperty-alignment: AlignCenter;")
        self.letterDisplayLab.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Preferred)

        vbox5.addWidget(self.octalDisplayLab)
        vbox5.addWidget(self.letterDisplayLab)
        vbox5.addWidget(self.errorLab)
        vbox5.addWidget(self.submitBtn)
        
        vbox0.addWidget(octalGB)
        vbox0.addWidget(hwidget1)
        self.setLayout(vbox0)
        self.submitBtn.clicked.connect(self.updateCheckBoxes)

    def updateCheckBoxes(self):
        permstr = str(self.octalDisplayLab.displayText())
        if len(permstr) != 4:
            self.errorLab.setText('Value must have 4 digits in length.')
            return
        for p in permstr:
            if ord(p)<48 or ord(p)>55:
                self.errorLab.setText('Value of each digit must be a number and range from 0 to 7 inclusive.')
                return
        specnum = int(permstr[0])
        usernum = int(permstr[1])
        groupnum = int(permstr[2])
        othernum = int(permstr[3])
        self.errorLab.setText('')
        specBinar = '{0:03b}'.format(specnum)
        userBinar = '{0:03b}'.format(usernum)
        groupBinar = '{0:03b}'.format(groupnum)
        otherBinar = '{0:03b}'.format(othernum)
        self.updateSpecCBs(specBinar)
        self.updateUserCBs(userBinar)
        self.updateGroupCBs(groupBinar)
        self.updateOtherCBs(otherBinar)
        self.letterDisplayLab.setText('%s%s%s'%(self.userLetter, self.groupLetter, self.otherLetter))
    
    def updateSpecCBs(self, num):
        self.setuidCB.setChecked(num[0] == '1')
        self.setgidCB.setChecked(num[1] == '1')
        self.stickyCB.setChecked(num[2] == '1')
        
    def updateUserCBs(self, num):
        self.ureadCB.setChecked(num[0] == '1')
        self.uwriteCB.setChecked(num[1] == '1')
        self.uexecCB.setChecked(num[2] == '1')
        if self.ureadCB.isChecked():
            self.userLetter = self.changeCharacterInString('r', 0, self.userLetter)
        else:
            self.userLetter = self.changeCharacterInString('-', 0, self.userLetter)
        if self.uwriteCB.isChecked():
            self.userLetter = self.changeCharacterInString('w', 1, self.userLetter)
        else:
            self.userLetter = self.changeCharacterInString('-', 1, self.userLetter)
        if self.uexecCB.isChecked():
            if self.setuidCB.isChecked():
                self.userLetter = self.changeCharacterInString('s', 2, self.userLetter)
            else:
                self.userLetter = self.changeCharacterInString('x', 2, self.userLetter)
        else:
            if self.setuidCB.isChecked():
                self.userLetter = self.changeCharacterInString('S', 2, self.userLetter)
            else:
                self.userLetter = self.changeCharacterInString('-', 2, self.userLetter)
        
    def updateGroupCBs(self, num):
        self.greadCB.setChecked(num[0] == '1')
        self.gwriteCB.setChecked(num[1] == '1')
        self.gexecCB.setChecked(num[2] == '1')
        if self.greadCB.isChecked():
            self.groupLetter = self.changeCharacterInString('r', 0, self.groupLetter)
        else:
            self.groupLetter = self.changeCharacterInString('-', 0, self.groupLetter)
        if self.gwriteCB.isChecked():
            self.groupLetter = self.changeCharacterInString('w', 1, self.groupLetter)
        else:
            self.groupLetter = self.changeCharacterInString('-', 1, self.groupLetter)
        if self.gexecCB.isChecked():
            if self.setgidCB.isChecked():
                self.groupLetter = self.changeCharacterInString('s', 2, self.groupLetter)
            else:
                self.groupLetter = self.changeCharacterInString('x', 2, self.groupLetter)
        else:
            if self.setgidCB.isChecked():
                self.groupLetter = self.changeCharacterInString('S', 2, self.groupLetter)
            else:
                self.groupLetter = self.changeCharacterInString('-', 2, self.groupLetter)

    def updateOtherCBs(self, num):
        self.oreadCB.setChecked(num[0] == '1')
        self.owriteCB.setChecked(num[1] == '1')
        self.oexecCB.setChecked(num[2] == '1')
        if self.oreadCB.isChecked():
            self.otherLetter = self.changeCharacterInString('r', 0, self.otherLetter)
        else:
            self.otherLetter = self.changeCharacterInString('-', 0, self.otherLetter)
        if self.owriteCB.isChecked():
            self.otherLetter = self.changeCharacterInString('w', 1, self.otherLetter)
        else:
            self.otherLetter = self.changeCharacterInString('-', 1, self.otherLetter)
        if self.oexecCB.isChecked():
            if self.stickyCB.isChecked():
                self.otherLetter = self.changeCharacterInString('t', 2, self.otherLetter)
            else:
                self.otherLetter = self.changeCharacterInString('x', 2, self.otherLetter)
        else:
            if self.stickyCB.isChecked():
                self.otherLetter = self.changeCharacterInString('T', 2, self.otherLetter)
            else:
                self.otherLetter = self.changeCharacterInString('-', 2, self.otherLetter)
                
    def changeCharacterInString(self, letter, index, inputStr):
        return inputStr[:index]+letter+inputStr[index+1:]
       
class CustomReadCheckBox(QCheckBox):
    def __init__( self, parent = None ):
        QCheckBox.__init__(self, parent)
        self._readOnly = True

    def isReadOnly( self ):
        return self._readOnly

    def mousePressEvent( self, event ):
        if ( self.isReadOnly() ):
            event.accept()
        else:
            QCheckBox.mousePressEvent(event)

    def mouseMoveEvent( self, event ):
        if ( self.isReadOnly() ):
            event.accept()
        else:
            QCheckBox.mouseMoveEvent(event)

    def mouseReleaseEvent( self, event ):
        if ( self.isReadOnly() ):
            event.accept()
        else:
            QCheckBox.mouseReleaseEvent(event)

    # Handle event in which the widget has focus and the spacebar is pressed.
    def keyPressEvent( self, event ):
        if ( self.isReadOnly() ):
            event.accept()
        else:
            QCheckBox.keyPressEvent(event)