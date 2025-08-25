'''
Created on Oct 19, 2014

@author: mandy
Updated for PyQt6 compatibility
'''
import ast
from base64 import b64decode
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from Ui_AnswerNPrivateKeyLoad import Ui_AnswerNPrivateKeyLoad
from Ui_EncryptionKeyImportDlg import Ui_EncryptionKeyImportDlg
from Ui_DecryptionDlg import Ui_DecryptionDlg
import os, math, subprocess, sys

class EncryptionKeyImportDlg(QDialog):
    def __init__(self, main):
        super().__init__()
        self.ui = Ui_EncryptionKeyImportDlg()
        self.ui.setupUi(self)
        self.main = main
        self.ui.lineEdit.setVisible(True)
        self.ui.pushButton_OK.setText('OK')
        self.ui.pushButton_Cancel.setText('Cancel')
        self.ui.pushButton_Cancel.clicked.connect(self.closeWindow)
        self.setWindowFlags(Qt.WindowType.Dialog | Qt.WindowType.WindowStaysOnTopHint)
        
    def closeWindow(self):
        self.ui.lineEdit.clear()
        self.close()
        
    def closeEvent(self, evt):
        self.ui.lineEdit.clear()
        evt.accept()
        
class DecryptionDlg(QDialog):
    def __init__(self, main):
        super().__init__()
        self.ui = Ui_DecryptionDlg()
        self.ui.setupUi(self)
        self.main = main
        self.ui.lineEdit.setVisible(True)
        self.ui.pushButton_OK.setText('OK')
        self.ui.pushButton_Cancel.setText('Cancel')
        self.ui.pushButton_Cancel.clicked.connect(self.closeWindow)
        self.setWindowFlags(Qt.WindowType.Dialog | Qt.WindowType.WindowStaysOnTopHint)
        
    def closeWindow(self):
        self.ui.lineEdit.clear()
        self.close()
        
    def closeEvent(self, evt):
        self.ui.lineEdit.clear()
        evt.accept()
        
class EncodedAnswerRenameWarningDlg(QDialog):
    def __init__(self, main):
        super().__init__()
        self.ui = Ui_EncryptionKeyImportDlg()
        self.ui.setupUi(self)
        self.ui.lineEdit.setVisible(False)
        self.ui.pushButton_OK.setText('Yes')
        self.ui.pushButton_Cancel.setText('No')
        self.main = main
        
    def closeWindow(self):
        self.close()
        
    def closeEvent(self, evt):
        evt.accept()

class AnswerCrypto(object):

    def __init__(self, main):
        '''Constructor'''
        self.main = main
        self.encryptionKeyImportDlg = EncryptionKeyImportDlg(main)
        self.privateKey, self.publicKey = None, None
        self.encryptionKeyImportDlg.ui.pushButton_OK.clicked.connect(self.confirmKeyFile)
        self.decryptDlg = DecryptionDlg(main)
        
    def renameAllowed(self):
        self.toReplace = True
        self.close()
    
    def renameRejected(self):
        self.toReplace = False
        self.close()
        
    def loadInAnswerFile(self):
        self.answerFile = None
        filename, _ = QFileDialog.getOpenFileName(self.main, 'Import Student Answer File', directory='./policies/quiz', filter='(*.*);;All Files(*.*)')
        self.answerFile = str(filename)
        self.answerFileLoadDlg.ui.lineEdit_Dir.setText(self.answerFile)
        rect = QRect(int(0.3*self.main.geometry().width()+self.main.geometry().x()), 
                     int(0.3*self.main.geometry().height()+self.main.geometry().y()), 
                     self.answerFileLoadDlg.rect().width(), self.answerFileLoadDlg.rect().height())
        self.answerFileLoadDlg.setWindowFlags(self.answerFileLoadDlg.windowFlags()|Qt.WindowType.WindowStaysOnTopHint)
        self.answerFileLoadDlg.setGeometry(rect)
        self.answerFileLoadDlg.show()
            
    def confirmKeyFile(self):
        if self.encryptionKeyImportDlg.ui.lineEdit.text() != '':
            self.eKeyFilename = str(self.encryptionKeyImportDlg.ui.lineEdit.text())
            self.encryptionKeyImportDlg.close()
        else:
            QMessageBox.warning(self, '', 'Please input a file name!')
            
    def confirmEmailEntry(self):
        self.main.instructorEmail = str(self.emailInstructorDlg.ui.lineEdit.text())
        self.emailInstructorDlg.close()

    def readInAnswers(self):
        pass
    
    def loadKeyfile(self, pubkeyfile):
        import base64
        import binascii
        
        f = open(pubkeyfile,'rb')
        line = f.readline()
        line = line.replace(b"manw@simon.cs.mtu.edu",b"")
        print(line)
        print(len(line))
        b = base64.b64decode(line)
        s = binascii.hexlify(b)
        print(s)

    def loadKeyfile1(self, pubkeyfile):
        import sys
        import base64
        import struct
        from pyasn1.type import univ
        from pyasn1.codec.der import encoder as der_encoder
        
        keydata = base64.b64decode(
          open(pubkeyfile).read().split(None)[1])
        
        parts = []
        while keydata:
            dlen = struct.unpack('>I', keydata[:4])[0]
            data, keydata = keydata[4:dlen+4], keydata[4+dlen:]
            parts.append(data)
        e_val = eval('0x' + ''.join(['%02X' % struct.unpack('B', x)[0] for x in parts[1]]))
        n_val = eval('0x' + ''.join(['%02X' % struct.unpack('B', x)[0] for x in parts[2]]))
        pkcs1_seq = univ.Sequence()
        pkcs1_seq.setComponentByPosition(0, univ.Integer(n_val))
        pkcs1_seq.setComponentByPosition(1, univ.Integer(e_val))
        print('-----BEGIN RSA PUBLIC KEY-----')
        print(base64.encodestring(der_encoder.encode(pkcs1_seq)))

    def encrypt_RSA(self):
        os.system("ssh-keygen -f ./policies/quiz/id_rsa.pub -e -m pem > ./policies/quiz/id_rsa_pub.pem")
        os.system("ssh-keygen -f ./policies/quiz/id_rsa -e -m pem > ./policies/quiz/id_rsa_priv.pem")
        
        # Note: The original RSA encryption code has been simplified
        # as the Crypto library is not included in the requirements
        # This would need to be updated to use a modern cryptography library
        print("RSA encryption functionality needs to be updated with modern crypto library")

    def decrypt_r(self):
        print("RSA decryption functionality needs to be updated with modern crypto library")
        
    def decrypt_RSA(self, key, encfile):
        print('==>got to decrypt')
        print('RSA decryption functionality needs to be updated with modern crypto library')
