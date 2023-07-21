import os
from multiprocessing import Process
from threading import Thread

import cv2

import DB
from App import app, Setup
from NetProgram import GetServer, Receive

t = Thread (target=Receive)
if __name__ == '__main__':
    t.start()
    DB.LoadBase()
    Setup()
    app.mainloop()
    while True:
        try:
            status = app.state()#
            if not status == 'normal':
                os._exit(1)

        except Exception as e:
            os._exit(1)
