import os
from tkinter import filedialog, messagebox
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

def cargar_claves(ruta_privada, ruta_publica):
    try:
        with open(ruta_privada, "rb") as f:
            clave_privada = serialization.load_pem_private_key(f.read(), password=None)
        with open(ruta_publica, "rb") as f:
            clave_publica = serialization.load_pem_public_key(f.read())
        return clave_privada, clave_publica
    except Exception as e:
        messagebox.showerror("Error", f"No se pudieron cargar las claves:\n{e}")
        return None, None

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


def cargar_clave_privada():
    ruta = filedialog.askopenfilename(
        title="Seleccionar clave privada",
        filetypes=[("Archivos PEM", "*.pem")]
    )
    if not ruta:
        return None

    try:
        with open(ruta, "rb") as f:
            serialization.load_pem_private_key(f.read(), password=None)
        messagebox.showinfo("Éxito", "Clave privada cargada correctamente.")
        return ruta
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo cargar la clave privada:\n{e}")
        return None


def cargar_clave_publica():
    ruta = filedialog.askopenfilename(
        title="Seleccionar clave pública",
        filetypes=[("Archivos PEM", "*.pem")]
    )
    if not ruta:
        return None

    try:
        with open(ruta, "rb") as f:
            serialization.load_pem_public_key(f.read())
        messagebox.showinfo("Éxito", "Clave pública cargada correctamente.")
        return ruta
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo cargar la clave pública:\n{e}")
        return None
