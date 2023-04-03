import os,sys,subprocess

if sys.argv[1]=="/":
    result = subprocess.run(["ls","-l",sys.argv[1]])
else:
    result = subprocess.run(["ls",sys.argv[1]],capture_output=True)
    #result=result+subprocess.run(["ls","-d","-l",sys.argv[1]])

print(result.stdout)
print("test")