import os, socket, select, sys, signal, daemon, client, server, option


def demonizer(STATE):

    with daemon.DaemonContext(stdout=open('démon.log','a+'),stderr=open('mrsync.err','a+'),detach_process=STATE['--no_detach']):

        def capture(sig,frame):

            global run
            print("SIGTERM receive. End of all communications")
            run = False


        HOST = 'localhost'
        PORT = 10873


        MAXBYTES = 1024
        list_pid_fils = []


        serversocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        serversocket.bind((HOST,PORT))
        serversocket.listen()
        print("server is listening on port:",PORT)
        socketlist = [serversocket]
        run = True


        while run:

            signal.signal(signal.SIGTERM,capture)

            (activesockets,_,_) = select.select(socketlist,[],[])

            for s in activesockets:

                if s == serversocket:
                    clientsocket, (addr,port) = serversocket.accept()
                    socketlist.append(clientsocket)

                else:
                    pidf = os.fork()
                    list_pid_fils.append(pidf)
                    if not pidf:

                        server.server()

                        os.dup2(s.fileno(),0)
                        os.dup2(s.fileno(),1)

                        


        for pid in list_pid_fils:
            os.kill(pid, signal.SIGTERM)
        
        for conn in socketlist:
            conn.close()

        serversocket.close()
        print("Au revoir")
        sys.exit(0)