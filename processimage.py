import cv2
import numpy as np
font = cv2.FONT_HERSHEY_SIMPLEX

def max_contour(hist_mask_image):
    gray_hist_mask_image = cv2.cvtColor(hist_mask_image, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(gray_hist_mask_image, 0, 255, 0)
    _, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    max_cnt = []
    max_area = 0

    for cont in contours:
        if cv2.contourArea(cont) > max_area:
            max_cnt = cont
            max_area = cv2.contourArea(cont)

    return max_cnt


def hist_masking(frame, lower_hsv, higher_hsv):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower_hsv, higher_hsv)
    blur = cv2.GaussianBlur(mask,(5,5),0)
    ret, thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY)
    thresh = cv2.dilate(thresh, None, iterations=1)
    thresh = cv2.erode(thresh, None, iterations=2)
    thresh = cv2.merge((thresh, thresh, thresh))

    return thresh


def distance(p1, p2):
    return np.sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)


def image_opr(frame, lower_hsv, higher_hsv):
    hist_mask_image = hist_masking(frame, lower_hsv, higher_hsv)
    max_cnt = max_contour(hist_mask_image)

    farthest = 0
    finger_pts = []
    dx = 0
    dy = 0

    height, width, channels = frame.shape

    origin_x, origin_y = (int(width/2), int(height/4*3))
    joystick_x, joystick_y = origin_x, origin_y

    cv2.circle(frame, (origin_x, origin_y), 25, (0, 255, 0), 2)

    if max_cnt is not None and cv2.contourArea(max_cnt) > 10000:
        epsilon = 0.02*cv2.arcLength(max_cnt,True)
        approx = cv2.approxPolyDP(max_cnt,epsilon,True)
        cv2.drawContours(frame,[approx],-1,(255,0,0),2)

        M = cv2.moments(approx)
        if M["m00"] != 0:
            center = (int(M["m10"] / M["m00"]),int(M["m01"] / M["m00"]))
            cv2.circle(frame, center, 5, (255, 0, 0), -1)

            hull = cv2.convexHull(approx, returnPoints=False)
            defects = cv2.convexityDefects(approx, hull)

            if defects is not None:
                for i in range(defects.shape[0]):
                    s,e,f,d = defects[i,0]
                    start = tuple(approx[s][0])
                    end = tuple(approx[e][0])
                    far = tuple(approx[f][0])

                    # if distance(far, center) > farthest:
                    #     farthest = distance(far, center)

                    if distance(end, center) > 100 and end not in finger_pts and end[1] <= center[1]+distance(far, center):
                        finger_pts.append(end)
                    if distance(start, center) > 100 and start not in finger_pts and start[1] <= center[1]+distance(far, center):
                        finger_pts.append(start)

                for pts in finger_pts:
                    cv2.circle(frame,pts,10,[0,100,255],-1)

                # cv2.circle(frame,center,int(1.05*farthest),[0,100,255],2)
                dx, dy = (center[0]-origin_x, center[1]-origin_y)

                if dx > 10:
                    joystick_x += 30
                elif dx < -10:
                    joystick_x -= 30
                if dy > 10:
                    joystick_y += 30
                elif dy < -10:
                    joystick_y -= 30
        cv2.circle(frame, (joystick_x,joystick_y), 15, (0, 255, 0), -1)
    else:
        print("Hand not in rectangle")

    cv2.putText(frame,('Fingers: %d' % len(finger_pts)),(20,50), font, 1,(255,0,255),2,cv2.LINE_AA)

    return frame, len(finger_pts), dx, dy
