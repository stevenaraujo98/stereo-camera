import cv2 as cv
from datetime import datetime
import tkinter as tk
import sys
from utils.consts import PATH_SAVE
import time 

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
else:
    print("Error - Introduce los argumentos correctamente")
    print('Ejemplo: python3 src/jetson.py stretch')
    exit()


# Factor adicional para reducir aún más el tamaño del video
reduction_factor = 0.8  # ajustar este valor de preferencia
is_necesary_redi = False
capturing = False
videoRecording = False
show_fps=True
prev_frame_time = 0
new_frame_time = 0

path_save_final = PATH_SAVE + robot_selected + "/2D/"

# Obtener la resolución del monitor automáticamente
screen_width, screen_height = get_screen_resolution()

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

# frame_width_one_len = int(cap.get(3)) // 2
frame_width_one_len = CONST_WIDTH_BOTH_LENS // 2
# frame_height_one_len = int(cap.get(4))
frame_height_one_len = CONST_HEIGHT

fps = cap.get(cv.CAP_PROP_FPS)
print("Both lens: ", CONST_WIDTH_BOTH_LENS, "x", frame_height_one_len, "|| Screen size:", screen_width, "x", screen_height, "|| Open CV: (", int(cap.get(3)), int(cap.get(4)), ")", "FPS configurados", fps)
# Redimensiona el fotograma si su tamaño es mayor que el tamaño del monitor
if CONST_WIDTH_BOTH_LENS >= screen_width or frame_height_one_len >= screen_height:
    # Calcula el factor de escala
    scale_factor = min(screen_width / CONST_WIDTH_BOTH_LENS, screen_height / frame_height_one_len) * reduction_factor
    print(scale_factor)
    is_necesary_redi = True


# cap.set(cv.CAP_PROP_BACKEND, cv.CAP_BACKEND_CUDA)
# cap.set(cv.CAP_PROP_CUDA_DEVICE, 0)


while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    # if frame is read correctly ret is True
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break

    frame = cv.rotate(frame, cv.ROTATE_180)
    tmp_frame = frame.copy()
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

    # Display the resulting frame
    if is_necesary_redi:
        tmp_frame = cv.resize(tmp_frame, None, fx=scale_factor, fy=scale_factor, interpolation=cv.INTER_AREA)
    cv.imshow('frame', tmp_frame)

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
            date_time = now.strftime(path_save_final + "videos/%H_%M_%S_%d_%m_%Y")
            file_name = f"{date_time}_VIDEO"
            print("path save:", file_name)
            salida_L = cv.VideoWriter(
                file_name + '_LEFT.avi', cv.VideoWriter_fourcc(*'XVID'), 30.0, (frame_width_one_len, frame_height_one_len))
            salida_R = cv.VideoWriter(
                file_name + '_RIGHT.avi', cv.VideoWriter_fourcc(*'XVID'), 30.0, (frame_width_one_len, frame_height_one_len))
        else:
            print("video finish")
            salida_L.release()
            salida_R.release()
        count = 1

    if capturing:
        now = datetime.now()
        date_time = now.strftime(path_save_final + "images/%H_%M_%S_%d_%m_%Y")
        file_name = f"{date_time}_IMG"
        # cv.imwrite(file_name + ".jpg", frame)
        cv.imwrite(file_name + "_LEFT.jpg", left)
        cv.imwrite(file_name + "_RIGHT.jpg", right)
        print(f"Image captured and saved as {file_name}")
        capturing = False


cap.release()
cv.destroyAllWindows()
