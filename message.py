import os, sys, pickle

MAX_BYTES = 1024


def send(tag, v) :
    '''
    Sends the data 'v' throught the file descriptor 'fd' with the associated tag
    '''
    binaries = pickle.dumps(v)
    n = os.write(1, binaries)

    if n != len(binaries) :
        log("Message couldn't be send entirely", 0, 0)


def receive() :
    '''
    Receive the data from the file descriptor 'fd' and returns a tuple (tag, v) associated
    '''
    data = b''
    
    try :
        buff = os.read(0, MAX_BYTES)
        while len(buff) == MAX_BYTES :
            data += buff
            buff = os.read(0, MAX_BYTES)

        data += buff

    except ConnectionResetError :
        log('Connection closed by remote host', 0, 0)  
    

    try :
        data = pickle.loads(data)

    except :
        log(f'Error reading input data : {data}', 0, 0)
        exit(1)

    return (None, data)



def log(msg, verbosity, priority) :
    '''
    Displays the information 'msg' if the priority is at least the level of verbosity specified
    '''
    if verbosity >= priority :
        print(msg, end='\n\n', file=sys.stderr)
        