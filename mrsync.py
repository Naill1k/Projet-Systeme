#!/usr/bin/env python3
import os, sys, pickle

import option

import sender



def server() :
    import filelist
    os.dup2(fdr, 0)
    os.dup2(fdw, 1)
    MAX_BYTES = 1024

    filelist = b''
    print('Server ready to receive file list', file=sys.stderr)
    
    buff = os.read(0, MAX_BYTES)
    while len(buff) == MAX_BYTES :
        filelist += buff
        buff = os.read(0, MAX_BYTES)

    filelist += buff
    filelist = pickle.loads(filelist)
    print('Server recieved file list :', filelist, file=sys.stderr)



def client() :
    import filelist
    print(filelist.liste)
    os.write(fdw, pickle.dumps(filelist.liste))
    print('Client sent file list')


fdr, fdw = os.pipe()

if os.fork() :
    server()
    os.close(fdr)
    os.close(fdw)

else :
    client()
    os.close(fdr)
    os.close(fdw)
