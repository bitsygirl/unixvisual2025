'''
Created on Jun 16, 2015

@author: manwang
Updated for Python 3 and PyQt6 compatibility
'''       
from PyQt6.QtCore import QRect, QRectF, QPointF, QFileInfo
from collections import namedtuple
from FileNode import FileNode
from EdgeItem import EdgeItem
import math, os

Path = namedtuple('Path', ('parent', 'name'))

def makePath(parent = None, name = None):
    return Path(parent, name)

def printAFileNode(n):
    if n.dirpath:
        print('node', n.dirpath, n.name)
    else:
        print('node', 'None', n.name)
            
def printListofList(listl):
    for i in range(len(listl)):
        for l in listl[i]:
            print(i, l.getFullPath(), l.specNode)
    
def printDictionaryOfFileNodes(dictionary):
    for i in range(0, len(dictionary)):
        for n in dictionary[i]:
            print(i, n.dirpath, n.name)
            print('parent')
            if n.parent:
                print(n.parent.dirpath, n.parent.name)
            else:
                print('None', 'None')
            print('children')
            for c in n.children:
                print(c.dirpath, c.name)
                
def list_files(startpath, depth=1000):
    count = 0
    dirlist = [makePath(None, os.path.normpath(startpath)+'/')]
    filelist = []
    if not os.access(startpath, os.R_OK):
        return dirlist, [-1]
    for root, dirs, files in os.walk(startpath):
#         print(root, dirs, files)
        if ".git" in root:
            continue
        level = root.replace(startpath, '').count(os.sep)
        if count == depth:
            break
#         indent = ' ' * 4 * (level)
#         print('{}{}/'.format(indent, os.path.basename(root)))
#         subindent = ' ' * 4 * (level + 1)
        rootpath = os.path.normpath(root)
        if rootpath[-1]!='/':
            rootpath += '/'
        for d in dirs:
            name = os.path.normpath(d)
            if name[-1] !='/':
                name += '/'
            path = makePath(rootpath, name)
            dirlist.append(path)
        for f in files:
            path = makePath(rootpath, os.path.normpath(f))
            filelist.append(path)
#             print('{}{}'.format(subindent, f))
#             print('{}{}'.format(subindent, os.path.join(root, f)))
        count+=1
    return dirlist, filelist

# def calculateLeaveNumber(root):
#     nodesToVisit = [root]
#     while nodesToVisit:
#         n = nodesToVisit[-1]
#         children = list(n.children)
#         if children:
#             if children[0].visited:
#                 n.leaves = 0
#                 for c in children:
#                     n.leaves += c.leaves
#                 n.visited = True
#                 nodesToVisit.pop()
#             else: 
#                 for c in children:
#                     nodesToVisit.append(c)
#         else:
#             n.visited = True
#             n.leaves = 1
#             nodesToVisit.pop()
            
# def calculateLevelCircles(rootX, rootY, vWidth, vHeight, dirHier, dirGraph):
#     if len(dirHier)>1:
#         d = (min(vWidth, vHeight)-120) / 2.0  / (len(dirHier)-1)
#         for level in range(1, len(dirHier)):
#             radius = d * level
#             dirGraph[level][1] = QRectF(rootX-radius, rootY-radius, 2*radius, 2*radius)
            
