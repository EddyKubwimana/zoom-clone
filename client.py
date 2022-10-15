import socket
import numpy as np
import pandas
import pickle

while True:
    host = '172.16.2.42'
    port = 5070
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.connect((host, port))
    print("enter the name of student who came in class")
    b = True
    id = []
    name = []
    course = []
    while b is True:
        id1 = input('enter the Id of the student')
        name1 = input( "enter the name of the student")
        course1 = input( "enter the name course a student has taken")
        id.append(id1)
        name.append(name1)
        course.append(course1)
        print("Don't you want to add another student, if yes, tap y otherwise press any key")
        option = input()
        if option.lower() == 'y':
            b = False
        else:
            print("continue enter the name")
    table = pandas.DataFrame({"id": id,"name": name, "course": course})
    my_bytes = pickle.dumps(table, protocol=4)
    server.send(my_bytes)
    reply = server.recv(1024).decode('utf-8')
    print(reply)