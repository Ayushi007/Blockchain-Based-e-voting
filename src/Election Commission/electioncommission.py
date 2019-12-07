import socket
import pickle
from threading import Thread
#import mysql.connector
import time
import random
import string
import os
from encryptions import *


HOST = '0.0.0.0'
os.system("sudo lsof -t -i tcp:5420 | xargs kill -9")
PORT_PUBLICKEY = 5420
os.system("sudo lsof -t -i tcp:5430 | xargs kill -9")
PORT_REGISTER = 5430
public_keys = []
p=179
g=137
valid = False
found_keys= False

y = [139, 24, 100, 32, 143, 163, 63, 90, 47, 98, 21, 171, 111, 131, 71, 40, 45, 110, 6, 130, 10, 163, 47, 13, 154, 81, 96, 90, 49, 171]
#Valid ids for now [538, 433, 350, 329, 407, 459, 687, 219, 482, 533, 131, 144, 499, 303, 429, 271, 260, 450, 693, 663, 175, 637, 304, 132, 165, 622, 529, 575, 574, 322]
candidate_id = ['CAND01', 'CAND02']
public_keys = []
cand_add_list = []

#creates a shared SQL database for storing registration information
"""def create_shared_database():
        e_voting_db = mysql.connector.connect(
                host = "localhost",
                user = "ayushi", #contains username
                passwd = "password" #contains password
        )
        mycursor = e_voting_db.cursor()
        mycursor.execute("CREATE DATABASE e_voting_db")
"""
#creates a table in shared db for voter information
"""def create_voter_table():
    e_voting_db = mysql.connector.connect(
            host = "localhost",
            user = "ayushi", #contains username
            passwd = "password" #contains password
            database = "e_voting_db"
            )
    mycursor = e_voting_db.cursor()
        #assuming secret message and reference number are both strings
        mycursor.execute("CREATE TABLE voters (secret VARCHAR(255), reference VARCHAR(255))")
"""
#populates the voter IDs and keys to create a list of govt. issued
# def populate_voters():


def listenPublicKeys():
    while(True):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT_PUBLICKEY))
        s.listen(1)
        (conn, (ip, port)) = s.accept()
        data = conn.recv(1024)
        pubKey = pickle.loads(data)
        public_keys.append(pubKey)
        print("Data- public keys", data)
        print("Converted public keys", pubKey)
        conn.close()
        for p in public_keys:
            print(p)

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
            
            status = conn.recv(1024)
            participant = str(status, 'utf-8')
            print("Participant is", participant)
            
            if(participant == 'Candidate'):
                conn.send(bytes("Starting", 'utf-8'))
                data = conn.recv(1024)
                print("Received m", data)
                m = str(data, 'utf-8')
                
                if m in candidate_id:
                    connect_multi = bytes('multichaind survey@10.168.0.6:9543 -daemon', 'utf-8')
                    conn.send(connect_multi)
                    print("Sent command to Candidate to get added to multichain")

                    cand_add = conn.recv(1024)
                    cand_add = str(cand_add, 'utf-8')
                    access_cmd = "multichain-cli survey grant "+ cand_add+" receive,send"
                    print("Candidate address received")
                    os.system(access_cmd)
                    print("Granted receive permission to Candidate:", cand_add)
                    cand_add_list.append(cand_add)
                    continue
                else :
                    data = bytes('invalid', 'utf-8')
                    conn.send(data)
                    continue
            
            conn.send(bytes("Starting", 'utf-8'))
            data = conn.recv(1024)
            print("Received m", data)
            #m = data  #g^r or candidate id
            m = int(str(data, 'utf-8'))
            #m = int.from_bytes(m, byteorder='big')
            print("converted m", m)
            
           
            #connect to the voter you just received data from and send a random number c.
            c = 1
            data = bytes(str(c), 'utf-8')
            #data = pickle.dumps(c)
            #print("c generated is", c)
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
                if ((m * i)%p == k):
                    valid = True
                    print("Valid Voter")
                    break
            if(not valid):
                invalidMsg = bytes('-1', 'utf-8')
                conn.send(invalidMsg)
                conn.close()
                continue
            #receive hash message with private key encrypted from voter if sent ok
            mess = conn.recv(1024)
            #mess = conn.recvfrom(4096)
            print("messageReceied", mess)
            converted_mess = pickle.loads(mess)
            print("signedMessage-converted", converted_mess)
            h = converted_mess[0]
            sig = converted_mess[1]
            #h, sig = pickle.loads(mess)
            #public key verification.

            for pks in public_keys:
                if(verify(pks,h,sig)):
                    found_keys = True
                    print("Voter's public key found")
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
                continue

            init_multichain = conn.recv(1024)
            connect_multi = bytes('multichaind survey@10.168.0.6:9543 -daemon', 'utf-8')
            conn.send(connect_multi)
            print("Sent command to Voter to get added to multichain")

            voter_add = conn.recv(1024)
            v_add = str(voter_add, 'utf-8')
            access_cmd = "multichain-cli survey grant "+ v_add+" receive,send"
            print("Voter_address received")
            os.system(access_cmd)
            print("Granted receive permission to Voter:", v_add)

            send_token = "multichain-cli survey sendassettoaddress "+v_add+" token 1"
            os.system(send_token)
            print("Token given to Voter: ", v_add)


#create_shared_database()
#create_voter_table()

#removing thread for listening to public keys, storing in file with voter ID
os.system("multichaind survey -daemon")
th_public=Thread(target=listenPublicKeys)
th_public.start()

th_register=Thread(target=listenRegistrationRequest)
th_register.start()
