import pickle
from datetime import datetime
from threading import Thread
from tkinter import Button

import App

import DB
import cv2
import face_recognition
from PIL import ImageTk
from PIL import Image

import NetProgram
from App import db, app
from Record import Record


path = 'Records\\'

def StringToPath(string):
    chars = ['\n', '\'', '\"', ' ', ':', '.']
    result = string
    for char in chars:
        result = result.replace(char, '')
    return result

class Connection:

    def __init__(self, c, fields, camera):
        self.c = c
        self.fields = fields
        self.camera = camera
        self.imageField = fields['image']
        self.SetDeleteButton()
        self.image = []
        self.size = 921762
        self.updated = b'1'
        self.rectangles = []
        self.canUpdateRectangles = True
        self.front_face_path = 'data\\haarcascade_frontalface_alt2.xml'
        self.cascade = cv2.cv2.CascadeClassifier(self.front_face_path)
        self.requiredFaces = []
        self.thread = Thread(target=self.UpdateRectangles)


    def SetDeleteButton(self):
        if self.fields:
            button = Button(app, text="Видалити: "+self.camera, command=lambda: self.Exit())
            self.fields['delete'] = button
            row = self.fields['row']
            button.grid(row=row, column=2)

    def StartWork(self):
        while True:
            try:
                info = self.Recv()
                self.UpdateImage(info)
                self.Send()
            except Exception as e:
                self.Exit()
                break

    def Recv(self):
        bytes = self.c.recv(self.size)
        return bytes

    def Send(self):
        self.c.send(self.updated)

    def UpdateImage(self, info):
        image = self.GetImage(info)
        if image is None :
            return
        self.SetImage(image)

    def GetImage(self, info):
        try:
            self.image = pickle.loads(info)
            return self.image
        except Exception as e:
            print(e)
            return None

    def SetImage(self, image):#
        if not self.thread.is_alive() and self.canUpdateRectangles:
            self.thread = Thread(target=self.UpdateRectangles)
            self.thread.start()
        self.SetRectangles()
        newImage = self.GetTk(image)
        self.imageField.configure(image=newImage)
        self.imageField.image = newImage

    def GetTk(self, frame):
        return ImageTk.PhotoImage(Image.fromarray(self.image))

    def UpdateRectangles(self):
        self.canUpdateRectangles = False
        faces = self.FindFaces()
        self.requiredFaces = self.CheckFaces(faces)
        self.canUpdateRectangles = True
        #self.SetRectangles()

    def FindFaces(self):
        faces = face_recognition.face_locations(self.image)
        return faces

    def CheckFaces(self, faces):
        requiredFaces = []
        for x, y, w, h in faces:
            faceInfo = [h, x, y-h, w-x]
            face = self.image[x:w, h:y]
            if self.BeInBase(face, [x, w, h, y]):
                requiredFaces.append(faceInfo)
        return requiredFaces

    def BeInBase(self, face, array):
        faceEnc = self.GetEnc(face)
        if not App.allowed:
            return False
        base = App.db
        keys = base.keys()
        if faceEnc is None:
            return
        for id in keys:
            face = base[id]['faceEncoding']
            if self.CompareFaces(face, faceEnc):
                self.LogInfo(base[id]['name'], array, self.camera)
                return True
        return False

    def CompareFaces(self, baseFace, newFace):
        return face_recognition.compare_faces([newFace], baseFace)[0]

    def SetRectangles(self):
        length = 2
        color = (255, 0, 0)
        for x, y, w, h in self.requiredFaces:
            cv2.rectangle(self.image, (x, y), (x + w, y + h), color, length)
        self.requiredFaces =[]

    def GetEnc(self, faceInfo):  #
        encoding = face_recognition.face_encodings(faceInfo)
        if not len(encoding):
            return None
        return encoding[0]

    def LogInfo(self, face, array, camera):
        global path
        name = face
        if not self.CheckTime(name):
            return
        time = datetime.now()
        filePath = StringToPath(path + name + str(time) + camera) + '.record'
        x= array[2]
        y = array[0]
        w = array[3]-array[2]
        h = array[1] - array[0]
        newImage = self.image.copy()
        cv2.rectangle(newImage, (x, y), (x+w, y+h), (255, 0, 0), 2)
        record = Record(newImage , time, camera)
        DB.CreateFile(filePath, record)
        self.AppendFileToDB(name, filePath)


    def AppendFileToDB(self, name, path):
        if name not in DB.db.keys():
            DB.db[name] = []
        DB.db[name].append(path)
        DB.SaveBase()

    def CheckTime(self, name):
        if not name in DB.db.keys() or len(DB.db[name]) < 2:
            return True
        path = DB.db[name][-1]
        record = DB.ReadFile(path)
        if self.CanAdd(record.date):
            return True
        return False

    def CanAdd(self, time):
        day = time.day
        hour = time.hour
        now = datetime.now()
        dayNow = now.day
        hourNow = now.hour
        if dayNow == day and hourNow - hour  < 2:
            return False
        return True

    def Exit(self):
        NetProgram.id -= 1
        self.c.close()
        for key in self.fields.keys():
            try:
                self.fields[key].destroy()
            except Exception as e:
                print(e)