# def dirGraphMapToScreen(scene):
#     dirHier = scene.dirHier
#     dirGraph = scene.dirGraph
#     numLevels = len(dirHier)
#     viewportWidth = scene.main.view.viewport().width()*0.5
#     viewportHeight = scene.main.view.viewport().height()
#     radius = (min(viewportWidth, viewportHeight) - 120) / 2.0
#     if numLevels >1:
#         d =  radius / (numLevels-1)
#     rootX = viewportWidth
#     rootY = 0.0
#     prevLeftLimit = 0
#     for level in range(len(dirHier)):
#         if level == 0:
#             rootNode = dirHier[0][0]
#             rootNode.relativeX = rootX
#             rootNode.relativeY = rootY
#             rootNode.wedgeAngle = 2 * math.pi 
#         elif level == 1:
#             node = dirHier[1][0]
#             parent = node.parent
#             node.wedgeAngle =float(node.leaves)/float(parent.leaves)*parent.wedgeAngle
#             node.rightLimit = -node.wedgeAngle/2.0
#             node.leftLimit = node.wedgeAngle/2.0
#             prevLeftLimit = node.leftLimit
#             node.relativeX = d+rootX
#             node.relativeY = 0
#             for i in range(1, len(dirHier[1])):
#                 node = dirHier[1][i]
#                 node.wedgeAngle = float(node.leaves)/float(node.parent.leaves)*node.parent.wedgeAngle
#                 node.angle = prevLeftLimit + node.wedgeAngle/2.0
#                 node.rightLimit = prevLeftLimit
#                 node.leftLimit = node.angle + node.wedgeAngle/2.0
#                 prevLeftLimit = node.leftLimit
#                 node.relativeX = d * math.cos(node.angle)+rootX
#                 node.relativeY = d * math.sin(node.angle)
#         else:
#             curParent = dirHier[level][0].parent
#             prevLeftLimit = curParent.rightLimit
#             for node in dirHier[level]:
#                 parent = node.parent
#                 if parent is not curParent:
#                     prevLeftLimit = parent.rightLimit
#                     curParent = parent
#                 node.wedgeAngle = float(node.leaves)/float(parent.leaves)*parent.wedgeAngle#, 2.0*math.pi/3.0)
#                 node.angle = prevLeftLimit + node.wedgeAngle/2.0
#                 node.rightLimit = prevLeftLimit
#                 node.leftLimit = node.angle + node.wedgeAngle/2.0
#                 prevLeftLimit = node.leftLimit
#                 node.relativeX = level*d*math.cos(node.angle)+rootX
#                 node.relativeY = level*d*math.sin(node.angle)
#     edges = set()
#     for nodes in dirHier:
#         for n in nodes:
#             for e in n.edgeList:
#                 edges.add(e)
#             n.setPos(n.relativeX+viewportWidth/2.0, -n.relativeY+viewportHeight/2.0)
#     for e in edges:
#         e.updatePosition()
#     
#     levelNodes = rootNode.children
#     level = 1
#     while levelNodes:
#         dirGraph[level] = [list(levelNodes), None]
#         levelNodes = set()
#         for n in dirGraph[level][0]:
#             if n.children:
#                 levelNodes = levelNodes.union(n.children)
#         level += 1
#     calculateLevelCircles(rootNode.pos().x(), rootNode.pos().y(), viewportWidth, viewportHeight, dirHier, dirGraph)
#     
# def genRadialLayout(scene, center, width, height):
#     dirHier = scene.dirHier
#     for d in scene.dirNodeList:
#         d.visited = False
#     calculateLeaveNumber(dirHier[0][0])
#     dirGraphMapToScreen(scene)
    
def constructSpecDirecTree(dirList, main):
    rootnode = FileNode(None, '/', False, main, True)
    dirHier = [[rootnode]]
    dirNodeList = [rootnode]
    for d in dirList:
        if d!='/':
            index = d.rfind('/')
            path = d[:index+1]
            name = d[index+1:]
            if d in main.obj_cred_mat.keys(): 
                isFile = not main.obj_cred_mat[d].directory
            else:
                isFile = False
            node = FileNode(path, name, isFile, main, True)
            dirNodeList.append(node)
    dirNodeList = sorted(dirNodeList, key=lambda x: len(x.getFullPath().split('/')))
    for n in dirNodeList:
        for p in dirNodeList:
            if p.fullpath != n.fullpath and p.fullpath == n.dirpath:
                n.parent = p
    for n in dirNodeList:
        if n.parent:
            n.parent.specChildren.add(n)
            #n.parent.children.add(n)
            n.parent.isFile = False
    tovisit = dirHier[0]
    while tovisit:
        nextlevel = set()
        for v in tovisit:
            nextlevel = nextlevel.union(set(v.specChildren))
        tovisit = list(nextlevel)
        tovisit = sorted(tovisit, key=lambda d:d.getFullPath())
        dirHier.append(tovisit)
#     for i in range(0, len(dirHier)):
#         for n in dirHier[i]:
#             print(i, n.getFullPath())
#             print('parent')
#             if n.parent:
#                 print(n.parent.getFullPath())
#             else:
#                 print('None')
#             print('children')
#             for c in n.specChildren:
#                 print(c.getFullPath())
    return dirHier, dirNodeList
    
def constructDirecTree(startpath, main, fnodeclicked):
    scene = main.scene
    dirNodeList = []
    main.access_root_dir = True
    dirlist, filelist = list_files(startpath, 1)
    if filelist == [-1]:
        main.access_root_dir = False
        filelist = []
    for d in dirlist:
        if fnodeclicked and d == dirlist[0]:
            node = fnodeclicked
        else:
            node = FileNode(d.parent, d.name, False, main)
        for n in reversed(dirNodeList):
            fullPath = n.getFullPath()
            if fullPath == d.parent:
                node.parent = n
                n.addChild(node)
                edge = EdgeItem(EdgeItem.FILE_CONN, n, node, main)
                n.edgeList.append(edge)
                scene.addItem(edge)
        dirNodeList.append(node)
        if node not in scene.items():
            scene.addItem(node)
    
    for f in filelist:
        node = FileNode(f.parent, f.name, True, main)
        for n in dirNodeList:
            fullPath = n.getFullPath()
            if fullPath == f.parent:
                node.parent = n
                n.addChild(node)
                edge = EdgeItem(EdgeItem.FILE_CONN, n, node, main)
                n.edgeList.append(edge)
                scene.addItem(edge)
        dirNodeList.append(node)
        scene.addItem(node)
    return dirNodeList
        
