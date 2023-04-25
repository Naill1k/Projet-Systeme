import os,sys, message


def list_files(path) :

    '''
    make a list of all files without repertories in the given path
    executed by default
    '''

    if os.path.isdir(path) and path[-1] != '/':
        return []
    
    res=[]
    for file in os.listdir(path):
        if not os.path.isdir(path+file):
            res.append((file,os.stat(path+file).st_mtime))

    return res




def dir_list_files(path) :

    '''
    make a list of all files and repertories in the given path
    useful for the option -d
    '''

    res=[]

    if os.path.isdir(path) and path[-1] != '/' :
        return [path]
    
    for file in os.listdir(path):
        if os.path.isdir(path+file):
            res.append((file+'/',os.stat(path+file).st_mtime))
        else:
            res.append((file,os.stat(path+file).st_mtime))

    return res



def rec_list_files(path) :

    '''
    make a list of all files and repertories in the given path
    recurse into directories
    useful for the option -r
    '''

    res = []

    if os.path.isdir(path) :
        path2 = ''
        if path[-1] != '/' :
            path2 = path.split('/')[-1] + '/'
            path += '/'
            res.append((path2,os.stat(path).st_mtime)) 

        try:
            for file in os.listdir(path) :
                if os.path.isdir(path+file) :
                    for r in rec_list_files((path+file)) :
                        res.append((path2+r[0],os.stat(path+r[0]).st_mtime))

                else:
                    res.append((path2+file,os.stat(path+file).st_mtime))
        except PermissionError:
            pass

    else:
        res.append((path.split('/')[-1],os.stat(path).st_mtime))

    return res