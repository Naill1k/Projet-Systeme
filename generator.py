
def comparator(src, dest, STATE) :

    '''
    compare two lists with different path
    and make a list of missing or old files of source path
    '''

    dest_files = [file[0] for file in dest]
    requiered_files = []

    for (s_file, stat_src) in src :
        mod_time_src = stat_src.st_mtime
        size_src = stat_src.st_size

        if s_file in dest_files :
            # File in destination
            if STATE['-I'] :
                requiered_files.append(s_file)

            elif (not STATE['--ignore_existing'] or s_file[-1] == '/') :
                index_dest = dest_files.index(s_file)
                (_, stat_dest) = dest[index_dest]
                mod_time_dest = stat_dest.st_mtime
                size_dest = stat_dest.st_size

                if ((STATE['-u']) and (mod_time_src < mod_time_dest))  or  ((STATE['--size_only']) and (size_src == size_dest)) :
                    continue

                if (mod_time_src > mod_time_dest) or (size_src != size_dest):
                    requiered_files.append(s_file)


        else : 
            # File not in destination
            if not STATE['--existing'] :
                requiered_files.append(s_file)


    return requiered_files