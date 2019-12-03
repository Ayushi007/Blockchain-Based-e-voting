import socket
import pickle
from encryptions import generate_keys
from encryptions import sign

myIp = '34.94.53.204'
ec_ip = '35.236.49.105'
myPort = 4322
ec_port = 5322

private_key, public_key = generate_keys()
print(public_key)
print("\n")
print (private_key)

def send_public_key():
	#s_tracker = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	#s_tracker.connect((ec_ip, ec_port))
	data = pickle.dumps(public_key)
	s_ec.send(data)
	print("Public_key sent")

s_ec = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s_ec.connect((ec_ip, ec_port))
print("Connection established")
send_public_key()

file1 = open('Privatekey.txt', 'w')
file1.write(str(private_key))
file1.close()
	


