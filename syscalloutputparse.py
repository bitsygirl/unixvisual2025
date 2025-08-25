'''
Created on Aug 10, 2015

@author: manwang
Updated for Python 3 compatibility
'''
from pyparsing import *
from utils import *

# tokens
COMMA = Literal(',').suppress()
COLON = Literal(':').suppress()

ID = Regex(idregex)

INITIALPIDSTMT = Literal('Initial pid:') - ID
INITIALEUIDSTMT = Literal('Initial euid:') - ID
INITIALEGIDSTMT = Literal('Initial egid:') - ID

PATH = Regex(pathregex)
PARAM = ID | PATH
PARAMLIST = delimitedList(PARAM, delim=',')
PARAMSTMT = Literal('Parameter:') - PARAMLIST
PARAMS = ZeroOrMore(PARAMSTMT) 

IDLIST = delimitedList(PARAM, delim=',')
IDINFOSTMT = Literal('ID:') - IDLIST

ERROR = Regex(r'.*')
ERRORLIST = delimitedList(ERROR, delim='\s')
ERRORSTMT = Literal('Error:') - ERROR

CALLSTMT = Literal('Call:') - ID
STATUSSTMT = Literal('Status:') - ID

ONESYSCALLSTMT = CALLSTMT - IDINFOSTMT - PARAMS - Optional(ERRORSTMT) - Optional(STATUSSTMT)

INITIALPIDSTMT.setParseAction(nest)
INITIALEUIDSTMT.setParseAction(nest)
INITIALEGIDSTMT.setParseAction(nest)
CALLSTMT.setParseAction(nest)
IDLIST.setParseAction(nest)
IDINFOSTMT.setParseAction(nest)
PARAMLIST.setParseAction(nest)
PARAMSTMT.setParseAction(nest)
ERRORSTMT.setParseAction(nest)
STATUSSTMT.setParseAction(nest)
ONESYSCALLSTMT.setParseAction(nest)
SPEC = Optional(INITIALPIDSTMT) + Optional(INITIALEUIDSTMT) + Optional(INITIALEGIDSTMT)+ ZeroOrMore(ONESYSCALLSTMT)

def syscalloutputparse(text):
    return SPEC.parseString(text, parseAll=True)

if __name__ == '__main__':
    text = "Initial pid: 8355\nInitial euid: 100\nInitial egid: 200\nCall:open\nID: 100\nParameter: myfile\nParameter: 1001, 384\nStatus:4\n"
    text+="Call:read\nID: 200\nParameter: myfile\nError: omg haha\nStatus:4\n"
    result = syscalloutputparse(text)
    print(result)
