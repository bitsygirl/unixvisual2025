'''
Created on Oct 19, 2014

@author: mandy
'''
# import Crypto
# from Crypto.PublicKey import RSA
# from Crypto import Random
import ast
from base64 import b64decode
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from Ui_AnswerNPrivateKeyLoad import Ui_AnswerNPrivateKeyLoad
from Ui_EncryptionKeyImportDlg import Ui_EncryptionKeyImportDlg
from Ui_DecryptionDlg import Ui_DecryptionDlg
import os, math, subprocess, sys

class EncryptionKeyImportDlg(QDialog):
    def __init__(self, main):
        QDialog.__init__(self)
        self.ui = Ui_EncryptionKeyImportDlg()
        self.ui.setupUi(self)
        self.main = main
        self.ui.lineEdit.setVisible(True)
        self.ui.pushButton_OK.setText('OK')
        self.ui.pushButton_Cancel.setText('Cancel')
        self.ui.pushButton_Cancel.clicked.connect(self.closeWindow)
        self.setWindowFlags(Qt.Dialog | Qt.WindowStaysOnTopHint)
        
    def closeWindow(self):
        self.ui.lineEdit.clear()
        self.close()
        
    def closeEvent(self, evt):
        self.ui.lineEdit.clear()
        evt.accept()
        
class DecryptionDlg(QDialog):
    def __init__(self, main):
        QDialog.__init__(self)
        self.ui = Ui_DecryptionDlg()
        self.ui.setupUi(self)
        self.main = main
        self.ui.lineEdit.setVisible(True)
        self.ui.pushButton_OK.setText('OK')
        self.ui.pushButton_Cancel.setText('Cancel')
        self.ui.pushButton_Cancel.clicked.connect(self.closeWindow)
        self.setWindowFlags(Qt.Dialog | Qt.WindowStaysOnTopHint)
        
    def closeWindow(self):
        self.ui.lineEdit.clear()
        self.close()
        
    def closeEvent(self, evt):
        self.ui.lineEdit.clear()
        evt.accept()
        
class EncodedAnswerRenameWarningDlg(QDialog):
    def __init__(self, main):
        QDialog.__init__(self)
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
    
# class EmailInstructorDlg(QDialog):
#     def __init__(self, main):
#         QDialog.__init__(self)
#         self.ui = Ui_EncryptionKeyImportDlg()
#         self.ui.setupUi(self)
#         self.main = main
#         self.ui.lineEdit.setVisible(True)
#         self.ui.pushButton_OK.setText('OK')
#         self.ui.pushButton_Cancel.setText('Close')
#         self.ui.label.setText("Please enter instructor's email address:")
#         self.ui.pushButton_Cancel.clicked.connect(self.closeWindow)
#         self.setWindowFlags(Qt.Dialog | Qt.WindowStaysOnTopHint)
        
#     def closeWindow(self):
#         reply = QMessageBox.warning(self, '', 'Are you sure to exit the submission process?\
#                                     \n Confirm this action will lose your answers!', QMessageBox.Yes|QMessageBox.No)
#         if reply == QMessageBox.Yes:
#             self.ui.lineEdit.clear()
#             self.close()
#         
#     def closeEvent(self, evt):
#         self.ui.lineEdit.clear()
#         evt.accept()
        
# class AnswerFileLoadDlg(QDialog):
#     def __init__(self, main):
#         QDialog.__init__(self)
#         self.ui = Ui_AnswerFileLoad()
#         self.ui.setupUi(self)
#         self.main = main
#         self.ui.pushButton_Cancel.clicked.connect(self.closeWindow)
#         
#     def closeWindow(self):
#         self.ui.lineEdit_Dir.clear()
#         self.main.ui.actionDecrypt.setChecked(False)
#         self.close()
#         self.main.ui.introLabel.setText('')
#         
#     def closeEvent(self, evt):
#         self.ui.lineEdit_Dir.clear()
#         self.main.ui.actionDecrypt.setChecked(False)
#         evt.accept()
#         self.main.ui.introLabel.setText('')
        
class AnswerCrypto(object):

    def __init__(self, main):
        '''Constructor'''
        self.main = main
