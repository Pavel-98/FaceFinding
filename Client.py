#import cv2

from NetProgram import StartSend

text = "З'єднання закрите"
try:
    StartSend()
except Exception as e:
    print(text)