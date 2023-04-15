import filelist, option, message

def server() :
    message.log('[SERVER] Ready to receive file list', 2)
    src_files = get_src_files()
    message.log(f'[SERVER] Source file list : {src_files}', 1)

    dest_files = filelist.rec_list_files(option.dest)
    message.log(f'[SERVER] Destination file list :{dest_files}', 1)


def get_src_files() :
    filelist = message.receive(0)
    return filelist

