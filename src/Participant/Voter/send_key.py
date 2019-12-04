import socket
import pickle
from encryptions import generate_keys

myIp = '0.0.0.0'
ec_ip = '10.168.0.6'
myPort = 4322
ec_port = 5420

s_tracker = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s_tracker.connect((ec_ip, ec_port))
private_key, public_key = generate_keys()
print("Public key", public_key)
print("Private key", private_key)
#data = bytes(public_key, 'utf-8')
data = pickle.dumps(public_key)
print("Data converted", data)
s_tracker.send(data)
s_tracker.close()

print("Public_key sent")
