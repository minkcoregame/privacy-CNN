import cv2
import socket
import struct
import pickle

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('127.0.0.1', 1234))
connection = client_socket.makefile('wb')

def send_img(Img):


    print("Img:", Img)

    cam = cv2.imread('/Users/suksomboon/Desktop/photo/nikola-tesla.jpg', 0)

    img_counter = 0

    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
    flag = True
    while (img_counter < 1):
        frame = cam
        result, frame = cv2.imencode('.jpg', frame, encode_param)
        data = pickle.dumps(frame, 0)
        size = len(data)

        print("{}: {}".format(img_counter, size))
        client_socket.sendall(struct.pack(">L", size) + data)
        print("Sent image complete")
        img_counter += 1

        client_socket.close()
