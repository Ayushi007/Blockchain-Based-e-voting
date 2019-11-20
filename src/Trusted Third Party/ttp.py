import socket
import pickle
from threading import Thread
import time
import random
import mysql.connector
#variable to store validity of incoming voter
valid = False
def validate_voter(data):
	e_voting_db = mysql.connector.connect(
  		host="localhost",
  		user="ayushi",
  		passwd="yourpassword",
  		database="e_voting_db"
	)
	mycursor = e_voting_db.cursor()
	mycursor.execute("SELECT * FROM voters")
	result = mycursor.fetchall()
	for res in result:
		print(res)
		#check for existence of tuple here (secret-reference)
while(True):
	    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	    s.bind((HOST, PORT_PUBLICKEY))
	    s.listen(10)
	    (conn, (ip, port)) = s.accept()
	    #tuple receive
	    data = conn.recv(1024)
	    #check in the shared database if it exists
	    valid = validate_voter(data)
	    #send accept and candidate list/ reject
	    if valid:
		#query candidate database to find public keys
		#send ok to voter 
		#send candidate list to choose from 
