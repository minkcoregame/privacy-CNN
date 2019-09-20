import cv2
import socket
import struct
import pickle

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('172.16.23.1', 1234))
connection = client_socket.makefile('wb')

def send_img(Img):


    print("Img:", Img)

    cam = cv2.imread(Img, 0)

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
    data = b""
    payload_size = struct.calcsize(">L")
    print("payload_size: {}".format(payload_size))

    print('Socket now listening')
    predict_result_filename = 'predict_result.txt'
    f = open(predict_result_filename, "w")
    try:
        data = b""
        payload_size = struct.calcsize(">L")
        print("payload_size: {}".format(payload_size))
        Flag = True
        while Flag:
            while len(data) < payload_size:
                print("Recv: {}".format(len(data)))
                data += client_socket.recv(4096)

            print('first data:',len(data))
            packed_msg_size = data[:payload_size]
            data = data[payload_size:]
            msg_size = struct.unpack(">L", packed_msg_size)[0]
            print("msg_size: {}".format(msg_size))

            while len(data) < 6130046-2:
                print("Client Recv: {}".format(len(data)))
                data += client_socket.recv(4096)
                print('data len:', len(data))

            f.write(f"{data},")
            f.close()


            print('Receive Encrypted IMG')
            client_socket.close()

            print('close socket')
            Flag = False


    finally:
        print('closing socket')
        client_socket.close()



