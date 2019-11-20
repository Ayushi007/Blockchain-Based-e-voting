import socket
import pickle
import encryptions
from encryptions import generate_keys
from encryptions import sign
import random
import string

def encryptedSecretMessage(stringLength):
    # Generate a random string of letters and digits
    lettersAndDigits = string.ascii_letters + string.digits
    message=''
    for i in range(stringLength):
        message+=random.choice(lettersAndDigits)
    private_key, public_key = generate_keys()
    return sign(message, private_key)

myIp='0.0.0.0'
ec_ip = '192.168.43.131'
myPort=4322
ec_port = 5321
id = 100
p=179
g=137

def register():
	s_ec = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s_ec.connect((ec_ip, ec_port))

    #ZKP Algorithm to make EC verify that id(=100) is valid
    # send random number to EC
    r = random.getrandbits(4)
    m = pow(g, r) % 179
    data1 = pickle.dumps(m)
    s_ec.send(data1)

    # Get random number from EC
    c = s_ec.recv(1024)
    s = r + c*(id)
    data2 =pickle.dumps(s)
    s_ec.send(data2)

    # Hashed Secret message
	hashMessage = encryptedSecretMessage(6)
	data = pickle.dumps(hashMessage)
	s_ec.send(data)

    # Reference number received from EC for that election
    ref_number = s_ec.recv(1024)
    file1 = open('refNum.txt', 'w')
    file1.write(ref_number)
    file1.close()
	s_ec.close()
	print("Registered successfully")
