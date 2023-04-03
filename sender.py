import os,sys,subprocess

if sys.argv[1][-1]=="/":
    result = subprocess.run(["ls",sys.argv[1]],capture_output=True)
    liste=result.stdout.decode().split()
else:
    result = subprocess.run(["ls",sys.argv[1]],capture_output=True)
    liste=[sys.argv[1]]
    liste.append(result.stdout.decode().split())

print(liste)