def constructDirGraphHier(root):
    dirHier = [[root]]
    tovisit = dirHier[0]
    while tovisit:
        nextlevel = []
        for v in tovisit:
            children = list(v.children)
            children.sort(key=lambda s: s.name.count('/'), reverse=True)
            nextlevel.extend(children)
        tovisit = nextlevel
        if tovisit:
            dirHier.append(tovisit)
    return dirHier
    
def getDirHierarchy(rootpath, main):
    scene = main.scene
    dirNodeList = constructDirecTree(rootpath, main, None)
    scene.dirNodeList = dirNodeList
    dirSet = set()
    for d in main.obj_cred_mat.keys():
        parents = d.split('/')
        parents = [p for p in parents if p != '']  # filter replaced with list comprehension
        for j in range(len(parents)+1):
            tempDir = '/'+'/'.join(parents[:j])
            dirSet.add(tempDir)
    dirList = list(dirSet)
    dirList.sort()
    #spec
    dirSpecHier, dirNodeSpecList = constructSpecDirecTree(dirList, main)
    scene.dirNodeList.extend(dirNodeSpecList)
    #
    dirHier = constructDirGraphHier(dirNodeList[0])
    #spec
    scene.dirHier = combineHierarchy(dirHier, dirSpecHier, 1, main)
    #2
    main.dirHier = dirHier
    main.dirSpecHier = dirSpecHier
#     scene.dirHier = dirHier
#     printListofList(dirHier)
#     print('scene.dirHier')
#     printListofList(scene.dirHier)
    scene.update()
    
def combineHierarchy(hier1, hier2, level, main):
    hier = hier1
    if level == len(hier1):
        hier1.append([])
    for i in range(level, len(hier1)):
        for d in hier2[i]:
            if i == 1:
                d.parent = hier1[0][0]
                d.dirpath = d.parent.getFullPath()
                hier1[0][0].children.add(d)
            if d not in hier[i]:
                d.dirpath = d.parent.getFullPath()
                hier[i].append(d)
                if d not in main.scene.items():
                    main.scene.addItem(d)
                edge = EdgeItem(EdgeItem.FILE_CONN, d.parent, d, main)
                d.edgeList.append(edge)
                main.scene.addItem(edge)
    return hier
    
def combineHierarchyByClickedNode(hier1, hier2, fnode, main):
    if not fnode.specChildren:
        return
    level = 0
    for i in range(len(hier2)):
        if fnode in hier2[i]:
            level = i+1
    hier = hier1
    if level == len(hier1):
        hier1.append([])
    for d in fnode.children:
        if d not in hier[level]:
            hier[level].append(d)
            d.dirpath = d.parent.getFullPath()
            if d not in main.scene.items():
                main.scene.addItem(d)
            edge = EdgeItem(EdgeItem.FILE_CONN, d.parent, d, main)
            d.edgeList.append(edge)
            main.scene.addItem(edge)
    return hier

def getDirHierFromObj(fnode, main):
    scene = main.scene
    dirNodeList = constructDirecTree(fnode.fullpath, main, fnode)
    for d in dirNodeList:
        scene.dirNodeList.append(d)
    dirHier = constructDirGraphHier(dirNodeList[0])
    for level in range(len(scene.dirHier)):
        if len(dirHier)>1:
            if fnode in scene.dirHier[level]:
                if level+1<len(scene.dirHier):
                    for d in dirHier[1]:
                        scene.dirHier[level+1].append(d)
                else:
                    scene.dirHier.append(dirHier[1])
#     genRadialLayout(scene, 0, 0, 0)
    scene.update()
    
# def retractDirHierFromObj(fnode, main):
#     if fnode.specNode:
#         if not fnode.specChildren:
#             return
#         fnode.specNodeExpand = False
#     scene = main.scene
#     nodeToRemove = []
#     nodeToVisit = [fnode]
#     while nodeToVisit:
#         n = nodeToVisit[0]
#         for c in n.children:
#             if c not in nodeToVisit:
#                 nodeToVisit.append(c)
#                 nodeToRemove.append(c)
#                 if c in scene.dirNodeList:
#                     scene.dirNodeList.remove(c)
#                 scene.removeItem(c)
#                 for e in c.edgeList:
#                     scene.removeItem(e)
#                     del e
#         nodeToVisit.remove(n)
#     count = len(nodeToRemove)
#     for level in range(len(scene.dirHier)):
#         for c in nodeToRemove:
#             if c in scene.dirHier[level]:
#                 scene.dirHier[level].remove(c)
#                 count -= 1
#                 if count == 0:
#                     break
#         if count == 0:
#             break
#     forRemoval = []
#     for i in scene.dirHier:
#         if i == []:
#             forRemoval.append(i)
#     for i in forRemoval:
#         scene.dirHier.remove(i)     
#         del i
#     if not fnode.specNode:
#         for e in fnode.edgeList:
#             scene.removeItem(e)
#             del e
#         fnode.edgeList = []
#     fnode.children = set()
#     genRadialLayout(scene, 0, 0, 0)
#     scene.update()
