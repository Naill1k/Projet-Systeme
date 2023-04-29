import os, socket, sys, signal, daemon, client, option, server


def demonizer(STATE):

    with daemon.DaemonContext(working_directory=os.path.expanduser("~"),stdout=open('démon.log','a+'),stderr=open('mrsync.err','a+'),detach_process=not(STATE['--no_detach'])):

        def capture(sig,frame):

            global run
            print("SIGTERM receive. End of all communications")
            run = False

        signal.signal(signal.SIGTERM,capture)


        HOST = STATE['host']
        PORT = STATE['--port']


        MAXBYTES = 1024
        list_pid_fils = []


        serversocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        serversocket.bind((HOST,PORT))
        serversocket.listen()
        print(f"Server is listening with address '{HOST}' on port '{PORT}'")
        run = True
        

        while run:

            conn,addr = serversocket.accept()

            pidf = os.fork()
            list_pid_fils.append(pidf)
            if not pidf:

                os.dup2(conn.fileno(),0)
                os.dup2(conn.fileno(),1)

                server.server()
                exit(0)


        for pid in list_pid_fils:
            os.kill(pid, signal.SIGTERM)

        serversocket.close()
        print("Au revoir")
        sys.exit(0)