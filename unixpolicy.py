"""
file:   unixpolicy.py
author: manwang
description:
        Functions for converting a unix policy into a 
        set of data structures representing the policy.
"""
from collections import namedtuple
from unixparse import unixparse

'''Unix'''
ObjectCred = namedtuple('ObjCred', ('directory', 'user', 'group'))
ObjectPermUnix = namedtuple('ObjectPermUnix', ('recursive', 'userperm', 'groupperm', 'otherperm'))
'''ACL'''
ObjectPermACL = namedtuple('ObjectPermACL', ('directory', 'recursive', 'permissions'))

def makeobjectcred(directory=False, user=None, group=None):
    return ObjectCred(directory, user, group)

def makeobjpermunix(recursive=False, userperm=[], groupperm=[], otherperm=[]):
    return ObjectPermUnix(recursive, userperm, groupperm, otherperm)

def makeobjpermacl(directory=False, recursive=False, permissions=[]):
    return ObjectPermACL(directory, recursive, permissions)

def formatForUNIX(stmt, obj_cred_mat, obj_perm_mat):
    permall = stmt[0]
    permuser = []
    permgroup = []
    permother = []
    if permall[0] == 'd':
        index = 1
        is_dir = True
    else:
        index = 0
        is_dir = False
    for p in permall[index:index+3]:
        if p != '-':
            permuser.append(p)
    for p in permall[index+3:index+6]:
        if p != '-':
            permgroup.append(p)
    for p in permall[index+6:]:
        if p != '-':
            permother.append(p)
    user = stmt[1]
    group = stmt[2]
    if stmt[3] == '-r':
        is_recur = True
    else:
        is_recur = False
    obj = stmt[-1]
    obj_cred_mat[obj] = makeobjectcred(is_dir, user, group)
    obj_perm_mat[obj] = makeobjpermunix(is_recur, permuser, permgroup, permother)
    
def formatForACL(stmt, user_obj_perm_mat, group_obj_perm_mat):
    perms = stmt[0]
    if perms[0] == 'd':
        index = 1
        is_dir = True
    else:
        index = 0
        is_dir = False
    permission = []
    pe = perms[index:]
    for p in pe:
        if p != '-':
            permission.append(p)
    userlist = stmt[1]
    grouplist = stmt[2]
    if stmt[3] == '-r':
        is_recur = True
    else:
        is_recur = False
    obj = stmt[-1]
    for u in userlist:
        if u not in user_obj_perm_mat.keys():
            user_obj_perm_mat[u] = {obj:makeobjpermacl(is_dir, is_recur, permission)}
        else:
            user_obj_perm_mat[u][obj] = makeobjpermacl(is_dir, is_recur, permission)
    for g in grouplist:
        if g not in group_obj_perm_mat.keys():
            group_obj_perm_mat[g] = {obj:makeobjpermacl(is_dir, is_recur, permission)}
        else:
            group_obj_perm_mat[g][obj] = makeobjpermacl(is_dir, is_recur, permission)
    
# def getabsolutedir(dir):
    
