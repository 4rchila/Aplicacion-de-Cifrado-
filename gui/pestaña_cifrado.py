import customtkinter as ctk
from tkinter import messagebox
from logic.cifrado import (
    cargar_claves_desde_archivos,
    cifrar_archivo,
    descifrar_archivo
)

class PestañaCifrado(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.configure(fg_color="#f7eedd", corner_radius=10)
        self.grid_rowconfigure(3, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.clave_privada = None
        self.clave_publica = None

        ctk.CTkLabel(
            self,
            text="Cifrado y Descifrado de Archivos",
            text_color="#e76940",
            font=ctk.CTkFont(size=20, weight="bold")
        ).pack(pady=(20, 10))

        claves_frame = ctk.CTkFrame(self, fg_color="#f7eedd", corner_radius=10)
        claves_frame.pack(pady=20, padx=20, fill="x")

        ctk.CTkLabel(
            claves_frame,
            text="Cargar claves para cifrar o descifrar:",
            text_color="white",
            font=ctk.CTkFont(size=14)
        ).pack(pady=(10, 5))

        ctk.CTkButton(
            claves_frame,
            text="Cargar Claves (.pem)",
            fg_color="#f7eedd",
            hover_color="#e76940",
            command=self.cargar_claves
        ).pack(pady=(5, 15))

        self.lbl_estado_claves = ctk.CTkLabel(
            claves_frame,
            text="Claves no cargadas.",
            text_color="#c8e2ff"
        )
        self.lbl_estado_claves.pack(pady=(0, 10))

        acciones_frame = ctk.CTkFrame(self, fg_color="#f7eedd", corner_radius=10)
        acciones_frame.pack(pady=20, padx=20, fill="both", expand=True)

        ctk.CTkLabel(
            acciones_frame,
            text="Seleccione una acción:",
            text_color="white",
            font=ctk.CTkFont(size=14)
        ).pack(pady=(15, 5))

        ctk.CTkButton(
            acciones_frame,
            text="Cifrar Archivo",
            fg_color="#f7eedd",
            hover_color="#e76940",
            command=self.cifrar
        ).pack(pady=(10, 10), padx=60, fill="x")

        ctk.CTkButton(
            acciones_frame,
            text="Descifrar Archivo",
            fg_color="#f7eedd",
            hover_color="#e76940",
            command=self.descifrar
        ).pack(pady=(10, 20), padx=60, fill="x")

        self.info_label = ctk.CTkLabel(
            acciones_frame,
            text="Seleccione un archivo .txt para cifrar o .bin para descifrar.",
            text_color="#b4c7e7",
            wraplength=450,
            justify="center"
        )
        self.info_label.pack(pady=(10, 15))

    def cargar_claves(self):
        self.clave_privada, self.clave_publica = cargar_claves_desde_archivos()
        if self.clave_privada and self.clave_publica:
            self.lbl_estado_claves.configure(
                text="Claves cargadas correctamente",
                text_color="#e76940"
            )
        else:
            self.lbl_estado_claves.configure(
                text="Error al cargar las claves",
                text_color="red"
            )

    def cifrar(self):
        if not self.clave_publica:
            messagebox.showwarning("Advertencia", "Primero carga las claves.")
            return
        cifrar_archivo(self.clave_publica)

    def descifrar(self):
        if not self.clave_privada:
            messagebox.showwarning("Advertencia", "Primero carga las claves.")
            return
        descifrar_archivo(self.clave_privada)
