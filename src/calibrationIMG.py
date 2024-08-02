import cv2 as cv
import numpy as np
from datetime import datetime
#import tkinter as tk
from utils.consts import PATH_SAVE
import time 
from utils.rectification import getStereoRectifier
import glob
import os

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

robot_selected = "rosmasterx3plus"
configNum = "Config1"
path_save_final = PATH_SAVE + robot_selected + "/2D/"


"""
# rectifier = getStereoRectifier("./src/calibration/imgOriginalRotada/stereoMap.xml") # Parece Original rotada a su forma real
# rectifier = getStereoRectifier("./src/calibration/imagenOriginal/stereoMap.xml") # Mal
# rectifier = getStereoRectifier("./src/calibration/guaradadoConQ/stereoMap.xml") # Parece Tal cual como se guardó
# rectifier = getStereoRectifier("./src/calibration/cambioRotacion/stereoMap.xml") # Mal
# rectifier = getStereoRectifier("./src/calibration/cambioPosicion/stereoMap.xml") # Mal
"""

rectifier = getStereoRectifier("./src/calibration/integradora/newStereoMap.xml")
# rectifier = getStereoRectifier("./src/calibration/re_calibration2/stereoMap.xml")

distancia = "550"
image_files = glob.glob(path_save_final + "images/" + distancia + "/*_LEFT.jpg")
for image_file in image_files:
    name = image_file[41:-9]
    print(name)
    
    frame = cv.imread(path_save_final + "images/" + distancia + "/" + name + "_LEFT.jpg")
    frameR = cv.imread(path_save_final + "images/" + distancia + "/" + name + "_RIGHT.jpg")


    frame_combined = np.hstack([frame, frameR])
    # frame_combined = cv.rotate(frame_combined, cv.ROTATE_180)
    frame_left_uncalibrated = frame_combined[:,:frame_combined.shape[1]//2]
    frame_right_uncalibrated = frame_combined[:,frame_combined.shape[1]//2:]
    # cv.imshow("left uncalib", frame_left_uncalibrated)
    # cv.imshow("right uncalib", frame_right_uncalibrated)

    # frame_left_calib, frame_right_calib = rectifier(frame_left_uncalibrated, frame_right_uncalibrated)
    frame_left_calib, frame_right_calib = rectifier(frame, frameR)


    # frame_left_calib = cv.rotate(frame_left_calib, cv.ROTATE_180)
    # frame_right_calib = cv.rotate(frame_right_calib, cv.ROTATE_180)

    # cv.imshow("left calib", frame_left_calib)
    # cv.imshow("right calib", frame_right_calib)
    # cv.waitKey(0)

    # crear la carpeta calibrated si no existe
    if not os.path.exists(path_save_final + "images/" + distancia + "/calibrated"):
        os.makedirs(path_save_final + "images/" + distancia + "/calibrated")
    # Guadar las imagenes rectificadas
    cv.imwrite(path_save_final + "images/" + distancia + "/calibrated/" + name + "_LEFT_CALIB.jpg", frame_left_calib)
    cv.imwrite(path_save_final + "images/" + distancia + "/calibrated/" + name + "_RIGHT_CALIB.jpg", frame_right_calib)

    # cv.destroyAllWindows()