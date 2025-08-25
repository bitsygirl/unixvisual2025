'''
Created on Jul 21, 2015

@author: manwang
'''
import socket, os, errno
import re
from PyQt4.QtGui import QMessageBox

class SystemCallSocket(object):

    def __init__(self, main):
        self.sock = None
        self.recvData = ''
        self.main = main
        self.scene = main.syscallViewScene
            
    def createServerSocket(self, programFile):
        BUFFER_SIZE = 100
        '''create a TCP/IP socket'''
#         if not self.sock:?
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        '''bind the socket to the port'''
        serverAddress = ('127.0.0.1', 0)
        
        self.sock.bind(serverAddress)
        serverAddress = self.sock.getsockname()
        print 'starting up on %s port %s'%serverAddress
        portbuf = str(serverAddress[1])
        '''listen for incoming connections'''
        self.sock.listen(1)
        
        '''fork a new process'''
        '''runit program actually connects to the socket'''
        from subprocess import Popen, PIPE
        process = Popen([self.main.currDir+"/runit", portbuf, programFile], stdout=PIPE)
        (output, err) = process.communicate()
        self.scene.codeOutputDlg.hide()
        if output:
            self.scene.codeOutputDlg.ui.textEdit_Output.setPlainText(output)
            self.scene.codeOutputDlg.show()
        childPid = os.fork()
        if childPid == 0:
            args = ("runit", portbuf, programFile)
            os.execvp(self.main.currDir+"/runit", args)
#             os.execvp("/home/campus16/manw/runit", args)
            return 1
        '''open socket for communication'''
        '''this is done by accepting a connection from another process'''
        connection, clientAddress = self.sock.accept()
        print 'Connection address:', clientAddress
        self.recvData = ''
        prev = ''
        while 1:
            try:
                data = connection.recv(BUFFER_SIZE)
            except socket.error as (code, msg):
                if code != errno.EINTR:
                    raise
            if not data: break
            if prev.find('Status')!=-1 and data==prev:
                prev = data
            else:
                self.recvData+=data
                prev = data
        connection.close()
        print "received data:", self.recvData
        temp = self.recvData.replace(' ', '')
        if re.match(r'^(Initialpid:[0-9]+(\n)*)+$', temp):
            QMessageBox.warning(self.main.syscallViewScene.codeDisplayDlg, 'Program Trace', 'The input program does not use any system call included by the visualization system\nNo visualization is generated!', QMessageBox.Ok)
            return -1
        self.scene.pass2visual(self.recvData)
#         childStatus = 0
#         tpid = os.waitpid(childPid, childStatus)
#         print "parent process done waiting for the child process!"
        '''
        Stop listening for connections.
        We could have closed this right after accept() since we only handle one connection.
        '''
        self.sock.close()
        return 0
    
    
