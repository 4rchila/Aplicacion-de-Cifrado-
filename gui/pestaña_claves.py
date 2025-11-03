# pestaña_claves.py
import customtkinter as ctk
from tkinter import filedialog, messagebox
import os

from logic.claves import(
    generar_claves,
    guardar_claves, 
    cargar_clave_privada,
    cargar_clave_publica
)

class FrameClaves(ctk.CTkFrame):
    def __init__(self, parent, volver_callback):
        super().__init__(parent, fg_color="#F7EEDD")
        self.volver_callback = volver_callback

        ctk.CTkLabel(self, text="Gestión de Claves RSA",
                     font=ctk.CTkFont(size=24, weight="bold"),
                     text_color="#901F01").pack(pady=(20,10))

        ctk.CTkButton(self, text="Cargar clave privada",
                      fg_color="#DE6339", border_color="#8B4512",
                      border_width=2, text_color="#F7EEDD",
                      command=self.cargar_privada).pack(pady=10, padx=40, fill="x")

        ctk.CTkButton(self, text="Cargar clave pública",
                      fg_color="#DE6339", border_color="#8B4512",
                      border_width=2, text_color="#F7EEDD",
                      command=self.cargar_publica).pack(pady=10, padx=40, fill="x")

        ctk.CTkButton(self, text="Generar y guardar claves",
                      fg_color="#DE6339", border_color="#8B4512",
                      border_width=2, text_color="#F7EEDD",
                      command=self.generar_guardar).pack(pady=30, padx=40, fill="x")

        ctk.CTkButton(self, text="← Volver al menú",
                      fg_color="#901F01", hover_color="#C23B22",
                      text_color="white",
                      command=self.volver_callback).pack(pady=30)

    def cargar_privada(self):
        ruta = cargar_clave_privada()
        if ruta:
            messagebox.showinfo("Clave cargada", f"Privada: {os.path.basename(ruta)}")

    def cargar_publica(self):
        ruta = cargar_clave_publica()
        if ruta:
            messagebox.showinfo("Clave cargada", f"Pública: {os.path.basename(ruta)}")

    def generar_guardar(self):
        carpeta = filedialog.askdirectory(title="Selecciona carpeta")
        if not carpeta: return
        
        priv, pub = generar_claves()
        guardar_claves(priv, pub,
            os.path.join(carpeta,"clave_privada.pem"),
            os.path.join(carpeta,"clave_publica.pem")
        )

        messagebox.showinfo("Éxito","Claves generadas correctamente")
