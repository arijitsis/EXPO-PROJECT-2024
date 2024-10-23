import cv2
import time
import handDetector as csl
from gestureDetector import gesture_Detection 


def main():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Camera could not be opened...")
        return
    
    detector = csl.handDetector()
    print("To quit: click on the window and press 'q'")
    
    while True:
        t1 = time.time()
        
        _, img = cap.read()
        # img = img.resize((600, 600))
        img = detector.findHands(img)
        lm_list = detector.findPosition(img)

        if len(lm_list) != 0:
            gesture_Detection(img, lm_list)
            
        t2 = time.time()
        fps = 1 / (t2 - t1)
        color = (0, 255, 0) if fps > 10 else (0, 0, 255)
        cv2.putText(img, str(int(fps)), (550,70), cv2.FONT_HERSHEY_PLAIN, 3,
                    color, 3)
            
        cv2.imshow("Hand Detection", img)
        if cv2.waitKey(1) == ord('q'):
            print("quitting now...")
            break
    
    # cleanup 
    cap.release()
    cv2.destroyAllWindows()
    return 


if __name__ == "__main__":
    main()
    
    