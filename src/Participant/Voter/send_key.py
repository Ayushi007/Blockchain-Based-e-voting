import socket
import pickle
from ..encryptions import generate_keys

myIp = '0.0.0.0'
ec_ip = '192.168.43.131'
myPort = 4322
ec_port = 5320

def send_public_key():
	s_tracker = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s_tracker.connect((ec_ip, ec_port))
	private_key, public_key = generate_keys()
	data = pickle.dumps(public_key)
	s_tracker.send(data)
	s_tracker.close()
	print("Public_key sent")
