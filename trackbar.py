import cv2
import numpy as np

def callback(x):
    pass

def hand_mask(height, width):
    cap = cv2.VideoCapture(0)
    cv2.namedWindow('image')

    # inital values which works for my skin colour
    ilowH = 1
    ihighH = 15
    ilowS = 40
    ihighS = 255
    ilowV = 0
    ihighV = 255

    # create trackbars for color change
    cv2.createTrackbar('lowH','image',ilowH,179,callback)
    cv2.createTrackbar('highH','image',ihighH,179,callback)

    cv2.createTrackbar('lowS','image',ilowS,255,callback)
    cv2.createTrackbar('highS','image',ihighS,255,callback)

    cv2.createTrackbar('lowV','image',ilowV,255,callback)
    cv2.createTrackbar('highV','image',ihighV,255,callback)

    while True:
        ret, frame = cap.read()
        frame = cv2.flip(frame, 1) # mirror image
        hand = frame[height//4:height//4*3,width//3*2:width]
        cv2.rectangle(frame, (width//3*2,height//4), (width,height//4*3), (0, 0, 255), 2)
        hsv = cv2.cvtColor(hand, cv2.COLOR_BGR2HSV)
        ilowH = cv2.getTrackbarPos('lowH', 'image')
        ihighH = cv2.getTrackbarPos('highH', 'image')
        ilowS = cv2.getTrackbarPos('lowS', 'image')
        ihighS = cv2.getTrackbarPos('highS', 'image')
        ilowV = cv2.getTrackbarPos('lowV', 'image')
        ihighV = cv2.getTrackbarPos('highV', 'image')
        lower_hsv = np.array([ilowH, ilowS, ilowV])
        higher_hsv = np.array([ihighH, ihighS, ihighV])
        mask = cv2.inRange(hsv, lower_hsv, higher_hsv)
        cv2.imshow('mask', mask)
        cv2.imshow('image', cv2.resize(frame, (640, 480)))
        if(cv2.waitKey(1) & 0xFF == ord('q')):
            break

    cv2.destroyAllWindows()
    return lower_hsv, higher_hsv
