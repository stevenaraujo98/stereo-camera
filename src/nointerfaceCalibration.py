import cv2 as cv
import numpy as np
from datetime import datetime
#import tkinter as tk
from utils.consts import PATH_SAVE
import time 
from utils.rectification import getStereoRectifier

"""
def get_screen_resolution():
    root = tk.Tk()
    root.withdraw()  # Oculta la ventana principal
    # Obtiene la resolución del monitor automáticamente
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    # Cierra la ventana de Tkinter
    root.destroy()
    return screen_width, screen_height
"""

# Factor adicional para reducir aún más el tamaño del video
reduction_factor = 0.8  # ajustar este valor de preferencia
is_necesary_redi = False
capturing = False
show_fps=True
prev_frame_time = 0
new_frame_time = 0

# Obtener la resolución del monitor automáticamente
# screen_width, screen_height = get_screen_resolution()

"""
default y minima resolucion 320 x 240
maxima resolucion 1920 x 1080
FULLHD 1920 x 1080 = 3840 x 1080 => 1920 x 1080
HD     1280 × 720  = 2560 x 720  => 1280 x 720
SD     854 × 480   = 1600 x 600  => 800 x 600
SD     640 x 360   = 1280 x 480  => 640 x 480
SD     426 × 240   = 640 x 240   => 320 x 240
"""
# CONST_WIDTH_BOTH_LENS, CONST_HEIGHT = 1920*2, 1080  # 3840x1080
# CONST_WIDTH_BOTH_LENS, CONST_HEIGHT = 1280*2, 720  # 2560x720
CONST_WIDTH_BOTH_LENS, CONST_HEIGHT = 800*2, 600  # 1600x60
# CONST_WIDTH_BOTH_LENS, CONST_HEIGHT = 640*2, 480   # 1280x480
# CONST_WIDTH_BOTH_LENS, CONST_HEIGHT = 320*2, 240  # 640x240

start_capturing = True
videoRecording = False
robot_selected = "waiter"
configNum = "Config1"
fps_selected = 10
path_save_final = PATH_SAVE + robot_selected + "/2D/"
cap = cv.VideoCapture("database/" + robot_selected + "/2D/videos/" + configNum + "/16_35_42_26_02_2024_VID_LEFT.avi")
capR = cv.VideoCapture("database/" + robot_selected + "/2D/videos/" + configNum + "/16_35_42_26_02_2024_VID_RIGHT.avi")

if not cap.isOpened():
    print("Cannot open left camera")
    exit()
if not capR.isOpened():
    print("Cannot open right camera")
    exit()
    

print("Configurando la camara")
#cap.set(cv.CAP_PROP_FRAME_WIDTH, CONST_WIDTH_BOTH_LENS)
#cap.set(cv.CAP_PROP_FRAME_HEIGHT, CONST_HEIGHT)
#cap.set(cv.CAP_PROP_FPS, 60)
print("Configuracin finalizada.")

frame_width_one_len = int(cap.get(3)) // 2
frame_height_one_len = int(cap.get(4))
size_one_len = (frame_width_one_len, frame_height_one_len)
fps = cap.get(cv.CAP_PROP_FPS)

"""
print("Both lens: ", int(cap.get(3)), "x", frame_height_one_len, "|| Screen size:", screen_width, "x", screen_height, "FPS configurados", fps)
# Redimensiona el fotograma si su tamaño es mayor que el tamaño del monitor
if int(cap.get(3)) >= screen_width or frame_height_one_len >= screen_height:
    # Calcula el factor de escala
    scale_factor = min(screen_width / int(cap.get(3)), screen_height / frame_height_one_len) * reduction_factor
    print(scale_factor)
    is_necesary_redi = True
"""

