import numpy as np
import matplotlib.pyplot as plt
import math
import cv2
import time


import pickle

# Local Pyfhel module
from Pyfhel import Pyfhel
from Pyfhel import PyCtxt
from Pyfhel import PyPtxt

from Pyfhel.util import ENCODING_t



# present c-obj
import contextlib

@contextlib.contextmanager
def printoptions(*args, **kwargs):
    original = np.get_printoptions()
    np.set_printoptions(*args, **kwargs)
    try:
        yield
    finally:
        np.set_printoptions(**original)

def readImage(filename):
    gray_img = cv2.imread(filename, cv2.IMREAD_GRAYSCALE)
    Imag_shape = gray_img.shape

    return gray_img, Imag_shape


def encryptImg(Img):
    Img_shape = Img.shape
    print(Img_shape)
    encImg = [[0 for j in range(Img_shape[1])] for i in range(Img_shape[0])]
    pyfhel = Pyfhel()  # Creating empty Pyfhel object
    pyfhel.contextGen(p=65537, m=1024, flagBatching=True)  # Generating context. (encrypt pixel)
    pyfhel.keyGen()  # keygeneration

    for py in range(Img_shape[0]):
        for px in range(Img_shape[1]):
            temp_pxl = Img[py, px]

            cxt_pxl = pyfhel.encryptFrac(temp_pxl)  # test floating number
            dec_pxl = pyfhel.decryptFrac(cxt_pxl)  # decrypt
            encImg[py][px] = cxt_pxl
    return encImg, pyfhel


def decryptImg(encImg,Img,pyfhel):
    ImgShape = Img.shape
    decImg = np.zeros([ImgShape[0],ImgShape[1]])
    #decImg = [[0 for j in range(ImgShape[0])] for i in range(ImgShape[1])]

    for py in range(ImgShape[0]):
        for px in range(ImgShape[1]):

            temp_pxl = encImg[py][px] # Encrypt pixel

            #print('tem_dec =',temp_pxl)
            dec_pxl = pyfhel.decryptFrac(temp_pxl)  # decrypt
            #print('decode pixel =', dec_pxl) # verify decrypt pixel
            temp_dec = float(dec_pxl)
            #print('tyep dec =',type(temp_dec))
            #print('decImg 1 =',decImg[py][px])

            decImg[py][px] = round(temp_dec)
            #print('decImg[py][px] =',decImg)
    return decImg
