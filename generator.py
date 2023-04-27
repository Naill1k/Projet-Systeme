import os


def comparator(src, dest, STATE) :

    '''
    compare two lists with different path
    and make a list of missing or old files of source path
    '''

    dest_files = [file[0] for file in dest]
    requiered_files = []

    for (file, mod_time) in src :
        if (not STATE['-I']) and (file in dest_files) :
            
            if (not STATE['-u']) :
                index_dest = dest_files.index(file)

                if mod_time > dest[index_dest][1] :
                    requiered_files.append(file)

        else :
            requiered_files.append(file)

    return requiered_files