import customtkinter as ctk
from PIL import Image
import os
from tkinter import filedialog, messagebox
import time
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

def cifrar_llaves_frame(main_container, show_frame_callback):
    frame = ctk.CTkFrame(main_container, fg_color="#f7eedd")
    
    selected_file_path = ctk.StringVar(value="")

    def select_file():
        file_path = filedialog.askopenfilename(
            title="Seleccionar archivo",
            filetypes=[
                ("Archivos de texto", "*.txt"),
            ]
        )
        if file_path:
            selected_file_path.set(file_path)
            file_name = os.path.basename(file_path)
            file_size = os.path.getsize(file_path) / 1024  