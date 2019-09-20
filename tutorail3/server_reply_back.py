import socket
import sys
import cv2
import pickle
import numpy as np
import struct ## new

HOST='127.0.0.1'
PORT=1234

s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
print('Socket created')

s.bind((HOST,PORT))
print('Socket bind complete')
s.listen(10)
print('Socket now listening')

conn,addr=s.accept()

data = b""
payload_size = struct.calcsize(">L")
print("payload_size: {}".format(payload_size))

try:
    while True:
        Flag = 0
        while len(data) < payload_size:
            print("Recv: {}".format(len(data)))
            data += conn.recv(4096)

        print("Done Recv: {}".format(len(data)))
        packed_msg_size = data[:payload_size]
        data = data[payload_size:]
        msg_size = struct.unpack(">L", packed_msg_size)[0]
        print("msg_size: {}".format(msg_size))
        while len(data) < msg_size:
            data += conn.recv(4096)
            print('data len:', len(data))
        frame_data = data[:msg_size]
        data = data[msg_size:]

        frame_pickle = pickle.loads(frame_data, fix_imports=True, encoding="bytes")
        frame = cv2.imdecode(frame_pickle, cv2.IMREAD_COLOR)
        # cv2.imshow('ImageWindow',frame)
        print('show image')
        cv2.imwrite('/Users/suksomboon/Desktop/photo/Img_client.jpg', frame)
        cv2.waitKey(1000)
        Flag = 1

        # After receive data, reply with the data
        if Flag:

            new_data = cv2.imread('/Users/suksomboon/Desktop/photo/nikola-tesla.jpg', 0)


            encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
            frame = new_data
            result, frame = cv2.imencode('.jpg', frame, encode_param)
            data = pickle.dumps(frame, 0)
            size = len(data)
            conn.sendall(struct.pack(">L", size) + data)
            print("Finish sending data to client")


            conn.close()




        else:
            print('no data')
            break

finally:
    # close coonection
    conn.close()
