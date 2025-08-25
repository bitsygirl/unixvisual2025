'''
Created on Sep 2, 2015

@author: manwang
Updated for Python 3 and PyQt6 compatibility
'''

from PyQt6.QtCore import QObject, qDebug
from PyQt6.QtNetwork import QTcpSocket, QTcpServer, QHostAddress
import os

class SystemCallQtSocket(QObject):
    def __init__(self, main):
        super().__init__()
        self.server = None#QTcpServer()
        self.sock = None
        self.recvData = ''
        self.main = main
        self.scene = main.syscallViewScene
#         self.server.newConnection.connect(self.acceptConnection)
#         self.server.listen(QHostAddress.Any, 8888)
    
    def acceptConnection(self):
        self.sock = self.server.nextPendingConnection()
        self.sock.readyRead.connect(self.startRead)
        print('sock', self.sock)
        
#     def disconnected(self):
#         self.sock.close()
    
    def startRead(self):
        qDebug("Reading: "+ str(self.sock.bytesAvailable()))
        data = self.sock.readAll().data()
        qDebug(str(data))
        self.recvData += data.decode('utf-8')
        print("received data:", self.recvData)
        self.scene.pass2visual(self.recvData)
        self.sock.close()
        
    def createServerSocket(self, programFile):
        '''create TCP/IP server'''
        self.server = QTcpServer()
        ret = self.server.listen(QHostAddress.SpecialAddress.LocalHost, 0)
        portbuf = self.server.serverPort()
        '''create a TCP/IP socket'''
        #qDebug("Listening:"+str(ret))
        print('Listening...')
        self.server.newConnection.connect(self.acceptConnection)
        
        '''fork a new process'''
        '''runit program actually connects to the socket'''
        childPid = os.fork()
        if childPid == 0:
            args = ("runit", str(portbuf), programFile)
            os.execvp("./policies/code/runit", args)
            print('runit error')
            return 1

#         childStatus = 0
#         tpid = os.waitpid(childPid, childStatus)
#         print("parent process done waiting for the child process!")
#         '''
#         Stop listening for connections.
#         We could have closed this right after accept() since we only handle one connection.
#         '''
#         self.sock.close()
        return 0
