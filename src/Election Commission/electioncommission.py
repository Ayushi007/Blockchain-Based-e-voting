import socket
import pickle
from threading import Thread
import mysql.connector
import time
import random

eligible_voters = []
HOST = '0.0.0.0'
PORT_PUBLICKEY = 5320
PORT_REGISTER = 5321
public_keys = []
p=179
g=137
valid = "not-ok"
y = ()
#creates a shared SQL database for storing registration information
def create_shared_database():

#populates the list eligible voters to create a list of govt. issued IDs for eligible voters using a file
def populate_voters():


def listenpublickeys():
	while(True):
	    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	    s.bind((HOST, PORT_PUBLICKEY))
	    s.listen(10)
	    (conn, (ip, port)) = s.accept()
	    data = conn.recv(1024)
	    public_keys.append(data)

def generateReferenceNumber(stringLength):
    # Generate a random string of letters and digits
    lettersAndDigits = string.ascii_letters + string.digits
    message=''
    for i in range(stringLength):
        message+=random.choice(lettersAndDigits)
    return message

def generateRandomNumber(bits):
	random.getrandbits(bits)

def listenRegistrationRequest():
	while(True):
	    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	    s.bind((HOST, PORT_PUBLICKEY))
	    s.listen(1)
	    (conn, (ip, port)) = s.accept()
	    data = conn.recv(1024)
		m = data  #g^r
	    #connect to the voter you just received data from and send a random number c
	    c = generateRandomNumber(4)
	    data = pickle.dumps(c)
	    conn.send(data)
	    #receive data from vote
	    data1 = conn.recv(1024)
		s = data1
	    #compute stuff and verify stuff
		#if match send ok to voter
		k = pow(g,s)%p
		valid = False
		for i in y:
			if (m * pow(i, c) == k):
				valid = True
				break
		if(!valid):
			conn.close()
			continue
	    #receive hash message from voter if sent ok
		data = conn.recv(1024)
	    #random number generate - reference number
		ref_no = generateRandomNumber(6)
	    #send reference number back to voter
		conn.send(data)
	    #store in shared database secret message and reference number


create_shared_database()
th_public=Thread(target=listenPublicKeys)
th_public.start()

th_register=Thread(target=listenRegistrationRequest)
th_register.start()
