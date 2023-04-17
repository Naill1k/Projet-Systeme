import os,filelist

def comparator(path_s,src,path_d,dest) :
    C=[]
    if path_s[-1] != '/':
        path_s = '/'.join(path_s.split('/')[:-1]) + '/'

    for file in src:
        if (file in dest) and (os.stat(path_s+file).st_mtime > os.stat(path_d+file).st_mtime) :
            C.append(file)

        elif file not in dest:
            C.append(file)

    return C