tm = cv.TickMeter()
rectifier = getStereoRectifier("./src/calibration/stereoMap.xml")
while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    ret, frameR = capR.read()
    
    frame_combined = np.hstack([frame,frameR])
    frame_combined = cv.rotate(frame_combined, cv.ROTATE_180)
    frame_left_uncalibrated = frame_combined[:,:frame_combined.shape[1]//2]
    frame_right_uncalibrated = frame_combined[:,frame_combined.shape[1]//2:]
    # cv.imshow("left uncalib", frame_left_uncalibrated)
    # cv.imshow("right uncalib", frame_right_uncalibrated)
    
    frame_left_calib, frame_right_calib = rectifier(frame_left_uncalibrated, frame_right_uncalibrated)
    cv.imshow("left calib", frame_left_calib)
    cv.imshow("right calib", frame_right_calib)
    
    # if frame is read correctly ret is True
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break
        
    frame = cv.rotate(frame, cv.ROTATE_180)
    tmp_frame = frame.copy()
    # print(frame.shape, tm.getFPS())

    # print(frame.shape)
    left = frame[:, :frame_width_one_len]
    right = frame[:, frame_width_one_len:]

    if show_fps:
        # font which we will be using to display FPS 
        font = cv.FONT_HERSHEY_SIMPLEX 
        # time when we finish processing for this frame 
        new_frame_time = time.time() 

        # Calculating the fps 

        # fps will be number of frame processed in given time frame 
        # since their will be most of time error of 0.001 second 
        # we will be subtracting it to get more accurate result 
        fps = 1/(new_frame_time-prev_frame_time) 
        prev_frame_time = new_frame_time 

        # converting the fps into integer 
        fps = int(fps) 

        # converting the fps to string so that we can display it on frame 
        # by using putText function 
        fps = str(fps) 

        # putting the FPS count on the frame 
        cv.putText(tmp_frame, fps, (7, 70), font, 3, (frame_width_one_len, frame_height_one_len, 0), 3, cv.LINE_AA) 

    """
    # Display the resulting frame
    if is_necesary_redi:
        # Redimensiona el fotograma manteniendo la proporción original
        tmp_frame = cv.resize(tmp_frame, None, fx=scale_factor, fy=scale_factor, interpolation=cv.INTER_AREA)
       """ 
    cv.imshow('frame', tmp_frame)
    # cv.imshow('left', left)
    # cv.imshow('right', right)
    if videoRecording:
        salida_L.write(left)
        salida_R.write(right)

    ### Se detiene con 0-------------------------------------------------------------
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
            date_time = now.strftime(PATH_SAVE + "waiter/2D/videos/%H_%M_%S_%d_%m_%Y")
            file_name = f"{date_time}_VIDEO"
            # 30.0 fps
            print("path save:", file_name)
            salida_L = cv.VideoWriter(
                file_name + '_LEFT.avi', cv.VideoWriter_fourcc(*'XVID'), 5.0, size_one_len)
            salida_R = cv.VideoWriter(
                file_name + '_RIGHT.avi', cv.VideoWriter_fourcc(*'XVID'), 5.0, size_one_len)
        else:
            print("video finish")
            salida_L.release()
            salida_R.release()

    if start_capturing:
        print("Starting video capture...", float(fps_selected), frame.shape[1], frame.shape[0], (frameR.shape[1], frameR.shape[0]))
        videoRecording = not videoRecording
        start_capturing = not start_capturing
        now = datetime.now()
        date_time = now.strftime(path_save_final + "videos/" + configNum + "/calibrated/%H_%M_%S_%d_%m_%Y")
        file_name = f"{date_time}_VIDEO"
        salida_L = cv.VideoWriter(
            file_name + '_LEFT.avi', cv.VideoWriter_fourcc(*'XVID'), float(fps_selected), (frame.shape[1], frame.shape[0]))
        salida_R = cv.VideoWriter(
            file_name + '_RIGHT.avi', cv.VideoWriter_fourcc(*'XVID'), float(fps_selected), (frameR.shape[1], frameR.shape[0]))
        
    if videoRecording:
        salida_L.write(cv.rotate(frame_left_calib, cv.ROTATE_180))
        salida_R.write(cv.rotate(frame_right_calib, cv.ROTATE_180))


    if capturing:
        now = datetime.now()
        date_time = now.strftime(PATH_SAVE + "waiter/2D/images/%H_%M_%S_%d_%m_%Y")
        file_name = f"{date_time}_IMG"
        cv.imwrite(file_name + ".jpg", frame)
        cv.imwrite(file_name + "_LEFT.jpg", left)
        cv.imwrite(file_name + "_RIGHT.jpg", right)
        print(f"Image captured and saved as {file_name}")
        capturing = False


cap.release()
cv.destroyAllWindows()
