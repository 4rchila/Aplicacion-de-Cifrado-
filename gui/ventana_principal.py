import customtkinter as ctk
from pestaña_firma import abrir_ventana_firma_digital  

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

def on_enter(event):
    event.widget.configure(
        fg_color="#FF8051",
        text_color="#2C2C2C"
    )

def on_leave(event):
    event.widget.configure(
        fg_color="#DE6339",
        text_color="#F7EEDD"
    )

def create_home_frame(main_container, app):
    frame = ctk.CTkFrame(main_container, fg_color="#F7EEDD")
    
    frame.grid_rowconfigure(0, weight=1)
    frame.grid_columnconfigure((0, 1, 2), weight=1)
    
    button_container = ctk.CTkFrame(frame, fg_color="#EDE4D3", corner_radius=15)
    button_container.grid(row=0, column=0, columnspan=3, padx=50, pady=50, sticky="nsew")
    button_container.grid_rowconfigure(0, weight=1)
    button_container.grid_columnconfigure((0, 1, 2), weight=1)
    
    ctk.CTkLabel(
        button_container,
        text="Claves, Cifrado y firmas digitales",
        text_color="#901F01",
        font=ctk.CTkFont(size=24, weight="bold")
    ).grid(row=0, column=0, columnspan=3, pady=(0, 40))
    
    btn1 = ctk.CTkButton(
        button_container, 
        text="Gestión de claves", 
        width=140, 
        height=120, 
        fg_color="#DE6339", 
        border_color="#8B4512",
        border_width=2, 
        font=ctk.CTkFont(size=16, weight="bold"),
        hover=False,
        text_color="#F7EEDD"
    )
    
    btn2 = ctk.CTkButton(
        button_container, 
        text="Cifrado y descifrado", 
        width=140, 
        height=120, 
        fg_color="#DE6339", 
        border_color="#8B4512",
        border_width=2, 
        font=ctk.CTkFont(size=16, weight="bold"),
        hover=False,
        text_color="#F7EEDD"
    )
    
    btn3 = ctk.CTkButton(
        button_container, 
        text="Firma digital", 
        width=140, 
        height=120, 
        fg_color="#DE6339", 
        border_color="#8B4512",
        border_width=2, 
        font=ctk.CTkFont(size=16, weight="bold"),
        hover=False,
        text_color="#F7EEDD",
        command=lambda: abrir_ventana_firma_digital(app)  # ¡LLAMADA AL MÓDULO!
    )
    
    btn1.grid(row=1, column=0, padx=20, pady=20)
    btn2.grid(row=1, column=1, padx=20, pady=20)
    btn3.grid(row=1, column=2, padx=20, pady=20)
    
    ctk.CTkLabel(
        button_container,
        text="Selecciona una opción para comenzar",
        text_color="#8B4512",
        font=ctk.CTkFont(size=14)
    ).grid(row=2, column=0, columnspan=3, pady=(20, 0))
    
    for btn in [btn1, btn2, btn3]:
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)
    
    return frame

app = ctk.CTk()
app.title("Panel de Control")
app.geometry("900x600")
app.configure(fg_color="#F7EEDD")

header_frame = ctk.CTkFrame(app, fg_color="#EDE4D3", corner_radius=0, height=80)
header_frame.pack(fill="x")
header_frame.pack_propagate(False)

header_content = ctk.CTkFrame(header_frame, fg_color="transparent")
header_content.pack(fill="both", padx=30, pady=15)

ctk.CTkLabel(
    header_content, 
    text="SISTEMA DE CIFRADO", 
    text_color="#901F01",
    font=ctk.CTkFont(size=26, weight="bold")
).pack(side="left")

status_frame = ctk.CTkFrame(header_content, fg_color="transparent")
status_frame.pack(side="right")

ctk.CTkLabel(
    status_frame,
    text="Estado del Sistema",
    text_color="#8B4512",
    font=ctk.CTkFont(size=12)
).pack(anchor="e")

ctk.CTkLabel(
    status_frame,
    text="🟢 Conectado",
    text_color="#901F01",
    font=ctk.CTkFont(size=14, weight="bold")
).pack(anchor="e")

main_container = ctk.CTkFrame(app, fg_color="transparent")
main_container.pack(fill="both", expand=True, padx=30, pady=30)

home_frame = create_home_frame(main_container, app)
home_frame.pack(fill="both", expand=True)

info_frame = ctk.CTkFrame(main_container, fg_color="#FFD199", corner_radius=10)
info_frame.pack(fill="x", pady=(20, 0))

ctk.CTkLabel(
    info_frame,
    text="💡 Sistema de cifrado - Listo para usar",
    text_color="#2C2C2C",
    font=ctk.CTkFont(size=12)
).pack(pady=15)

footer_frame = ctk.CTkFrame(app, fg_color="#EDE4D3", corner_radius=0, height=60)
footer_frame.pack(fill="x", side="bottom")
footer_frame.pack_propagate(False)

ctk.CTkLabel(
    footer_frame,
    text="Proyecto IV, Estructura de Datos II",
    text_color="#8B4512",
    font=ctk.CTkFont(size=12)
).pack(pady=20)

app.mainloop()