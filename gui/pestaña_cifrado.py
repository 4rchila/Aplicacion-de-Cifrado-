# pestaña_cifrado.py
import customtkinter as ctk
from tkinter import messagebox
import sys
import os
from logic.cifrado import (
    cargar_claves_desde_archivos,
    cifrar_archivo,
    descifrar_archivo
)

class FrameCifrado(ctk.CTkFrame):
    def __init__(self, parent, volver_callback):
        super().__init__(parent, fg_color="#F7EEDD")
        self.volver_callback = volver_callback
        self.clave_privada = None
        self.clave_publica = None

        ctk.CTkLabel(self, text="Cifrado y Descifrado",
                     font=ctk.CTkFont(size=24, weight="bold"),
                     text_color="#901F01").pack(pady=20)

        ctk.CTkButton(self, text="Cargar claves (.pem)",
                      fg_color="#DE6339", border_color="#8B4512",
                      border_width=2, text_color="#F7EEDD",
                      command=self.cargar_claves).pack(pady=20, padx=60, fill="x")

        self.lbl_estado = ctk.CTkLabel(self, text="Claves no cargadas",
                                       text_color="#8B4512")
        self.lbl_estado.pack()

        ctk.CTkButton(self, text="Cifrar archivo",
                      fg_color="#DE6339", border_color="#8B4512",
                      border_width=2, text_color="#F7EEDD",
                      command=self.cifrar).pack(pady=20, padx=60, fill="x")

        ctk.CTkButton(self, text="Descifrar archivo",
                      fg_color="#DE6339", border_color="#8B4512",
                      border_width=2, text_color="#F7EEDD",
                      command=self.descifrar).pack(pady=20, padx=60, fill="x")

        ctk.CTkButton(self, text="← Volver al menú",
                      fg_color="#901F01", text_color="white",
                      command=self.volver_callback).pack(pady=40)

    def cargar_claves(self):
        self.clave_privada, self.clave_publica = cargar_claves_desde_archivos()
        if self.clave_privada and self.clave_publica:
            self.lbl_estado.configure(text="✅ Claves cargadas", text_color="#008000")
        else:
            self.lbl_estado.configure(text="❌ Error", text_color="red")

    def cifrar(self):
        if not self.clave_publica:
            return messagebox.showwarning("Atención","Primero carga las claves")
        cifrar_archivo(self.clave_publica)

    def descifrar(self):
        if not self.clave_privada:
            return messagebox.showwarning("Atención","Primero carga las claves")
        descifrar_archivo(self.clave_privada)
