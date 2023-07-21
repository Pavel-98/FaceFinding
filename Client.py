#import cv2

from NetProgram import StartSend
'''c = cv2.VideoCapture(0)

#    1
while True:
        frame, inf = c.read()
        cv2.imshow('frame', frame)'''
text = "З'єднання закрите"
try:
    StartSend()
except Exception as e:
    print(text)