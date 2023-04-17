import os, message

MAX_BYTES = 1024

def sender(fdr, fdw) :
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