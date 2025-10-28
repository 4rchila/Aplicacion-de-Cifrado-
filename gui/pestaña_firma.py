import customtkinter as ctk
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization
from cryptography.exceptions import InvalidSignature
import tkinter as tk
from tkinter import filedialog, messagebox
import os

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

class FirmaDigitalLogic:
    
    def __init__(self):
        self.private_key = None
        self.public_key = None
    
    def generar_par_claves(self, tamaño_clave=2048):
        self.private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=tamaño_clave
        )
        self.public_key = self.private_key.public_key()
        return self.private_key, self.public_key
    
    def guardar_claves(self, archivo_privada, archivo_publica):
        if self.private_key is None or self.public_key is None:
            raise ValueError("Primero debe generar las claves")
        
        with open(archivo_privada, "wb") as f:
            f.write(self.private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption()
            ))
        
        with open(archivo_publica, "wb") as f:
            f.write(self.public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            ))
    
    def cargar_clave_privada(self, archivo_clave):
        with open(archivo_clave, "rb") as f:
            self.private_key = serialization.load_pem_private_key(
                f.read(),
                password=None
            )
    
    def cargar_clave_publica(self, archivo_clave):
        with open(archivo_clave, "rb") as f:
            self.public_key = serialization.load_pem_public_key(f.read())
    
    def firmar_archivo(self, archivo_entrada, archivo_salida=None):
        if self.private_key is None:
            raise ValueError("Primero debe cargar una clave privada")
        
        with open(archivo_entrada, "rb") as f:
            datos = f.read()
        
        firma = self.private_key.sign(
            datos,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        
        if archivo_salida is None:
            archivo_salida = archivo_entrada + ".firma"
        
        with open(archivo_salida, "wb") as f:
            f.write(firma)
        
        return firma, archivo_salida
    
    def verificar_firma(self, archivo_original, archivo_firma):
        if self.public_key is None:
            raise ValueError("Primero debe cargar una clave pública")
        
        with open(archivo_original, "rb") as f:
            datos_originales = f.read()
        
        with open(archivo_firma, "rb") as f:
            firma = f.read()
        
        try:
            self.public_key.verify(
                firma,
                datos_originales,
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )
            return True, "✓ FIRMA VÁLIDA: El archivo es auténtico y no ha sido modificado"
            
        except InvalidSignature:
            return False, "✗ FIRMA INVÁLIDA: El archivo ha sido modificado o la firma es incorrecta"

class ScrollableFrame(ctk.CTkScrollableFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

class VentanaFirmaDigital(ctk.CTkToplevel):
    
    def __init__(self, parent):
        super().__init__(parent)
        
        self.title("Sistema de Firma Digital")
        self.geometry("700x600")  
        self.configure(fg_color="#F7EEDD")
        self.resizable(True, True)
        
        self.transient(parent)
        self.grab_set()
        
        self.logica = FirmaDigitalLogic()
        self.crear_interfaz()
    
    def crear_interfaz(self):
        self.main_scrollable = ScrollableFrame(
            self, 
            fg_color="#F7EEDD",
            scrollbar_button_color="#8B4512",
            scrollbar_button_hover_color="#A0522D"
        )
        self.main_scrollable.pack(fill="both", expand=True, padx=10, pady=10)
        
        titulo = ctk.CTkLabel(
            self.main_scrollable, 
            text="Sistema de Firma Digital",
            text_color="#901F01",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        titulo.pack(pady=(0, 20))
        
        frame_claves = ctk.CTkFrame(self.main_scrollable, fg_color="#EDE4D3", corner_radius=15)
        frame_claves.pack(fill="x", pady=(0, 15), padx=10)
        
        ctk.CTkLabel(
            frame_claves,
            text="1. Gestión de Claves",
            text_color="#8B4512",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(anchor="w", padx=20, pady=(15, 10))
        
        btn_generar_claves = ctk.CTkButton(
            frame_claves,
            text="Generar Nuevas Claves",
            fg_color="#DE6339",
            hover_color="#FF8051",
            text_color="#F7EEDD",
            font=ctk.CTkFont(size=14),
            command=self.generar_claves
        )
        btn_generar_claves.pack(padx=20, pady=(0, 15))
        
        frame_cargar_claves = ctk.CTkFrame(frame_claves, fg_color="transparent")
        frame_cargar_claves.pack(fill="x", padx=20, pady=(0, 15))
        
        ctk.CTkLabel(
            frame_cargar_claves,
            text="Clave Privada:",
            text_color="#8B4512",
            font=ctk.CTkFont(size=12)
        ).pack(anchor="w")
        
        frame_privada = ctk.CTkFrame(frame_cargar_claves, fg_color="transparent")
        frame_privada.pack(fill="x", pady=(5, 10))
        
        self.entry_privada = ctk.CTkEntry(frame_privada, placeholder_text="Ruta de la clave privada...")
        self.entry_privada.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        btn_examinar_privada = ctk.CTkButton(
            frame_privada,
            text="Examinar",
            width=80,
            fg_color="#8B4512",
            hover_color="#A0522D",
            text_color="#F7EEDD",
            font=ctk.CTkFont(size=12),
            command=self.examinar_clave_privada
        )
        btn_examinar_privada.pack(side="right")
        
        ctk.CTkLabel(
            frame_cargar_claves,
            text="Clave Pública:",
            text_color="#8B4512",
            font=ctk.CTkFont(size=12)
        ).pack(anchor="w")
        
        frame_publica = ctk.CTkFrame(frame_cargar_claves, fg_color="transparent")
        frame_publica.pack(fill="x", pady=(5, 10))
        
        self.entry_publica = ctk.CTkEntry(frame_publica, placeholder_text="Ruta de la clave pública...")
        self.entry_publica.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        btn_examinar_publica = ctk.CTkButton(
            frame_publica,
            text="Examinar",
            width=80,
            fg_color="#8B4512",
            hover_color="#A0522D",
            text_color="#F7EEDD",
            font=ctk.CTkFont(size=12),
            command=self.examinar_clave_publica
        )
        btn_examinar_publica.pack(side="right")
        
        frame_firmar = ctk.CTkFrame(self.main_scrollable, fg_color="#EDE4D3", corner_radius=15)
        frame_firmar.pack(fill="x", pady=(0, 15), padx=10)
        
        ctk.CTkLabel(
            frame_firmar,
            text="2. Firmar Archivo",
            text_color="#8B4512",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(anchor="w", padx=20, pady=(15, 10))
        
        ctk.CTkLabel(
            frame_firmar,
            text="Archivo a firmar:",
            text_color="#8B4512",
            font=ctk.CTkFont(size=12)
        ).pack(anchor="w", padx=20)
        
        frame_archivo_firmar = ctk.CTkFrame(frame_firmar, fg_color="transparent")
        frame_archivo_firmar.pack(fill="x", padx=20, pady=(5, 15))
        
        self.entry_archivo_firmar = ctk.CTkEntry(frame_archivo_firmar, placeholder_text="Seleccione archivo para firmar...")
        self.entry_archivo_firmar.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        btn_examinar_firmar = ctk.CTkButton(
            frame_archivo_firmar,
            text="Examinar",
            width=80,
            fg_color="#8B4512",
            hover_color="#A0522D",
            text_color="#F7EEDD",
            font=ctk.CTkFont(size=12),
            command=self.examinar_archivo_firmar
        )
        btn_examinar_firmar.pack(side="right")
        
        btn_firmar = ctk.CTkButton(
            frame_firmar,
            text="Firmar Archivo",
            fg_color="#DE6339",
            hover_color="#FF8051",
            text_color="#F7EEDD",
            font=ctk.CTkFont(size=14, weight="bold"),
            command=self.firmar_archivo_gui
        )
        btn_firmar.pack(padx=20, pady=(0, 15))
        
        frame_verificar = ctk.CTkFrame(self.main_scrollable, fg_color="#EDE4D3", corner_radius=15)
        frame_verificar.pack(fill="x", pady=(0, 15), padx=10)
        
        ctk.CTkLabel(
            frame_verificar,
            text="3. Verificar Firma",
            text_color="#8B4512",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(anchor="w", padx=20, pady=(15, 10))
        
        ctk.CTkLabel(
            frame_verificar,
            text="Archivo original:",
            text_color="#8B4512",
            font=ctk.CTkFont(size=12)
        ).pack(anchor="w", padx=20)
        
        frame_archivo_original = ctk.CTkFrame(frame_verificar, fg_color="transparent")
        frame_archivo_original.pack(fill="x", padx=20, pady=(5, 10))
        
        self.entry_archivo_original = ctk.CTkEntry(frame_archivo_original, placeholder_text="Seleccione archivo original...")
        self.entry_archivo_original.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        btn_examinar_original = ctk.CTkButton(
            frame_archivo_original,
            text="Examinar",
            width=80,
            fg_color="#8B4512",
            hover_color="#A0522D",
            text_color="#F7EEDD",
            font=ctk.CTkFont(size=12),
            command=self.examinar_archivo_original
        )
        btn_examinar_original.pack(side="right")
        
        ctk.CTkLabel(
            frame_verificar,
            text="Archivo de firma:",
            text_color="#8B4512",
            font=ctk.CTkFont(size=12)
        ).pack(anchor="w", padx=20, pady=(5, 0))
        
        frame_archivo_firma = ctk.CTkFrame(frame_verificar, fg_color="transparent")
        frame_archivo_firma.pack(fill="x", padx=20, pady=(5, 15))
        
        self.entry_archivo_firma = ctk.CTkEntry(frame_archivo_firma, placeholder_text="Seleccione archivo de firma...")
        self.entry_archivo_firma.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        btn_examinar_firma = ctk.CTkButton(
            frame_archivo_firma,
            text="Examinar",
            width=80,
            fg_color="#8B4512",
            hover_color="#A0522D",
            text_color="#F7EEDD",
            font=ctk.CTkFont(size=12),
            command=self.examinar_archivo_firma
        )
        btn_examinar_firma.pack(side="right")
        
        btn_verificar = ctk.CTkButton(
            frame_verificar,
            text="Verificar Firma",
            fg_color="#DE6339",
            hover_color="#FF8051",
            text_color="#F7EEDD",
            font=ctk.CTkFont(size=14, weight="bold"),
            command=self.verificar_firma_gui
        )
        btn_verificar.pack(padx=20, pady=(0, 15))
        
        frame_resultados = ctk.CTkFrame(self.main_scrollable, fg_color="#EDE4D3", corner_radius=15)
        frame_resultados.pack(fill="x", pady=(0, 15), padx=10)
        
        ctk.CTkLabel(
            frame_resultados,
            text="Resultados",
            text_color="#8B4512",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(anchor="w", padx=20, pady=(15, 10))
        
        self.texto_resultados = ctk.CTkTextbox(
            frame_resultados,
            fg_color="#F7EEDD",
            text_color="#2C2C2C",
            font=ctk.CTkFont(size=12),
            wrap="word",
            height=150  
        )
        self.texto_resultados.pack(fill="x", padx=20, pady=(0, 15))
        
        btn_limpiar = ctk.CTkButton(
            frame_resultados,
            text="Limpiar Resultados",
            fg_color="#8B4512",
            hover_color="#A0522D",
            text_color="#F7EEDD",
            font=ctk.CTkFont(size=12),
            command=self.limpiar_resultados
        )
        btn_limpiar.pack(padx=20, pady=(0, 15))
        
        self.label_estado = ctk.CTkLabel(
            self.main_scrollable,
            text="Estado: No hay claves cargadas",
            text_color="#901F01",
            font=ctk.CTkFont(size=12, weight="bold")
        )
        self.label_estado.pack(pady=(10, 20))
    
    def agregar_resultado(self, mensaje, es_error=False):
        color = "#901F01" if es_error else "#2C2C2C"
        self.texto_resultados.insert("end", f"{mensaje}\n")
        self.texto_resultados.see("end")
        self.update()
    
    def limpiar_resultados(self):
        self.texto_resultados.delete("1.0", "end")
    
    def actualizar_estado_claves(self):
        privada = self.logica.private_key is not None
        publica = self.logica.public_key is not None
        
        if privada and publica:
            self.label_estado.configure(text="Estado: Claves cargadas ✓", text_color="#2E8B57")
        elif privada:
            self.label_estado.configure(text="Estado: Solo clave privada cargada", text_color="#DE6339")
        elif publica:
            self.label_estado.configure(text="Estado: Solo clave pública cargada", text_color="#8B4512")
        else:
            self.label_estado.configure(text="Estado: No hay claves cargadas", text_color="#901F01")
    
    def examinar_clave_privada(self):
        archivo = filedialog.askopenfilename(
            title="Seleccionar clave privada",
            filetypes=[("Archivos PEM", "*.pem"), ("Todos los archivos", "*.*")]
        )
        if archivo:
            self.entry_privada.delete(0, "end")
            self.entry_privada.insert(0, archivo)
            self.cargar_clave_privada_gui(archivo)
    
    def examinar_clave_publica(self):
        archivo = filedialog.askopenfilename(
            title="Seleccionar clave pública",
            filetypes=[("Archivos PEM", "*.pem"), ("Todos los archivos", "*.*")]
        )
        if archivo:
            self.entry_publica.delete(0, "end")
            self.entry_publica.insert(0, archivo)
            self.cargar_clave_publica_gui(archivo)
    
    def examinar_archivo_firmar(self):
        archivo = filedialog.askopenfilename(
            title="Seleccionar archivo a firmar",
            filetypes=[("Todos los archivos", "*.*")]
        )
        if archivo:
            self.entry_archivo_firmar.delete(0, "end")
            self.entry_archivo_firmar.insert(0, archivo)
    
    def examinar_archivo_original(self):
        archivo = filedialog.askopenfilename(
            title="Seleccionar archivo original",
            filetypes=[("Todos los archivos", "*.*")]
        )
        if archivo:
            self.entry_archivo_original.delete(0, "end")
            self.entry_archivo_original.insert(0, archivo)
    
    def examinar_archivo_firma(self):
        archivo = filedialog.askopenfilename(
            title="Seleccionar archivo de firma",
            filetypes=[("Archivos de firma", "*.firma"), ("Todos los archivos", "*.*")]
        )
        if archivo:
            self.entry_archivo_firma.delete(0, "end")
            self.entry_archivo_firma.insert(0, archivo)
    
    def generar_claves(self):
        try:
            self.agregar_resultado("Generando nuevo par de claves...")
            
            self.logica.generar_par_claves()
            
            archivo_privada = filedialog.asksaveasfilename(
                title="Guardar clave privada como",
                defaultextension=".pem",
                filetypes=[("Archivos PEM", "*.pem")]
            )
            
            if archivo_privada:
                archivo_publica = filedialog.asksaveasfilename(
                    title="Guardar clave pública como",
                    defaultextension=".pem",
                    filetypes=[("Archivos PEM", "*.pem")]
                )
                
                if archivo_publica:
                    self.logica.guardar_claves(archivo_privada, archivo_publica)
                    
                    self.entry_privada.delete(0, "end")
                    self.entry_privada.insert(0, archivo_privada)
                    self.entry_publica.delete(0, "end")
                    self.entry_publica.insert(0, archivo_publica)
                    
                    self.agregar_resultado(f"✓ Clave privada guardada en: {archivo_privada}")
                    self.agregar_resultado(f"✓ Clave pública guardada en: {archivo_publica}")
                    self.agregar_resultado("✓ Par de claves generado exitosamente")
            
            self.actualizar_estado_claves()
            
        except Exception as e:
            self.agregar_resultado(f"✗ Error al generar claves: {str(e)}", True)
    
    def cargar_clave_privada_gui(self, archivo):
        try:
            self.logica.cargar_clave_privada(archivo)
            self.agregar_resultado(f"✓ Clave privada cargada: {archivo}")
            self.actualizar_estado_claves()
        except Exception as e:
            self.agregar_resultado(f"✗ Error al cargar clave privada: {str(e)}", True)
    
    def cargar_clave_publica_gui(self, archivo):
        try:
            self.logica.cargar_clave_publica(archivo)
            self.agregar_resultado(f"✓ Clave pública cargada: {archivo}")
            self.actualizar_estado_claves()
        except Exception as e:
            self.agregar_resultado(f"✗ Error al cargar clave pública: {str(e)}", True)
    
    def firmar_archivo_gui(self):
        archivo = self.entry_archivo_firmar.get()
        
        if not archivo:
            messagebox.showerror("Error", "Por favor, seleccione un archivo para firmar")
            return
        
        if not self.logica.private_key:
            messagebox.showerror("Error", "Primero debe cargar una clave privada")
            return
        
        try:
            self.agregar_resultado(f"Firmando archivo: {archivo}")
            
            firma, archivo_firma = self.logica.firmar_archivo(archivo)
            
            self.agregar_resultado(f"✓ Firma guardada en: {archivo_firma}")
            self.agregar_resultado("✓ Archivo firmado exitosamente")
            
            self.entry_archivo_firma.delete(0, "end")
            self.entry_archivo_firma.insert(0, archivo_firma)
            
        except Exception as e:
            self.agregar_resultado(f"✗ Error al firmar archivo: {str(e)}", True)
    
    def verificar_firma_gui(self):
        archivo_original = self.entry_archivo_original.get()
        archivo_firma = self.entry_archivo_firma.get()
        
        if not archivo_original or not archivo_firma:
            messagebox.showerror("Error", "Por favor, seleccione ambos archivos (original y firma)")
            return
        
        if not self.logica.public_key:
            messagebox.showerror("Error", "Primero debe cargar una clave pública")
            return
        
        try:
            self.agregar_resultado(f"Verificando firma...")
            self.agregar_resultado(f"Archivo original: {archivo_original}")
            self.agregar_resultado(f"Archivo de firma: {archivo_firma}")
            
            es_valida, mensaje = self.logica.verificar_firma(archivo_original, archivo_firma)
            
            if es_valida:
                self.agregar_resultado("✅ " + mensaje)
                messagebox.showinfo("Resultado", mensaje)
            else:
                self.agregar_resultado("❌ " + mensaje)
                messagebox.showerror("Resultado", mensaje)
            
        except Exception as e:
            self.agregar_resultado(f"✗ Error al verificar firma: {str(e)}", True)

def abrir_ventana_firma_digital(parent):
    """Abre la ventana de firma digital desde el archivo principal"""
    ventana = VentanaFirmaDigital(parent)
    return ventana

if __name__ == "__main__":
    app = ctk.CTk()
    abrir_ventana_firma_digital(app)
    app.mainloop()