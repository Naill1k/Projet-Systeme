#!/usr/bin/env python3
import os, option, filelist, message

import server
import client

if option.args.list_only :
    if option.args.recursive :
        src_files = filelist.rec_list_files(option.src)
    elif option.args.dirs :
        src_files = filelist.dir_list_files(option.src)
    else :
        src_files = filelist.list_files(option.src)

    message.log('The source files are :', 1)
    message.log(src_files)

fdr1, fdw1 = os.pipe()  # Pipe client -> server
fdr2, fdw2 = os.pipe()  # Pipe server -> client

if os.fork() :
    os.dup2(fdr1, 0)
    os.dup2(fdw2, 1)

    os.close(fdr2)
    os.close(fdw1)
    
    server.server()

    os.close(fdr1)
    os.close(fdw2)

else :
    os.close(fdr1)
    os.close(fdw2)

    client.client(fdr2, fdw1)
    
    os.close(fdr2)
    os.close(fdw1)
    