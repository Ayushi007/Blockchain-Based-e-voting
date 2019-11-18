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

def register():
	s_ec = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s_ec.connect((ec_ip, ec_port))


	hashMessage = encryptedSecretMessage(6)
	data = pickle.dumps(hashMessage)
	s_ec.send(data)
    ref_number = s_ec.recv(1024)
    file1 = open('refNum.txt', 'w')
    file1.write(ref_number)
    file1.close()
	s_ec.close()
	print("Registered successfully")
