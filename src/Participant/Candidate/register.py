import socket
import pickle

#Ip of the candidate.
myIp='10.168.0.7'
ec_ip = '10.168.0.6'
myPort = 4322
ec_port = 5322
id = 1

s_ec = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s_ec.connect((ec_ip, ec_port))

#send ID:
data1 = bytes(str(id),'utf-8')
s_ec.send(data1)

#recieve acknowledgment:

ack = s_ec.recv(1024)

