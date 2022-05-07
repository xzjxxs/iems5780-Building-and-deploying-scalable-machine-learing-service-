# 1155161089 XUZijun
# server.py
# Deploying the Model as the Server Program

import io
import cv2
import base64
import socket
import numpy as np
from PIL import Image
from queue import Queue
from threading import Thread
from tensorflow.keras.models import load_model

q = Queue()
client_socket = None


# Listen for incoming connection
def thread1():
    global client_socket
    # create an INET socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # bind the socket to the host and a port
    server_socket.bind(("0.0.0.0", 8080))
    # Listen for incoming connections from clients
    server_socket.listen(10)

    while True:
        # accept connections from outside
        (client_socket, address) = server_socket.accept()
        # Read data from client and send it back
        data = client_socket.recv(1024000)
        q.put(data)


# Receive data from client, decode message, and feed image into neural network
def thread2():
    convert_d = {"Asian Brown Flycatcher": 0,
                 "Blue Rock Thrush": 1,
                 "Brown Shrike": 2,
                 "Grey-faced Buzzard": 3}

    def grayscale(img):
        if img.shape[-1] == 3:
            grayimg = np.zeros((256, 256, 1))
            grayimg[:, :, 0] = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
            return grayimg
        else:
            return img.reshape(256, 256, 1)
    model = load_model("bird_model/bird_model.h5")
    
    while True:
        message = q.get()
        try:
            img = Image.open(io.BytesIO(message))
            img = img.resize((256, 256), resample=Image.NEAREST)
            img_array = np.array(img)
            k1 = np.zeros((1, 256, 256, 1))
            k1[0] = grayscale(img_array)
            predict = model.predict(k1)
            m = list()
            for i, k in enumerate(convert_d.keys()):
                m.append("{}%: {}".format(round(predict[0][i] * 100, 2), k))
            client_socket.sendall("\n".join(m).encode("UTF-8"))
            print("\n".join(m))
        except Exception as e:
            print(e)
            client_socket.sendall("The url may be not an image!".encode("UTF-8"))


threads = list()

tcpThread = Thread(target=thread1)
tcpThread.start()
threads.append(tcpThread)

cnnThread = Thread(target=thread2)
cnnThread.start()
threads.append(cnnThread)
