import os, message, filelist, generator, signal, sys

def receiver(STATE) :
    signal.signal(signal.SIGALRM, timeout)
    signal.alarm(STATE['--timeout'])

    # Calculates the list of files in the destination
    if STATE['-r'] :
        dest_files = filelist.rec_list_files(STATE['dest'])
    elif STATE['-d'] :
        dest_files = filelist.dir_list_files(STATE['dest'])
    else :
        dest_files = filelist.list_files(STATE['dest'], STATE['-v'])  
    message.log(f'[RECEIVER] Destination file list : {[file[0] for file in dest_files]}', STATE['-v'], 1)


    try : os.chdir(STATE['dest'])
    except OSError :
        message.log(f"[RECEIVER] Error : couldn't change directory", STATE['-v'], 0)
        sys.exit(23)
    message.log(f'[RECEIVER] CWD : {os.getcwd()}', STATE['-v'], 2)
    
    iter_src(dest_files, STATE)
    



def iter_src(dest_files, STATE) :
    for path in STATE['src'] :
        # Asks the client for the list of files in the source
        message.log('[RECEIVER] Ready to receive file list', STATE['-v'], 2)
        src_files = message.receive()  
        message.log(f'[RECEIVER] Source file list : {[file[0] for file in src_files]}', STATE['-v'], 1)

        if (STATE['--delete']) and (len(STATE['src']) == 1) and (os.path.isdir(STATE['src'][0])):
            for (file, stat) in dest_files :
                if not file in [f[0] for f in src_files] :
                    message.log(f"[RECEIVER] Deleting '{file}' : not present in the source", STATE['-v'], 1)
                    try : os.remove(file)
                    except OSError : message.log(f"[RECEIVER] Error : couldn't delete '{file}'", STATE['-v'], 0)
        
        # Determines the files missing from the destination
        requiered_files = generator.comparator(src_files, dest_files, STATE)
        message.log(f'[RECEIVER] Files to copy : {requiered_files}', STATE['-v'], 2)

        message.log('[RECEIVER] Asking required files', STATE['-v'], 1)
        ask_files(requiered_files, dest_files, STATE)

        message.send(None)  # End
    message.log('[RECEIVER] Received all required files', STATE['-v'], 1)




def ask_files(requiered_files, dest_files, STATE) :
    for file in requiered_files :

        if file[-1] == '/' :  # If it's a directory, we just create it and go to the next file
            message.log(f"[RECEIVER] Creating directory '{file}'", STATE['-v'], 2)
            try :
                os.mkdir(file)
            except FileExistsError :
                message.log(f"Error : couldn't create directory, file already exists with the same name '{file}'", STATE['-v'], 0)
                sys.exit(23)

        else :
            message.log(f"[RECEIVER] Asking for '{file}'", STATE['-v'], 2)
            message.send(file)   # Asks the client for the specified file
            data = message.receive() # Data contains the content of the file requested
            message.log(f'[RECEIVER] Received content', STATE['-v'], 2)
            signal.alarm(STATE['--timeout'])  # reset the alarm

            try :
                fd = os.open(file, os.O_WRONLY | os.O_CREAT)
                os.truncate(fd, 0)  # Empties the content of the file (in case it already existed)
                
            except IsADirectoryError :
                message.log(f"A directory already exists with the same name '{file}'", STATE['-v'], 0)
                if STATE['--force'] :
                    os.system(f'rm -r {file}')
                    fd = os.open(file, os.O_WRONLY | os.O_CREAT)
                else :
                    sys.exit(23)


            binaries = data.encode()
            total_bytes_written = 0
            try :
                while total_bytes_written < len(binaries):
                    bytes_written = os.write(fd, binaries[total_bytes_written:])
                    if bytes_written == 0:
                        raise
                    total_bytes_written += bytes_written

            except :
                message.log(f"[RECEIVER] Error during the copy of the file '{file}'", STATE['-v'], 0)
                sys.exit(23)


def timeout(sig, _) :
    '''
    Handles the timeout option
    '''
    message.log('Communication timeout', 0, 0)
    exit(30)