#         self.answerFileLoadDlg = AnswerFileLoadDlg(main)
        self.encryptionKeyImportDlg = EncryptionKeyImportDlg(main)
#         self.renameWarningDlg = EncodedAnswerRenameWarningDlg(main)
#         self.emailInstructorDlg = EmailInstructorDlg(main)
        self.privateKey, self.publicKey = None, None
        #self.privateKey, self.publicKey = self.generateKeyPairs(1024)
#         self.answerFileLoadDlg.ui.pushButton_Load.clicked.connect(self.loadInAnswerFile)
#         self.answerFileLoadDlg.ui.pushButton_OK.clicked.connect(self.confirmAnswerFile)
        self.encryptionKeyImportDlg.ui.pushButton_OK.clicked.connect(self.confirmKeyFile)
        self.decryptDlg = DecryptionDlg(main)
#         self.emailInstructorDlg.ui.pushButton_OK.clicked.connect(self.confirmEmailEntry)
#         self.renameWarningDlg.ui.pushButton_OK.clicked.connect(self.renameAllowed)
#         self.renameWarningDlg.ui.pushButton_Cancel.clicked.connect(self.renameRejected)
#         self.encrypt_RSA('')
#         self.decrypt_RSA(self.key, './policies/quiz/answer_enc.txt')#, './policies/answer_dec.txt')

#     def generateKeyPairs(self, bits=2048):
#         new_key = RSA.generate(bits, e=65537)
#         public_key = new_key.publickey().exportKey("PEM")
#         private_key = new_key.exportKey("PEM")
#         return private_key, public_key
        
    def renameAllowed(self):
        self.toReplace = True
        self.close()
    
    def renameRejected(self):
        self.toReplace = False
        self.close()
        
    def loadInAnswerFile(self):
        self.answerFile = None
        self.answerFile = QFileDialog.getOpenFileName(self.main, 'Import Student Answer File', directory='./policies/quiz', filter='(*.*);;All Files(*.*)')
        self.answerFile = str(self.answerFile)
        self.answerFileLoadDlg.ui.lineEdit_Dir.setText(self.answerFile)
        rect = QRect(0.3*self.main.geometry().width()+self.main.geometry().x(), 0.3*self.main.geometry().height()+self.main.geometry().y(), self.answerFileLoadDlg.rect().width(), self.answerFileLoadDlg.rect().height())
        self.answerFileLoadDlg.setWindowFlags(self.answerFileLoadDlg.windowFlags()|Qt.WindowStaysOnTopHint)
        self.answerFileLoadDlg.setGeometry(rect)
        self.answerFileLoadDlg.show()
        
#     def confirmAnswerFile(self):
#         if self.answerFileLoadDlg.ui.lineEdit_Dir.text() != '':
#             self.answerFileLoadDlg.close()
#             self.readInAnswers()
#         else:
#             QMessageBox.warning(self, '', 'Please input a file name!')
        
    def confirmKeyFile(self):
        if self.encryptionKeyImportDlg.ui.lineEdit.text() != '':
            self.eKeyFilename = str(self.encryptionKeyImportDlg.ui.lineEdit.text())
            self.encryptionKeyImportDlg.close()
        else:
            QMessageBox.warning(self, '', 'Please input a file name!')
            
    def confirmEmailEntry(self):
        self.main.instructorEmail = str(self.emailInstructorDlg.ui.lineEdit.text())#'manw@mtu.edu'
        self.emailInstructorDlg.close()
#         self.encrypt_RSA(self.main.autogradingTest.answers)

    def readInAnswers(self):
