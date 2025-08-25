'''
Created on Mar 18, 2016

@author: manwang
'''

from PyQt4.QtGui import QGraphicsTextItem, QPen, QTextBlockFormat, QTextCursor, QColor, QDialog, QApplication, QPushButton, \
                        QTextEdit, QWidget, QVBoxLayout, QFont, QBrush, QFontMetricsF
from PyQt4.QtCore import Qt, QString, QRect, QMetaObject
import MyFunctions

try:
    _fromUtf8 = QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s
        
class TitleNode(QGraphicsTextItem):
    def __init__(self, msg):
        QGraphicsTextItem.__init__(self)
        self.setHtml('<center>%s</center>'%msg)
        
    def paint(self, painter, option, widget=None):
        QGraphicsTextItem.paint(self, painter, option, widget)
        
class FilePermNode(QGraphicsTextItem):
    def __init__(self, parent, main):
        QGraphicsTextItem.__init__(self, parent)
        self.main = main
        
    def paint(self, painter, option, widget=None):
        QGraphicsTextItem.paint(self, painter, option, widget)
        
    def mousePressEvent(self, evt):
        if evt.button() == Qt.LeftButton:
            self.main.permissionCalDialog.show()
            self.main.permissionCalDialog.tabWidget.setCurrentIndex(1)
            permtxt = str(self.toPlainText())
            index1, index2 = permtxt.find('Permission bits:'), permtxt.rfind('(')
            permtxt = permtxt[index1+len('Permission bits:')+1:index2]
            self.main.permissionCalDialog.octal2Letter.octalDisplayLab.setText(permtxt)
            self.main.permissionCalDialog.octal2Letter.updateCheckBoxes()
        QGraphicsTextItem.mousePressEvent(self, evt)
        
class Ui_CheckNodeDialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(200, 200)
        self.verticalLayoutWidget = QWidget(Dialog)
        self.verticalLayoutWidget.setObjectName(_fromUtf8("verticalLayoutWidget"))
        self.verticalLayout = QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.analysisEdit = QTextEdit(self.verticalLayoutWidget)
        self.analysisEdit.setReadOnly(True)
        self.analysisEdit.setObjectName(_fromUtf8("analysisEdit"))
        self.verticalLayout.addWidget(self.analysisEdit)
        self.closePushButton = QPushButton(self.verticalLayoutWidget)
        self.closePushButton.setObjectName(_fromUtf8("closePushButton"))
        self.verticalLayout.addWidget(self.closePushButton)
        self.retranslateUi(Dialog)
        QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QApplication.translate("Dialog", "", None, QApplication.UnicodeUTF8))
        self.closePushButton.setText(QApplication.translate("Dialog", "Close", None, QApplication.UnicodeUTF8))

class CheckNodeDialog(QDialog):
    def __init__(self, main, analysis):
        QDialog.__init__(self, main)
        self.main = main
        self.ui = Ui_CheckNodeDialog()
        self.ui.setupUi(self)
        self.setLayout(self.ui.verticalLayout)
        flags = Qt.Dialog | Qt.WindowStaysOnTopHint
        self.setWindowFlags(flags)
        self.ui.analysisEdit.setText(analysis)
        self.ui.closePushButton.clicked.connect(self.close)

    def readPermInfo(self, permInfo):
        self.ui.analysisEdit.setText(permInfo)
        
    def closeEvent(self, evt):
        evt.accept()
        
class CheckNode(QGraphicsTextItem):
    def __init__(self, main, msg, iconMark):
        QGraphicsTextItem.__init__(self)
        self.main = main
        self.highlight = None
        self.setVisible(False)
        self.index = -1
        MyFunctions.setFontForUI(self, 19)
