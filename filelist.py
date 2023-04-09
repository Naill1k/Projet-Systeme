import os,sys

def list_files(path):
    result = []
    if os.path.isdir(path):
        if path[-1] != '/':
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

print(list_files("reptest"))