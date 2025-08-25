#Question types:
#1. Show the output of a command running against an input object ('ls -l', 'ls -n', 'id username', 'groups username')
#2. Show the permissions a user has to an object
#3. Whether a certain user can read/write/execute an input object
#4. Whether any user from a certain group can read/write/execute a certain object
#5. The real and effective uids when a user execute a program with suid bit on
#6. The real and effective gids when a user execute a program with sgid bit on
#Questions are divided by dashed lines and the following information should be filled out
#Question type: The number for each type listed above
#Question text
#Choice 1 text
#Choice 2 text
#Choice 3 text
#Choice 4 text
#If the question needs to load in a .unix file, specify the directory of the file. If it is the same with the previous question, put 'Same'. If no file needs to be loaded, put 'None' here.
----------------------------------------------------
0
----------------------------------------------------
3
Can Mary read file /document/log.
True
False
None
None
./policies/quiz/simple.unix
----------------------------------------------------
3
Can Lucy read file /document/log.
True
False
None
None
Same
----------------------------------------------------
3
Jim can read file /test/test1.c.
True
False
None
None
Same
----------------------------------------------------
4
When /projects/program1 is executed by Jim, which group will it ran as
#Mary can not read file /projects/program1.c.
manager
developer
tester
None
Same
----------------------------------------------------
1
Which of the operations is Nick allowed to apply to directory /Sales/Home?
List files and directories in it
Add/Remove a file within this directory
Traverse the directory
None
./policies/quiz/company.unix
----------------------------------------------------
2
Evan can create a file under directory /Technique/projectA.
True
False
None
None
Same
----------------------------------------------------
2
Tom can list the content of directory /Technique/projectA/doc/people.
True
False
None
None
Same
----------------------------------------------------
2
Tom can remove files under directory /Technique/projectA.
True
False
None
None
Same
----------------------------------------------------