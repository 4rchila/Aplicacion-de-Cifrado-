from tkinter import filedialog, messagebox
from logic.claves import cargar_claves

def cargar_claves_desde_archivos():
    try:
        clave_privada, clave_publica = cargar_claves(
            "data/claves_privadas/clave_privada.pem",
            "data/claves_publicas/clave_publica.pem"
        )
        return clave_privada, clave_publica
    except Exception as e:
        messagebox.showerror("Error", f"No se pudieron cargar las claves:\n{e}")
        return None, None


def cifrar_archivo(clave_publica):
    try:
        from logic.cifrado import cifrar_archivo as cifrar

        ruta_archivo = filedialog.askopenfilename(
            title="Seleccionar archivo para cifrar",
            filetypes=[("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*")]
        )
        if not ruta_archivo:
            return

        cifrar(ruta_archivo, clave_publica)
        messagebox.showinfo("Éxito", "El archivo se cifró correctamente.")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo cifrar el archivo:\n{e}")


def descifrar_archivo(clave_privada):
    try:
        from logic.cifrado import descifrar_archivo as descifrar

        ruta_archivo = filedialog.askopenfilename(
            title="Seleccionar archivo para descifrar",
            filetypes=[("Archivos cifrados", "*.bin"), ("Todos los archivos", "*.*")]
        )
        if not ruta_archivo:
            return

        descifrar(ruta_archivo, clave_privada)
        messagebox.showinfo("Éxito", "El archivo se descifró correctamente.")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo descifrar el archivo:\n{e}")
