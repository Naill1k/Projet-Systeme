#!/usr/bin/env python3
import os

import server
import client



fdr, fdw = os.pipe()

if os.fork() :
    os.dup2(fdr, 0)
    os.dup2(fdw, 1)
    
    server.server()

else :
    client.client(fdr, fdw)
    
os.close(fdr)
os.close(fdw)