import os, socket, select, sys, signal, daemon, server


def demonizer(STATE):

    with daemon.DaemonContext(stdout=open('démon.log','a+'),stderr=open('mrsync.err','a+'),detach_process=STATE['--no_detach']):

        def capture(sig,frame):
            global run
            print("SIGTERM receive. End of all communications")
            run = False

        signal.signal(signal.SIGTERM,capture)

        HOST = STATE['host']
        PORT = STATE['--port']

        MAXBYTES = 1024
        # list_pid_fils = []

        serversocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        serversocket.bind((HOST,PORT))
        serversocket.listen()
        print(f"Server is listening with address '{HOST}' on port '{PORT}'")
        socketlist = [serversocket]
        run = True
        os.chdir('home/naillik')


        while run:
            (activesockets,_,_) = select.select(socketlist,[],[])

            for s in activesockets :
                if s == serversocket :
                    clientsocket, (addr,port) = serversocket.accept()
                    print(f"Incoming connection from '{addr}' on port '{port}'", file=sys.stderr)
                    socketlist.append(clientsocket)
                    
                else :
                    print('Executing server in CWD :', os.getcwd(), file=sys.stderr)
                    os.dup2(s.fileno(), 0)
                    os.dup2(s.fileno(), 1)

                    server.server()
                    exit(0)

                    # pidf = os.fork()
                    # list_pid_fils.append(pidf)
                    # if not pidf:

                    #     os.dup2(s.fileno(), 0)
                    #     os.dup2(s.fileno(), 1)

                    #     server.server()
                    #     exit(0)



        # for pid in list_pid_fils:
        #     os.kill(pid, signal.SIGTERM)
        
        for conn in socketlist:
            conn.close()

        serversocket.close()
        print("Au revoir")
        sys.exit(0)
