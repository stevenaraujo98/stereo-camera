import cv2 as cv
from datetime import datetime
import tkinter as tk
import sys
from utils.consts import PATH_SAVE

def get_screen_resolution():
    root = tk.Tk()
    root.withdraw()  # Oculta la ventana principal
    # Obtiene la resolución del monitor automáticamente
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    # Cierra la ventana de Tkinter
    root.destroy()
    return screen_width, screen_height

def visualize(image, box_color=(0, 255, 0), text_color=(0, 0, 255), fps=None):
    output = image.copy()

    if fps is not None:
        cv.putText(output, 'FPS: {:.2f}'.format(fps), (0, 15), cv.FONT_HERSHEY_SIMPLEX, 0.5, text_color)

    return output

# Comprobación de seguridad, ejecutar sólo si se reciben 2 argumentos reales
if len(sys.argv) == 2:
    robot_selected = sys.argv[1]
    fps_selected = "10"
elif len(sys.argv) == 3:
    robot_selected = sys.argv[1]
    fps_selected = sys.argv[2]
else:
    print("Error - Introduce los argumentos correctamente")
    print('Ejemplo: python3 src/jetson.py stretch')
    exit()


# Factor adicional para reducir aún más el tamaño del video
reduction_factor = 0.8  # ajustar este valor de preferencia
start_capturing = True
videoRecording = False
path_save_final = PATH_SAVE + robot_selected + "/2D/"

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
# CONST_WIDTH_BOTH_LENS, CONST_HEIGHT = 1920*2, 1080  # 3840x1080
CONST_WIDTH_BOTH_LENS, CONST_HEIGHT = 1280*2, 720  # 2560x720
# CONST_WIDTH_BOTH_LENS, CONST_HEIGHT = 800*2, 600  # 1600x60
# CONST_WIDTH_BOTH_LENS, CONST_HEIGHT = 640*2, 480   # 1280x480
# CONST_WIDTH_BOTH_LENS, CONST_HEIGHT = 320*2, 240  # 640x240

cap = cv.VideoCapture(0)
if not cap.isOpened():
    print("Cannot open camera")
    exit()

print("Configurando la camara")
cap.set(cv.CAP_PROP_FRAME_WIDTH, CONST_WIDTH_BOTH_LENS)
cap.set(cv.CAP_PROP_FRAME_HEIGHT, CONST_HEIGHT)
# cap.set(cv.CAP_PROP_FPS, 20)
print("Configuracin finalizada.")

fps = cap.get(cv.CAP_PROP_FPS)
print("Both lens: ", CONST_WIDTH_BOTH_LENS, "x", CONST_HEIGHT, "|| Screen size:", screen_width, "x", screen_height, "|| Open CV: (", int(cap.get(3)), int(cap.get(4)), ")", "FPS configurados", fps)

# cap.set(cv.CAP_PROP_BACKEND, cv.CAP_BACKEND_CUDA)
# cap.set(cv.CAP_PROP_CUDA_DEVICE, 0)

# tm = cv.TickMeter()
while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    # if frame is read correctly ret is True
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break

    frame = cv.rotate(frame, cv.ROTATE_180)

    # print(frame.shape)
    left = frame[:, :frame.shape[1]//2]
    right = frame[:, frame.shape[1]//2:]

    if start_capturing:
        print("Starting video capture...", float(fps_selected))
        videoRecording = not videoRecording
        start_capturing = not start_capturing
        now = datetime.now()
        date_time = now.strftime(path_save_final + "videos/%H_%M_%S_%d_%m_%Y")
        file_name = f"{date_time}_VIDEO"
        salida_L = cv.VideoWriter(
            file_name + '_LEFT.avi', cv.VideoWriter_fourcc(*'XVID'), float(fps_selected), (frame.shape[1]//2, frame.shape[0]))
        salida_R = cv.VideoWriter(
            file_name + '_RIGHT.avi', cv.VideoWriter_fourcc(*'XVID'), float(fps_selected), (frame.shape[1]//2, frame.shape[0]))
    
    if videoRecording:
        salida_L.write(left)
        salida_R.write(right)


salida_L.release()
salida_R.release()
cap.release()
cv.destroyAllWindows()
