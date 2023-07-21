import tkinter
from tkinter import Label

from PIL import ImageTk
from PIL import Image

import DB

records = []
recordLabels = []
recordNumber = 2

class RecordApp:

    def __init__(self):
        self.app = self.GetRecordsApp()
        self.scrollbar = None
        self.columnCount = 1
        self.checked = self.GetOptions()
        self.nextButton = self.GetNextButton()
        self.previousButton = self.GetPreviousButton()
        self.AddRecords(0)

    def GetNextButton(self):
        nextButton = tkinter.Button(self.app, command=lambda: self.ShowRecord(1), text="Наступний")
        nextButton.grid(row=1, column=3, sticky='E')
        return nextButton

    def GetPreviousButton(self):
        nextButton = tkinter.Button(self.app, command=lambda: self.ShowRecord(-1), text="Попередній")##
        nextButton.grid(row=1, column=1, sticky='W')
        return nextButton

    def GetRecordsApp(self):
        recordApp = tkinter.Toplevel()
        recordApp.title("Записи")
        return recordApp

    def GetOptions(self):
        self.columnCount += 1
        pathList = list(DB.db.keys())
        startValue = tkinter.StringVar()
        if not len(pathList):
            pathList.append('')
        startValue.set(pathList[0])
        itemsList = tkinter.OptionMenu(self.app, startValue, *pathList, command=self.AddRecords)
        itemsList.grid(row=1, column=self.columnCount)#, sticky='W')
        return startValue

    def AddRecords(self, args):
        global recordNumber, records
        records = []
        recordNumber = -1
        id = self.checked.get()
        if id == '':
            return
        self.FindRecords(id)
        self.ShowRecord(1)

    def ShowRecord(self, i):
        global recordNumber
        if self.checked.get() == '':
            return
        self.DeleteRecords()
        record = records[recordNumber]
        self.CreateRecordLabel(record)
        self.NextNumber(i)

    def NextNumber(self, i):
        global recordNumber
        recordNumber += 1
        if recordNumber == len(records):
            recordNumber = 0
        elif recordNumber < 0:
            recordNumber = len(records)-1

    def FindRecords(self, id):
        self.DeleteRecords()
        recordsPath = DB.db[id]
        for recordPath in recordsPath:
            record = DB.ReadFile(recordPath)
            records.append(record)



    def AppendRecord(self, recordPath, number=3):
        record = DB.ReadFile(recordPath)
        self.CreateRecordLabel(record, number)

    def CreateRecordLabel(self, record, number=3):
        global recordLabels
        image = ImageTk.PhotoImage(Image.fromarray(record.image))
        labelImage = tkinter.Label(self.app)
        labelImage.configure(image=image)
        labelImage.image=image
        labelImage.grid(row=number, column=1)
        labelData = Label(self.app, text="Дата: \n " + str(record.date)[:19])
        labelData.grid(row=number, column=2)
        labelCamera = Label(self.app, text="Джерело: \n " + str(record.camera))
        labelCamera.grid(row=number, column=3)
        recordLabels = [labelImage, labelData, labelCamera]

    def DeleteRecords(self):
        records = []
        for label in recordLabels:
                label.destroy()





