import os, filelist, option, message, generator

def server() :

    # Asks the client for the list of files in the source
    message.log('[SERVER] Ready to receive file list', 2)
    (tag, src_files) = message.receive(0)  
    message.log(f'[SERVER] Source file list : {src_files}', 1)

    # Calculates the list of files in the destination
    dest_files = filelist.rec_list_files(option.dest)  
    message.log(f'[SERVER] Destination file list :{dest_files}', 1)

    # Determines the files missing from the destination
    list_src = filelist.simplifier(option.src,src_files)
    list_dest = filelist.simplifier(option.dest,dest_files)
    missing_files = generator.comparator(option.src, list_src, option.dest, list_dest)
    message.log(f'[SERVER] Files to copy : {missing_files}', 2)

    os.chdir(option.dest)
    message.log('[SERVER] Asking required files', 1)
    for file in missing_files :
        if file[-1] == '/' :  # If it's a directory, we just create it and go to the next file
            message.log(f"[SERVER] Creating directory '{file}'", 2)
            os.mkdir(file)
        
        else :
            message.log(f"[SERVER] Asking for '{file}'", 2)
            message.send(1, 'Query', file)   # Asks the client for the specified file
            (tag, data) = message.receive(0) # Data contains the content of the file requested
            message.log(f'[SERVER] Received content', 2)

            fd = os.open(file, os.O_WRONLY | os.O_CREAT)
            binaries = data.encode()

            n = os.write(fd, binaries)
            if n != len(binaries) :
                message.log(f"[SERVER] An error occurred while writing in the file '{file}' : {n} bytes written out of {len(binaries)}")
            else :
                message.log(f'[SERVER] File copied succesfully', 2)


    message.log('[SERVER] Received all required files', 1)
    message.send(1, 'End', None)
