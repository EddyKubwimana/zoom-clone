import socket
while True:
    host = '172.16.8.80'
    port = 5050
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.connect((host, port))
    print("what do you want to say")
    print()
    message = input(">>>")
    server.send(message.encode('utf-8'))
    reply = server.recv(1024).decode('utf-8')
    print(reply)