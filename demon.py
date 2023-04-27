import os, socket, sys, signal, daemon, client, option, server


def demonizer(STATE):

    with daemon.DaemonContext(stdout=open('démon.log','a+'),stderr=open('mrsync.err','a+'),detach_process=not(STATE['--no_detach'])):

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
        run = True



        while run:

            signal.signal(signal.SIGTERM,capture)

            conn,addr = serversocket.accept()

            pidf = os.fork()
            list_pid_fils.append(pidf)
            if not pidf:

                server.server()

                print("ok")

                os.dup2(conn.fileno(),1)
                os.dup2(conn.fileno(),0)


        for pid in list_pid_fils:
            os.kill(pid, signal.SIGTERM)

        serversocket.close()
        print("Au revoir")
        sys.exit(0)