import customtkinter as ctk
from PIL import Image
import os
import sys
from tkinter import filedialog, messagebox
from logic.claves import (
    generar_claves,
    guardar_claves,
    cargar_clave_privada,
    cargar_clave_publica
)
from gui.pestaña_cifrado import PestañaCifrado

class PanelLateral(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="#122448", corner_radius=15)
        self.grid_rowconfigure((0, 1, 2, 3, 4), weight=1)
        self.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            self, text="GESTIÓN DE CLAVES",
            text_color="#e76940", font=ctk.CTkFont(size=18, weight="bold")
        ).pack(pady=(25, 10))

        ctk.CTkLabel(
            self, text="Cargar claves RSA\npara usarlas en el sistema",
            text_color="white", justify="center"
        ).pack(pady=(0, 20))

        ctk.CTkButton(
            self, text="Cargar Clave Privada", fg_color="#1c3c6b", hover_color="#e76940",
            command=self._cargar_privada
        ).pack(pady=(0, 10), padx=20, fill="x")

        ctk.CTkButton(
            self, text="Cargar Clave Pública", fg_color="#1c3c6b", hover_color="#1a4d8f",
            command=self._cargar_publica
        ).pack(pady=(0, 20), padx=20, fill="x")

        # Estado visual
        self.ruta_privada = ctk.StringVar(value="No cargada")
        self.ruta_publica = ctk.StringVar(value="No cargada")

        ctk.CTkLabel(self, textvariable=self.ruta_privada, text_color="#ede4d3", wraplength=180).pack(pady=(5, 10))
        ctk.CTkLabel(self, textvariable=self.ruta_publica, text_color="#ede4d3", wraplength=180).pack(pady=(5, 20))

    def _cargar_privada(self):
        ruta = cargar_clave_privada()
        if ruta:
            self.ruta_privada.set(f"Privada cargada: {os.path.basename(ruta)}")

    def _cargar_publica(self):
        ruta = cargar_clave_publica()
        if ruta:
            self.ruta_publica.set(f"Pública cargada: {os.path.basename(ruta)}")

class FrameLlaves(ctk.CTkFrame):
    def __init__(self, parent, controlador):
        super().__init__(parent, fg_color="#f7eedd")
        self.controlador = controlador

        ctk.CTkLabel(
            self, text="CREACIÓN DE LLAVES RSA",
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color="#e76940"
        ).pack(pady=30)

        ctk.CTkButton(
            self, text="Generar y Guardar Claves",
            fg_color="#122448", hover_color="#1a4d8f",
            command=self._crear_llaves
        ).pack(pady=20)

        self.resultado = ctk.CTkLabel(self, text="", text_color="#122448", font=ctk.CTkFont(size=14))
        self.resultado.pack(pady=10)

        ctk.CTkButton(
            self, text="← Volver al Menú",
            fg_color="#172b54", border_color="#6de0ff", border_width=1,
            hover_color="#6de0ff", text_color="white",
            command=lambda: controlador.mostrar_frame("MenuCifrado")
        ).pack(pady=40)

    def _crear_llaves(self):
        carpeta = filedialog.askdirectory(title="Seleccionar carpeta para guardar las claves")
        if not carpeta:
            return

        ruta_privada = os.path.join(carpeta, "clave_privada.pem")
        ruta_publica = os.path.join(carpeta, "clave_publica.pem")

        try:
            priv, pub = generar_claves()
            guardar_claves(priv, pub, ruta_privada, ruta_publica)
            self.resultado.configure(text="Claves generadas y guardadas con éxito")
            messagebox.showinfo("Éxito", f"Claves guardadas en:\n{carpeta}")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron generar las claves:\n{e}")


class MenuCifradoFrame(ctk.CTkFrame):
    def __init__(self, parent, controlador):
        super().__init__(parent, fg_color="#f7eedd")
        self.controlador = controlador

        self.grid_rowconfigure((0, 1), weight=1)
        self.grid_columnconfigure((0, 1), weight=1)

        side_panel = PanelLateral(self)
        side_panel.grid(row=0, column=0, padx=(0, 30), pady=40, sticky="nsew")

        button_container = ctk.CTkFrame(self, fg_color="#122448", corner_radius=15)
        button_container.grid(row=0, column=1, pady=80, sticky="n")
        button_container.grid_rowconfigure(0, weight=1)
        button_container.grid_columnconfigure((0, 1), weight=1)

        icon_size = (50, 50)
        imagen_claves = Image.open("utils/102649.png")
        imagen_encriptado = Image.open("utils/2630160.png")

        file_ctk = ctk.CTkImage(dark_image=imagen_claves, light_image=imagen_claves, size=icon_size)
        img_ctk = ctk.CTkImage(dark_image=imagen_encriptado, light_image=imagen_encriptado, size=icon_size)

        btn1 = ctk.CTkButton(
            button_container, text="Creación de llaves\nPúblicas y Privadas",
            image=file_ctk, compound="top", width=160, height=130,
            fg_color="#172b54", border_color="#6de0ff",
            hover_color="#1a4d8f", border_width=1,
            font=ctk.CTkFont(size=14, weight="bold"),
            command=lambda: controlador.mostrar_frame("FrameLlaves")
        )

        btn2 = ctk.CTkButton(
            button_container, text="Encriptar Datos",
            image=img_ctk, compound="top", width=160, height=130,
            fg_color="#172b54", border_color="#6de0ff",
            hover_color="#1a4d8f", border_width=1,
            font=ctk.CTkFont(size=14, weight="bold"),
            command=lambda: controlador.mostrar_frame("FrameCifrado")
        )

        btn1.grid(row=0, column=0, padx=25, pady=25)
        btn2.grid(row=0, column=1, padx=25, pady=25)

class AppPrincipal(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Gestor de Claves y Cifrado")
        self.geometry("900x600")
        self.configure(fg_color="#122448")

        self.frames = {}

        for F in (MenuCifradoFrame, FrameLlaves):
            frame = F(self, self)
            self.frames[F.__name__] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        frame_cifrado = PestañaCifrado(self)
        self.frames["FrameCifrado"] = frame_cifrado
        frame_cifrado.grid(row=0, column=0, sticky="nsew")

        self.mostrar_frame("MenuCifrado")

    def mostrar_frame(self, nombre):
        frame = self.frames[nombre]
        frame.tkraise()


if __name__ == "__main__":
    app = AppPrincipal()
    app.mainloop()
