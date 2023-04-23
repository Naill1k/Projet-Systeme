import os, message, filelist

MAX_BYTES = 1024

def sender(STATE) :
    if STATE['-r'] :
        src_files = filelist.rec_list_files(STATE['src'])
    elif STATE['-d'] :
        src_files = filelist.dir_list_files(STATE['src'])
    else :
        src_files = filelist.list_files(STATE['src'])

    message.log(f'[SENDER] Sending : {src_files}', STATE['-v'], 2)
    message.send('Files', src_files)
    message.log('[SENDER] Sent source file list', STATE['-v'], 2)

    os.chdir(STATE['src'])
    while True :
        (tag, file) = message.receive()
        if not file :
            message.log('[SENDER] All requested files are sent', STATE['-v'], 2)
            break

        message.log(f"[SENDER] Opening file '{file}'", STATE['-v'], 1)

        fd = os.open(file, os.O_RDONLY)

        data = b''
        buff = b'empty'
        while len(buff) != 0 :
            buff = os.read(fd, MAX_BYTES)
            data += buff

        message.log(f'[SENDER] Sending file content', STATE['-v'], 2)
        message.send('Content', data.decode())
        message.log(f'[SENDER] File content sent', STATE['-v'], 2)