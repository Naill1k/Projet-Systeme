import os, message, filelist, signal, time

MAX_BYTES = 1024

def sender(STATE) :
    signal.signal(signal.SIGALRM, timeout)
    signal.alarm(STATE['--timeout'])

    for path in STATE['src'] :
        if STATE['-r'] :
            src_files = filelist.rec_list_files(path)
        elif STATE['-d'] :
            src_files = filelist.dir_list_files(path)
        else :
            src_files = filelist.list_files(path, STATE['-v'])

        message.log(f'[SENDER] Sending : {src_files}', STATE['-v'], 2)
        message.send(src_files)
        message.log('[SENDER] Sent source file list', STATE['-v'], 2)


        os.chdir('/'.join(path.split('/')[:-1]))
        message.log(f'[SENDER] CWD : {os.getcwd()}', STATE['-v'], 2)

        answer(STATE)


    message.log('[SENDER] All requested files are sent', STATE['-v'], 2)




def answer(STATE) :
    while True :
        file = message.receive()
        signal.alarm(STATE['--timeout'])  # reset the alarm

        if file is None :  # The receiver sends None when all requiered files are received
            break

        message.log(f"[SENDER] Opening file '{file}'", STATE['-v'], 1)

        fd = os.open(file, os.O_RDONLY)

        data = b''
        buff = b'empty'
        while len(buff) != 0 :
            buff = os.read(fd, MAX_BYTES)
            data += buff

        message.log(f'[SENDER] Sending file content', STATE['-v'], 2)
        message.send(data.decode())
        message.log(f'[SENDER] File content sent', STATE['-v'], 2)




def timeout(sig, _) :
    '''
    Handles the timeout option
    '''
    message.log('Communication timeout', 0, 0)
    exit(30)