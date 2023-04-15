import os, filelist, option, message

MAX_BYTES = 1024

def client(fdr, fdw) :
    src_files = filelist.rec_list_files(option.src)
    message.log(f'[CLIENT] Sending : {src_files}', 2)
    message.send(fdw, None, src_files)
    message.log('[CLIENT] Sent source file list', 2)

    os.chdir(option.src)
    while True :
        (tag, file) = message.receive(fdr)
        if not file :
            message.log('[CLIENT] All requested files are sent', 2)
            break

        message.log(f"[CLIENT] Opening file : '{file}'")

        fd = os.open(file, os.O_RDONLY)

        data = b''
        buff = b'empty'
        while len(buff) != 0 :
            buff = os.read(fd, MAX_BYTES)
            data += buff

        message.log(f'[CLIENT] Sending file content', 2)
        message.send(fdw, 'Content', data.decode())