def unixpolicy(source, verbose=False):
    '''
    Initialize an RBAC policy representation.
    Args:
        source (file or filename): The RBAC policy file
        verbose (bool): be verbose.
    
    Returns: 
        root_dir (string): root directory.
            the directory to start from to extract information on the real OS
        user_group_mat (dict): user and group assignment.
            user_group_mat['user] returns the groups the user assigned to
        For UNIX model:
            obj_cred_mat (dict): contains the directory flag and the owner user and group info of objects.
                obj_cred_mat['/path/to/obj'] returns a namedtuple with fields of a flag for whether the object 
                is a directory, the owner user and the owner group of the object.
            obj_perm_mat (dict): contains the permissionbits of the objects.
                obj_perm_mat['/path/to/obj'] returns a namedtuple with fields of a flag for the permission 
                recursiveness, the permission bits for identities in user, group and other categories.
                The permission bits for each category are represented in list.
        For ACL model:
            user_obj_perm_mat (dict): user permissions on objects.
                user_obj_perm_mat['user']['/path/to/obj']: returns a namedtuple that has flag of directory,
                    recursiveness of the permission and the permission list.
            group_obj_perm_mat (dict): group permissions on objects.
                group_obj_perm_mat['group']['/path/to/obj']: returns a namedtuple that has flag of directory,
                    recursiveness of the permission and the permission list.
    '''
    isUNIX_flag = True
    user_group_mat = {}
    '''UNIX'''
    obj_cred_mat = {}
    obj_perm_mat = {}
    '''ACL'''
    user_obj_perm_mat = {}
    group_obj_perm_mat = {}
    try:
        text = source.read()
    except AttributeError:
        with open(source, 'r') as f:
            text = f.read()
    stmts = unixparse(text)
    stmttype = stmts[0]
    
    if stmttype == 'ACL':
        isUNIX_flag = False
    for stmt in stmts:
        stmttype = stmt[0]
        if stmttype == 'root:':
            root_dir = stmt[1]
        elif stmttype == 'user:':
            user_list = stmt[1]
        elif stmttype == 'group:':
            group = stmt[1]
            users = stmt[2]
            for u in users:
                if u in user_group_mat.keys():
                    user_group_mat[u].add(group)
                else:
                    user_group_mat[u] = set([group])
        elif stmttype == 'object:':
            if isUNIX_flag:
                formatForUNIX(stmt[1:], obj_cred_mat, obj_perm_mat)
            else:
                formatForACL(stmt[1:], user_obj_perm_mat, group_obj_perm_mat)
    for u in user_list:
        if u not in user_group_mat.keys():
            user_group_mat[u] = set()
    if isUNIX_flag:
        return isUNIX_flag, root_dir, user_group_mat, obj_cred_mat, obj_perm_mat
    else:
        return isUNIX_flag, root_dir, user_group_mat, user_obj_perm_mat, group_obj_perm_mat
    
if __name__ == '__main__':
    import sys
    if len(sys.argv)<2:
        source = sys.stdin
    else:
        source = sys.argv[1]
    flag, root, user_group_mat, mat1, mat2 = unixpolicy(source)
    print '== Model type =='
    print flag
    print '== Root directory =='
    print root
    print '== User assignment to group =='
    for key, value in user_group_mat.items():
        print 'user = {0}'.format(key)
        print '    groups = {0}'.format(','.join(value))
    if flag:
        print '== Object credential matrix =='
        for res, creddict in mat1.items():
            print 'res = {0}'.format(res)
            print '    directory = {0}'.format(creddict.directory)
            print '        user = {0}'.format(creddict.user)
            print '        group = {0}'.format(creddict.group)
        print '== Object permission matrix =='
        for res, permdict in mat2.items():
            print 'res = {0}'.format(res)
            print '    recursive = {0}'.format(permdict.recursive)
            print '     permUser = {0}'.format(','.join(permdict.userperm))
            print '     permGroup = {0}'.format(','.join(permdict.groupperm))
            print '     permOther = {0}'.format(','.join(permdict.otherperm))
    else:
        print '== User permissions to objects matrix =='
        for user, resdict in mat1.items():
            print 'user = {0}'.format(user)
            for res, perms in resdict.items():
                print '    resource = {0}'.format(res)
                print '        directory = {0}'.format(perms.directory)
                print '        recursive = {0}'.format(perms.recursive)
                print '        permissions = {0}'.format(','.join(perms.permissions))
        print '== Group permissions to objects matrix =='
        for group, resdict in mat2.items():
            print 'group = {0}'.format(group)
            for res, perms in resdict.items():
                print '    resource = {0}'.format(res)
                print '        directory = {0}'.format(perms.directory)
                print '        recursive = {0}'.format(perms.recursive)
                print '        permissions = {0}'.format(','.join(perms.permissions))