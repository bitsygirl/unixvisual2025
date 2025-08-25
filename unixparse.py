'''
Created on Aug 10, 2015

@author: carr
'''
from pyparsing import *
from utils import *

# tokens
UNIXLIT = Literal('UNIX')
ACLLIT = Literal('ACL')

DIR = Literal('d')
READ = Literal('r')
WRITE = Literal('w')
EXECUTE = Literal('x')
SETID = Literal('s') | Literal('S')
NOPERM = '-'

COMMA = Literal(',').suppress()
COLON = Literal(':').suppress()

ID = Regex(idregex)

USER = ID
GROUP = ID
PATH = Regex(pathregex)

COMMENT = Optional(pythonStyleComment).suppress()

ROOT = Literal('root:') - PATH

# USERLIST = USER + ZeroOrMore(Literal(',').suppress() + USER)
USERLIST = delimitedList(USER, delim=',')
GROUPLIST = delimitedList(GROUP, delim=',')

USERSTMT = Literal('user:') - USERLIST + COMMENT
USERS = ZeroOrMore(USERSTMT) 

GROUPSTMT = Literal('group:') - GROUP - USERLIST + COMMENT
GROUPS = ZeroOrMore(GROUPSTMT) 

UNIXPERMBITS = Optional(DIR) + And([(READ | NOPERM) + (WRITE | NOPERM) + (EXECUTE | SETID | NOPERM)]*3)
ACCESSCREDENTIAL = USER + COLON + GROUP
RES = Optional(Literal('-r')) + PATH
UNIXOBJSTMT = Literal('object:') + UNIXPERMBITS + ACCESSCREDENTIAL + RES
UNIXOBJS = ZeroOrMore(UNIXOBJSTMT) + COMMENT
UNIX = UNIXLIT + ROOT + USERS + GROUPS + UNIXOBJS

ACLPERMBITS = Optional(Literal('d')) + (READ | NOPERM) + (WRITE | NOPERM) + (EXECUTE | NOPERM)
ACCESSLISTCREDENTIAL = USERLIST + COLON + GROUPLIST
ACLOBJSTMT = Literal('object:') + ACLPERMBITS + ACCESSLISTCREDENTIAL + RES
ACLOBJS = ZeroOrMore(ACLOBJSTMT) + COMMENT
ACL = ACLLIT + ROOT + USERS + GROUPS + ACLOBJS

ROOT.setParseAction(nest)
USERLIST.setParseAction(nest)
GROUPLIST.setParseAction(nest)
USERSTMT.setParseAction(nest)
GROUPSTMT.setParseAction(nest)
UNIXPERMBITS.setParseAction(nest)
ACLPERMBITS.setParseAction(nest)
UNIXOBJSTMT.setParseAction(nest)
ACLOBJSTMT.setParseAction(nest)

SPEC = ACL | UNIX

def unixparse(text):
    return SPEC.parseString(text, parseAll=True)

def printthing(x, depth=1):
    if isinstance(x, list):
        if len(x) > 1:
            for e in x:
                printthing(e, depth+1)
        else:
            print '{0}{1}'.format(' ' * 4 * depth, x)
    else:
        print '{0}{1}'.format(' ' * 4 * depth, x)

if __name__ == '__main__':
    import sys
    with open(sys.argv[1], 'r') as f:
        text = f.read()
    print text
    result = unixparse(text)
    for i, stmt in enumerate(result):
        print i, stmt[0]
        rest = stmt[1:]
        for thing in rest:
            printthing(thing)
    print result
