'''
Created on Aug 17, 2015

@author: manwang
'''
from syscalloutputparse import *

def syscalloutput(text):
    results = syscalloutputparse(text)
    output = []
    prevcall = None
    for stmt in results:
        if stmt[0] == 'Initial pid:':
            output = [stmt[1]]
        elif stmt[0] == 'Initial euid:':
            output.append (stmt[1])
        elif stmt[0] == 'Initial egid:':
            output.append (stmt[1])
        else:
            for onecall in stmt:
                prevcall = onecall
                stmttype = onecall[0]
                if stmttype == 'Call:':
                    temp = [onecall[1]]
                    param = []
                elif stmttype == 'ID:':
                    ids = list(onecall[1])
                    temp.append(ids)
                elif stmttype == 'Parameter:':
                    param.extend(onecall[1])
                elif stmttype == 'Error:':
                    error = onecall[1]
                elif stmttype == 'Status:':
                    temp.append(param)
                    temp.append(onecall[1])
            if len(temp) == 2:
                temp.append(param)
            temp.append(error)
            output.append(temp)
    return output
    
if __name__ == '__main__':
    text = "Initial pid: 8355\nInitial euid: 100\nInitial egid: 200\nCall:open\nID: 10,20,30,40\nParameter: myfile\nParameter: 1001, 384\nError: No error\nStatus:4\n"
    text+="Call:read\nID: 1,2,3,4\nParameter: myfile\nParameter: 1001, 384\nError: Operation not permitted\nStatus:4\n"
    result = syscalloutput(text)
    print result