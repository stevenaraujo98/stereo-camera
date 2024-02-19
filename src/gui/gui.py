import tkinter as tk
from tkinter import messagebox, ttk
import cv2
import PIL.Image
import PIL.ImageTk
from utils.themes import Theme

class App(tk.Tk):
    def __init__(self, video_source=0):
        super().__init__()
        self.title("Tkinter and OpenCV")
        self.screen_width = self.winfo_screenwidth()
        self.screen_height = self.winfo_screenheight()
        self.geometry(f'{self.screen_width}x{self.screen_height}')
        # self.config(bg=Theme.BACKGROUND)
        self.vid = None
        self.__launch_dialog()

    def __launch_dialog(self):
        # Textos
        self.texto1 = tk.Label(self, text="Configuración de cámara", font=16)
        self.texto1.grid(row=0, column=0, columnspan=2, padx=5, pady=10)

        self.texto2 = tk.Label(self, text="Resolución:", font=12)
        self.texto2.grid(row=1, column=0, padx=5, pady=5, sticky="e")

        self.combo = ttk.Combobox(self, state="readonly", values=["1920x1080", "1280×720", "800x600", "640x480", "320x240"], font=12)
        self.combo.set("1920x1080")
        self.combo.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        self.checkbox_value = tk.BooleanVar(self)
        self.checkbox = tk.Checkbutton(self, text="Grabar video", variable=self.checkbox_value, command=self.checkbox_clicked, font=12, padx=0)
        self.checkbox.grid(row=2, column=0, columnspan=2, pady=5, sticky="w")

        self.button = tk.Button(
            text="Aceptar",
            cursor="hand2",
            command=self.start_camera,
            font=12
        )
        self.button.grid(row=3, column=0, columnspan=2, padx=5, pady=5)
        
    def checkbox_clicked(self):
        print(self.checkbox_value.get())
    
    def start_camera(self):
        list_size = self.combo.get().split("x")
        camera_width = int(list_size[0])
        camera_height = int(list_size[1])
        print(camera_width, camera_height)

        # Ocultar los widgets de configuración
        self.texto1.grid_forget()
        self.texto2.grid_forget()
        self.combo.grid_forget()
        self.checkbox.grid_forget()
        self.button.grid_forget()


        self.center_panel = tk.Frame(
            self, width=640, height=480, padx=10)
        self.center_panel.pack(side="left", fill="both", expand=True, anchor=tk.N)

        # Mostrar la visualización de la cámara
        self.vid = cv2.VideoCapture(0)
        # self.canvas = tk.Canvas(self, width=camera_width, height=camera_height)
        self.canvas = tk.Canvas(self.center_panel, width=self.vid.get(
            cv2.CAP_PROP_FRAME_WIDTH), height=self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.canvas.grid(row=0, column=0)

        # self.canvas_2 = tk.Canvas(self, width=camera_width, height=camera_height)
        self.canvas_2 = tk.Canvas(self.center_panel, width=self.vid.get(
            cv2.CAP_PROP_FRAME_WIDTH), height=self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT))
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
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            cv2.imwrite("snapshot.png", cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            print("Snapshot saved as snapshot.png")

    def update_camera(self):
        ret, frame = self.vid.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            self.photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
            self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)
            self.canvas_2.create_image(0, 0, image=self.photo, anchor=tk.NW)

        self.after(10, self.update_camera) #10 milisegundos

    def return_to_config(self):
        # Ocultar los widgets de configuración
        # self.canvas.grid_forget()
        # self.canvas.destroy()
        # self.canvas_2.grid_forget()
        # self.canvas_2.destroy()
        # self.btn_snapshot.grid_forget()
        # self.return_button.grid_forget()
        self.center_panel.destroy()
        
        # Detener la visualización de la cámara
        if self.vid and self.vid.isOpened():
            self.vid.release()

        # Volver a mostrar los widgets de configuración
        self.__launch_dialog()

    def __del__(self):
        if self.vid and self.vid.isOpened():
            self.vid.release()
