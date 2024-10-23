import cv2
import math
import pyautogui 
from time import sleep  

from threading import Thread

def gesture_Detection(img, lm_list):    
    seeking_gesture(img, lm_list)
    scrolling_gesture(img, lm_list)
    pause_gesture(img, lm_list)
    

# function that handles logic for detecting seeking gestures
# for seeking 10 seconds forward or 10 seconds back 
def seeking_gesture(img, lm_list, ):
    # y-coords of landmarks of index finger
    ind_x1, ind_y1 = lm_list[8].cx, lm_list[8].cy
    ind_x2, ind_y2 = lm_list[7].cx, lm_list[7].cy
    ind_x3, ind_y3 = lm_list[6].cx, lm_list[6].cy
    ind_x4, ind_y4 = lm_list[5].cx, lm_list[5].cy
    
    if all(is_fingers_folded_vertically(lm_list, 8, 12, 16, 20)):
        return img
    
    # x-y coords of landmarks of thumb finger               
    tb_x1, tb_y1 = lm_list[4].cx, lm_list[4].cy
    tb_x2, tb_y2 = lm_list[3].cx, lm_list[3].cy
    tb_x3, tb_y3 = lm_list[2].cx, lm_list[2].cy
    tb_x4, tb_y4 = lm_list[1].cx, lm_list[1].cy
    
    # checks if the landmarks on the index finger lie on a (relativly) straight line horizontally
    is_indexFinger_level = is_difference_less_than(15, ind_y1, ind_y2, ind_y3, ind_y4)
    is_indexFinger_facing_left = ind_x1 > ind_x2 > ind_x3 > ind_x4
    is_indexFinger_facing_right = ind_x1 < ind_x2 < ind_x3 < ind_x4
    
    
    # checks if the landmarks on the thumb are:
    thumb_is_standing = tb_y1 < tb_y2 < tb_y3 < tb_y4
    thumb_is_facing_left = tb_x1 > tb_x2 > tb_x3 > tb_x4 
    thumb_is_facing_right = tb_x1 < tb_x2 < tb_x3 < tb_x4  

    if thumb_is_standing:
        if thumb_is_facing_right and is_indexFinger_level and is_indexFinger_facing_right:
            cv2.putText(img, "Forward", (100, 70), cv2.FONT_HERSHEY_PLAIN,
                        3, (0, 0, 0), 3)
            press("right", 1, no_of_presses=2)
            
            
        if thumb_is_facing_left and is_indexFinger_level and is_indexFinger_facing_left:
            cv2.putText(img, "Backward", (100, 70), cv2.FONT_HERSHEY_PLAIN,
                        3, (0, 0, 0), 3)
            press("left", 1, no_of_presses=2)
        
    return img
    
 
 
# function that handles logic for detecting scrolling gestures
# for scrolling up or down     
def scrolling_gesture(img, lm_list):
    finger_fold_status = is_fingers_folded_vertically(lm_list,  12, 16, 20)            # to check if 3 fingers are folded-
    is_horizontally_straight = False                                        # -vertically, not horizontally
    
   # check if the fingertips of the index and ring finger are level
    if is_difference_less_than(15, lm_list[8].cy, lm_list[16].cy):
        is_horizontally_straight = True
    
    if is_horizontally_straight:
                                            
        # check if all the fingers are folded  
        if all(finger_fold_status):
            cv2.putText(img, "Scroll Down", (100, 70), cv2.FONT_HERSHEY_PLAIN,
                        3, (0, 0, 0), 3)
            scroll(-100)
        # checks if any of the fingers are not folded
        if not any(finger_fold_status):
            cv2.putText(img, "Scroll Up", (100, 70), cv2.FONT_HERSHEY_PLAIN,
                        3, (0, 0, 0), 3)
            scroll(100)
            
    return img

# function that handles logic for detecting pause/unpause gestures
# for pauseing/unpausing
paused = False
def pause_gesture(img, lm_list):
    global paused
    thumb_tip = lm_list[4].cx, lm_list[4].cy
    index_tip = lm_list[8].cx, lm_list[8].cy
    
    dist = int(math.dist(thumb_tip, index_tip))
    if dist < 30 and all(is_fingers_folded_vertically(lm_list, 12, 16, 20)):
        if paused:
            cv2.putText(img, "UnPause", (100, 70), cv2.FONT_HERSHEY_PLAIN,
                            3, (0, 0, 0), 3)
            paused = False
        else:
            cv2.putText(img, "Pause", (100, 70), cv2.FONT_HERSHEY_PLAIN,
                        3, (0, 0, 0), 3)
            paused = True
        
        press("space", sleep_for=1)
        # Thread(target=press, args=("space", 1, )).start()
    return img


def is_difference_less_than(val_to_compare: float, *vals: list[float]) -> bool:
    for i in range(len(vals) - 1):
        if abs(vals[i] - vals[i + 1]) >= val_to_compare:
            return False
    return True


def is_fingers_folded_vertically(lm_list, *indexes) -> list[bool]:
    
    finger_folded = []
    for finger_tip in indexes: 
        y1 = lm_list[finger_tip].cy  # y-coords of fingertip
        y2 = lm_list[finger_tip-3].cy # y-coords of FINGER_MCP landmark 
        
        # check if the fingertip is higher than FINGER_MCP landmark,     
        if y1 > y2: 
            finger_folded.append(True)
        else:
            finger_folded.append(False)

    return finger_folded

def press(key, sleep_for, no_of_presses=1):
    pyautogui.press(key, no_of_presses)
    sleep(sleep_for)
    
def scroll(clicks):
    pyautogui.scroll(clicks)
