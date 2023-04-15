import os,sys


def list_files(path):
    if os.path.isdir(path) and path[-1] != '/':
        return "skipping"
    res=[]
    for file in os.listdir(path):
        if not os.path.isdir(path+file):
            res.append(path+file)
    return res


def dir_list_files(path):
    res=[]
    if path=='*':
        for file in os.listdir():
            res.append(file)
        return res
    if path[-1]=='*':
        for file in os.listdir(path[:-1]):
            res.append(file)
        return res
    if os.path.isdir(path) and path[-1] != '/':
        return [path]
    for file in os.listdir(path):
        res.append(path+file)
    return res



'''
Make a list (recursive) of all files and repertories of a given path,starting at the current path.
If the path (i.e. the argument) finishes with a '/', then not include the path in the list,
else include it. 
'''

def rec_list_files(path):
    result = []
    if os.path.isdir(path):
        if path[-1] != '/':
            result.append(path)
            path += '/'
        for file in os.listdir(path):
            if os.path.isdir(path+file):
                result += rec_list_files(path+file)
            else:
                result.append(path+file)
    else:
        result.append(path)
    return result

def rec_list_files2(path):
    if os.path.isdir(path):
        res = []
        for file in os.listdir(path):
            if os.path.isdir(path+"/"+file+"/"):
                res.append(rec_list_files2(path+"/"+file))
            else:
                res.append(file)
        if path[-1] != '/':
            return [os.path.basename(path), res]
        return res
    else:
        return [path]
    

def simplifier(path,list):
    L=[]
    if path[-1] != '/':
        n=len(path.split(os.sep))-1
        for l in list:
            L.append('/'.join(l.split(os.sep)[n:]))
    else:
        n=len(path.split(os.sep))-1
        for l in list:
            L.append('/'.join(l.split(os.sep)[n:]))
    return L