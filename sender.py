import filelist,os

def statistics(list):
    S=[]
    for l in list:
        stat=os.stat(l)
        name=l.split(os.sep)[-1]
        size=stat.st_size
        time=stat.st_mtime
        S.append((name,size,time))
    return S


print(statistics(filelist.rec_list_files("reptest/SRC")))