import socket
import threading
import pandas as pd
host = '172.16.2.42'
port = 5090
FORMAT = 'utf-8'
SIZE = 1024
#function that receive and send the message

def clients(communication_socket , address):
    
    print(f"you are connected to {address}")
    message = communication_socket.recv(SIZE).decode(FORMAT)
    message.to_csv('studentpresent.csv')
    print("here is your message")
    print(message)
    print("type your message here")
    user_message = input(">>>")
    communication_socket.send(user_message.encode(FORMAT))

# function that initialize the server and listen to connection to the port
def connection():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen()
    while True:
        communication_socket, address = server.accept()
        thread = threading.Thread(target = clients, args = (communication_socket, address))
        thread.start()
#call of connectionf function

connection()
