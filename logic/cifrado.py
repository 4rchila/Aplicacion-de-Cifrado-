# logic/cifrado.py
import os
import glob
from tkinter import filedialog, messagebox
from logic.claves import cargar_claves
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding

DATA_PRIV = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "claves_privadas")
DATA_PUB = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "claves_publicas")

def _buscar_pares_claves():
    """
    Busca pares de claves *_private.pem y *_public.pem en las carpetas data.
    Devuelve una lista de tuplas (nombre_base, ruta_priv, ruta_pub).
    """
    pares = []
    priv_files = glob.glob(os.path.join(DATA_PRIV, "*_private.pem"))
    for p in priv_files:
        base = os.path.basename(p).rsplit("_private.pem", 1)[0]
        pub_candidate = os.path.join(DATA_PUB, f"{base}_public.pem")
        if os.path.exists(pub_candidate):
            pares.append((base, p, pub_candidate))
    return pares

def cargar_claves_desde_archivos():
    """
    Intenta cargar automáticamente un par de claves si solo hay uno.
    Si hay varios o ninguno, abre diálogos para seleccionar los archivos.
    Devuelve (clave_privada_obj, clave_publica_obj) o (None, None) en error.
    """
    try:
        os.makedirs(DATA_PRIV, exist_ok=True)
        os.makedirs(DATA_PUB, exist_ok=True)

        pares = _buscar_pares_claves()

        # Si existe exactamente un par, lo cargamos automáticamente
        if len(pares) == 1:
            _, ruta_priv, ruta_pub = pares[0]
            priv, pub = cargar_claves(ruta_priv, ruta_pub)
            if priv and pub:
                return priv, pub
            else:
                messagebox.showerror("Error", "No se pudo cargar el par de claves detectado automáticamente.")
                return None, None

        # Si hay múltiples pares — pedir al usuario elegir uno de cada carpeta
        if len(pares) > 1:
            # Preguntar al usuario qué par quiere (puede elegirse la privada y pública independientemente)
            # Primero seleccionamos la clave privada desde la carpeta de privadas (constructor del diálogo pone el folder)
            ruta_priv = filedialog.askopenfilename(
                title="Seleccionar clave privada (.pem)",
                initialdir=DATA_PRIV,
                filetypes=[("Archivos PEM", "*.pem")]
            )
            if not ruta_priv:
                return None, None

            ruta_pub = filedialog.askopenfilename(
                title="Seleccionar clave pública (.pem)",
                initialdir=DATA_PUB,
                filetypes=[("Archivos PEM", "*.pem")]
            )
            if not ruta_pub:
                return None, None

            priv, pub = cargar_claves(ruta_priv, ruta_pub)
            return priv, pub

        # Si no se encontró ningún par, verificamos si existen archivos sueltos en las carpetas
        # y permitimos al usuario seleccionarlos manualmente.
        # Mostrar diálogo para la privada (por si existe)
        ruta_priv = filedialog.askopenfilename(
            title="Seleccionar clave privada (.pem)",
            initialdir=DATA_PRIV,
            filetypes=[("Archivos PEM", "*.pem")]
        )
        if not ruta_priv:
            # el usuario canceló (o no hay)
            messagebox.showwarning("Cancelado", "No se seleccionó clave privada.")
            return None, None

        ruta_pub = filedialog.askopenfilename(
            title="Seleccionar clave pública (.pem)",
            initialdir=DATA_PUB,
            filetypes=[("Archivos PEM", "*.pem")]
        )
        if not ruta_pub:
            messagebox.showwarning("Cancelado", "No se seleccionó clave pública.")
            return None, None

        priv, pub = cargar_claves(ruta_priv, ruta_pub)
        return priv, pub

    except Exception as e:
        messagebox.showerror("Error", f"No se pudieron cargar las claves:\n{e}")
        return None, None


def cifrar_archivo(clave_publica):
    """
    Pide archivo a cifrar, cifra su contenido con la clave pública (RSA OAEP)
    y guarda el resultado en <archivo>.bin
    """
    try:
        if clave_publica is None:
            messagebox.showwarning("Atención", "Clave pública no proporcionada.")
            return

        ruta_archivo = filedialog.askopenfilename(
            title="Seleccionar archivo para cifrar",
            filetypes=[("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*")]
        )
        if not ruta_archivo:
            return

        # Leer todo el archivo (funciona para archivos pequeños/medianos)
        with open(ruta_archivo, "rb") as f:
            datos = f.read()

        # RSA OAEP (nota: RSA puede cifrar hasta cierto tamaño; para archivos grandes usar híbrido)
        cifrado = clave_publica.encrypt(
            datos,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

        salida = ruta_archivo + ".bin"
        with open(salida, "wb") as f:
            f.write(cifrado)

        messagebox.showinfo("Éxito", f"Archivo cifrado correctamente:\n{salida}")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo cifrar el archivo:\n{e}")


def descifrar_archivo(clave_privada):
    """
    Pide archivo .bin cifrado con cifrar_archivo y lo descifra con la clave privada RSA OAEP.
    Guarda el contenido descifrado en <archivo>.dec (misma extensión original no se recupera).
    """
    try:
        if clave_privada is None:
            messagebox.showwarning("Atención", "Clave privada no proporcionada.")
            return

        ruta_archivo = filedialog.askopenfilename(
            title="Seleccionar archivo cifrado para descifrar",
            filetypes=[("Archivos cifrados", "*.bin"), ("Todos los archivos", "*.*")]
        )
        if not ruta_archivo:
            return

        with open(ruta_archivo, "rb") as f:
            datos_cifrados = f.read()

        datos_descifrados = clave_privada.decrypt(
            datos_cifrados,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

        salida = ruta_archivo + ".dec"
        with open(salida, "wb") as f:
            f.write(datos_descifrados)

        messagebox.showinfo("Éxito", f"Archivo descifrado correctamente:\n{salida}")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo descifrar el archivo:\n{e}")
