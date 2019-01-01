import cv2
import numpy as np
from trackbar import *
from processimage import *
from controls import *

# Usage: run main.py
# 0 fingers to drag mouse or move arrow keys (change mode)
# 1 finger to single click or press space bar if within center circle (change mode)
# 2 fingers to double click
# 3 fingers to mouse scroll
# 4 fingers to change modes (mouse control or keyboard control)
# 5 fingers to move mouse
# Press ESC to exit
# Note: all movement determined relative to green joystick origin position

def main():
    hand_hist_created = False
    cap = cv2.VideoCapture(0)
    width = int(cap.get(3))
    height = int(cap.get(4))
    key_mode = False # False for mouse, True for keyboard
    task_done = [False, False, False] # single click/space bar, double click and switch mode
    print("place hand in rectangle")

    while cap.isOpened():
        pressed_key = cv2.waitKey(1)
        ret, frame = cap.read()
        frame = cv2.flip(frame, 1) # mirror image

        if hand_hist_created:
            cv2.rectangle(frame, (width//3*2,height//4), (width,height//4*3), (0, 0, 255), 2)
            hand = frame[height//4:height//4*3,width//3*2:width]
            output, fingers, dx, dy = image_opr(hand, lower_hsv, higher_hsv)
            task_done, key_mode = controls(fingers, dx, dy, task_done, key_mode)
            cv2.imshow("Hand ROI", cv2.resize(output, (640, 480)))

        else:
            print("use trackbars to configure mask")
            print("press q when done")
            lower_hsv, higher_hsv = hand_mask(height, width)
            print(lower_hsv)
            print(higher_hsv)
            hand_hist_created = True

        # cv2.imshow("Live Feed", cv2.resize(frame, (640, 480)))

        if pressed_key == 27: # esc key presss
            break

    cv2.destroyAllWindows()
    cap.release()


if __name__ == '__main__':
    main()
