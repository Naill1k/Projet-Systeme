import os, filelist, option, message, generator, receiver

def server() :
    # Asks the client for the list of files in the source
    message.log('[SERVER] Ready to receive file list', 2)
    (tag, src_files) = message.receive(0)  
    message.log(f'[SERVER] Source file list : {src_files}', 1)

    # Calculates the list of files in the destination
    dest_files = filelist.rec_list_files(option.dest)  
    message.log(f'[SERVER] Destination file list :{dest_files}', 1)

    # Determines the files missing from the destination
    requiered_files = generator.comparator(option.src, src_files, option.dest, dest_files)
    message.log(f'[SERVER] Files to copy : {requiered_files}', 2)

    os.chdir(option.dest)
    receiver.receiver(requiered_files)
