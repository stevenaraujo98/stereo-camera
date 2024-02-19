import numpy as np
import cv2 as cv
from datetime import datetime
# from matplotlib import pyplot as plt
from gui.gui import App
import tkinter as tk


'''
capturing = False
videoRecording = False
CONST_WIDTH = 1921*2  # 640
# CONST_HEIGHT = 1080 # 480
path_save = "./assets/"

# default y minima resolucion 320 x 240
# maxima resolucion 1920 x 1080
#        cada lente  = total
# 8K     7680 x 4320 = NO
# 4K     3840 x 2160 = NO
# 2K     2560 x 1440 = NO
# FULLHD 1920 x 1080 = 3840 x 1080 => 1920
# HD     1280 × 720  = 2560 x 720  => 1280
# SD     854 × 480   = 1600 x 600  => 800
# SD     640 x 360   = 1280 x 480  => 640
# SD     426 × 240   = 640 x 240   => 320

cap = cv.VideoCapture(0)
# cap_2 = cv.VideoCapture(1)
if not cap.isOpened():
    print("Cannot open camera")
    exit()

cap.set(cv.CAP_PROP_FRAME_WIDTH, CONST_WIDTH)
# cap.set(cv.CAP_PROP_FRAME_HEIGHT, CONST_HEIGHT)
frame_width = int(cap.get(3)) // 2
frame_height = int(cap.get(4))
size = (frame_width, frame_height)
fps = cap.get(cv.CAP_PROP_FPS)

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    frame = cv.rotate(frame, cv.ROTATE_180)
    # if frame is read correctly ret is True
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break

    # print(frame.shape)
    left = frame[:, :frame_width]
    right = frame[:, frame_width:]

    # Our operations on the frame come here
    # gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

    # Display the resulting frame
    cv.imshow('frame', frame)
    # cv.imshow('left', left)
    # cv.imshow('right', right)
    if videoRecording:
        salida_L.write(left)
        salida_R.write(right)

    key = cv.waitKey(1)
    if key == ord('q'):
        # Close
        break
    elif key == ord('c'):
        # Capture
        print("Capturing image...")
        capturing = True
    elif key == ord('v'):
        # Capture
        print("Capturing Video...")
        videoRecording = not videoRecording
        if videoRecording:
            now = datetime.now()
            date_time = now.strftime(path_save + "videos/%H_%M_%S_%d_%m_%Y")
            file_name = f"{date_time}_VIDEO"
            # 30.0 fps
            salida_L = cv.VideoWriter(
                file_name + '_LEFT.mp4', cv.VideoWriter_fourcc(*'MP4V'), 20.0, size)
            salida_R = cv.VideoWriter(
                file_name + '_RIGHT.mp4', cv.VideoWriter_fourcc(*'MP4V'), 20.0, size)
        else:
            print("video finish")
            salida_L.release()
            salida_R.release()

    if capturing:
        now = datetime.now()
        date_time = now.strftime(path_save + "imgs/%H_%M_%S_%d_%m_%Y")
        file_name = f"{date_time}_IMG"
        cv.imwrite(file_name + ".jpg", frame)
        cv.imwrite(file_name + "_LEFT.jpg", left)
        cv.imwrite(file_name + "_RIGHT.jpg", right)
        print(f"Image captured and saved as {file_name}")
        capturing = False


cap.release()
cv.destroyAllWindows()
'''

# Create a window and pass it to the Application object
app = App()
app.mainloop()