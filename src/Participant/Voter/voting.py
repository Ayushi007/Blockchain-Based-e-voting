import socket
import pickle

myIp='10.168.0.7'
ttp_ip = '10.168.0.6'
myPort = 4322
ttp_port = 5322

receive_list = []

s_ttp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s_ttp.connect((ttp_ip, ttp_port))
print("Connection established")

print("Send reference number")
file1 = open('refNum.txt', 'r')
refno =file1.read()
file1.close()
data = bytes(str(refno), 'utf-8')
s_ttp.send(data)
#recieve a list which has first elemet 0 or 1 depicting success or not and next dictionary.
receive_list = s_ttp.recv(1024)

if(receive_list[0]):
    print("candidate list and public addresses")
    for i,j in receive_list[1].items():
        print("candidate name: {}   public address{}").format(i,j)
    #The person u want to send.
    #send using multichain.
else:
    
    print("not a registered voter")







