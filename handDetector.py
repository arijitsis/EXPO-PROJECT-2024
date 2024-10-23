import cv2
import mediapipe.python.solutions.hands as mpHands # for processing hands
import mediapipe.python.solutions.drawing_utils as mpDraw # for drawing hand landmarks 
from collections import namedtuple


class handDetector():
    def __init__(self, mode=False, maxHands=1, detectionCon=0.7, trackCon=0.7):
        self.results = None
        self.hands = mpHands.Hands(mode, maxHands, 1, detectionCon, trackCon )
        
    def findHands(self, img):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                mpDraw.draw_landmarks(img, handLms,
                    mpHands.HAND_CONNECTIONS)
        return img
    
    
    def findPosition(self, img):
        lmList = []
        landmark = namedtuple('landmark', ['id', 'cx', 'cy'])
        if self.results.multi_hand_landmarks:
            for myHand in self.results.multi_hand_landmarks:
                for id, lm in enumerate(myHand.landmark):
                    h, w, _ = img.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    lmList.append(landmark(id, cx, cy))
                    cv2.circle(img, (cx, cy), 3, (255, 0, 255), 3)
        return lmList
    