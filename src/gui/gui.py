import tkinter as tk
from tkinter import ttk
import cv2
import PIL.Image
import PIL.ImageTk
from camera import process, get_name
from utils.consts import LIST_NAME_ROBOTS, LIST_RESOLUTIONS

class App(tk.Tk):
    def __init__(self, video_source=0):
        super().__init__()
        self.title("Tkinter and OpenCV")
        self.screen_width = self.winfo_screenwidth()
        self.screen_height = self.winfo_screenheight()
        self.geometry(f'{self.screen_width}x{self.screen_height}')
        # self.config(bg=Theme.BACKGROUND)
        self.vid = None
        self.record_video = False  # Variable para indicar si se debe grabar video
        self.video_writer_left = None  # Variable para el escritor de video
        self.video_writer_right = None  # Variable para el escritor de video
        self.is_necesary_redi = False
        self.reduction_factor = 0.8  # ajustar este valor de preferencia
        self.__launch_dialog()

    def __launch_dialog(self):
        self.first_panel = tk.Frame(self, width=640, height=480, padx=10)
        self.first_panel.pack(expand=True, anchor=tk.N)

        # Textos
        self.title1 = tk.Label(self.first_panel, text="ROBOT VISION SYSTEM", font=('Helvetica', 24, 'bold'), fg='#EA6749')
        self.title1.grid(row=0, column=0, columnspan=2, padx=5, pady=10)
        self.title2 = tk.Label(self.first_panel, text="STEREO VISION", font=('Helvetica', 20, 'bold'), fg="#C42E0B")
        self.title2.grid(row=1, column=0, columnspan=2, padx=5, pady=10)

        self.texto1 = tk.Label(self.first_panel, text="Configuración de cámara", font=16)
        self.texto1.grid(row=2, column=0, columnspan=2, padx=5, pady=10)

        self.texto2 = tk.Label(self.first_panel, text="Resolución:", font=12)
        self.texto2.grid(row=3, column=0, padx=5, pady=5, sticky="e")

        self.combo_resolucion = ttk.Combobox(self.first_panel, state="readonly", values=LIST_RESOLUTIONS, font=12)
        self.combo_resolucion.set(LIST_RESOLUTIONS[0])
        self.combo_resolucion.grid(row=3, column=1, padx=5, pady=5, sticky="w")

        self.texto2 = tk.Label(self.first_panel, text="Robot:", font=12)
        self.texto2.grid(row=4, column=0, padx=5, pady=5, sticky="e")

        self.combo_robot = ttk.Combobox(self.first_panel, state="readonly", values=LIST_NAME_ROBOTS, font=12)
        self.combo_robot.set(LIST_NAME_ROBOTS[0])
        self.combo_robot.grid(row=4, column=1, padx=5, pady=5, sticky="w")

        self.checkbox_value = tk.BooleanVar(self.first_panel)
        self.checkbox = tk.Checkbutton(self.first_panel, text="Grabar video", variable=self.checkbox_value, command=self.checkbox_clicked, font=12, padx=0)
        self.checkbox.grid(row=5, column=0, columnspan=2, pady=5, sticky="w")

        self.button = tk.Button(
            self.first_panel,
            text="Aceptar",
            cursor="hand2",
            command=self.start_camera,
            font=12
        )
        self.button.grid(row=6, column=0, columnspan=2, padx=5, pady=5)
        
    def checkbox_clicked(self):
        self.record_video = self.checkbox_value.get()
        print("Grabar video:", self.record_video)
    
    def start_camera(self):        
        list_size = self.combo_resolucion.get().split("x")
        self.path_robot = self.combo_robot.get()
        print("Robot:", self.path_robot)
        self.camera_width = int(list_size[0])
        camera_height = int(list_size[1])
        print(self.camera_width, camera_height)

        # Ocultar los widgets de configuración
        self.first_panel.destroy()

        self.center_panel = tk.Frame(
            self, width=640, height=480, padx=10)
        self.center_panel.pack(expand=True, anchor=tk.N)

        # Configuracion de cámara
        print("Iniciando configuración de cámara...")
        self.vid = cv2.VideoCapture(0)
        self.vid.set(cv2.CAP_PROP_FRAME_WIDTH, self.camera_width*2)
        print("Configuración termianda!", int(self.vid.get(3)) // 2, "x", int(self.vid.get(4)), self.vid.get(cv2.CAP_PROP_FPS))

        if(int(self.vid.get(3)) >= self.screen_width or int(self.vid.get(4)) >= self.screen_height):
            self.scale_factor = min(self.screen_width / int(self.vid.get(3)), self.screen_height / int(self.vid.get(4))) * self.reduction_factor
            # Calcula el tamaño final del fotograma después de la redimensión
            final_width = int(self.screen_width * self.scale_factor)
            final_height = int(self.screen_height * self.scale_factor)

            self.is_necesary_redi = True

            print("Resolucion para el canvas", final_width, final_height)
            ## RESOLUCION DE CANVAS MAL, ERROR
            self.canvas = tk.Canvas(self.center_panel, width=final_width // 2, height=final_height)
            self.canvas_2 = tk.Canvas(self.center_panel, width=final_width // 2, height=final_height)
        else:
            self.canvas = tk.Canvas(self.center_panel, width=self.camera_width, height=camera_height)
            self.canvas_2 = tk.Canvas(self.center_panel, width=self.camera_width, height=camera_height)

        # Mostrar la visualización de la cámara
        self.canvas.grid(row=0, column=0)
        self.canvas_2.grid(row=0, column=1)
        self.update_camera()

        self.btn_snapshot = tk.Button(
            self.center_panel, text="Snapshot", cursor="hand2", width=30, command=self.snapshot, font=12, bg="#f0f0f0")
        self.btn_snapshot.grid(row=1, column=0, padx=10, pady=10)

        # Agregar botón de regreso
        self.return_button = tk.Button(
            self.center_panel,
            text="Regresar",
            cursor="hand2", 
            width=30,
            command=self.return_to_config,
            font=12
        )
        self.return_button.grid(row=1, column=1, padx=10, pady=10)

    def snapshot(self):
        ret, frame = self.vid.read()
        if ret:
            # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame, frame_left, frame_right = process(frame, self.camera_width)
            file_name = get_name(self.path_robot)

            print(f"Image captured and saved as {file_name}")
            cv2.imwrite(file_name + ".jpg", frame)
            cv2.imwrite(file_name + "_LEFT.jpg", frame_left)
            cv2.imwrite(file_name + "_RIGHT.jpg", frame_right)
            print("Snapshot saved as snapshot.png")

    def update_camera(self):
        ret, frame = self.vid.read()
        if ret:
            fr_tmp, frame_left, frame_right = process(frame, self.camera_width)
            
            if self.is_necesary_redi:
                frame_right_tmp = cv2.resize(frame_right, None, fx=self.scale_factor, fy=self.scale_factor, interpolation=cv2.INTER_AREA)
                frame_left_tmp = cv2.resize(frame_left, None, fx=self.scale_factor, fy=self.scale_factor, interpolation=cv2.INTER_AREA)
                self.photo_right = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(cv2.cvtColor(frame_right_tmp, cv2.COLOR_BGR2RGB)))
                self.photo_left = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(cv2.cvtColor(frame_left_tmp, cv2.COLOR_BGR2RGB)))
            else:
                self.photo_right = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(cv2.cvtColor(frame_right, cv2.COLOR_BGR2RGB)))
                self.photo_left = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(cv2.cvtColor(frame_left, cv2.COLOR_BGR2RGB)))
            
            self.canvas.create_image(0, 0, image=self.photo_right, anchor=tk.NW)
            self.canvas_2.create_image(0, 0, image=self.photo_left, anchor=tk.NW)

            # Si se debe grabar video, guarda el fotograma en el archivo de video
            if self.record_video:
                if self.video_writer_left is None or self.video_writer_right is  None:
                    file_name = get_name(self.path_robot, 0)
                    print(file_name, self.camera_width, frame.shape[0])
                    # Crea el escritor de video si aún no se ha creado
                    fourcc = cv2.VideoWriter_fourcc(*'XVID')
                    self.video_writer_left = cv2.VideoWriter(file_name + '_LEFT.avi', fourcc, 20.0, (self.camera_width, frame.shape[0]))
                    self.video_writer_right = cv2.VideoWriter(file_name + '_RIGHT.avi', fourcc, 20.0, (self.camera_width, frame.shape[0]))

                # Escribe el fotograma en el archivo de video
                self.video_writer_left.write(frame_left)
                self.video_writer_right.write(frame_right)

        self.after_id = self.after(10, self.update_camera) #10 milisegundos

    def return_to_config(self):
        # Ocultar los widgets de configuración
        self.center_panel.destroy()
        self.is_necesary_redi = False
        
        # Detener la visualización de la cámara
        if self.vid and self.vid.isOpened():
            self.vid.release()
        
        if self.after_id:
            self.after_cancel(self.after_id)

        # Detener la grabación de video si está en curso
        if self.video_writer_left is not None or self.video_writer_right is not None:
            self.video_writer_left.release()
            self.video_writer_right.release()
            self.video_writer_left = None
            self.video_writer_right = None
            self.record_video = False

        # Volver a mostrar los widgets de configuración
        self.__launch_dialog()

    def __del__(self):
        if self.vid and self.vid.isOpened():
            self.vid.release()
