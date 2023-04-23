#!/usr/bin/env python3
import os, option, filelist, message

import server
import client

fd_log = os.open('log', os.O_WRONLY | os.O_CREAT)
if fd_log != 3 :
    exit(4)

STATE = option.state  # Dictionnary containing all the requiered information (flags, files, ...)

if STATE['--server'] :
    message.log(f'Starting server because of --server option, CWD : {os.getcwd()}', STATE['-v'], 2)
    server.server()
    exit()


if STATE['--list_only'] :
    if STATE['-r'] :
        src_files = filelist.rec_list_files(STATE['src'])
    elif STATE['-d'] :
        src_files = filelist.dir_list_files(STATE['src'])
    else :
        src_files = filelist.list_files(STATE['src'])

    message.log(f'The source files are : {src_files}', STATE['-v'], 1)



fdr1, fdw1 = os.pipe()  # Pipe client -> server
fdr2, fdw2 = os.pipe()  # Pipe server -> client



if os.fork() :  # Main process
    os.dup2(fdr2, 0)
    os.close(fdr2)

    os.dup2(fdw1, 1)
    os.close(fdw1)  

    os.close(fdr1)
    os.close(fdw2)

    client.client(STATE)
    

else :  # Subprocess
    os.dup2(fdr1, 0)
    os.close(fdr1)

    os.dup2(fdw2, 1)
    os.close(fdw2)

    os.close(fdr2)
    os.close(fdw1)

    if STATE['connection'] == 'ssh' :
        message.log('Opening ssh connection', STATE['-v'], 1)
        os.execvp('ssh', ['ssh', '-e', 'none', STATE['host'], '--', 'Syst2/Projet-Systeme/mrsync.py', '--server', STATE['src'], STATE['dest']])


    if STATE['connection'] != 'daemon' :
        server.server()

os.close(fd_log)