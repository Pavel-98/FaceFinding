import pickle
import face_recognition
#from socket import socket
import socket
import tkinter
from threading import Thread

import cv2
import numpy
from PIL import Image, ImageTk

from App import AddItem, DeleteItem, app, db, width, height
from DB import GetByteData, GetObjectData
from Program import Connection

host = '192.168.0.103'
port = 4321
front_face_path = 'data\\haarcascade_frontalface_alt2.xml'#'data\\haarcascade_frontalface_default.xml'
size = 921762
cascade = cv2.CascadeClassifier(front_face_path)
enc1 = None
enc2 = None
clientsFrames = {}
frames = []
id = 0
limit = 2
connections = []
connectionNumber = 0
camera = str(socket.gethostname())

def GetClient():
    s = socket.socket(socket.AF_INET,
                      socket.SOCK_STREAM)


    s.connect((host, port))
    s.send(GetByteData(camera))
    s.recv(1)
    return s

def GetServer():
    s = socket.socket(socket.AF_INET,
                      socket.SOCK_STREAM)

    s.bind(('', port))
    #app.mainloop()
    return s

def StartSend():
    s = GetClient()
    c = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    while True:
        o, frame = c.read()
        info = pickle.dumps(frame)
        s.send(info)
        go = s.recv(1)
        while not go:
            go = s.recv(1)

def StartThread(c, id):
    thread = Thread(target=WorkWithClient, args=(c, id))
    thread.start()

def Receive():
    global id
    s = GetServer()
    s.listen(1)
    while True:
        c, o = s.accept()
        tryConnect (c)

def  tryConnect(c):
    global id
    if id < limit:
        cameraId = GetObjectData(c.recv(50))
        c.send(b'1')
        StartThread(c, cameraId)
        id += 1
    else:
       c.send(b'2')
       c.close()

'''def Show(frame, fields):
    FindFace(frame)#s[id])
    imag = ImageTk.PhotoImage(Image.fromarray(frame))#s[id]))
    fields['image'].configure(image=imag)
    fields['image'].image = imag

def UpdateImage(c, fields):
    frame = []
    id = clientsFrames[c]
    frames.append(frame)
    #Thread(target=FindFace, args=(id,)).start()
    while True:
        info = c.recv(size)
        length = len(info)
        if length != size:
            c.send(b'2')
            continue
        try:
            frame = pickle.loads(info)
            #frames[id] = frame
            Show(frame, fields)
        except Exception as e:
            print(e)
            Exit(c, fields)
        c.send(b'2' )
        if cv2.waitKey(20) & 0xff == ord('q'):
            Exit(c, fields)
            break'''




def WorkWithClient(c, id):
    global connectionNumber
    fields = AddItem()
    connection = Connection(c, fields, id)
    connections.append(connection)
    connectionNumber += 1
    connection.StartWork()








