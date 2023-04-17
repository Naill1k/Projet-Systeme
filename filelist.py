import os,sys



def list_files(path) :
    '''
    make a list of all files without repertories in the given path
    executed by default
    '''
    if os.path.isdir(path) and path[-1] != '/':
        return "skipping "+path.split('/')[-1]
    
    res=[]
    for file in os.listdir(path):
        if not os.path.isdir(path+file):
            res.append(file)

    return res



def dir_list_files(path) :
    '''
    make a list of all files and repertories in the given path
    useful for the option -d
    '''
    res=[]
    if os.path.isdir(path) and path[-1] != '/':
        return [path]
    
    for file in os.listdir(path):
        if os.path.isdir(path+file):
            res.append(file+'/')
        else:
            res.append(file)

    return res



def rec_list_files(path) :
    '''
    make a list of all files and repertories in the given path
    recurse into directories
    usefull for the option -r
    '''
    res = []
    if os.path.isdir(path) :
        path2 = ''
        if path[-1] != '/':
            path2 = path.split('/')[-1] + '/'
            path += '/'
            res.append(path2) 

        for file in os.listdir(path):
            if os.path.isdir(path+file):
                for r in rec_list_files(path+file) :
                    res.append(path2+r)

            else:
                res.append(path2+file)
    else:
        res.append(path.split('/')[-1])

    return res