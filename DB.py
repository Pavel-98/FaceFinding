import os
import pickle

from Record import Record

path = 'DB.file'
db = {}#{"КПС-1": ["КПС-12022-06-0421:37:14:303836Camera.record"],
      #"KPS-2": ['KPS-22022-06-0421:37:14:303836Camera.record']}


def Exist(path):
    return os.path.exists(path)

def CreateDB():
    CreateFile(path, db)

def CheckDB():
    if not Exist(path):
        CreateDB()

def GetByteData(data):
    return pickle.dumps(data)

def GetObjectData(byteData):
    return pickle.loads(byteData)

def CreateFile(path, data ):
    file = open(path, 'wb')
    bytes = GetByteData(data)
    pickle.dump(bytes, file)
    file.close()

def ReadFile(path):
    if Exist(path):
        file = open(path, 'rb')
        bytes = pickle.load(file)
        file.close()
        return GetObjectData(bytes)

def GetRecordsPath(id):
    if id in db.keys():
        return db[id]

def GetRecords(id):
    records = []
    recordsPath = GetRecordsPath(id)
    for path in recordsPath:
        record = ReadFile(path)
        records.append(record)
    return records

def SaveBase():
    CreateFile(path, db)
    LoadBase()

def LoadBase():
    global db
    CheckDB()
    db = ReadFile(path)
    return






