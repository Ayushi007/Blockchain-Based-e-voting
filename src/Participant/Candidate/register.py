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

myIp='10.168.0.9'
ec_ip = '10.168.0.6'
myPort = 4323
ec_port = 5430
id = 'CAND01'
p = 179
g = 137

s_ec = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s_ec.connect((ec_ip, ec_port))
print("Connection established with Election Commission")
#ZKP Algorithm to make EC verify that id(=100) is valid
# send random number to EC

s_ec.send(bytes("Candidate",'utf-8'))
start = s_ec.recv(1024)
data1 = bytes(id, 'utf-8')
s_ec.send(data1)

response = s_ec.recv(1024)
resp = str(response, 'utf-8')
if(resp == 'invalid'):
    s_ec.close()
    exit()

command = str(response, 'utf-8')
print("Receiving command",command) 
os.system(command)

command_getaddress = "multichain-cli survey getnewaddress"
os.system(command_getaddress+"> address.txt")
print("OS System ran")
add_file = open('address.txt', 'r')
content = add_file.read()
address_voter = content.split('\n')[-2]
print("Address of Voter:", address_voter)

address_voter = bytes(address_voter, 'utf-8')
print("Sending address in byte format",address_voter)
s_ec.send(address_voter)

s_ec.close()
