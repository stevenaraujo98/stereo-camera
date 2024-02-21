import cv2 as cv
from datetime import datetime
import tkinter as tk

def get_screen_resolution():
    root = tk.Tk()
    root.withdraw()  # Oculta la ventana principal
    # Obtiene la resolución del monitor automáticamente
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    # Cierra la ventana de Tkinter
    root.destroy()
    return screen_width, screen_height

# Factor adicional para reducir aún más el tamaño del video
reduction_factor = 0.8  # ajustar este valor de preferencia
is_necesary_redi = False
capturing = False
videoRecording = False
CONST_WIDTH_BOTH_LENS = 1920*2  # 3840
# CONST_WIDTH_BOTH_LENS = 1280*2  # 2560
# CONST_WIDTH_BOTH_LENS = 800*2  # 1600
# CONST_WIDTH_BOTH_LENS = 640*2  # 1280
# CONST_WIDTH_BOTH_LENS = 320*2  # 640
# CONST_HEIGHT = 1080 # 480
path_save = "./assets/"

# Obtener la resolución del monitor automáticamente
screen_width, screen_height = get_screen_resolution()

"""
default y minima resolucion 320 x 240
maxima resolucion 1920 x 1080
FULLHD 1920 x 1080 = 3840 x 1080 => 1920
HD     1280 × 720  = 2560 x 720  => 1280
SD     854 × 480   = 1600 x 600  => 800
SD     640 x 360   = 1280 x 480  => 640
SD     426 × 240   = 640 x 240   => 320
"""

cap = cv.VideoCapture(0)
if not cap.isOpened():
    print("Cannot open camera")
    exit()

print("Configurando la camara")
cap.set(cv.CAP_PROP_FRAME_WIDTH, CONST_WIDTH_BOTH_LENS)
# cap.set(cv.CAP_PROP_FRAME_HEIGHT, CONST_HEIGHT)
cap.set(cv.CAP_PROP_FPS, 30)
print("Configuracin finalizada.")
frame_width_one_len = int(cap.get(3)) // 2
frame_height_one_len = int(cap.get(4))
size_one_len = (frame_width_one_len, frame_height_one_len)
fps = cap.get(cv.CAP_PROP_FPS)

# Redimensiona el fotograma si su tamaño es mayor que el tamaño del monitor
if int(cap.get(3)) > screen_width or frame_height_one_len > screen_height:
    # Calcula el factor de escala
    scale_factor = min(screen_width / int(cap.get(3)), screen_height / frame_height_one_len) * reduction_factor
    print(scale_factor)
    is_necesary_redi = True

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    # if frame is read correctly ret is True
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break

    frame = cv.rotate(frame, cv.ROTATE_180)

    # print(frame.shape)
    left = frame[:, :frame_width_one_len]
    right = frame[:, frame_width_one_len:]

    # Display the resulting frame
    if is_necesary_redi:
        # Redimensiona el fotograma manteniendo la proporción original
        cv.imshow('frame', cv.resize(frame, None, fx=scale_factor, fy=scale_factor, interpolation=cv.INTER_AREA))
    else:
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
                file_name + '_LEFT.avi', cv.VideoWriter_fourcc(*'XVID'), 20.0, size_one_len)
            salida_R = cv.VideoWriter(
                file_name + '_RIGHT.avi', cv.VideoWriter_fourcc(*'XVID'), 20.0, size_one_len)
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