#         with open(self.answerFile, 'r') as f:
#             message = f.read()
#         # Import key using RSA module
# #         public_key = RSA.importKey(open('./policies/quiz/key.txt').read())
#         # Generate a cypher using the PKCS1.5 standard
#         key = RSA.importKey(self.publicKey)
#         cipher = PKCS1_v1_5.new(key)
#         # Encrypy as bytes
#         encrypted_bytes = cipher.encrypt(message)
#         # Write encrypted string to file
#         print "Writing encrypted string to %s..." % ENCRYPTED_STRING_PATH
#         #ciphertext = encrypted_bytes.encode("base64")
# #         with open(ENCRYPTED_STRING_PATH, "wb") as f:
# #             f.write(encrypted_bytes.encode("base64"))
# #         
# #         with open(ENCRYPTED_STRING_PATH, "rb") as f:
# #             f.write(encrypted_bytes.encode("base64"))
# 
#         # Generate a cypher using the PKCS1.5 standard
# #         key = RSA.importKey(open('./policies/quiz/key_private.txt').read())
#         key = RSA.importKey(self.privateKey)
#         cipher = PKCS1_v1_5.new(key)
#         pt2 = cipher.decrypt(encrypted_bytes, "---")
#         print 'after', pt2
# #         lines = message.split('\n')
# # #         message = 'To be encrypted'
# #         print 'before', message
# #         key = RSA.importKey(open('./policies/quiz/key.txt').read())
# #         cipher = PKCS1_OAEP.new(key)
# # #         ciphertext = ''
# # #         for l in lines:
# # #             cryptLine = cipher.encrypt(l)
# # #             ciphertext+=cryptLine+'\n'
# #         ciphertext = cipher.encrypt(message)
# #         print 'encrypted', ciphertext
# #         with open('./policies/cypherAnswer', 'w') as f:
# #             f.write(ciphertext)
# #         f.close()
# #         
# #         key = RSA.importKey(open('./policies/quiz/key_private.txt').read())
# #         cipher = PKCS1_OAEP.new(key)
# # #         with open('./policies/cypherAnswer', 'r') as f:
# # #             lines = f.readlines()
# #         message = ''
# # #         for l in lines:
# # #             decryptLine = cipher.decrypt()
# # #             message += decryptLine+'\n'
# #         decryptLine = cipher.decrypt(ciphertext)
# #         message += decryptLine+'\n'
# #         print 'after', message
#          
#         self.encrypt_RSA(self.publicKey, '')
#         self.decrypt_RSA(self.key, './policies/quiz/answer_dec.txt')
        pass
    
    def loadKeyfile(self, pubkeyfile):
        import base64
        import binascii
        
        f = open(pubkeyfile,'rb') # load file from adbkey.pub
        line = f.readline() # actually oneline is enough
        line = line.replace("manw@simon.cs.mtu.edu","") # remove text information
        print line
        print len(line)
        b = base64.b64decode(line) # decode base64 into binary
        s = binascii.hexlify(b) # get hexdecimal of the binary
        print s

    def loadKeyfile1(self, pubkeyfile):
        import sys
        import base64
        import struct
        from pyasn1.type import univ
        from pyasn1.codec.der import encoder as der_encoder
        # get the second field from the public key file.
        keydata = base64.b64decode(
          open(pubkeyfile).read().split(None)[1])
        
        parts = []
        while keydata:
            # read the length of the data
            dlen = struct.unpack('>I', keydata[:4])[0]
        
            # read in <length> bytes
            data, keydata = keydata[4:dlen+4], keydata[4+dlen:]
        
            parts.append(data)
        e_val = eval('0x' + ''.join(['%02X' % struct.unpack('B', x)[0] for x in parts[1]]))
        n_val = eval('0x' + ''.join(['%02X' % struct.unpack('B', x)[0] for x in parts[2]]))
        pkcs1_seq = univ.Sequence()
        pkcs1_seq.setComponentByPosition(0, univ.Integer(n_val))
        pkcs1_seq.setComponentByPosition(1, univ.Integer(e_val))
        print '-----BEGIN RSA PUBLIC KEY-----'
        print base64.encodestring(der_encoder.encode(pkcs1_seq))


    def encrypt_RSA(self):
        os.system("ssh-keygen -f ./policies/quiz/id_rsa.pub -e -m pem > ./policies/quiz/id_rsa_pub.pem")
        os.system("ssh-keygen -f ./policies/quiz/id_rsa -e -m pem > ./policies/quiz/id_rsa_priv.pem")
