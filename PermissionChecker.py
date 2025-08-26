'''
Created on Jun 22, 2015

@author: manwang
Updated for Python 3 compatibility
'''
import pwd, grp, os
from stat import *
import MyFunctions
from collections import namedtuple
from UserNode import *
from GroupNode import GroupNode
from PyQt6.QtWidgets import QMessageBox

Permission = namedtuple('Permission', ('category', 'permList'))

def makePermission(cate = 'other', perms = []):
    return Permission(cate, perms)
    
def getFileUserAndGroup(path, fnode, scene):
    user = None
    group = None
    uid = -1
    gid = -1
    creds = scene.main.obj_cred_mat
    if path:
        if os.path.exists(path):
            try:
                stat_info = os.stat(path)
            except Exception as e:
                return None, None, -1, -1
            uid = stat_info.st_uid
            gid = stat_info.st_gid
            user = pwd.getpwuid(uid)[0]
            group = grp.getgrgid(gid)[0]
        else:
            filename = ''
            if path[-1] == '/' and path != '/':
                fpath = path[:-1]
            else:
                fpath = path
            if scene.main.root_dir and (scene.main.root_dir in fpath):
                if scene.main.root_dir[-1] != '/':
                    index = 0
                else:
                    index = 1
                for k in creds.keys():
                    if fpath == scene.main.root_dir+k[index:]:
                        filename = k
            else:
                filename = fpath
            if filename != '' and filename in creds:
                v = creds[filename]
                user = v.user
                group = v.group
                uid = -1
                gid = -1
            else:
                user = None
                group = None
                uid, gid = -1, -1
    return user, group, uid, gid

def getPermissionbitForFile(filepath, fnode, scene):
    obj_perm = scene.main.obj_perm_mat
    if os.path.exists(filepath):
        try:
            st = os.stat(filepath)
        except Exception as e:
            return "%05o" % int(0o0)
        return "%05o" % (st.st_mode & 0o7777)
    else:
        filename = ''
        if filepath[-1] == '/' and filepath != '/':
            fpath = filepath[:-1]
        else:
            fpath = filepath
        if  scene.main.root_dir and scene.main.root_dir in fpath:
            if scene.main.root_dir[-1] != '/':
                index = 0
            else:
                index = 1
            for k in obj_perm.keys():
                if fpath == scene.main.root_dir+k[index:]:
                    filename = k
        else:
            filename = fpath
        if filename != '' and filename in obj_perm:
            permnum = 0
            v = obj_perm[filename]
            uperm = convertRWXToOct(v.userperm)
            gperm = convertRWXToOct(v.groupperm)
            operm = convertRWXToOct(v.otherperm)
            permnum=uperm*64+gperm*8+operm
            if ('s' in v.userperm) or ('S' in v.userperm):
                permnum+=2048
            if ('s' in v.groupperm) or ('S' in v.groupperm):
                permnum+=1024
            if ('t' in v.otherperm) or ('T' in v.otherperm):
                permnum+=512
            return "%05o" % permnum
        else:
            return "%05o" % int(0o0)

def convertRWXToOct(permset):
    permnum = 0
    if 'r' in permset:
        permnum+=4
    if 'w' in permset:
        permnum+=2
    if ('x' in permset) or ('s' in permset) or ('t' in permset):
        permnum+=1
    return permnum

def convertOctToRWX(perm, bits, setid = False, stkbit = False):
    permList = []
    if bool(perm&0o4):
        permList.append('r')
    if bool(perm&0o2):
        permList.append('w')
    if bool(perm&0o1):
        if setid:
            permList.append('s')
        elif bits=='other' and stkbit:
            permList.append('t')
        else:
            permList.append('x')
    else:
        if setid:
            permList.append('S')
        elif bits == 'other' and stkbit:
            permList.append('T')
    return permList

def convertOctToRWXString(perm, setid = False, otherbit = False, stkbit = False):
    perms = ''
    if bool(perm&0o4):
        perms+='r'
    else:
        perms+='-'
    if bool(perm&0o2):
        perms+='w'
    else:
        perms+='-'
    if bool(perm&0o1):
        if setid:
            perms+='s'
        else:
            perms+='x'
    else:
        if setid:
            perms+='S'
        else:
            perms+='-'
    if otherbit:
        if stkbit:
            perms+='t'
        else:
            perms+='-'
    return perms

