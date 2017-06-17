import numpy as np
from PIL import ImageGrab
import cv2, time, pyautogui, math
from directkeys import PressKey, W, A, S, D, UP, DOWN, LEFT, RIGHT, ReleaseKey

def roi(img, vertices):
    #blank mask:
    mask = np.zeros_like(img)
    # fill the mask
    cv2.fillPoly(mask, vertices, 255)
    # now only show the area that is the mask
    masked = cv2.bitwise_and(img, mask)
    return masked

def process_img(image):
    vertices = np.array([[200, 50], [200, 170], [400, 170], [400, 50]])
    lower = np.array([0, 75, 0])
    upper = np.array([75, 255, 100])
    shapeMask = cv2.inRange(image, lower, upper)
    shapeMask = roi(shapeMask, [vertices])
    return shapeMask

def main():
    last_time = time.time()
    while True:
        screen =  np.array(ImageGrab.grab(bbox=(0,40,660,540)))
        print('Frame took {} seconds'.format(time.time()-last_time))
        last_time = time.time()
        new_screen = process_img(screen)

        cv2.imshow('window', new_screen)
        lines = cv2.HoughLinesP(new_screen,1,np.pi/180,45, 20, 15)
        #cv2.imshow('window',cv2.cvtColor(screen, cv2.COLOR_BGR2RGB))
        PressKey(UP)
        ReleaseKey(DOWN)
        ReleaseKey(LEFT)
        ReleaseKey(RIGHT)
        #time.sleep(5)

        #Main bulk of the detection: depending on the lines it sees on the arrows, it will go a certain direction.
        #Right now this works for all angles 0 to 180 degrees (if 0 is the arrow pointing left and 180 is the arrow pointing right).
        #This doesn't work if the arrow is pointing behind us - any of the degrees 180 to 360 are interpretted as the opposite (eg 225 degrees should be pointing behind us to the right, but it gets interpreted as left, or as 45 degrees)
        if lines is not None :
           print(len(lines))
        if lines is not None and len(lines[0]) == 1 and len(lines[0][0]) == 4:
            print(lines[0][0])
            slope = (lines[0][0][3] - lines[0][0][1]) / (lines[0][0][2] - lines[0][0][0])
            print(slope)

            length = math.sqrt((lines[0][0][2] - lines[0][0][0])**2 + (lines[0][0][3] - lines[0][0][1])**2)
            print(length)
            if (slope == 1.0 or slope == -1.0) and length < 100:
                print("forward")
                ReleaseKey(RIGHT)
                ReleaseKey(LEFT)
                PressKey(UP)
                #time.sleep(0.1)
            elif slope < 0 and length > 120:
                print("left")
                PressKey(UP)
                PressKey(LEFT)
                #time.sleep(0.1)
            elif slope > 0 and length > 120:
                print("right")
                PressKey(UP)
                PressKey(RIGHT)
                #time.sleep(0.1)
        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break

main()
