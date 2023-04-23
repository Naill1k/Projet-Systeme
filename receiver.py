import os, message, generator, filelist

def receiver(STATE) :
    # Calculates the list of files in the destination
    if STATE['-r'] :
        dest_files = filelist.rec_list_files(STATE['dest'])
    elif STATE['-d'] :
        dest_files = filelist.dir_list_files(STATE['dest'])
    else :
        dest_files = filelist.list_files(STATE['dest'])  
    message.log(f'[RECEIVER] Destination file list : {dest_files}', STATE['-v'], 1)


    # Asks the client for the list of files in the source
    message.log('[RECEIVER] Ready to receive file list', STATE['-v'], 2)
    (tag, src_files) = message.receive()  
    message.log(f'[RECEIVER] Source file list : {src_files}', STATE['-v'], 1)


    # Determines the files missing from the destination
    message.log(f'[RECEIVER] CWD : {os.getcwd()}', STATE['-v'], 2)
    requiered_files = generator.comparator(STATE['src'], src_files, STATE['dest'], dest_files, STATE)
    message.log(f'[RECEIVER] Files to copy : {requiered_files}', STATE['-v'], 2)

    os.chdir(STATE['dest'])
    message.log('[RECEIVER] Asking required files', STATE['-v'], 1)
    for file in requiered_files :
        if (STATE['--existing']) and (not file in dest_files) :
                continue
        
        if file[-1] == '/' :  # If it's a directory, we just create it and go to the next file
            message.log(f"[RECEIVER] Creating directory '{file}'", STATE['-v'], 2)
            os.mkdir(file)
        
        else :
            if (STATE['--ignore_existing']) and (file in dest_files) :
                continue

            message.log(f"[RECEIVER] Asking for '{file}'", STATE['-v'], 2)
            message.send('Query', file)   # Asks the client for the specified file
            (tag, data) = message.receive() # Data contains the content of the file requested
            message.log(f'[RECEIVER] Received content', STATE['-v'], 2)

            fd = os.open(file, os.O_WRONLY | os.O_CREAT)
            binaries = data.encode()

            n = os.write(fd, binaries)
            if n != len(binaries) :
                message.log(f"[RECEIVER] An error occurred while writing in the file '{file}' : {n} bytes written out of {len(binaries)}", STATE['-v'], 0)
            else :
                message.log(f'[RECEIVER] File copied succesfully', STATE['-v'], 2)


    message.log('[RECEIVER] Received all required files', STATE['-v'], 1)
    message.send('End', None)