import cv2;
import mediapipe as mp;
import numpy as np;
import time
import handtrackingmodule as htm
import math
from comtypes import CLSCTX_ALL;
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume;




###################################
wCam,hCam=640,480;
volume=0;


###################################
cap=cv2.VideoCapture(0);


devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = interface.QueryInterface(IAudioEndpointVolume)
#volume.GetMute()
# volume.GetMasterVolumeLevel()
# total range is -65 to 0 0 is full
#through this we will get the total range of our volume
# print(volume.GetVolumeRange());
#volrange return the array of [-65,0]
volRange=volume.GetVolumeRange();
# volume.SetMasterVolumeLevel(0, None);
minVol=volRange[0];
maxVol=volRange[1];









cap.set(3,wCam);
cap.set(4,hCam);
pTime=0;
cTime=1;
detector=htm.handDetector();
while True:
    success,img=cap.read();
    img=detector.findHands(img);
    lmList=detector.findPosition(img,draw=False);
    if len(lmList)!=0:
        # print(lmList[2],lmList[8]);
        x1, y1=lmList[4][1],lmList[4][2];
        x2, y2 = lmList[8][1], lmList[8][2];
        cx,cy=(x1+x2)//2,(y1+y2)//2;
        cv2.circle(img,(x1,y1),15,(255,0,255),cv2.FILLED);
        cv2.circle(img, (x2, y2), 15, (255, 0, 255), cv2.FILLED);
        #for define the circle the between the two points
        cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED);
        cv2.line(img,(x1,y1),(x2,y2),(255,0,255),3);
        #for finding the length of line between two points
        # wholesquareroot(x2-x1 whole square,y2-y1 whole square,z2-z1
        length=math.hypot(x2-x1,y2-y1);
        # print(length);

        #hand range from 300 maximum mininum was 50
        #volume range -65 to 0;
        vol=np.interp(length,[50,300],[minVol,maxVol]);
        # here length parameter is of line, and then total length is 50 to 300 then we convert into 400minimum and 150 maximu.
        volBar = np.interp(length, [50, 300], [400, 150]);
        volPercentage = np.interp(length, [50, 300], [0, 100]);
        print(vol,int(length));
        volume.SetMasterVolumeLevel(vol, None);


        #if length of line less than 50 color changes
        if length<50:
            cv2.circle(img, (cx, cy), 15, (0, 255, 255), cv2.FILLED);
        #HERE WE show volume bar parameters are starting and ending position. width is 35,height is 250
        cv2.rectangle(img,(50,150),(85,400),(0,255,0));
        cv2.rectangle(img, (50, int(volBar)), (85, 400), (0, 255, 0),cv2.FILLED);
        cv2.putText(img, f'FPS:{int(volPercentage)}%', (100, 450), cv2.FONT_HERSHEY_PLAIN, 2,(0, 255, 0), 3)







    cTime=time.time();
    fps=1/(cTime-pTime);
    pTime=cTime;
    cv2.putText(img,f'FPS:{int(fps)}',(40,50),cv2.FONT_HERSHEY_PLAIN,2,(0,255,0),3)
    cv2.imshow("image",img);
    cv2.waitKey(1);
