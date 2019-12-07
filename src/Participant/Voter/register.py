import socket
import pickle
from encryptions import *
import random
import string
from send_key import *
import subprocess
import os

def encryptedSecretMessage(stringLength):
    # Generate a random string of letters and digits
    letters_and_digits = string.ascii_letters + string.digits
    message = ''
    for i in range(stringLength):
        message += random.choice(letters_and_digits)
    message = message.encode('utf-8')
   # private_key, public_key = generate_keys()
    return sign(private_key, message)

myIp='10.138.0.2'
ec_ip = '10.168.0.6'
myPort = 4322
ec_port = 5430
id = 304
p = 179
g = 137

s_ec = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s_ec.connect((ec_ip, ec_port))
print("Connection established with Election Commission")
#ZKP Algorithm to make EC verify that id(=100) is valid
# send random number to EC
conn.send(bytes('Voter', 'utf-8'))
start_step = conn.recv(1024)
print("EC responded: ",str(start_step, 'utf-8'))
r = random.getrandbits(4)
m = pow(g, r) % p
print("Send g^r%p", m)
data1 = bytes(str(m),'utf-8')
#data1 = pickle.dumps(m)
s_ec.send(data1)

# Get random number from EC
c = s_ec.recv(1024)
#print("Received c", c)
#c = int(str(c, 'utf-8'))
#c = int.from_bytes(c,byteorder='big')
#print("Converted c", c)
s = (r + id)%(p-1)
data2 = bytes(str(s), 'utf-8')
#data2 = pickle.dumps(s)
print("Send s = r+id", s)
s_ec.send(data2)

# Hashed Secret message
print("Private_key", private_key)
print("Public_key", public_key)
signedMessage, signature = encryptedSecretMessage(4)
print("hashMessage", signedMessage)
print("signature", signature)
#signedMessage = bytes(str(signedMessage), 'utf-8')
#sig = bytes(str(signature), 'utf-8')
mess = pickle.dumps([signedMessage, signature])
print("mess-pickl-dumps", mess)
#data = pickle.dumps(hashMessage)
s_ec.send(mess)
#s_ec.send((signedMessage, sig))

# Reference number received from EC for that election
ref_number = s_ec.recv(1024)
ref_number = str(ref_number, 'utf-8')
if(ref_number == -1):
    print("Invalid voter")
    s_ec.close()
    exit()




file1 = open('refNum.txt', 'w')
file1.write(str(ref_number)+'\n')

file1.close()

initiate_msg = "connect blockchain"
initiate_msg = bytes(initiate_msg,'utf-8')
print("Sending initiate message",initiate_msg)
s_ec.send(initiate_msg)

command = s_ec.recv(1024)
command = str(command, 'utf-8')
print("Receiving command",command) 
os.system(command)

command_getaddress = "multichain-cli survey getnewaddress"
os.system(command_getaddress+"> address.txt")
print("Os System ran")
add_file = open('address.txt', 'r')
content = add_file.read()
address_voter = content.split('\n')[-2]
#output = subprocess.check_output(command_getaddress)
#print("Output of get address",output)
#output = output.split('\n')[-2]
print("Address of voter",address_voter)

address_voter = bytes(address_voter, 'utf-8')
print("Sending address in byte format",address_voter)
s_ec.send(address_voter)

s_ec.close()
