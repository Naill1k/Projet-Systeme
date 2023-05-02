import os, sys, pickle

MAX_BYTES = 1024


def send(v) :
    '''
    Sends the data 'v' throught stdout
    '''
    binaries = pickle.dumps(v)
    total_bytes_written = 0

    try :
        while total_bytes_written < len(binaries):
            bytes_written = os.write(1, binaries[total_bytes_written:])
            if bytes_written == 0:
                log("Message couldn't be send entirely", 0, 0)
                sys.exit(23)
            total_bytes_written += bytes_written

    except ConnectionResetError :
        log('Connection closed by remote host', 0, 0)
        sys.exit(11)




def receive() :
    '''
    Receive the data from stdin and returns the value 'v' associated
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
        sys.exit(11)
    

    try :
        v = pickle.loads(data)

    except :
        log(f'Error reading input data : {data}', 0, 0)
        sys.exit(11)

    return v



def log(msg, verbosity, priority) :
    '''
    Displays the information 'msg' if the priority is at least the level of verbosity specified
    '''
    if verbosity >= priority :
        print(msg, end='\n\n', file=sys.stderr)
        