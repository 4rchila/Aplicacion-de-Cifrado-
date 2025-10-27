import customtkinter as ctk
from PIL import Image
import os
from tkinter import filedialog, messagebox
import time
import sys
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

 
def generar_claves():
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=4096)
    public_key = private_key.public_key()
    return private_key, public_key

def guardar_claves(private_key, public_key, ruta_privada, ruta_publica):
    os.makedirs(os.path.dirname(ruta_privada), exist_ok=True)
    os.makedirs(os.path.dirname(ruta_publica), exist_ok=True)
    with open(ruta_privada, "wb") as f:
        f.write(
            private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=serialization.NoEncryption()
            )
        )
    
    with open(ruta_publica, "wb") as f:
        f.write(
            public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            )
        )
    
def cargar_claves(ruta_privada, ruta_publica):
    with open(ruta_privada, "rb") as f:
        private_key = serialization.load_pem_private_key(f.read(), password=None)
    
    with open(ruta_publica, "rb") as f:
        public_key = serialization.load_pem_public_key(f.read())
    return private_key, public_key


# === PANEL IZQUIERDO FUNCIONAL ===
class PanelLateral(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="#122448", corner_radius=15)
        self.grid_rowconfigure((0, 1, 2, 3, 4), weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Variables para mostrar rutas
        self.ruta_privada = ctk.StringVar(value="No cargada")
        self.ruta_publica = ctk.StringVar(value="No cargada")

        # --- Encabezado ---
        ctk.CTkLabel(
            self, text="🔐 GESTIÓN DE CLAVES",
            text_color="#e76940",
            font=ctk.CTkFont(size=18, weight="bold")
        ).pack(pady=(25, 10))

        ctk.CTkLabel(
            self, text="Cargar claves RSA\npara usarlas en el sistema",
            text_color="white", justify="center"
        ).pack(pady=(0, 20))

        # --- Botones ---
        ctk.CTkButton(
            self, text="📂 Cargar Clave Privada",
            fg_color="#1c3c6b", hover_color="#e76940",
            command=self.cargar_clave_privada
        ).pack(pady=(0, 10), padx=20, fill="x")

        ctk.CTkButton(
            self, text="📂 Cargar Clave Pública",
            fg_color="#1c3c6b", hover_color="#1a4d8f",
            command=self.cargar_clave_publica
        ).pack(pady=(0, 20), padx=20, fill="x")

        # --- Etiquetas con estado de carga ---
        self.label_priv = ctk.CTkLabel(
            self, textvariable=self.ruta_privada, text_color="#ede4d3", wraplength=180
        )
        self.label_priv.pack(pady=(5, 10))

        self.label_pub = ctk.CTkLabel(
            self, textvariable=self.ruta_publica, text_color="#ede4d3", wraplength=180
        )
        self.label_pub.pack(pady=(5, 20))

        # --- Info decorativa (opcional) ---
        info_card = ctk.CTkFrame(self, fg_color="#f7eedd", corner_radius=10, border_color="#e76940", border_width=1)
        info_card.pack(pady=15, padx=20, fill="x")
        ctk.CTkLabel(info_card, text="Archivos procesados: 0", text_color="white").pack(pady=10)

        info_card2 = ctk.CTkFrame(self, fg_color="#f7eedd", corner_radius=10, border_color="#e76940", border_width=1)
        info_card2.pack(pady=10, padx=20, fill="x")
        ctk.CTkLabel(info_card2, text="Última operación: --/--/----", text_color="white").pack(pady=10)


    # --- Función para cargar clave privada ---
    def cargar_clave_privada(self):
        ruta = filedialog.askopenfilename(
            title="Seleccionar clave privada",
            filetypes=[("Archivos PEM", "*.pem"), ("Todos los archivos", "*.*")]
        )
        if not ruta:
            return

        try:
            with open(ruta, "rb") as f:
                serialization.load_pem_private_key(f.read(), password=None)
            self.ruta_privada.set(f"Privada cargada: {ruta.split('/')[-1]}")
            messagebox.showinfo("Éxito", "Clave privada cargada correctamente.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar la clave privada:\n{e}")


    # --- Función para cargar clave pública ---
    def cargar_clave_publica(self):
        ruta = filedialog.askopenfilename(
            title="Seleccionar clave pública",
            filetypes=[("Archivos PEM", "*.pem"), ("Todos los archivos", "*.*")]
        )
        if not ruta:
            return

        try:
            with open(ruta, "rb") as f:
                serialization.load_pem_public_key(f.read())
            self.ruta_publica.set(f"Pública cargada: {ruta.split('/')[-1]}")
            messagebox.showinfo("Éxito", "Clave pública cargada correctamente.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar la clave pública:\n{e}")

    
def on_enter(event):
    event.widget.master.configure(
    fg_color="#e76940",
    text_color="#f7eedd",
    border_color="#cb532c",
    border_width=1
)
def on_leave(event):
    event.widget.master.configure(
    fg_color="#f7eedd",
    text_color="#e76940",
    border_color="#e76940",
    border_width=1
)
    
def crear_llave_frame(main_container, show_frame_callback):
    frame = ctk.CTkFrame(main_container, fg_color="#f7eedd")

    frame.grid_rowconfigure((0, 2), weight=1)
    frame.grid_rowconfigure(1, weight=0)
    frame.grid_columnconfigure((0, 1), weight=1)

    # === PANEL IZQUIERDO DECORATIVO ===
    side_panel = PanelLateral(frame)
    side_panel.grid(row=1, column=0, padx=(0, 30), pady=40, sticky="nsew")

    # === PANEL CENTRAL PRINCIPAL ===
    button_container = ctk.CTkFrame(frame, fg_color="#122448", corner_radius=15)
    button_container.grid(row=1, column=1, pady=80, sticky="n")
    button_container.grid_rowconfigure(0, weight=1)
    button_container.grid_columnconfigure((0, 1, 2), weight=1)

    # Cargar íconos (deja espacio aunque no los tengas todavía)
    imagen_archivo = Image.open("../utils/archivo.png")
    imagen_foto = Image.open("../utils/imagen.png")
    imagen_audio = Image.open("../utils/auriculares.png")
    icon_size = (50, 50)
    
    file_ctk = ctk.CTkImage(dark_image=imagen_archivo, light_image=imagen_archivo, size=icon_size)
    img_ctk = ctk.CTkImage(dark_image=imagen_foto, light_image=imagen_foto, size=icon_size)
    audio_ctk = ctk.CTkImage(dark_image=imagen_audio, light_image=imagen_audio, size=icon_size)
    
    btn1 = ctk.CTkButton(button_container, text="Compresión de Texto", image=file_ctk, compound="top",
                         width=160, height=130, fg_color="#172b54", border_color="#6de0ff",
                         hover=False, border_width=1, font=ctk.CTkFont(size=14, weight="bold"),
                         command=lambda: show_frame_callback("Texto"))

    btn2 = ctk.CTkButton(button_container, text="Compresión de Imágenes", image=img_ctk, compound="top",
                         width=160, height=130, fg_color="#172b54", border_color="#6de0ff",
                         hover=False, border_width=1, font=ctk.CTkFont(size=14, weight="bold"),
                         command=lambda: show_frame_callback("Imagen"))

    btn3 = ctk.CTkButton(button_container, text="Compresión de Audio", image=audio_ctk, compound="top",
                         width=160, height=130, fg_color="#172b54", border_color="#6de0ff",
                         hover=False, border_width=1, font=ctk.CTkFont(size=14, weight="bold"),
                         command=lambda: show_frame_callback("Audio"))

    # Colocar botones
    btn1.grid(row=0, column=0, padx=25, pady=25)
    btn2.grid(row=0, column=1, padx=25, pady=25)
    btn3.grid(row=0, column=2, padx=25, pady=25)

    for btn in [btn1, btn2, btn3]:
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)

    frame = ctk.CTkFrame(main_container, fg_color="#122448")

    ctk.CTkLabel(frame, text=title, font=ctk.CTkFont(size=24, weight="bold"), text_color="#6de0ff").pack(pady=40)
    ctk.CTkButton(frame, text="← Volver al Inicio", fg_color="#172b54", border_color="#6de0ff",
                  border_width=1, hover_color="#6de0ff", text_color="white",
                  command=lambda: show_frame_callback("Home")).pack(pady=20)
    ctk.CTkLabel(frame, text="Zona de vista previa / configuración", 
                 text_color="white", font=ctk.CTkFont(size=16)).pack(pady=20)
