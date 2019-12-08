	import socket
	import pickle
	from threading import Thread
	import time
	import random
	import json
	
	HOST = '0.0.0.0'
	PORT_VOTING = 5320
	PORT_ELECTION = 5322
	
	valid = False
	
	voter_details =[]
	
	def listen_voting():
	    while(True):
	        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	        s.bind((HOST,PORT_ELECTION))
	        s.listen(10)
	        (conn, (ip, port)) = s.accept()
	        voter_content = conn.recv(1024)
	        open('voter_details.txt',w+)
	        file_voter.write(str(voter_contents))
	        file_voter.close()
	        
	        #open file and read the content in a tuple
	        with open('voter_details.txt', 'r') as fp:
	        	for i in fp.readlines():
	            tmp = i.split(",")
	        	voter_details.append((float(tmp[0]), float(tmp[1])))
	            
	        conn.send(bytes("Send Candidate details", 'utf-8'))
	        candidate_list = conn.recv(1024)
	
	th_public=Thread(target=listen_voting)
	th_public.start()
	th_public.join(10)
	
	while(True):
	    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	    s.bind((HOST,PORT_VOTING))
	    s.listen(10)
	    (conn, (ip, port)) = s.accept()
	    mess = conn.recv(1024)
	    print("messageReceied", mess)
	    converted_mess = pickle.loads(mess)
	    refno = converted_mess[0]
	    hashmsg = converted_mess[1]
	    for i in voter_details:
	        if(voter_details[i][0] == refno):
	            if(voter_details[i][1] ==hasmessah):
	                conn.send(bytes(candidate_list, 'utf-8'))
	            else:
	                print("invalid voter")
	                conn.send(bytes(str(0), 'utf-8'))
	        else:
	            print("invalid voter")
            conn.send(bytes(str(0), 'utf-8'))







