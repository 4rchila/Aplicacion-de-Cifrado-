import customtkinter as ctk
from gui.pestaña_firma import abrir_ventana_firma_digital  
from gui.pestaña_claves import FrameClaves
from gui.pestaña_cifrado import FrameCifrado

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

def on_enter(event):
    event.widget.configure(fg_color="#FF8051", text_color="#2C2C2C")

def on_leave(event):
    event.widget.configure(fg_color="#DE6339", text_color="#F7EEDD")

def create_home_frame(main_container, app, show_frame):
    frame = ctk.CTkFrame(main_container, fg_color="#F7EEDD")
    
    frame.grid_rowconfigure(0, weight=1)
    frame.grid_columnconfigure((0, 1, 2), weight=1)
    
    container = ctk.CTkFrame(frame, fg_color="#EDE4D3", corner_radius=15)
    container.grid(row=0, column=0, columnspan=3, padx=50, pady=50, sticky="nsew")
    container.grid_rowconfigure(0, weight=1)
    container.grid_columnconfigure((0, 1, 2), weight=1)
    
    ctk.CTkLabel(
        container, text="Claves, Cifrado y Firmas Digitales",
        text_color="#901F01", font=ctk.CTkFont(size=24, weight="bold")
    ).grid(row=0, column=0, columnspan=3, pady=(0, 40))
    
    btn1 = ctk.CTkButton(
        container, text="Gestión de claves", width=140, height=120,
        fg_color="#DE6339", border_color="#8B4512", border_width=2,
        font=ctk.CTkFont(size=16, weight="bold"), text_color="#F7EEDD",
        hover=False,
        command=lambda: show_frame("MenuClavesFrame")
    )
    
    btn2 = ctk.CTkButton(
        container, text="Cifrado y descifrado", width=140, height=120,
        fg_color="#DE6339", border_color="#8B4512", border_width=2,
        font=ctk.CTkFont(size=16, weight="bold"), text_color="#F7EEDD",
        hover=False,
        command=lambda: show_frame("PestañaCifrado")
    )
    
    btn3 = ctk.CTkButton(
        container, text="Firma digital", width=140, height=120,
        fg_color="#DE6339", border_color="#8B4512", border_width=2,
        font=ctk.CTkFont(size=16, weight="bold"), text_color="#F7EEDD",
        hover=False,
        command=lambda: abrir_ventana_firma_digital(app)
    )
    
    btn1.grid(row=1, column=0, padx=20, pady=20)
    btn2.grid(row=1, column=1, padx=20, pady=20)
    btn3.grid(row=1, column=2, padx=20, pady=20)
    
    for btn in (btn1, btn2, btn3):
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)
    
    ctk.CTkLabel(
        container, text="Selecciona una opción para comenzar",
        text_color="#8B4512", font=ctk.CTkFont(size=14)
    ).grid(row=2, column=0, columnspan=3, pady=(20, 0))
    
    return frame


app = ctk.CTk()
app.title("Panel de Control")
app.geometry("900x600")
app.configure(fg_color="#F7EEDD")

frames = {}

def show_frame(nombre):
    frame = frames[nombre]
    frame.tkraise()

header = ctk.CTkFrame(app, fg_color="#EDE4D3", height=80)
header.pack(fill="x")
header.pack_propagate(False)

ctk.CTkLabel(
    header, text="SISTEMA DE CIFRADO", text_color="#901F01",
    font=ctk.CTkFont(size=26, weight="bold")
).pack(side="left", padx=30, pady=15)

main_container = ctk.CTkFrame(app, fg_color="transparent")
main_container.pack(fill="both", expand=True, padx=30, pady=30)

home_frame = create_home_frame(main_container, app, show_frame)
home_frame.pack(fill="both", expand=True)

frames["MenuClavesFrame"] = FrameClaves(main_container, lambda: show_frame("home"))
frames["PestañaCifrado"] = FrameCifrado(main_container, lambda: show_frame("home"))

for fr in frames.values():
    fr.place(relwidth=1, relheight=1)

frames["home"] = home_frame
home_frame.tkraise()

app.mainloop()

