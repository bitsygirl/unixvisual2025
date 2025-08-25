'''
Accessible Access Control 1.0
2012-2104 Michigan Technological University
Supported in part by NSF grants: DUE-1140512, DUE-1245310 and IIS-1363
Developer: Man Wang
Advisors:Dr. Steve Carr, Dr. Jean Mayo, Dr. Ching-Kuang Shene and Dr. Chaoli Wang
Updated for PyQt6 compatibility
'''

# PyQt6 imports
from PyQt6.QtCore import Qt, QObject, QPointF, QRectF, QLineF, pyqtSignal, QTimer, QRect, QFileInfo
from PyQt6.QtWidgets import *
from PyQt6.QtGui import QPen, QBrush, QColor, QFont, QPainter, QPixmap, QIcon, QTransform

from Ui_AutogradingTestDlg import *
from Ui_TestQuestionLoad import *
import smtplib, subprocess
import os, getpass, socket, datetime
import http.client, urllib.parse
# from AnswerCrypto import AnswerCrypto
        
class AutogradingImageQuestion(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_ImageQuestion()
        self.ui.setupUi(self)
        flags = Qt.WindowType.Dialog | Qt.WindowType.WindowStaysOnTopHint
        self.setWindowFlags(flags)
        
# class AutogradingSubmssionDlg(QDialog):
#     def __init__(self):
#         super().__init__()
#         self.ui = Ui_submission()
#         self.ui.setupUi(self)
#         flags = Qt.WindowType.Dialog | Qt.WindowType.WindowStaysOnTopHint
#         self.setWindowFlags(flags)

class AutogradingQuestionLoadDlg(QDialog):
    def __init__(self, main):
        super().__init__()
        self.ui = Ui_TestQuestionLoad()
        self.ui.setupUi(self)
        self.main = main
        self.ui.pushButton_Cancel.clicked.connect(self.closeWindow)
        self.ui.lineEdit_Dir.textChanged.connect(self.changeText)
        
    def changeText(self, text):
        self.ui.lineEdit_Dir.setText(text)
        
    def closeWindow(self):
        self.ui.lineEdit_Dir.clear()
        self.main.ui.actionTest.setChecked(False)
        self.close()
        
    def closeEvent(self, evt):
        self.ui.lineEdit_Dir.clear()
        self.main.ui.actionTest.setChecked(False)
        evt.accept()
        
class AutogradingTest(QDialog):
    
    QUIZ_TRADITIONAL = 0
    QUIZ_TRYING = 1
    QUIZ_SHOWANSWER = 2
    
    def __init__(self, main):
        super().__init__()
        self.MAX_CHOICE_NUM = 4
        self.QUES_TYPE = 0
        self.QUES_TEXT = self.QUES_TYPE+1
        self.QUES_CHOICE1 = self.QUES_TEXT+1
        self.QUES_SPECPATH = self.QUES_CHOICE1+self.MAX_CHOICE_NUM
        self.NUM_ITEMS = self.QUES_SPECPATH+1
        self.QUIZ_DIR = main.diagramDir+'/quiz/'
        
        self.main = main
        self.scene = main.scene
#         self.answerCrypto = AnswerCrypto(main)
        self.imageQuestions = AutogradingImageQuestion()
        self.questionDlg = AutogradingQuestionLoadDlg(self.main)
        
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        flags = Qt.WindowType.Dialog | Qt.WindowType.WindowStaysOnTopHint
        self.setWindowFlags(flags)
        self.ui.nextBtn.clicked.connect(self.nextQuestion)
        self.ui.radioButton_1.clicked.connect(self.enableNextBtn)
        self.ui.radioButton_2.clicked.connect(self.enableNextBtn)
        self.ui.radioButton_3.clicked.connect(self.enableNextBtn)
        self.ui.radioButton_4.clicked.connect(self.enableNextBtn)
        self.imageQuestions.ui.pushButton.clicked.connect(self.nextQuestion)
        self.imageQuestions.ui.radioButton_1.clicked.connect(self.enableImageNexBtn)
        self.imageQuestions.ui.radioButton_2.clicked.connect(self.enableImageNexBtn)
        self.imageQuestions.ui.radioButton_3.clicked.connect(self.enableImageNexBtn)
        self.imageQuestions.ui.radioButton_4.clicked.connect(self.enableImageNexBtn)
#         self.submissionDlg.ui.pushButton.clicked.connect(self.sendGradeAndRestoreGUI)
#         self.submissionDlg.ui.pushButton_2.clicked.connect(self.cancelSubmission)
        self.questionDlg.ui.pushButton_Load.clicked.connect(self.loadInQuestions)
        self.questionDlg.ui.pushButton_OK.clicked.connect(self.confirmQuestions)
        self.initParam()
        
    def initParam(self):
        self.questionFile = None
        self.answers = ''
        self.answerTrial = 0
    
        self.questionId = 0
        self.totalQuesNum = 0
        self.questions = []
        self.count = 0
        self.tryintTimeCount = 0
        self.ui.correctAnsLabel.setText('')
        self.clearAllRadioButtons()

        
    def loadInQuestions(self):
        self.initParam()
        self.questionFile, _ = QFileDialog.getOpenFileName(self.main, 'Import Quiz Question File', directory=self.QUIZ_DIR, filter='(*.qes);;All Files(*.*)')
        self.questionDlg.ui.lineEdit_Dir.setText(self.questionFile)
        rect = QRect(int(0.3*self.main.geometry().width()+self.main.geometry().x()), 
                     int(0.3*self.main.geometry().height()+self.main.geometry().y()), 
                     self.questionDlg.rect().width(), self.questionDlg.rect().height())
        self.questionDlg.setWindowFlags(self.questionDlg.windowFlags()|Qt.WindowType.WindowStaysOnTopHint)
        self.questionDlg.setGeometry(rect)
        self.questionDlg.show()
        
#     def fillInQuestionFilePath(self):
#         self.questionFile = str(self.questionDlg.ui.lineEdit_Dir.text())
#         print(self.questionFile, self.questionDlg.ui.lineEdit_Dir.text())
        
    def toolbarAllItems(self, state):
        self.main.ui.actionNew.setEnabled(state)
        self.main.ui.actionImport.setEnabled(state)
        self.main.ui.actionChangeRoot.setEnabled(state)
        self.main.ui.actionToolBox.setEnabled(state)
        self.main.ui.actionSpecification.setEnabled(state)
        self.main.ui.actionQuery_Window.setEnabled(state)
        self.main.ui.actionView_User.setEnabled(state)
        self.main.userComboBox.setEnabled(state)
        self.main.ui.actionView_Group.setEnabled(state)
        self.main.groupComboBox.setEnabled(state)
        self.main.ui.actionView_Object.setEnabled(state)
        self.main.ui.actionView_ProgramTrace.setEnabled(state)
        self.main.ui.actionAnimation.setEnabled(state)
        self.main.animationControlButton.setEnabled(state)
        self.main.stopAnimationButton.setEnabled(state)
        
    def setMainToolbarForQuestionType(self, questionType):
        self.toolbarAllItems(False)
        if questionType == '2':
            self.main.ui.actionView_User.setEnabled(True)
            self.main.userComboBox.setEnabled(True)
        elif questionType == '3':
            self.main.ui.actionView_Group.setEnabled(True)
            self.main.groupComboBox.setEnabled(True)
            
    def confirmQuestions(self):
        if self.questionDlg.ui.lineEdit_Dir.text() != '':
            if self.questionFile == None: #for manuel entry of the path
                self.questionFile = str(self.questionDlg.ui.lineEdit_Dir.text())
            self.questionDlg.close()
            self.main.setMainWindowAllGuiState(False)
            self.startup()
        else:
            QMessageBox.warning(self, '', 'Please input a file name!')
            
    def startup(self):
        self.main.newDiagram()
        self.main.mode = self.main.QUIZ_MODE
        self.readInQuestions()
        self.show()
        self.setQuestion(0)
        
    def sendGradeAndRestoreGUI(self):
        self.emailGradeResult()
        self.close()
        self.imageQuestions.close()
        filename = QFileInfo(self.QUIZ_DIR).absoluteFilePath()
        filename = filename + '/answer.txt'
        QMessageBox.warning(self.main, '', "The answers have been stored in "+str(filename)+\
                                ".\nPlease send the file to the instructor!")
        self.main.newDiagram()
        self.toolbarAllItems(True)
        
    def returnBackToNormalMode(self):
        self.questionFile = None
        self.answers = ''
        self.questionId = 0
        self.totalQuesNum = 0
        self.questions = []
        
        self.main.setMainWindowAllGuiState(True)
        self.main.filebrowser.hide()
        self.main.specDialog.hide()
        self.main.mode = self.main.NORMAL_MODE
        
    def closeEvent(self, evt):
        if self.questionId < self.totalQuesNum-1:
            response = QMessageBox.warning(self, '', 'Are you sure to quit the quiz?', 
                                         buttons=QMessageBox.StandardButton.Yes|QMessageBox.StandardButton.No)
            if response == QMessageBox.StandardButton.Yes:
                self.main.ui.actionTest.setChecked(False)
                self.imageQuestions.close()
                self.returnBackToNormalMode()
                evt.accept()
                self.initParam()
#                 self.main.hintForTest()
            else:
                evt.ignore()
        else:
            self.returnBackToNormalMode()
#             self.main.hintForTest()
        
            
    def enableNextBtn(self):
        self.ui.nextBtn.setEnabled(True)
    
    def enableImageNexBtn(self):
        self.imageQuestions.ui.pushButton.setEnabled(True)

    def readInQuestions(self):
        index = 0
        self.quizMode = -1
        with open(self.questionFile, 'r') as f:
            for line in f:
                if line[0] != '#' and line[0] != '-':
                    line = line[:line.find('\n')]
                    if self.quizMode == -1:
                        self.quizMode = int(line)
                        if self.quizMode == self.QUIZ_TRADITIONAL:
                            self.ui.correctAnsLabel.setVisible(False)
                        else:
                            self.ui.correctAnsLabel.setVisible(True)
                    else:
                        if index == 0:
                            onequestion = [line]
                        else:
                            onequestion.append(line)
                        index+=1
                        if index == self.NUM_ITEMS:
                            self.questions.append(onequestion)
                            self.totalQuesNum +=1
                        index = index%self.NUM_ITEMS
        f.close()
    
    def setQuestion(self, qid):
        if qid == 0:
            self.answers = ''
        if os.path.isfile(self.questions[qid][self.QUES_CHOICE1]):#check whether has image in choices
            self.hide()
            self.imageQuestions.ui.groupBox.setTitle('Question '+str(qid+1))
            self.imageQuestions.ui.labQuestion1.setText(self.questions[qid][self.QUES_TEXT])
            if self.questions[qid][self.QUES_CHOICE1] != 'None':
                self.imageQuestions.ui.label_2.setVisible(True)
                self.imageQuestions.ui.label_2.setPixmap(QPixmap(self.questions[qid][self.QUES_CHOICE1]).scaled(self.imageQuestions.ui.IMAGESIZE, self.imageQuestions.ui.IMAGESIZE))
            else:
                self.imageQuestions.ui.label_2.setVisible(False)
            if self.questions[qid][self.QUES_CHOICE1+1] != 'None':
                self.imageQuestions.ui.label_3.setVisible(True)
                self.imageQuestions.ui.label_3.setPixmap(QPixmap(self.questions[qid][self.QUES_CHOICE1+1]).scaled(self.imageQuestions.ui.IMAGESIZE, self.imageQuestions.ui.IMAGESIZE))
            else:
                self.imageQuestions.ui.label_3.setVisible(False)
            if self.questions[qid][self.QUES_CHOICE1+2] != 'None':
                self.imageQuestions.ui.label_4.setVisible(True)
                self.imageQuestions.ui.label_4.setPixmap(QPixmap(self.questions[qid][self.QUES_CHOICE1+2]).scaled(self.imageQuestions.ui.IMAGESIZE, self.imageQuestions.ui.IMAGESIZE))
            else:
                self.imageQuestions.ui.label_4.setVisible(False)
            if self.questions[qid][self.QUES_CHOICE1+3] != 'None':
                self.imageQuestions.ui.label_5.setVisible(True)
                self.imageQuestions.ui.label_5.setPixmap(QPixmap(self.questions[qid][self.QUES_CHOICE1+3]).scaled(self.imageQuestions.ui.IMAGESIZE, self.imageQuestions.ui.IMAGESIZE))
            else:
                self.imageQuestions.ui.label_5.setVisible(False)
            if qid < self.totalQuesNum-1:
                self.imageQuestions.ui.pushButton.setText('Next')
            else:
                self.imageQuestions.ui.pushButton.setText('Finish')
            self.imageQuestions.ui.pushButton.setEnabled(False)
            self.imageQuestions.show()
            self.main.specDialog.hide()
        else:
            self.imageQuestions.hide()
            self.show()
            self.ui.groupBox.setTitle('Question '+str(qid+1))
            self.ui.labQuestion1.setText(self.questions[qid][self.QUES_TEXT])
            self.ui.labQuestion1.adjustSize()
            if self.questions[qid][self.QUES_CHOICE1] != 'None':
                self.ui.radioButton_1.setVisible(True)
                self.ui.radioButton_1.setText(self.questions[qid][self.QUES_CHOICE1])
            else:
                self.ui.radioButton_1.setVisible(False)
            if self.questions[qid][self.QUES_CHOICE1+1] != 'None':
                self.ui.radioButton_2.setVisible(True)
                self.ui.radioButton_2.setText(self.questions[qid][self.QUES_CHOICE1+1])
            else:
                self.ui.radioButton_2.setVisible(False)
            if self.questions[qid][self.QUES_CHOICE1+2] != 'None':
                self.ui.radioButton_3.setVisible(True)
                self.ui.radioButton_3.setText(self.questions[qid][self.QUES_CHOICE1+2])
            else:
                self.ui.radioButton_3.setVisible(False)
            if self.questions[qid][self.QUES_CHOICE1+3] != 'None':
                self.ui.radioButton_4.setVisible(True)
                self.ui.radioButton_4.setText(self.questions[qid][self.QUES_CHOICE1+3])
            else:
                self.ui.radioButton_4.setVisible(False)
                
            if qid < self.totalQuesNum-1:
                self.ui.nextBtn.setText('Next')
            else:
                self.ui.nextBtn.setText('Finish')
            self.ui.nextBtn.setEnabled(False)
        questionType = self.questions[qid][self.QUES_TYPE]
        if self.questions[qid][self.QUES_SPECPATH] not in ['Same', 'same', 'None']:
            self.determineWayToGetSpecFile(self.questions[qid][self.QUES_SPECPATH])
        self.setViewMode(questionType)

    def setViewMode(self, questionType):
    #1. No visualization will be provided but the specification of the specified file will be available. -- Text choices
    #2. Show User View with Directory Tree-- Text choices
    #3. Show Group View with Directory Tree-- Text choices
    #4. Show no view -- Text choices
    #5. Show no view -- Image choices
        self.main.ui.actionView_User.setChecked(False)
        self.main.ui.actionView_Group.setChecked(False)
        if questionType == '1':
            self.main.showSpecDialog()
            self.main.filebrowser.hide()
        elif questionType == '2':
            self.main.specDialog.hide()
            self.main.ui.actionView_User.setChecked(True)
            self.main.viewModeChanged(self.main.ui.actionView_User)
        elif questionType == '3':
            self.main.specDialog.hide()
            self.main.ui.actionView_Group.setChecked(True)
            self.main.viewModeChanged(self.main.ui.actionView_Group)
        elif questionType == '4':
            self.main.newDiagram()
            self.main.specDialog.hide()
            self.main.filebrowser.hide()
        self.setMainToolbarForQuestionType(questionType)
            
    def determineWayToGetSpecFile(self, specFile):
        expandedName = specFile[specFile.rfind('.')+1:]
        if expandedName == 'unix':
            self.main.iohelper.importSpec(specFile)

    def nextQuestion(self):
        if self.questionId<self.totalQuesNum-1:
            if self.quizMode == self.QUIZ_TRADITIONAL:
                self.saveStudentChoices()
                self.questionId += 1
                self.clearAllRadioButtons()
                self.setQuestion(self.questionId)
            elif self.quizMode == self.QUIZ_TRYING:
                self.saveAnswersForTryingMode()
                self.tryintTimeCount +=1
                correctness =  self.showCorrectChoice()
                if correctness == 'Correct':
                    if self.count%2!=0:
                        self.answers += self.questions[self.questionId][self.QUES_TEXT]+'\n'
                        self.answers += str(self.tryintTimeCount)+'\n'
                        self.ui.correctAnsLabel.setText('')
                        self.tryintTimeCount = 0
                        self.questionId += 1
                        self.clearAllRadioButtons()
                        self.setQuestion(self.questionId)
                    self.count+=1
            elif self.quizMode == self.QUIZ_SHOWANSWER: 
                if self.count%2==0:
                    self.saveStudentChoices()
                    self.showCorrectChoice()
                    self.count+=1
                    self.ui.radioButton_1.setEnabled(False)
                    self.ui.radioButton_2.setEnabled(False)
                    self.ui.radioButton_3.setEnabled(False)
                    self.ui.radioButton_4.setEnabled(False)
                    return
                else:
                    self.ui.correctAnsLabel.setText('')
                    self.questionId += 1
                    self.setQuestion(self.questionId)
                    self.count+=1
                self.clearAllRadioButtons()
        else:
            self.saveStudentChoices()
            self.encryptAnswers()
            self.sendGradeAndRestoreGUI()

    def clearAllRadioButtons(self):
        self.ui.nextBtn.setEnabled(False)
        self.ui.radioButton_1.setAutoExclusive(False)
        self.ui.radioButton_1.setChecked(False)
        self.ui.radioButton_1.setAutoExclusive(True)
        self.ui.radioButton_2.setAutoExclusive(False)
        self.ui.radioButton_2.setChecked(False)
        self.ui.radioButton_2.setAutoExclusive(True)
        self.ui.radioButton_3.setAutoExclusive(False)
        self.ui.radioButton_3.setChecked(False)
        self.ui.radioButton_3.setAutoExclusive(True)
        self.ui.radioButton_4.setAutoExclusive(False)
        self.ui.radioButton_4.setChecked(False)
        self.ui.radioButton_4.setAutoExclusive(True)
        self.ui.radioButton_1.setEnabled(True)
        self.ui.radioButton_2.setEnabled(True)
        self.ui.radioButton_3.setEnabled(True)
        self.ui.radioButton_4.setEnabled(True)

    def encryptAnswers(self):
#         self.answerCrypto.
        pass
    
    def saveStudentChoices(self):
        self.currentChoice = ''
        self.answers += self.questions[self.questionId][self.QUES_TEXT]+'\n'
        if self.isVisible():
            if self.ui.radioButton_1.isChecked():
                self.answers += self.ui.radioButton_1.text()+'\n'
                self.answers += '1\n'
                self.currentChoice = '1'
            elif self.ui.radioButton_2.isChecked():
                self.answers += self.ui.radioButton_2.text()+'\n'
                self.answers += '2\n'
                self.currentChoice = '2'
            elif self.ui.radioButton_3.isChecked():
                self.answers += self.ui.radioButton_3.text()+'\n'
                self.answers += '3\n'
                self.currentChoice = '3'
            elif self.ui.radioButton_4.isChecked():
                self.answers += self.ui.radioButton_4.text()+'\n'
                self.answers += '4\n'
                self.currentChoice = '4'
        else:
            if self.imageQuestions.ui.radioButton_1.isChecked():
                self.answers += '1\n'
                self.currentChoice = '1'
            elif self.imageQuestions.ui.radioButton_2.isChecked():
                self.answers += '2\n'
                self.currentChoice = '2'
            elif self.imageQuestions.ui.radioButton_3.isChecked():
                self.answers += '3\n'
                self.currentChoice = '3'
            elif self.imageQuestions.ui.radioButton_4.isChecked():
                self.answers += '4\n' 
                self.currentChoice = '4'
    
    def saveAnswersForTryingMode(self):
        self.currentChoice = ''
        if self.isVisible():
            if self.ui.radioButton_1.isChecked():
                self.currentChoice = '1'
            elif self.ui.radioButton_2.isChecked():
                self.currentChoice = '2'
            elif self.ui.radioButton_3.isChecked():
                self.currentChoice = '3'
            elif self.ui.radioButton_4.isChecked():
                self.currentChoice = '4'
        else:
            if self.imageQuestions.ui.radioButton_1.isChecked():
                self.currentChoice = '1'
            elif self.imageQuestions.ui.radioButton_2.isChecked():
                self.currentChoice = '2'
            elif self.imageQuestions.ui.radioButton_3.isChecked():
                self.currentChoice = '3'
            elif self.imageQuestions.ui.radioButton_4.isChecked():
                self.currentChoice = '4'

    
    def showCorrectChoice(self):
        params = urllib.parse.urlencode({
            'modeID' : str(self.quizMode),
            'questionID': str(self.questionId),
            'answerID': self.currentChoice
            })
        headers = {"Content-type": "application/x-www-form-urlencoded",
                   "Accept": "text/plain"}
        conn = http.client.HTTPConnection("cs.mtu.edu:80")
        conn.request("POST", "/~manw/testphp/test.php", params, headers)
        response = conn.getresponse()
        data = response.read()
        conn.close()
        if self.quizMode == self.QUIZ_SHOWANSWER:
            feedback = (data.decode('utf-8').replace('\n', '')).split(' ')
            if feedback[0] == 'Correct':
                self.ui.correctAnsLabel.setStyleSheet("QLabel { color : green; }")
                self.ui.correctAnsLabel.setText(feedback[0]+'!')
            else:
                warningText = feedback[0]+'. '+'The correct answer is Choice '+feedback[1]
                self.ui.correctAnsLabel.setStyleSheet("QLabel { color : red; }")
                self.ui.correctAnsLabel.setText(warningText)
            return None
        elif self.quizMode == self.QUIZ_TRYING:
            feedback = (data.decode('utf-8').replace('\n', '')).split(' ')
            if feedback[0] == 'Correct':
                self.ui.correctAnsLabel.setStyleSheet("QLabel { color : green; }")
                self.ui.correctAnsLabel.setText(feedback[0]+'!')
            else:
                warningText = 'Please try again.'
                self.ui.correctAnsLabel.setStyleSheet("QLabel { color : red; }")
                self.ui.correctAnsLabel.setText(warningText)
            return data.decode('utf-8').replace('\n', '')
        
    def emailGradeResult(self): 
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("gmail.com",80))
            ipaddress = (s.getsockname()[0])
            s.close()
            import platform
            if platform.system() != 'Windows':
                studentuid = os.getuid()
                attachemntContent = "Submission time: "+ str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")) + '\n'+\
                "Student UID: "+ str(studentuid)+'\n'+ \
                "Student username: " + str(getpass.getuser()) + '@'+ str(socket.gethostname()) + '\n'+\
                "IP address: "+ str(ipaddress) +'\n' + \
                "Exam input file: " + os.path.basename(str(self.questionFile)) + '\n'+\
                '\n'+ self.answers
            else:
                attachemntContent = "Submission time: "+ str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")) + '\n'+\
                "Student username: " + str(getpass.getuser()) + '@'+ str(socket.gethostname()) + '\n'+\
                "IP address: "+ str(ipaddress) +'\n' + \
                "Exam input file: " + os.path.basename(str(self.questionFile)) + '\n'+\
                '\n'+ self.answers
            
            filename = QFileInfo(self.QUIZ_DIR).absoluteFilePath()
            filename = filename + '/answer.txt'
            with open(filename, 'w') as f:
                f.write(attachemntContent)
            f.close()
