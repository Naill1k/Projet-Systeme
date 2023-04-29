import os, socket, sys, signal, daemon, server, time


def demonizer(STATE):

    with daemon.DaemonContext(working_directory=os.path.expanduser("~"), stdout=open('démon.log','a+'), stderr=open('mrsync.err','a+'), detach_process=not(STATE['--no_detach'])) :
        
        def capture(sig,frame) :
            '''
            Properly closes all communications
            '''
            nonlocal serversocket
            print("Signal SIGTERM received, sending the daemon back to hell.")
            
            print('Killing all subprocesses and closing socket')
            for pid in list_pid_fils:
                os.kill(pid, signal.SIGUSR1)

            serversocket.close()
            print("Au revoir")
            sys.exit(0)


        def handler(sig, _) :
            nonlocal list_pid_fils
            '''
            To prevent creating zombies when a client has finished
            '''
            pid,_ = os.wait()
            list_pid_fils.remove(pid)
        

        def close_socket(sig, _) :
            nonlocal conn
            conn.close()
            sys.exit(0)
            
        signal.signal(signal.SIGTERM, capture)
        signal.signal(signal.SIGCHLD, handler)
        signal.signal(signal.SIGUSR1, close_socket)


        HOST = STATE['host']
        PORT = STATE['--port']


        MAXBYTES = 1024
        list_pid_fils = []

        serversocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        serversocket.bind((HOST,PORT))
        serversocket.listen()
        print(f"Daemon is listening with address '{HOST}' on port '{PORT}'", end='\n\n')        

        while True :
            conn,addr = serversocket.accept()

            pidf = os.fork()
            list_pid_fils.append(pidf)

            if not pidf:
                os.dup2(conn.fileno(),0)
                os.dup2(conn.fileno(),1)

                server.server()

                conn.close()
                sys.exit(0)


        

        



