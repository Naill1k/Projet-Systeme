import os, sys, pickle, option

MAX_BYTES = 1024


def send(fd, tag, v) :
    '''
    Sends the data 'v' throught the file descriptor 'fd' with the associated tag
    '''
    binaries = pickle.dumps(v)
    n = os.write(fd, binaries)

    if n != len(binaries) :
        log("Message couldn't be send entirely", 1)


def receive(fd) :
    '''
    Receive the data from the file descriptor 'fd' and returns a tuple (tag, v) associated
    '''
    data = b''
    
    buff = os.read(fd, MAX_BYTES)
    while len(buff) == MAX_BYTES :
        data += buff
        buff = os.read(fd, MAX_BYTES)

    data += buff
    data = pickle.loads(data)

    return (None, data)



def log(msg, priority=0) :
    '''
    Displays the information 'msg' if the priority is at least the level of verbosity specified
    '''
    v_lvl = option.args.verbose
    if v_lvl >= priority :
        print(msg, '\n', file=sys.stderr)