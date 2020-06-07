import cv2
import time
import winsound
from pynput.keyboard import Key, Controller

#--config
mute = True
minimize = True
beep = True
#config--


keyboard = Controller()

kernel_ero = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))

vcap = cv2.VideoCapture(0)


def readframe(vcap):
    ret, frame = vcap.read()
    if not ret:
        return ret, None, None
    ts = vcap.get(cv2.CAP_PROP_POS_MSEC)
    frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    return ret, ts, frame


buff = []
while len(buff) < 3:
    ret, ts, frame = readframe(vcap)
    if ret:
        buff.append(frame)

while True:
    time.sleep(0.04)
    ret, ts, frame = readframe(vcap)
    if ret:
        buff.append(frame)
        buff.pop(0)

    d1 = cv2.absdiff(buff[0], buff[2])
    d2 = cv2.absdiff(buff[2], buff[1])
    motion = cv2.bitwise_and(d1, d2)
    ret, motion = cv2.threshold(motion, 25, 255, cv2.THRESH_BINARY)
    cv2.erode(motion, motion, kernel_ero)

    mean, stddev = cv2.meanStdDev(motion)
    if stddev[0][0] > 20:
        motionum = 0
        h, w = motion.shape
        for x in range(0, w-1, 2):
            for y in range(0, h-1, 2):
                if motion[y][x] == 255:
                    motionum += 1

        print("Motion detected")
        #beep
        if beep:
            winsound.Beep(440, 500)
        #Close windows
        if minimize:
            keyboard.press(Key.cmd)
            keyboard.press('d')
            keyboard.release('d')
            keyboard.release(Key.cmd)
        #Mute mic bind ctrl+m
        if mute:
            keyboard.press(Key.ctrl)
            keyboard.press('m')
            keyboard.release(Key.ctrl)
            keyboard.release('m')
        time.sleep(60) #To prevent the key shortcuts getting spammed the program will sleep for 60 secs when it detect motion
