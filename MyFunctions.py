# COMPLETE MyFunctions.py file with font fixes:

'''
Created on Apr 20, 2015

@author: manwang
Updated for PyQt6 compatibility
'''
import re, errno, math, os, grp
from PyQt6.QtCore import QPointF, Qt
from PyQt6.QtGui import QPen, QBrush, QColor, QFont

'''Colors'''
EMERALD = QColor(80, 200,120)

'''Common'''
def is_subdir(path, directory):
    path = os.path.realpath(path)
    directory = os.path.realpath(directory)
    relative = os.path.relpath(path, directory)
    return not relative.startswith(os.pardir + os.sep)

def nameOnlyContainLetterNumbers(name):
    if re.match("^[A-Za-z0-9/]*$", name):
        return True
    return False

def checkNameDuplication(name, checklist):
    for t in checklist:
        if t == name:
            return True
    return False

def make_sure_path_exists(path):
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise   
        
def getAbsolutePath(path):
    if path[0] == '~':
        path = os.path.expanduser('~')+path[1:]
    else:
        path = os.path.abspath(path)
    return path
                    
def writeToFile(filename, message):
        with open(filename, 'a+') as f:
            f.write(message)
        f.close()
        
def removeItemFromCombobox(combobox, itemname):
    index = combobox.findText(itemname)
    if index != -1:
        combobox.removeItem(index)
        
def getNodeFromListByName(name, nodeList):
    for n in nodeList:
        if name == n.name:
            return n
    return None

def lenPoints(point1, point2):
    distX = point2.x()-point1.x()
    distY = point2.y()-point1.y()
    return math.sqrt((distX*distX)+(distY*distY))

def computeAngleDegree(point1, point2):
    temp = (point2.y()-point1.y())/(point2.x()-point1.x())
    return math.atan(temp)*180/math.pi

def computeControlPointForBezierCurve(point1, point2, isFileConn):
    ratio = 0.7
    midx = ratio*point1.pos().x()+(1-ratio)*point2.pos().x()
    midy = ratio*point1.pos().y()+(1-ratio)*point2.pos().y()
    if isFileConn and hasattr(point1, 'angle') and hasattr(point2, 'angle') and point1.angle<point2.angle:
        c1 = QPointF((1-ratio)*point1.pos().x()+ratio*midx, (1-ratio)*point1.pos().y()+ratio*midy) 
        c2 = QPointF((1-ratio)*point2.pos().x()+ratio*midx, (1-ratio)*point2.pos().y()+ratio*midy) 
    else:
        c1 = QPointF(ratio*point2.pos().x()+(1-ratio)*midx, ratio*point1.pos().y()+(1-ratio)*midy) 
        c2 = QPointF(ratio*point1.pos().x()+(1-ratio)*midx, ratio*point2.pos().y()+(1-ratio)*midy) 
    return c1, c2

def setupComboBoxItems(comboBox, itemList):
    for i in itemList:
        comboBox.addItem(i)
        
def drawHighlightBox(item, painter, color=Qt.GlobalColor.red):
    painter.save()
    painter.setPen(QPen(QBrush(color), 2.0))
    painter.setBrush(Qt.BrushStyle.NoBrush)
    painter.drawRect(item.rect().adjusted(-5, -5, 5, 5))
    painter.restore()
    
def drawHighlightBkground(item, painter, color):
    painter.save()
    painter.setPen(QPen(QBrush(color), 2.0))
    painter.setBrush(color)
    painter.drawRect(item.boundingRect())
    painter.restore()
    
def getGroupsOfUser(user):
    from sys import platform as _platform
    import subprocess
    try:
        output = subprocess.Popen(["groups", user], 
                                  stdout=subprocess.PIPE).communicate()[0]
        # Handle bytes vs string for Python 3
        if isinstance(output, bytes):
            output = output.decode('utf-8')
        startIndex = output.find(':')
        if  startIndex != -1:
            groups = output[startIndex+2:-1].split(' ')
        else:
            groups = output[:-1].split(' ')
        return groups
    except:
        return []

def getUserAndGroupListOnSystem(rootdir, progDir):
    userset, groupset, user_group_sys_mat = set(), set(), {}
    from sys import platform as _platform
    if _platform == "darwin":
        import pwd
        for p in pwd.getpwall():
            if p[0].find('_')==-1:
                userset.add(p[0])
        groups = grp.getgrall()
        counter = 0
        for group in groups:
            g = group[0]
            if g.find('_')==-1:
                groupset.add(g)
            for user in group[3]:
                if user.find('_')==-1:
                    userset.add(user)
            counter+=1
        for u in userset:
            usergroup = getGroupsOfUser(u)
            toRemove = set()
            for g in usergroup:
                if g.find('_')!=-1:
                    toRemove.add(g)
            for r in toRemove:
                usergroup.remove(r)
            user_group_sys_mat.update({u: set(usergroup)})
    else:
        import subprocess
        '''get all users'''
        try:
            output = subprocess.Popen(["cut", "-d:", "-f1", "/etc/passwd"], 
                                      stdout=subprocess.PIPE).communicate()[0]
            if isinstance(output, bytes):
                output = output.decode('utf-8')
            userset = set(output.split('\n'))
            userset = set(x for x in userset if x != '')
        except:
            userset = set()
        '''get all groups'''
        try:
            output = subprocess.Popen(["cut", "-d:", "-f1", "/etc/group"], 
                                      stdout=subprocess.PIPE).communicate()[0]
            if isinstance(output, bytes):
                output = output.decode('utf-8')
            groupset = set(output.split('\n'))
            groupset = set(x for x in groupset if x != '')
        except:
            groupset = set()
        '''assign user to groups'''
        for u in userset:
            usergroup = getGroupsOfUser(u)
            user_group_sys_mat.update({u: set(usergroup)})
    os.chdir(progDir)
    return list(userset), list(groupset), user_group_sys_mat
                
def checkDirectoryExistence(direc):
    hasDir = False
    if os.path.isdir(direc):
        hasDir = os.path.exists(direc)
    return hasDir

def setFontForUI(widget, size=20):
    import platform
    
    # Ensure size is integer (PyQt6 requirement)
    size = int(size)
    
    operSys = platform.system()
    if operSys == 'Linux':
        font = widget.font()
        font.setPointSize(size)
        widget.setFont(font)
    elif operSys == 'Darwin':
        # MINIMAL FIX: Just replace the missing 'Courier' with 'Monaco' 
        # Keep everything else the same as original
        font = QFont('Monaco', size)
        widget.setFont(font)

# Also fix any direct QFont('Courier', size) calls
# Replace lines like: font = QFont('Courier', size)
# With this cross-platform function:

def getSystemFont(size=12):
    import platform
    
    # Ensure size is integer
    size = int(size)
    
    operSys = platform.system()
    
    if operSys == 'Darwin':  # macOS
        # Use Monaco for monospace (replaces Courier)
        return QFont('Monaco', size)
    elif operSys == 'Linux':
        # Use Liberation Mono for monospace
        return QFont('Liberation Mono', size)
    elif operSys == 'Windows':
        # Use Consolas for monospace
        return QFont('Consolas', size)
    else:
        # Generic monospace fallback
        return QFont('monospace', size)
