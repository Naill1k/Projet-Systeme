import sender, receiver, message

def client(STATE) :
    # Sends STATE dictionnary to server
    message.log(f'[CLIENT] Sending STATE dictionnary', STATE['-v'], 2)
    message.send('State', STATE)
    message.receive()  # ACK from server
    message.send('ACK', None)
    message.log('[CLIENT] Sent STATE dictionnary', STATE['-v'], 2)
    
    if STATE['mode'] == 'PULL' :
        message.log('[CLIENT] Becoming receiver', STATE['-v'], 2)
        receiver.receiver(STATE)  # Actually destination files
    
    else :
        message.log('[CLIENT] Becoming sender', STATE['-v'], 2)
        sender.sender(STATE)
    