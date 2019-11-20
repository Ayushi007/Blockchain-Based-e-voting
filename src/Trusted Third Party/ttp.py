import socket
import pickle
from threading import Thread
import time
import random

while(True):
	    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	    s.bind((HOST, PORT_PUBLICKEY))
	    s.listen(10)
	    (conn, (ip, port)) = s.accept()
	    #tuple receive
	    data = conn.recv(1024)
	    #check in the shared database if it exists
	    #send accept and candidate list/ reject
	    