#         os.system("openssl x509 -in ./policies/quiz -pubkey -noout > ssl.pub")
#         #subprocess.call(["ssh-keygen", "-f", "./policies/quiz/id_rsa.pub", "-e", "-m", "pem", ">", "./policies/quiz/id_rsa.pem"])
#         os.system("openssl rsautl -encrypt -pubin -inkey ./policies/quiz/id_rsa.pem -in ./policies/quiz/answer.txt -out ./policies/quiz/answer_enc.txt")
#         from Crypto.Cipher import PKCS1_OAEP
#         #self.loadKeyfile1('./policies/quiz/id_rsa.pub')
        file_to_encrypt = open('./policies/quiz/answer.txt', 'rb').read()
        pub_key = open('./policies/quiz/id_rsa_pub.pem', 'r').read()
        o = RSA.importKey(pub_key)
#         
#         random_generator = Random.new().read
#         key = RSA.generate(1024, random_generator) #generate pub and priv key
#         o = key.publickey() # pub key export for exchange
#         print 'public key:', o
#         rsakey = PKCS1_OAEP.new(o)
#         print 'rsakey', rsakey
        to_join = []
        step = 0
         
        while 1:
            # Read 128 characters at a time.
            s = file_to_encrypt[step*128:(step+1)*128]
            if not s: break
            # Encrypt with RSA and append the result to list.
            # RSA encryption returns a tuple containing 1 string, so i fetch the string.
            to_join.append(o.encrypt(s, 0)[0])
            step += 1
#         
#         # Join the results.
#         # I hope the \r\r\r sequence won't appear in the encrypted result,
#         # when i explode the string back for decryption.
        encrypted = ''.join(to_join)
        # Write the encrypted file.
        open('./policies/quiz/encrypted_file.txt', 'wb').write(encrypted)
         
        to_join = []
        step = 0
         
        while 1:
            # Read 128 characters at a time.
            s = encrypted[step*128:(step+1)*128]
            if not s: break
            # Encrypt with RSA and append the result to list.
            # RSA encryption returns a tuple containing 1 string, so i fetch the string.
            priv_key = open('./policies/quiz/id_rsa_priv.pem', 'r').read()
            o = RSA.importKey(priv_key)
#             cipher = PKCS1_OAEP.new(o)
            to_join.append(o.decrypt(s))
            step += 1
         
        # Join the results.
        # I hope the \r\r\r sequence won't appear in the encrypted result,
        # when i explode the string back for decryption.
        decrypted = ''.join(to_join)
        # Write the encrypted file.
#         decrypted = key.decrypt(encrypted)
        open('./policies/quiz/decrypted_file.txt', 'wb').write(decrypted)
        
        
        
        
        
        
#     def encrypt_RSA(self):
#         random_generator = Random.new().read
#         key = RSA.generate(1024, random_generator) #generate pub and priv key
#         self.key = key
#         publickey = key.publickey() # pub key export for exchange
#         subprocess.call(["./policies/quiz/encrypt", publickey, "./policies/quiz/answer.txt", "./policies/quiz/answer_enc.txt"])