#             #self.main.answerDecryption.emailInstructorDlg.show()
#             osplatform = sys.platform
#             if osplatform == "darwin":
#                 batcmd = 'ls /Applications | grep Thunderbird'
#                 if os.system(batcmd) == 0:
#                     thunderbirdCommandStr = 'open /Applications/Thunderbird.app --args -compose attachment="'+str(filename)+'"'
#                     os.system(thunderbirdCommandStr)
#                 #else:
#                     #self.main.answerDecryption.encrypt_RSA(None, self.answers)
#                     #QMessageBox.critical(self.main, '', "The answers have been stored in '"+str(filename)+"'.\nPlease send your answers to the instructor through email\nand install Thunderbird for later submissions!")
#             elif osplatform == "linux" or osplatform == "linux2":
#                 batcmd = 'which thunderbird'
#                 if os.system(batcmd) == 0:
#                     thunderbirdDir = subprocess.check_output(batcmd, shell=True)
#                     thunderbirdCommandStr = str(thunderbirdDir)+' -compose attachment='+str(filename)
#                     os.system(thunderbirdCommandStr)
#                 #else:
#                     #self.main.answerDecryption.encrypt_RSA(None, self.answers)
#                     #QMessageBox.critical(self.main, '', "The answers have been stored in '"+str(filename)+"'.\nPlease send your answers to the instructor through email\nand install Thunderbird for later submissions!")
#