#         self.setFont(QFont('Lucida Grande', 19))
        self.relativeX, self.relativeY = -1, -1
        self.setTextWidth(150)
        self.analysis = msg
        self.analysisDialog = CheckNodeDialog(main, self.analysis)
        self.analysisDialog.hide()
        self.setHtml('<center>%s</center>'%iconMark)
        self.iconmark = iconMark
        
    def getMessage(self):
        msg = ''
        txt = str(self.toPlainText())
        index = txt.find(':')
        user = txt[:index]
        perms = txt[index+1:]
        permset = set()
        if self.main.objectViewScene.isFile:
            for p in perms:
                if p == 'r':
                    permset.add('read')
                elif p == 'w':
                    permset.add('write')
                elif p in ['x', 's']:
                    permset.add('execute')
        else:
            for p in perms:
                if p == 'r':
                    permset.add('list the objects beneath')
                elif p == 'w':
                    permset.add('add/remove objects in it')
                elif p in ['x', 's']:
                    permset.add('pass through and access objects in it')
        permstr = ', '.join(permset)
        if self.index == 0:
            secstr = 'user'
        elif self.index == 1:
            secstr = 'group'
        elif self.index == 2:
            secstr = 'other'
        else:
            return
        currentGroup = str(self.main.objectViewScene.objectViewGroupComboBox.currentText())
        groupText = ''
        if currentGroup != self.main.objectViewScene.ALLGROUPTEXT:
            groupText = 'as a member of Group "%s"'%(currentGroup)
        if permset:
            if user == 'others':
                msg += 'The rest of the users can %s the object as specified in the %s permission bits.'%(permstr, secstr)
            else:
                msg += 'User "%s" %s can %s the object as specified in the %s permission bits.'%(user, groupText, permstr, secstr)
        else:
            if user == 'others':
                msg += 'The rest of the users do not have access to the object.'
            else:
                msg += 'User "%s" %s does not have access to the object.'%(user, groupText)
        return msg
    
    def highlightText(self):
        self.setHtml('<center><span style="background-color: #d6d7d5">%s</span></center>'%self.iconmark)
        
    def restoreText(self):
        self.setHtml('<center>%s</center>'%self.iconmark)
                  
    def mousePressEvent(self, evt):
        if evt.button() == Qt.LeftButton:
            if self in self.main.objectViewScene.clickableCheckNodes:
                for section in self.main.objectViewScene.checkgridNodes:
                    for i in section:
                        for j in i:
                            if j not in self.main.objectViewScene.clickableCheckNodes:
                                j.setVisible(False)
                                j.analysisDialog.hide()
                            else:
                                j.setVisible(True)
                            j.highlight = False
                if self.main.objectViewScene.selectedItem == self:
#                     self.main.objectViewScene.setGroupForUserComboBox(self.main.objectViewScene.objectViewuserComboBox.currentIndex())
                    self.main.objectViewScene.selectedItem = None
                    self.highlight = False
                    count = 0
                    for i in self.main.objectViewScene.checkgridNodes[self.index][self.indexuser]:
                        if count<len(self.main.objectViewScene.checkgridNodes[self.index][self.indexuser])-1:
                            i.setVisible(False)
                        count += 1
                    for i in self.main.objectViewScene.dirNodes:
                        self.main.objectViewScene.setHighlightSec(i, str(i.permInfo.toPlainText()), -1)
                    self.main.objectViewScene.msg.setPlainText(self.main.objectViewScene.msgDefault)
                else:
                    txt = str(self.toPlainText())
                    user = txt[:txt.find(':')]
                    self.main.objectViewScene.selectedItem = self
                    self.highlight = True
                    index = []
                    for i in self.main.objectViewScene.checkgridNodes[self.index][self.indexuser]:
                        index.append(i.index)
                        i.setVisible(True)
                    for i in self.main.objectViewScene.dirNodes:
                        self.main.objectViewScene.setHighlightSec(i, str(i.permInfo.toPlainText()), \
                                                                  index[self.main.objectViewScene.dirNodes.index(i)])
                    self.main.objectViewScene.msg.setPlainText(self.getMessage())
                self.main.objectViewScene.msg.setPos(20, self.main.scene.sceneRect().height()-\
                        self.main.objectViewScene.msg.boundingRect().height()-5)
#                 self.main.objectViewScene.msg.setGeometry(20, self.main.scene.sceneRect().height()-\
#                         self.main.objectViewScene.msg.boundingRect().height()-20,\
#                         self.main.objectViewScene.detailPBtn.geometry().x(),\
#                         self.self.main.objectViewScene.msg.geometry().height()
#                         )
            else:
                self.analysisDialog.show()
        QGraphicsTextItem.mousePressEvent(self, evt)
        
    def paint(self, painter, option, widget=None):
        if self.highlight==True:
            self.highlightText()
        elif self.highlight == False:
            self.restoreText()
        QGraphicsTextItem.paint(self, painter, option, widget)
        
# class FrameNode(QGraphicsRectItem):
#     def __init__(self, main):