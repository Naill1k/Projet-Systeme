import os, select, socket, sys, signal, time, daemon


'''
def capture(sig,frame):

    global run
    print("SIGTERM receive. End of all communications")
    run = False


HOST = 'localhost'
PORT = 10873


MAXBYTES = 1024


serversocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
serversocket.bind((HOST,PORT))
serversocket.listen()
print("server is listening on port:",PORT)
run = True


while run:

    signal.signal(signal.SIGTERM,capture)

    (activesockets,_,_) = select.select(socketlist,[],[])

    for s in activesockets:

        if s == serversocket:
            clientsocket,(addr,port) = serversocket.accept()
            socketlist.append(clientsocket)
            print("connection from the addr",addr)

        else:
            msg = s.recv(MAXBYTES)

            if len(msg) == 0:
                s.close()
                socketlist.remove(s)

            else:
                TO DO

for c in socketlist:
    c.close
serversocket.close()
print("Au revoir")
sys.exit(0)

'''

def function():
    i=0
    while True:
        print(i,": Hello, world!")
        i += 1
        time.sleep(5)

with daemon.DaemonContext(stdout=open('démon.log','a+'),stderr=open('mrsync.err','a+'),detach_process=True):
    function()
