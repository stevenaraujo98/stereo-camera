import numpy as np
import cv2 as cv
from datetime import datetime
# from matplotlib import pyplot as plt

cap = cv.VideoCapture(0)
if not cap.isOpened():
    print("Cannot open camera")
    exit()

capturing = False

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    # if frame is read correctly ret is True
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break

    # print(frame.shape)  # 240, 640, 3
    left = frame[:, :320] # 240x320
    right = frame[:, 320:] # 240x320

    # Our operations on the frame come here
    # gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

    # Display the resulting frame
    cv.imshow('frame', frame)
    cv.imshow('left', left)
    cv.imshow('right', right)

    key = cv.waitKey(1)
    if key == ord('q'):
        # Close
        print(ord('c'))
        break
    elif key == ord('c'):
        # Capture
        print("Capturing image...")
        capturing = True

    if capturing:
        now = datetime.now()
        date_time = now.strftime("./imgs/%H_%M_%S_%d_%m_%Y")
        file_name = f"{date_time}_IMG"
        cv.imwrite(file_name + ".jpg", frame)
        cv.imwrite(file_name + "_LEFT.jpg", left)
        cv.imwrite(file_name + "_RIGHT.jpg", right)
        print(f"Image captured and saved as {file_name}")
        capturing = False

cap.release()
cv.destroyAllWindows()