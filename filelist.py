import os,sys, message


def list_files(path, v) :

    '''
    make a list of all files without repertories in the given path
    executed by default
    '''

    if not os.path.isdir(path) :  # It is a regular file
        return [(path.split('/')[-1], os.stat(path))]
    
    else :
        if path[-1] != '/':
            return []
    
    res=[]
    for file in os.listdir(path):
        if not os.path.isdir(path+file):
            res.append((file, os.stat(path+file)))
        else :
            message.log(f"Skipping directory '{path+file}'", v, 0)

    return res




def dir_list_files(path) :

    '''
    make a list of all files and repertories in the given path
    useful for the option -d
    '''

    res=[]

    if not os.path.isdir(path) :  # It is a regular file
        return [(path.split('/')[-1], os.stat(path))]
    
    else :
        if path[-1] != '/' :
            return [(path.split('/')[-1]+'/', os.stat(path))]
    
    for file in os.listdir(path):
        if os.path.isdir(path+file):
            res.append((file+'/', os.stat(path+file)))
        else:
            res.append((file, os.stat(path+file)))

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
            res.append((path2, os.stat(path))) 

        try:
            for file in os.listdir(path) :
                if os.path.isdir(path+file) :
                    for r in rec_list_files((path+file)) :
                        res.append((path2+r[0], os.stat(path+r[0])))

                else:
                    res.append((path2+file, os.stat(path+file)))
        except PermissionError:
            pass

    else:
        res.append((path.split('/')[-1], os.stat(path)))

    return res