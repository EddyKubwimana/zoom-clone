# This is server code to send video (over UDP) and message frames (over TCP)

import cv2, imutils, socket
import numpy as np
import time
import base64
import threading, wave, pyaudio, pickle, struct
import sys
import queue
import os

# For details visit pyshine.com
q = queue.Queue(maxsize=10)

BUFF_SIZE = 65536
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, BUFF_SIZE)
host_ip = '172.16.8.70'  # socket.gethostbyname(host_name)
print(host_ip)
port = 9699
socket_address = (host_ip, port)
server_socket.bind(socket_address)
print('Listening at:', socket_address)
vid = cv2.VideoCapture(0)


def generate_video():
    WIDTH = 400
    while True:
        try:
            _, frame = vid.read()
            frame = imutils.resize(frame, width=WIDTH)
            q.put(frame)
        except:
            os._exit(1)
    print('Player closed')
    BREAK = True
    vid.release()


def send_video():
    fps, st, frames_to_count, cnt = (0, 0, 1, 0)
    cv2.namedWindow('TRANSMITTING VIDEO')
    cv2.moveWindow('TRANSMITTING VIDEO', 10, 30)
    while True:
        msg, client_addr = server_socket.recvfrom(BUFF_SIZE)
        print('GOT connection from ', client_addr)
        WIDTH = 400
        while (True):
            frame = q.get()
            encoded, buffer = cv2.imencode('.jpeg', frame, [cv2.IMWRITE_JPEG_QUALITY, 80])
            message = base64.b64encode(buffer)
            server_socket.sendto(message, client_addr)
            frame = cv2.putText(frame, 'FPS: ' + str(round(fps, 1)), (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7,
                                (0, 0, 255), 2)

            cv2.imshow('TRANSMITTING VIDEO', frame)
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                os._exit(1)
                TS = False
                break


def send_message():
    s = socket.socket()
    s.bind((host_ip, (port - 1)))
    s.listen(5)
    client_socket, addr = s.accept()
    cnt = 0
    while True:
        if client_socket:
            while True:
                print('SERVER TEXT SENDING:')
                data = input()
                a = pickle.dumps(data)
                message = struct.pack("Q", len(a)) + a
                client_socket.sendall(message)

                cnt += 1


def get_message():
    s = socket.socket()
    s.bind((host_ip, (port - 2)))
    s.listen(5)
    client_socket, addr = s.accept()
    data = b""
    payload_size = struct.calcsize("Q")

    while True:
        try:
            while len(data) < payload_size:
                packet = client_socket.recv(4 * 1024)  # 4K
                if not packet: break
                data += packet
            packed_msg_size = data[:payload_size]
            data = data[payload_size:]
            msg_size = struct.unpack("Q", packed_msg_size)[0]
            while len(data) < msg_size:
                data += client_socket.recv(4 * 1024)
            frame_data = data[:msg_size]
            data = data[msg_size:]
            frame = pickle.loads(frame_data)
            print('', end='\n')
            print('CLIENT TEXT RECEIVED:', frame, end='\n')
            print('SERVER TEXT SENDING:')


        except Exception as e:
            print(e)
            pass
t1 = threading.Thread(target=send_message, args=())
t2 = threading.Thread(target=get_message, args=())
t3 = threading.Thread(target=generate_video, args=())
t4 = threading.Thread(target=send_video, args=())
t1.start()
t2.start()
t3.start()
t4.start()

