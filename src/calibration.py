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
name_left = "16_35_42_26_02_2024_VID_LEFT"
name_right = "16_35_42_26_02_2024_VID_RIGHT"
cap = cv.VideoCapture(path_save_final + "videos/" + configNum + "/" + name_left + ".avi")
capR = cv.VideoCapture(path_save_final + "videos/" + configNum + "/" + name_right + ".avi")
# cap = cv.VideoCapture(path_save_final + "videos/cortados/L_left.mp4")
# capR = cv.VideoCapture(path_save_final + "videos/cortados/L_right.mp4")

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
rectifier = getStereoRectifier("./src/calibration/integradora/newStereoMap.xml")
# rectifier = getStereoRectifier("./src/calibration/re_calibration2/stereoMap.xml")

"""
# rectifier = getStereoRectifier("./src/calibration/imgOriginalRotada/stereoMap.xml") # Parece Original rotada a su forma real
# rectifier = getStereoRectifier("./src/calibration/guaradadoConQ/stereoMap.xml") # Parece Tal cual como se guardó
"""

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    ret, frameR = capR.read()
    
    # if frame is read correctly ret is True
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break

    """
    frame_combined = np.hstack([frame,frameR])
    # frame_combined = cv.rotate(frame_combined, cv.ROTATE_180)
    frame_left_uncalibrated = frame_combined[:,:frame_combined.shape[1]//2]
    frame_right_uncalibrated = frame_combined[:,frame_combined.shape[1]//2:]
    """
    # cv.imshow("left uncalib", frame_left_uncalibrated)
    # cv.imshow("right uncalib", frame_right_uncalibrated)
    
    frame_left_calib, frame_right_calib = rectifier(frame, frameR)
    """
    frame_left_calib, frame_right_calib = rectifier(frame_left_uncalibrated, frame_right_uncalibrated)
    """
    # frame_left_calib = cv.rotate(frame_left_calib, cv.ROTATE_180)
    # frame_right_calib = cv.rotate(frame_right_calib, cv.ROTATE_180)
    cv.imshow("left calib", frame_left_calib)
    cv.imshow("right calib", frame_right_calib)
    

    key = cv.waitKey(1)
    if key == ord('q'):
        # Close
        break

    if start_capturing:
        print("Starting video capture...", float(fps_selected), frame.shape[1], frame.shape[0], (frameR.shape[1], frameR.shape[0]))
        videoRecording = not videoRecording
        start_capturing = not start_capturing
        """
        now = datetime.now()
        date_time = now.strftime(path_save_final + "videos/" + configNum + "/calibrated/%H_%M_%S_%d_%m_%Y")
        file_name = f"{date_time}_VIDEO"
        salida_L = cv.VideoWriter(
            file_name + "/" + name_left  + '.avi', cv.VideoWriter_fourcc(*'XVID'), float(fps_selected), (frame.shape[1], frame.shape[0]))
        salida_R = cv.VideoWriter(
            file_name + '_RIGHT.avi', cv.VideoWriter_fourcc(*'XVID'), float(fps_selected), (frameR.shape[1], frameR.shape[0]))
        """
        salida_L = cv.VideoWriter(
            path_save_final + "videos/" + configNum + "/calibrated/" + name_left + "_calibrated.avi", 
            cv.VideoWriter_fourcc(*'XVID'), 
            float(fps_selected), 
            (frame.shape[1], frame.shape[0])
        )
        salida_R = cv.VideoWriter(
            path_save_final + "videos/" + configNum + "/calibrated/" + name_right + "_calibrated.avi", 
            cv.VideoWriter_fourcc(*'XVID'), 
            float(fps_selected), 
            (frameR.shape[1], frameR.shape[0])
        )
        
    if videoRecording:
        salida_L.write(frame_left_calib)
        salida_R.write(frame_right_calib)



cap.release()
cv.destroyAllWindows()
