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
        str_time = "imgs/" + str_time + "_IMG"
    else:
        str_time = "videos/" + str_time + "_VID"

    return f"{PATH_SAVE  + path_robot}/{str_time}"

def resize_resolution(frame):
    # Redimensiona el fotograma si su tamaño es mayor que el tamaño del monitor
    if int(cap.get(3)) > screen_width or frame_height_one_len > screen_height:
        # Calcula el factor de escala
        scale_factor = min(screen_width / int(cap.get(3)), screen_height / frame_height_one_len)
        print(scale_factor)
        is_necesary_redi = True
    dim = ()
    return cv.resize(frame, dim, interpolation = cv.INTER_AREA)
