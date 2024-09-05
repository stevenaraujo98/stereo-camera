import cv2 as cv
from datetime import datetime
from utils.consts import PATH_SAVE

def process(frame, frame_width):
    frame = cv.rotate(frame, cv.ROTATE_180)

    left = frame[:, :frame_width]
    right = frame[:, frame_width:]

    return frame, left, right

def get_name(path_robot, is_img = 1):
    now = datetime.now()
    str_time = now.strftime("%H_%M_%S_%d_%m_%Y")
    if is_img:
        str_time = "images/" + str_time + "_IMG"
    else:
        str_time = "videos/" + str_time + "_VID"

    return f"{PATH_SAVE  + path_robot}/2D/{str_time}"
