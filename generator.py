import os

def comparator(path_s,src,path_d,dest, STATE) :
    '''
    compare two lists with different path
    and make a list of missing or old files of source path
    '''
    C=[]
    if path_s[-1] != '/':
        path_s = '/'.join(path_s.split('/')[:-1]) + '/'

    for file in src:
        if (file in dest) :
            if (not STATE['-u']) and False :#(os.stat(path_s+file).st_mtime > os.stat(path_d+file).st_mtime) :
                C.append(file)

        elif file not in dest:
            C.append(file)

    return C