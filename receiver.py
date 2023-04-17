import os, message

def receiver(requiered_files) :
    message.log('[SERVER] Asking required files', 1)
    for file in requiered_files :
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