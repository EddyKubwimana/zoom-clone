import socket
import numpy as np
import pandas

while True:
    host = '172.16.2.42'
    port = 5090
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
        id.append(id)
        name.append(name1)
        course.append(course)
        print("Don't you want to add another student, if yes, tap y otherwise press any key")
        option = input()
        if option.lower() == 'y':
            b = False
        else:
            continue
    pd = pandas
    pd["id"] = np.array(id)
    pd["name"] = np.array(name)
    pd["course"] = np.array(course)
    server.send(pd.encode('utf-8'))
    reply = server.recv(1024).decode('utf-8')
    print(reply)