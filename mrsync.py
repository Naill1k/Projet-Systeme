#!/usr/bin/env python3
import os

import server
import client



fdr1, fdw1 = os.pipe()  # Pipe client -> server
fdr2, fdw2 = os.pipe()  # Pipe server -> client

if os.fork() :
    os.dup2(fdr1, 0)
    os.dup2(fdw2, 1)

    os.close(fdr2)
    os.close(fdw1)
    
    server.server()

    os.close(fdr1)
    os.close(fdw2)

else :
    os.close(fdr1)
    os.close(fdw2)

    client.client(fdr2, fdw1)
    
    os.close(fdr2)
    os.close(fdw1)
    