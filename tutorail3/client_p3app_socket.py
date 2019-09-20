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

def receive_message():
    print('Socket now listening')
    try:
        data = b""
        payload_size = struct.calcsize(">L")
        print("payload_size: {}".format(payload_size))
        while True:
            while len(data) < payload_size:
                print("Client Recv: {}".format(len(data)))
                data += client_socket.recv(4096)


            print("Client Done Recv: {}".format(len(data)))
            packed_msg_size = data[:payload_size]
            data = data[payload_size:]
            msg_size = struct.unpack(">L", packed_msg_size)[0]
            print("msg_size: {}".format(msg_size))
            while len(data) < msg_size:
                data += client_socket.recv(4096)
                print('data len:', len(data))
            frame_data = data[:msg_size]
            data = data[msg_size:]

            frame = pickle.loads(frame_data, fix_imports=True, encoding="bytes")
            frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)
            print('show image')
            cv2.imwrite('/Users/suksomboon/Desktop/photo/Img_server.jpg', frame)
            cv2.waitKey(1000)

            client_socket.close()
    finally:
        print('closing socket')
        client_socket.close()


