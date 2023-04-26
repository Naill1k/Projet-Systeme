#!/usr/bin/env python3
import os, option, filelist, message

import server
import client


STATE = option.state  # Dictionnary containing all the requiered information (flags, files, ...)

if STATE['--server'] :
    message.log(f'Starting server because of --server option, CWD : {os.getcwd()}', STATE['-v'], 2)
    server.server()
    exit()


if STATE['--list_only'] :
    print('List of files :')
    for path in STATE['src'] :
        print()
        if STATE['-r'] :
            os.system('ls --recursive -l ' + path)

        else :
            os.system('ls -l ' + path)

    exit(0)
    



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
        path_mrsync = 'Syst2/Projet-Systeme/mrsync.py'  # The path for the mrsync.py file on the remote host
        os.execvp('ssh', ['ssh', '-e', 'none', STATE['host'], '--', path_mrsync, '--server', STATE['dest']])


    if STATE['connection'] != 'daemon' :
        server.server()

