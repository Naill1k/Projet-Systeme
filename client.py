import filelist, option, message

MAX_BYTES = 1024

def client(fdr, fdw) :
    src_files = filelist.rec_list_files(option.src)
    message.log(f'[CLIENT] Sending : {src_files}', 2)
    message.send(fdw, None, src_files)
    message.log('[CLIENT] Sent source file list', 2)