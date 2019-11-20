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
	   	#connect to the voter you just received data from and send a random number c
	    randomNo = generateRandomNumber(64)
	    data = pickle.dumps(randomNo)
	    conn.send(data)
	    #receive data from voter again 
	    data = conn.recv(1024)
	    #compute stuff and verify stuff (Krithiga will send)
	    #if match send ok to voter
	    #receive hash message from voter if sent ok
	    #random number generate - reference number
	    #send reference number back to voter
	    #store in shared database secret message and reference number


create_shared_database()
th_public=Thread(target=listenPublicKeys)
th_public.start()

th_register=Thread(target=listenRegistrationRequest)
th_register.start()



   
