import os,filelist

list_s=filelist.simplifier("reptest/SRC/",filelist.rec_list_files("reptest/SRC/"))
list_d=filelist.simplifier("reptest/DEST/",filelist.rec_list_files("reptest/DEST/"))

def comparator(path_s,src,path_d,dest):
    if (path_s[-1] != '/') and (path_s.split(os.sep)[-1] not in dest):
        return src
    C=[]
    for file in src:
        if file in dest and os.stat(path_s+file).st_mtime>os.stat(path_d+file).st_mtime:
                C.append(file)
        elif file not in dest:
             C.append(file)
    return C


def comparator2(path_s,src,path_d,dest):
    if (path_s[-1] != '/') and (path_s.split(os.sep)[-1] not in dest):
        return src
    C=[]
    inter=list(set(src) & set(dest))
    diff = list(set(src)-set(dest))
    for d in diff:
        C.append(d)
    for i in inter:
        if os.stat(path_s+i).st_mtime>os.stat(path_d+i).st_mtime:
             C.append(i)
    return C


print(list_s)
print(list_d)    
print()
print(comparator("reptest/SRC/",list_s,"reptest/DEST/",list_d))
print(comparator2("reptest/SRC/",list_s,"reptest/DEST/",list_d))
    