#         f = open('./policies/quiz/answer.txt', 'r')
#         answer = f.read()
#         f.close()
#         encrypted = publickey.encrypt(answer, 1024)#'encrypt this message', 32)
#         #message to encrypt is in the above line 'encrypt this message'
#         
#         print 'encrypted message:', encrypted #ciphertext
#         encFile = './policies/quiz/answer_enc.txt'
#         f = open (encFile, 'w')
#         f.write(str(encrypted)) #write ciphertext to file
#         f.close()
#         '''
#         param: public_key_loc Path to public key
#         param: message String to be encrypted
#         return base64 encoded encrypted string
#         '''
#         key = open('./policies/quiz/key.txt', 'r').read()
#         rsakey = RSA.importKey(key)
#         rsakey = PKCS1_OAEP.new(rsakey)
#         encrypted = rsakey.encrypt(message)
#         return encrypted.encode('base64')
#         self.answerFileDir = './policies/quiz'#self.answerFile[:self.answerFile.rfind('/')]
#         self.answerFile = self.answerFileDir+'/answer.gpg'
#         if subprocess.call(batcmd, shell=True) == 0:
#             while os.path.isfile(self.answerFile):
#                 self.eanswerFilename = self.answerFile[self.answerFile.rfind('/')+1:]
# #                 reply = QMessageBox.warning(self.main, '', "Attempt to save the encrypted file as '"+self.answerFile+"'. But the file '"+self.eanswerFilename+\
# #                                              "'already exists under this directory. Would you like to replace it?",\
# #                                               QMessageBox.Yes|QMessageBox.No)
# #                 self.renameWarningDlg.ui.label.setText("Attempt to save the encrypted file as '"+self.answerFile+"'. But the file '"+self.eanswerFilename+\
# #                                               "'already exists under this directory. Would you like to replace it?")
# #                 self.renameWarningDlg.show()
#                 QMessageBox.warning(self.main, '', "Attempt to save the encrypted file as '"+self.answerFile+"'. But the file '"+self.eanswerFilename+\
#                                              "'already exists under this directory. Please rename the existing file and click 'OK' to continue!")
# #                 if reply == QMessageBox.No:
# #                self.answerFile = self.answerFileDir+'/'+self.eanswerFilename
# #                 else:
# #                     subprocess.call('rm '+self.answerFile, shell=True)
# #                     break
#             tempFile = self.answerFileDir+'/temp.qiza'
#             with open(tempFile, 'w') as f:
#                 f.write(message)
#             encryptCommand = 'gpg --output '+self.answerFile+' --encrypt --recipient '+self.main.instructorEmail+' '+tempFile
#             if subprocess.call(encryptCommand, shell=True) == 0:
#                 subprocess.call('rm '+tempFile, shell=True)
#                 QMessageBox.critical(self.main, '', "The encrypted answer file has been stored in '"+self.answerFile+\
#                                      "'.\nPlease send your answers to the instructor through email and install\nThunderbird for later submissions!")

    def decrypt_r(self):
        file_to_decrypt = open('./policies/quiz/encrypted_file.txt', 'rb').read()
        priv_key = open('./policies/quiz/id_rsa', 'rb').read()
        o = RSA.importKey(priv_key)
        
        to_join = []
        step = 0
        
        while 1:
            # Read 128 characters at a time.
            s = file_to_decrypt[step*128:(step+1)*128]
            if not s: break
            # Encrypt with RSA and append the result to list.
            # RSA encryption returns a tuple containing 1 string, so i fetch the string.
            to_join.append(o.decrypt(s))
            step += 1
        
        decrypted = '\r\r'.join(to_join)
        # Write the encrypted file.
        open('./policies/quiz/decrypted_file.txt', 'wb').write(decrypted)
        
#             externKey='./policies/quiz/id_rsa.pub'
#             publickey = open(externKey, "r")
#             decryptor = RSA.importKey(publickey, passphrase="f00bar")
#             retval=None
#         
#             file = open('./policies/quiz/encrypted_file.txt', "rb")
#             retval = decryptor.decrypt(file.read())
#             file.close()
#             return retval

    def decrypt_RSA(self, key, encfile):
        print '==>got to decrypt'
        subprocess.call(["./policies/quiz/decrypt", self.key.privatekey(), "./policies/quiz/answer_enc.txt", "./policies/quiz/answer_dec.txt"])
    #         f = open(encfile, 'r')
    #         encrypted = f.read()
    #         f.close()
    #         print '==>read done'
    #         print 'print', encrypted
    #         decrypted = key.decrypt(ast.literal_eval(str(encrypted)))
    #         print 'decrypted', decrypted
    #         print '==>decrypt done'
    #         f = open ('./policies/quiz/answer_dec.txt', 'w')
    #         f.write(str(decrypted))
    #         f.close()
    #         print '==>decrypt write to file done'
            
            
    #         decrypted = fileFull[:fileFull.rfind('.')]
    # #         '''
    # #         param: public_key_loc Path to your private key
    # #         param: package String to be decrypted
    # #         return decrypted string
    # #         '''
    # #         key = open('./policies/quiz/key_private.txt', "r").read()
    # #         rsakey = RSA.importKey(key)
    # #         rsakey = PKCS1_OAEP.new(rsakey)
    # #         decrypted = rsakey.decrypt(b64decode(package))
    #         batcmd = 'which gpg'
    #         if os.system(batcmd) == 0:
    #             command = 'gpg --output '+decrypted+' --decrypt --no-tty '+fileFull
    #             subprocess.call(command, shell=True)
    #         self.main.hintForDecryption()