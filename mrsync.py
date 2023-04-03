import os,sys,subprocess

if sys.argv[-1]=="/":
    result = subprocess.run(["ls","-l",sys.argv[1]])
else:
    result = subprocess.call(["ls","-l",sys.argv[1]])
    #result=result+subprocess.run(["ls","-d","-l",sys.argv[1]])
print("test")