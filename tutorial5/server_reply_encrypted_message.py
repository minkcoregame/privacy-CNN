import socket
import sys
import cv2
import pickle
import numpy as np
import struct ## new

import enc_util




def Encypt_img(InFile):
    Img, ImgShape = enc_util.readImage(InFile)

    dim = (50, 50)
    small_img = cv2.resize(Img, dim, interpolation=cv2.INTER_CUBIC)

    # print('Img =', small_img)
    ImgShape = small_img.shape
    print('ImgShape =', ImgShape)

    # Test encrypt
    encImg, pyfhel = enc_util.encryptImg(small_img)

    return encImg, pyfhel



HOST='172.16.23.1'
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
        print('show image')
        img_get_filename = '/home/kalika/Hackday2/pythonCode/Img_client.jpg'
        cv2.imwrite(img_get_filename, frame)
        cv2.waitKey(1000)
        Flag = 1

        # After receive data, reply with the data
        if Flag:

            encImg, pyfhel = Encypt_img(img_get_filename) # do the encryption on the file and reply the encryption file.
            #data = pickle.dumps(encImg, 0)
            #pickle.dump(encImg, open("enc_img.pickle","wb"))
            with open('/home/kalika/Hackday2/pythonCode/encIMG.dat', 'w') as f:
                for _ in range(len(encImg)):
                    f.write(f"{encImg},")

            f = open('/home/kalika/Hackday2/pythonCode/encIMG.dat', 'rb')
            print
            'Sending...'
            l = f.read(1024)
            while (l):
                print('Sending...')
                conn.send(l)
                l = f.read(1024)
            f.close()
            print("Finish sending encrypted data to client")


        else:
            print('no data')
            break

finally:
    # close coonection
    conn.close()