def convertNineBitsOctToRWX(perm):
    """
    FIXED FUNCTION: Convert octal permission string to rwx string
    Input: '00640' (5-digit octal string)
    Output: 'rw-r-----' (9-character rwx string)
    """
    perms = ''
    
    # Handle the case where perm might be shorter than 5 digits
    if len(perm) < 5:
        perm = perm.zfill(5)  # Pad with leading zeros
    
    # Extract the permission digits (last 3 digits)
    start = len(perm) - 3  # Start from the last 3 digits
    userp = int(perm[start], 8)     # User permissions (6 in 0640)
    groupp = int(perm[start+1], 8)  # Group permissions (4 in 0640)  
    otherp = int(perm[start+2], 8)  # Other permissions (0 in 0640)
    
    # Convert the full permission integer for special bit checking
    full_perm = int(perm, 8)
    
    # Convert each octal digit to rwx string
    perms += convertOctToRWXString(userp, full_perm & S_ISUID)
    perms += convertOctToRWXString(groupp, full_perm & S_ISGID)
    perms += convertOctToRWXString(otherp, False, True, full_perm & S_ISVTX)
    
    return perms

def checkParentDirectoriesForUserNode(filepath, fnode, unode, scene):
    dirlist = filepath.split('/')
    dirs = [x for x in dirlist if x != '']
    for i in range(len(dirs)-1):
        path = '/'
        path += '/'.join(dirs[:i+1])
        perm = checkUserPermForFile(path, fnode, unode, scene)
        if 'x' not in perm[1] and 's' not in perm[1] and 't' not in perm[1]:
            return 0
    return 1
        
def checkParentDirectoriesForGroupNode(filepath, gnode, scene):
    import re
    dirlist = filepath.split('/')
    dirs = [x for x in dirlist if x != '']
    for i in range(len(dirs)-1):
        path = '/'
        path += '/'.join(dirs[:i+1])
        path = re.sub('/+', '/', path)
        fileuser, filegroup, uid, gid = getFileUserAndGroup(path, None, scene)
        if fileuser == None and uid == -1:
            return None
        perms = getPermissionbitForFile(path, None, scene)
        perms = int(perms, 8)
        groupnode = MyFunctions.getNodeFromListByName(filegroup, scene.groupNodeList)
        if gnode== groupnode:
            p = (perms&0o070)>>3
            if p>0:
                perm = convertOctToRWX(p, 'group', perms & S_ISGID)
                if 'x' not in perm and 's' not in perm:
                    return 0
                else:
                    return 1
        p = perms&0o007
        perm = convertOctToRWX(p, 'other', False, perms & S_ISVTX)
        if 'x' not in perm and 't' not in perm:
            return 0
        else:
            return 1

def checkUserPermForOneFileViaGroup(gnode, d, fhighlight, scene, permset = set(['r', 'w', 'x'])):
    result = [0, 0]
    if d.permset == set():
        filepath = d.getFullPath()
        if scene.main.focusNode in scene.userNodeList:
            if not checkParentDirectoriesForUserNode(filepath, d, scene.main.focusNode, scene):
                return result
        elif scene.main.focusNode in scene.groupNodeList:
            if not checkParentDirectoriesForGroupNode(filepath, scene.main.focusNode, scene):
                return result
        fileuser, filegroup, uid, gid = getFileUserAndGroup(filepath, d, scene)
        if fileuser == None and uid == -1:
            return None
        perms = getPermissionbitForFile(filepath, d, scene)
        perms = int(perms, 8)
        groupnode = MyFunctions.getNodeFromListByName(filegroup, scene.groupNodeList)
        if gnode!= groupnode:
            return result
        p = (perms&0o070)>>3
        if fhighlight:
            if p>0 and d.accessible==-1:
                d.accessible = 1
                d.permset = d.permset.union(set(convertOctToRWX(p, 'group', perms & S_ISGID)))
            elif p == 0:
                d.accessible = -2
        result = [0, p]
        if permset.issubset(set(convertOctToRWX(p, 'group', perms & S_ISGID))):
            result[0] = 1
    return result
        
def checkUserPermForFileViaGroup(gnode, scene, permset = set(['r', 'w', 'x'])):
    for d in scene.dirNodeList:
        checkUserPermForOneFileViaGroup(gnode, d, True, scene, permset)
                
