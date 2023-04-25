import os


def comparator(path_s,src,path_d,dest, STATE) :

    '''
    compare two lists with different path
    and make a list of missing or old files of source path
    '''

    if path_s[-1] != '/':
        path_s = '/'.join(path_s.split('/')[:-1]) + '/'

    D = []
    C = []

    for dest_files in dest:
        D.append(dest_files[0])

    for src_files in src:

        if src_files[0] in D:
            
            if (not STATE['-u']):

                index_dest = D.index(src_files[0])

                if src_files[1] > dest[index_dest][1]:
                    C.append(src_files[0])

        else:
            
            C.append(src_files[0])

    return C