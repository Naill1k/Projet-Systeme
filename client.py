import os, filelist, option, message, sender

MAX_BYTES = 1024

def client(fdr, fdw) :
    if option.args.recursive :
        src_files = filelist.rec_list_files(option.src)
    elif option.args.dirs :
        src_files = filelist.dir_list_files(option.src)
    else :
        src_files = filelist.list_files(option.src)

    message.log(f'[CLIENT] Sending : {src_files}', 2)
    message.send(fdw, None, src_files)
    message.log('[CLIENT] Sent source file list', 2)

    os.chdir(option.src)
    sender.sender(fdr, fdw)