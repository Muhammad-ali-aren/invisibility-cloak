
import cv2 as cv
import matplotlib.pyplot as plt
import numpy as np
cap = cv.VideoCapture(0)
import time
import argparse

def removing_noise(full_frame):
    closing_kernel = np.ones((3,3),np.uint8)
    opening_kernel = np.ones((3,3),np.uint8)
    closed = cv.morphologyEx(full_frame,cv.MORPH_CLOSE,closing_kernel)
    clean_frame = cv.morphologyEx(closed,cv.MORPH_OPEN,opening_kernel)
    return clean_frame

def invisibile_cloak(args):
    cap = cv.VideoCapture(0) 
    if not cap.isOpened:
        print("error can't open camera")
        return
    color = args.cloth_color.lower()
    lower = None
    upper = None
    if  color == "green":
        lower = np.array([50, 80, 50])
        upper = np.array([90, 255, 255])
    elif color == "red":
        lower = np.array([-10, 100, 100])
        upper = np.array([10, 255, 255])
    elif color == "blue":
        lower = np.array([100, 150, 0])
        upper = np.array([140, 255, 255])
    elif color == "white":
        lower = np.array([0, 0, 200])  
        upper = np.array([180, 50, 255])
    else:
        print("error, unsupported cloth color, please give green or blue")
        cap.release()
        cv.destroyAllWindows()
        return


    time.sleep(2)
    ret, to_replace = cap.read()
    if not ret:
        print("failed to capture the background")
        cap.release()
        cv.destroyAllWindows()
        return

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        hsv = cv.cvtColor(frame,cv.COLOR_BGR2HSV)
        mask = cv.inRange(hsv,lower,upper)
        cloak = cv.bitwise_and(to_replace,to_replace,mask=mask)
        inverse = cv.bitwise_not(mask)
        current_bg = cv.bitwise_and(frame,frame,mask=inverse)
        full_frame = cv.add(cloak,current_bg)

        clean_frame = removing_noise(full_frame)
        cv.imshow("Invisible Cloak", clean_frame)
        if cv.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv.destroyAllWindows()

parser = argparse.ArgumentParser(prog="invisible_cloak",description="if you have green,red or blue color cloth it'll act as your invisiblity cloak")

parser.add_argument("--cloth_color",type=str,help="color of your cloth that you want to act as your invisibility cloak")
args = parser.parse_args()

if __name__ == "__main__":
    invisibile_cloak(args)