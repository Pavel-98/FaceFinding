import math
import os
import threading
import tkinter
from threading import Thread
from time import sleep
from tkinter import Tk, filedialog

import PIL
#from PIL import Image

#import PIL
#from PIL.Image import Image
import cv2
import face_recognition
import numpy
from PIL import Image, ImageTk
from PIL.ImageTk import PhotoImage

#from rogram import GetEnc
import DB
from RecordApp import RecordApp

n = 0
width = 50
height = 50
baseNumber=2
limit = 5
app = Tk()
app.title("Система")
addToBaseText = "База "
addItemText = "Додати"
deleteText = "Видалити"
addFaceText = "Додати лице "
addProfileText = "Додати профіль"
getRecordsAppText = "Записи"
db = {}
id = 0
newFace = None
newProfile = None
newNameLabel = None
base = None
dbPath = 'Base.file'
allowed = False
seconds = 0.5

def Setup():
    global n
    n += 1
    baseButton = tkinter.Button(app, command =GetBaseApp, text=addToBaseText)#
    recordsButton = tkinter.Button(app, command=GetRecordsApp, text=getRecordsAppText)
    baseButton.grid(row=n, column=1)
    recordsButton.grid(row=n, column=2)
    LoadBase()

def GetBaseApp():
    global base
    base = tkinter.Toplevel()
    base.title("Відстежування")
    GetBaseItem(base)

def AddFace(root):
    global baseNumber, db, newFace
    faceInfo = Dialog(root)
    face = faceInfo[0]
    if face:
        tkinterFace = ImageTk.PhotoImage(image=face, master=root)
        label = tkinter.Label(root, image=tkinterFace)
        label.grid(row=baseNumber, column=1)
        label.configure(image=tkinterFace)
        label.image = tkinterFace
        newFace = face

    return

def AddProfile(root):
    global baseNumber, db, newProfile
    faceInfo = Dialog(root)
    profile = faceInfo[0]
    if profile:
        tkinterProfile = ImageTk.PhotoImage(image=profile, master=root)
        label = tkinter.Label(root, image=tkinterProfile)
        label.grid(row=baseNumber, column=1)
        label.configure(image=tkinterProfile)
        label.image = tkinterProfile
        newProfile = profile
    return

def DeleteWidget(widgets):
    for widget in widgets:
        widget.destroy()

def DeleteBaseItem(id1):
    global db
    db.pop(id1)
    UpdateBase()

def GetEnc(faceInfo, w, h):

    if faceInfo is  None:
        return None
    enc1 = face_recognition.face_encodings(faceInfo)[0]
    return enc1
def UpdateBase():
    global base, newFace, newProfile, newNameLabel
    base.destroy()
    newFace = None
    newProfile = None
    SaveBase()
    LoadBase()
    GetBaseApp()
def AddToBase(root):
    global newFace, newProfile, id, newNameLabel, allowed
    allowed = False
    sleep(seconds)
    name = newNameLabel.get("1.0", "end")
    if (not (newFace or newProfile)) or name == '' or name in list(db.keys()):
        return
    faceArray = numpy.array(newFace)
    profileArray = numpy.array(newProfile)
    if not newProfile:
        profileArray = None
    if not newFace:
        faceArray = None
    try:
        faceEncoding = GetEnc(cv2.cvtColor(faceArray, cv2.COLOR_BGR2RGB), width, height)
    except:
        return
    profileEncoding = GetEnc(profileArray, width, height)
    db[name] = {'face': faceArray, 'faceEncoding': faceEncoding, 'profile': profileArray, 'profileEncoding': profileEncoding, 'name': name}
    id += 1
    UpdateBase()
    return

def CheckBase():
    if not os.path.exists(dbPath):
        SaveBase()

def LoadBase():
    global db, baseNumber, allowed
    CheckBase()
    db = DB.ReadFile(dbPath)
    baseNumber = len(list(db.keys())) + 2
    sleep(seconds)
    allowed = True

def SaveBase():
    DB.CreateFile(dbPath, db)

def GetBaseItem(root):
    global baseNumber, newNameLabel
    ShowBase(root)
    if baseNumber >= limit:
        return
    newNameLabel = tkinter.Text(root, height=1, width=10)
    newNameLabel.grid(row=baseNumber, column=1)
    faceButton = tkinter.Button(root, command=lambda: AddFace(root), text=addFaceText)
    faceButton.grid(row=baseNumber, column=2)

    addButton = tkinter.Button(root, text=addItemText, command=lambda:AddToBase(root))
    addButton.grid(row=baseNumber, column=3)
    baseNumber += 1

def AddItem():
    global n
    n += 1
    imageField = tkinter.Label(app)#\
    imageField.grid (row=n, column=1)
    return {'image': imageField, 'row': n}

def DeleteItem(fields):
    global n
    n -= 1
    for key in fields.keys():
        fields[key].destroy()

def Dialog(base):
    file_types = [('Image files', '*.jpg;*.png'), (
    'All files', '*')]
    file_name = filedialog.askopenfilename(title='Select a file', filetypes=file_types, parent=base)
    if file_name == '':
        return [None]
    return [CheckFile(file_name, base), file_name]


def CheckFile(filename, root):
    try:
        image = Image.open(filename)
        x = 100
        y = 100
        image = image.resize((x, y))
        return image
    except Exception as e:
        print(e)
        return None

def ShowBase(root):

    global db, baseNumber
    baseNumber=1
    for key in db.keys():
        image = Image.fromarray(db[key]['face'])
        if image:
            face = PhotoImage(master=root, image=image)
            labelFace = tkinter.Label(root, image=face)
            labelFace.configure(image=face)
            labelFace.image = face
            labelFace.grid(row=baseNumber, column=1)


        name = db[key]['name']
        if name:
            labelProfile = tkinter.Label(root, text=name)
            labelProfile.grid(row=baseNumber, column = 2)
        deleteButton = tkinter.Button(root, text=deleteText, command=lambda name1=name: DeleteBaseItem(name1))
        deleteButton.grid(row=baseNumber, column=3)
        baseNumber += 1



def appendRow(items, row ):
    position = 1
    for item in items:
        item.grid(row=row, column=position)
        position += 1

def GetRecordItem(root, row, record):
    dateLabel = tkinter.Label(root, text=record.date)
    imageLabel = tkinter.Label(root, image=record.image)
    cameraLabel = tkinter.Label(text=record.camera)
    items = [dateLabel, imageLabel, cameraLabel]
    appendRow(items, row)

def GetRecordsApp():
    app = RecordApp()












