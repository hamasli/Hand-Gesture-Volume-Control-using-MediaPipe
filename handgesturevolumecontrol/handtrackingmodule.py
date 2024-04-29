import cv2
import mediapipe as mp
import time

class handDetector():
    def __init__(self, mode=False, maxHands=2,model_complexity=1 ,detectionCon=0.5,trackCon=0.5):
        # static_image_mode = False,
        # max_num_hands = 2,
        # min_detection_confidence = 0.5,
        # min_tracking_confidence = 0.5
        self.mode=mode;
        self.maxHands=maxHands;
        self.model_complexity=model_complexity;
        self.detectionCon=detectionCon;
        self.trackCon=trackCon;
        self.model_complexity = 1;

        #to use hands module for hand detection.
        # mpHands = mp.solution.hands: This line imports the "hands" solution from the MediaPipe
        # library and assigns it to the variable mpHands.
        # The mp.solution.hands module provides tools and functions for hand tracking using the MediaPipe framework.
        #
        # hands = mpHands.Hands():
        # This line creates an instance of the Hands class from the mpHands module. The Hands class is responsible
        # for performing hand tracking using the pre-trained hand tracking model provided by MediaPipe.
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands, self.model_complexity, self.detectionCon,
                                        self.trackCon);
        self.mpDraw = mp.solutions.drawing_utils

    def findHands(self,image,draw=True):
        #the handwritten above class and instances only works on RGB image
        imgRGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB);
        self.results = self.hands.process(imgRGB);
        # print(results); #this just show some results to check it detects something or not then
        # print(results.multi_hand_landmarks);
        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(image, handLms, self.mpHands.HAND_CONNECTIONS);
        return image;

    def findPosition(self,image,handNo=0,draw=True):
        lmList=[];
        #here we are picking hand whose id =1 and show his landmarks
        if self.results.multi_hand_landmarks:
            myHand=self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(myHand.landmark):
                # here we will get x,y coordinates in decimalpoints but we need in pixels
                # print(id,lm);
                h, w, c = image.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                #print(id, cx, cy);
                lmList.append([id,cx,cy])
                if draw:
                    cv2.circle(image, (cx, cy), 8, (255, 0, 255), cv2.FILLED)

                # # using above landmarks coordinates drawing the circle around landmark whose id=0
                # if id == 0:
                #     cv2.circle(image, (cx, cy), 30, (255, 255, 0), cv2.FILLED)
            # here we use simple bg image not rgb
        # each handlms contain id and landmarks position x and y coordiantes for object location

        return lmList;




def main():
    lmList = [];
    pTime = 0;
    cTime = 0;
    cap = cv2.VideoCapture(0);
    detector=handDetector();
    while True:
        success, image = cap.read();
        image=detector.findHands(image);
        lmList=detector.findPosition(image);
        if len(lmList)!=0:
            print(lmList[4]);
        cTime = time.time();
        fps = 1 / (cTime - pTime);
        pTime = cTime;
        # this code will display fps on per second on image
        cv2.putText(image, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN,
                    3, (255, 0, 255), 3)

        cv2.imshow("image", image);
        cv2.waitKey(1);


if __name__ == "__main__":
    main()
