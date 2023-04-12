import os,sys


def list_files(path):
    print(subprocess(["ls","-l",path]))


list_files("reptest/SRC")

def dir_list_files(path):
    return None




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
            full_path = path + file
            if os.path.isdir(full_path):
                result += list_files(full_path)
            else:
                result.append(full_path)
    else:
        result.append(path)
    return result


def rec_list_files2(path):
    result = []
    if os.path.isdir(path):
        for file in os.listdir(path):
            if os.path.isdir(path+"/"+file+"/"):
                result.append(list_files2(path+"/"+file))
            else:
                result.append(file)
        if path[-1] != '/':
            return [os.path.basename(path), result]
        return result
    else:
        return [path]