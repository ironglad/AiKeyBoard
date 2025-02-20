from asyncio import sleep
import cv2
import cvzone
from cvzone.HandTrackingModule import HandDetector
from time import  sleep
from pynput.keyboard import Controller

cap=cv2.VideoCapture(0)
cap.set(3,1280)
cap.set(4,720)

detector=HandDetector(detectionCon=1)
keys=[["Q","W","E","R","T","Y","U","I","O","P"],
     ["A","S","D","F","G","H","J","K","L",";"],
     ["Z","X","C","V","B","N","M",",",".","/"] ]
finalText=""
Keyboard=Controller()

def drawAll(img,buttonList):
    for button in buttonList:
        x, y =button.pos
        w, h =button.size
        cvzone.cornerRect(img, (x, y, w, h), rt=0)
        cv2.rectangle(img,button.pos, (x + w, y + h), (255, 0, 255), cv2.FILLED)
        cv2.putText(img, button.text, (x + 15, y + 60),
                    cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)
    return img


class Button():
    def __init__(self,pos,text,size=[85,85]):
        self.pos=pos
        self.size=size
        self.text=text




buttonList=[]
for i in range(len(keys)):
    for j, key in enumerate(keys[i]):
        buttonList.append(Button([100 * j + 50, 100 * i + 50], key))


while True:
    success,img=cap.read()
    img=detector.findHands(img)
    lmList,bboxInfo=detector.findPosition(img)
    img= drawAll(img, buttonList)

    if lmList:
        for button in buttonList:
            x,y=button.pos
            w,h=button.size

            if x<lmList[8][0]<x+w and y<lmList[8][1]<y+h:
                cv2.rectangle(img,(x-5,y-5), (x + w+5, y + h+5), (175, 0, 175), cv2.FILLED)
                cv2.putText(img, button.text, (x + 15, y + 60),
                            cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)

                l, _, _ = detector.findDistance(8, 12, img,draw=False)
                print(l)
                ## when clicked
                if l<30:
                    Keyboard.press(button.text)
                    cv2.rectangle(img, button.pos, (x + w, y + h), (0, 255, 0   ), cv2.FILLED)
                    cv2.putText(img, button.text, (x + 15, y + 60),
                                cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)

                    finalText+= button.text
                    sleep(0.15)


    # img = mybutton.draw(img)
    # img = mybutton1.draw(img)
    # img = mybutton2.draw(img)
    cv2.rectangle(img, (50,350), (700,450), (175,0,175), cv2.FILLED)
    cv2.putText(img, finalText, (60,  430),
                cv2.FONT_HERSHEY_PLAIN, 5, (255, 255, 255), 5)

    cv2.imshow("Image",img)
    cv2.waitKey(1)
