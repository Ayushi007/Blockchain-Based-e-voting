import socket
import pickle
from threading import Thread
import mysql.connector
import time
import random
import string


HOST = '0.0.0.0'
PORT_PUBLICKEY = 5320
PORT_REGISTER = 5322
public_keys = []
p=179
g=137
valid = False
found_keys= False
y = [137, 153, 18, 139, 69, 145, 175, 168, 104, 107, 160, 82, 136, 16, 44, 121, 
109, 76, 30, 172, 115, 3, 53, 101, 54, 59, 28, 77, 167, 146, 133, 142, 122, 67, 50, 48, 
132, 5, 148, 49, 90, 158, 166, 9, 159, 124, 162, 177, 84, 52, 143, 80, 41, 68, 8, 22, 150,
144, 38, 15, 86, 147, 91, 116, 140, 27, 119, 14, 128, 173, 73, 156, 71, 61, 123, 25, 24, 66, 
92, 74, 114, 45, 79, 83, 94, 169, 62, 81, 178, 42, 26, 161, 40, 110, 34, 4, 11, 75, 72, 19, 97, 
43, 163, 135, 58, 70, 103, 149, 7, 64, 176, 126, 78, 125, 120, 151, 102, 12, 33, 46, 37, 57, 
112, 129, 131, 47, 174, 31, 130, 89, 21, 13, 170, 20, 55, 17, 2, 95, 127, 36, 99, 138, 111, 171, 
157, 29, 35, 141, 164, 93, 32, 88, 63, 39, 152, 60, 165, 51, 6, 106, 23, 108, 118, 56, 154, 155,
113, 87, 105, 65, 134, 100, 96, 85, 10, 117, 98, 1]

candidate_id = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]



#creates a shared SQL database for storing registration information
def create_shared_database():
        e_voting_db = mysql.connector.connect(
                host = "localhost",
                user = "ayushi", #contains username
                passwd = "password" #contains password
        )
        mycursor = e_voting_db.cursor()
        mycursor.execute("CREATE DATABASE e_voting_db")

#creates a table in shared db for voter information
def create_voter_table():
    e_voting_db = mysql.connector.connect(
            host = "localhost",
            user = "ayushi", #contains username
            passwd = "password" #contains password
            database = "e_voting_db"
            )
    mycursor = e_voting_db.cursor()
        #assuming secret message and reference number are both strings
        mycursor.execute("CREATE TABLE voters (secret VARCHAR(255), reference VARCHAR(255))")

#populates the voter IDs and keys to create a list of govt. issued
# def populate_voters():


#def listenpublickeys():
#	while(True):
#	    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#	    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#	    s.bind((HOST, PORT_PUBLICKEY))
#	    s.listen(10)
#	    (conn, (ip, port)) = s.accept()
#	    data = conn.recv(1024)
#	    public_keys.append(data)

def generateReferenceNumber(stringLength):
    # Generate a random string of letters and digits
    lettersAndDigits = string.ascii_letters + string.digits
    message=''
    for i in range(stringLength):
        message+=random.choice(lettersAndDigits)
    return message

def generateRandomNumber(bits):
        return random.getrandbits(bits)

def listenRegistrationRequest():
        while(True):
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind((HOST, PORT_REGISTER))
            s.listen(1)
            (conn, (ip, port)) = s.accept()
            data = conn.recv(1024)
            print("Received m", data)
            #m = data  #g^r or candidate id
            m = int(str(data, 'utf-8'))
            #m = int.from_bytes(m, byteorder='big')
            print("converted m", m)
            #if it is a candidate
            if m in candidate_id:
                data = bytes('valid', 'utf-8') 
                conn.send(data)
                #store in candidate database.
                #creates public address and instantitates into multichain
            else:
                #connect to the voter you just received data from and send a random number c.
                c = generateRandomNumber(4)
                data = bytes(str(c), 'utf-8')
                #data = pickle.dumps(c)
                print("c generated is", c)
                conn.send(data)
                #receive data from vote
                data1 = conn.recv(1024)
                s = data1
                print("Received s", s)
                #compute stuff and verify stuff
                #if match send ok to voter
                #s = int.from_bytes(s, byteorder='big')
                s = int(str(s, 'utf-8'))
                print("converted s", s)
                k = pow(g,s)%p
                print("k is", k)
                valid = False
                for i in y:
                    if ((m * pow(i, 4))%p == k):
                        valid = True
                        print("Valid Voter")
                        break
                if(not valid):
                    conn.close()
                    continue
                #receive hash message with private key encrypted from voter if sent ok
                h,sig= conn.recv(1024)
                #public key verification.
               
                for pks in public_keys:
                    if(verify(pk,h,sig)):
                    found_keys = True
                    #random number generate - reference number
                    ref_no = generateRandomNumber(6)
                    print("Generated ref_number", ref_no)
                    data_ref = bytes(str(ref_no), 'utf-8')
                    #send reference number back to voter
                    conn.send(data_ref)
                    #store in shared database //secret message// (we can just send reference number its enough) and reference number
                    #creates public address and instantitates into multichain and assigns an asset using multichain.
                    break
                if(not found_keys):
                    print("Authentication failed")
                    conn.close()




#create_shared_database()
#create_voter_table()

#removing thread for listening to public keys, storing in file with voter ID
#th_public=Thread(target=listenPublicKeys)
#th_public.start()

th_register=Thread(target=listenRegistrationRequest)
th_register.start()
