import socket
import pickle
from encryptions import *
import random
import string
from send_key import *

def encryptedSecretMessage(stringLength):
    # Generate a random string of letters and digits
    letters_and_digits = string.ascii_letters + string.digits
    message = ''
    for i in range(stringLength):
        message += random.choice(letters_and_digits)
    message = message.encode('utf-8')
   # private_key, public_key = generate_keys()
    return sign(private_key, message)

myIp='10.168.0.7'
ec_ip = '10.168.0.6'
myPort = 4322
ec_port = 5430
id = 100
p = 179
g = 137

s_ec = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s_ec.connect((ec_ip, ec_port))
print("Connection established with Election Commission")
#ZKP Algorithm to make EC verify that id(=100) is valid
# send random number to EC
r = random.getrandbits(4)
m = pow(g, r) % p
print("Send g^r%p", m)
data1 = bytes(str(m),'utf-8')
#data1 = pickle.dumps(m)
s_ec.send(data1)

# Get random number from EC
c = s_ec.recv(1024)
print("Received c", c)
c = int(str(c, 'utf-8'))
#c = int.from_bytes(c,byteorder='big')
print("Converted c", c)
s = (r + c*id)%(p-1)
data2 = bytes(str(s), 'utf-8')
#data2 = pickle.dumps(s)
print("Send s = r+c*id", s)
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
file1 = open('refNum.txt', 'w')
file1.write(str(ref_number)+'\n')
file1.close()
s_ec.close()
print("Registered successfully")
