'''
Created on Sep 3, 2015

@author: manwang
Updated for PyQt6 compatibility
'''
from PyQt6.QtWidgets import QDialog, QTableWidgetItem
from PyQt6.QtCore import Qt
from Ui_ProcessNodeParamDialog import Ui_ProcessNodeParamDialog
import PermissionChecker

class ProcessNodeParamDialog(QDialog):

    def __init__(self, main, scene):
        super().__init__()
        self.main = main
        self.scene = scene
        self.ui = Ui_ProcessNodeParamDialog()
        self.ui.setupUi(self)
        self.setLayout(self.ui.verticalLayout)
        flags = Qt.WindowType.Dialog | Qt.WindowType.WindowStaysOnTopHint
        self.setWindowFlags(flags)
        self.ui.closePushButton.clicked.connect(self.close)
    
    def setupParamValueList(self, procname, paramvaluelist):
        paramnamelist = []
        if procname == 'open':
            paramnamelist = ['int open(const char *pathname, int flags, mode_t mode)',\
                              'Path Name', 'Flags', 'Mode', 'Error']
        elif procname == 'read':
            paramnamelist = ['ssize_t read(int fd, void *buffer, size_t count)', \
                             'File Descriptor', 'Count', 'Error']
        elif procname == 'write':
            paramnamelist = ['ssize_t write(int fd, const void *buffer, size_t count)',\
                             'File Descriptor', 'Count', 'Error']
        elif procname == 'fork':
            paramnamelist = ['pid_t fork(void)', 'Return Value', 'Error']
        elif procname == 'execvp':
            paramnamelist = ['int execvp(const char *file, char *const argv[])', 'File']
            i=0
            while i < len(paramvaluelist):
                paramnamelist.append('Parameter '+str(i+1))
                i+=1
            paramnamelist[len(paramvaluelist)] = 'Error'
        elif procname == 'execl':
            paramnamelist = ['int execl(const char *path, const char *arg, ...)', 'Path']
            i=0
            while i < len(paramvaluelist):
                paramnamelist.append('Parameter '+str(i+1))
                i+=1
            paramnamelist[len(paramvaluelist)] = 'Error'
        elif procname == 'execlp':
            paramnamelist = ['int execlp(const char *file, const char *arg0, ...)', 'Path']
            i=0
            while i < len(paramvaluelist):
                paramnamelist.append('Parameter '+str(i+1))
                i+=1
            paramnamelist[len(paramvaluelist)] = 'Error'
        elif procname == 'execv':
            paramnamelist = ['int execv(const char *path, char *const argv[])', 'Path']
            i=0
            while i < len(paramvaluelist):
                paramnamelist.append('Parameter '+str(i+1))
                i+=1
            paramnamelist[len(paramvaluelist)] = 'Error'  
        elif procname == 'execvpe':
            paramnamelist = ['int execvpe(const char *file, char *const argv[], char *const envp[])', 'Path']
            i=0
            while i < len(paramvaluelist):
                paramnamelist.append('Parameter '+str(i+1))
                i+=1
            paramnamelist[len(paramvaluelist)] = 'Error'
        elif procname == 'setuid':
            paramnamelist = ['int setuid(uid_t uid)', 'Effective uid', 'Error']
        elif procname == 'setgid':
            paramnamelist = ['int setgid(gid_t gid)', 'Effective gid', 'Error']
        elif procname == 'seteuid':
            paramnamelist = ['int seteuid(uid_t euid)', 'Effective uid', 'Error']
        elif procname == 'setegid':
            paramnamelist = ['int setegid(gid_t egid)', 'Effective gid', 'Error']
        elif procname == 'setreuid':
            paramnamelist = ['int setreuid(uid_t ruid, uid_t euid)', 'Real uid', 'Effective uid', 'Error']
        elif procname == 'setregid':
            paramnamelist = ['int setregid(gid_t rgid, gid_t egid)', 'Real gid', 'Effective gid', 'Error']
        return paramnamelist
    
    def setParam(self, procname, paramvaluelist):
        if procname == 'Parent' or procname == 'Child':
            return
        paramnamelist = self.setupParamValueList(procname, paramvaluelist)
        self.ui.browser.clearContents()
        self.ui.browser.setItem(0, 0, QTableWidgetItem(paramnamelist[0]))
        for i in range(len(paramvaluelist)):  # xrange → range for Python 3
            self.ui.browser.setItem(i+1, 0, QTableWidgetItem(paramnamelist[i+1]))
            self.ui.browser.setItem(i+1, 1, QTableWidgetItem(paramvaluelist[i]))
        if procname == 'open':
            filepath = paramvaluelist[0]
            fileuser, filegroup, uid, gid = PermissionChecker.getFileUserAndGroup(filepath, None, self.scene)
            perms = PermissionChecker.getPermissionbitForFile(filepath, None, self.scene)
            permletters = PermissionChecker.convertNineBitsOctToRWX(perms)
            start = len(paramvaluelist)+1
            self.ui.browser.setItem(start, 0, QTableWidgetItem('File User Owner'))
            self.ui.browser.setItem(start, 1, QTableWidgetItem(str(uid)))
            self.ui.browser.setItem(start+1, 0, QTableWidgetItem('File Group Owner'))
            self.ui.browser.setItem(start+1, 1, QTableWidgetItem(str(gid)))
            self.ui.browser.setItem(start+2, 0, QTableWidgetItem('File Permissions'))
            self.ui.browser.setItem(start+2, 1, QTableWidgetItem(permletters))
