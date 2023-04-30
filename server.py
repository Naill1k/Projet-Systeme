import message, sender, receiver

def server() :
    # Asks the client for the STATE dictionnary
    STATE = message.receive()
    message.send(None)
    message.receive()  # ACK from client
    message.log(f'[SERVER] STATE dictionnary : {STATE}', STATE['-v'], 2)

        
    if STATE['mode'] == 'PULL' :
        message.log('[SERVER] Becoming sender', STATE['-v'], 2)
        sender.sender(STATE)
    
    else :
        message.log('[SERVER] Becoming receiver', STATE['-v'], 2)
        receiver.receiver(STATE)