def checkUserPermForOneFileViaUser(unode, d, fhighlight, scene, permset = set(['r', 'w', 'x'])):
    result = [0, 0]
    filepath = d.getFullPath()
    if scene.main.focusNode in scene.userNodeList:
        if not checkParentDirectoriesForUserNode(filepath, d, scene.main.focusNode, scene):
            return result
    elif scene.main.focusNode in scene.groupNodeList:
        if not checkParentDirectoriesForGroupNode(filepath, scene.main.focusNode, scene):
            return result
    fileuser, filegroup, uid, gid = getFileUserAndGroup(filepath, d, scene)
    if fileuser == None and uid == -1:
            return result
    perms = getPermissionbitForFile(filepath, d, scene)
    perms = int(perms, 8)
    if unode.name == fileuser:
        p = (perms&0o700)>>6
        if fhighlight:
            if p>0: 
                d.accessible = 0
                d.permset = d.permset.union(set(convertOctToRWX(p, 'user', perms & S_ISUID)))
            else:
                d.accessible = -2
        result = [0, p]
        if permset.issubset(set(convertOctToRWX(p, 'user', perms & S_ISUID))):
            result[0] = 1
    return result
                
def checkUserPermForFileViaUser(unode, scene, permset = set(['r', 'w', 'x'])):
    for d in scene.dirNodeList:
        checkUserPermForOneFileViaUser(unode, d, True, scene, permset)
            
def checkUserPermForOneFileViaOther(d, fhighlight, scene, permset = set(['r', 'w', 'x'])):
    result = [0, 0]
    if d.permset == set():
        filepath = d.getFullPath()
        if scene.main.focusNode in scene.userNodeList:
            if not checkParentDirectoriesForUserNode(filepath, d, scene.main.focusNode, scene):
                return result
        elif scene.main.focusNode in scene.groupNodeList:
            if not checkParentDirectoriesForGroupNode(filepath, scene.main.focusNode, scene):
                return result
        perms = getPermissionbitForFile(filepath, d, scene)
        perms = int(perms, 8)
        p = perms&0o007
        if fhighlight:
            if p>0 and d.accessible==-1:
                d.accessible = 2
                d.permset = d.permset.union(set(convertOctToRWX(p, 'other', False, perms & S_ISVTX)))
            elif p==0:
                d.accessible = -2
        result = [0, p]
        if permset.issubset(set(convertOctToRWX(p, 'other', False, perms & S_ISVTX))):
            result[0] = 1
    return result

def checkParentDirectoriesForOther(filepath, scene):
    dirlist = filepath.split('/')
    dirs = [x for x in dirlist if x != '']
    for i in range(len(dirs)-1):
        path = '/'
        path += '/'.join(dirs[:i+1])
        perms = getPermissionbitForFile(path, None, scene)
        perms = int(perms, 8)
        p = perms&0o007
        perm = convertOctToRWX(p, 'other', False, perms & S_ISVTX)
        if 'x' not in perm and 's' not in perm and 't' not in perm:
            return 0
    return 1
      
def checkUserPermForFileViaOther(scene, permset = set(['r', 'w', 'x'])):
    for d in scene.dirNodeList:
        checkUserPermForOneFileViaOther(d, True, scene, permset)
        
def checkUserPermForFile(filepath, fnode, usernode, scene):
    fileuser, filegroup, uid, gid = getFileUserAndGroup(filepath, fnode, scene)
    if fileuser == None and uid == -1:
        return None
    perms = getPermissionbitForFile(filepath, fnode, scene)
    perms = int(perms, 8)
    groupnode = MyFunctions.getNodeFromListByName(filegroup, scene.groupNodeList)
    permission = makePermission()
    if usernode.name == fileuser:
        p = (perms&0o700)>>6
        permission = makePermission('user', convertOctToRWX(p, 'user', perms & S_ISUID))
    elif usernode.isMemberOfGroup(groupnode):
        p = (perms&0o070)>>3
        permission = makePermission('group', convertOctToRWX(p, 'group', perms & S_ISGID))
    else:
        p = perms&0o007
        permission = makePermission('other', convertOctToRWX(p, 'other', False, perms & S_ISVTX))
    return permission
