import os, sys, pickle

MAX_BYTES = 1024


def send(tag, v) :
    '''
    Sends the data 'v' throught the file descriptor 'fd' with the associated tag
    '''
    binaries = pickle.dumps(v)
    n = os.write(1, binaries)

    if n != len(binaries) :
        log("Message couldn't be send entirely", 1)


def receive() :
    '''
    Receive the data from the file descriptor 'fd' and returns a tuple (tag, v) associated
    '''
    data = b''
    
    buff = os.read(0, MAX_BYTES)
    while len(buff) == MAX_BYTES :
        data += buff
        buff = os.read(0, MAX_BYTES)

    data += buff
    if len(data) == 0 :
        log('Error reading input file')
    
    try :
        data = pickle.loads(data)
        # if (type(data) == str) and (data[:3] == 'LOG') :  # If data is a string starting with 'LOG', it is displayed
        #     log(data[3:])
        #     receive()

    except :
        log(data)
        data = pickle.loads(data) # type: ignore

    return (None, data)



def log(msg, verbosity=0, priority=0) :
    '''
    Displays the information 'msg' if the priority is at least the level of verbosity specified
    '''
    if verbosity >= priority :
        print(msg, end='\n\n', file=sys.stderr)
        