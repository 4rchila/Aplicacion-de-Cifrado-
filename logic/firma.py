import hashlib
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization
from cryptography.exceptions import InvalidSignature
import os

from hash_utils import FNV1Hash

class FirmaDigital:
    def __init__(self):
        self.private_key = None
        self.public_key = None
        self.hash_algorithm = "sha256"  
    
    def set_hash_algorithm(self, algorithm):
        """
        Establece el algoritmo de hash a usar
        Opciones: 'sha256', 'fnv1_32', 'fnv1_64', 'fnv1a_32', 'fnv1a_64'
        """
        valid_algorithms = ['sha256', 'fnv1_32', 'fnv1_64', 'fnv1a_32', 'fnv1a_64']
        if algorithm not in valid_algorithms:
            raise ValueError(f"Algoritmo no válido. Opciones: {valid_algorithms}")
        
        self.hash_algorithm = algorithm
        print(f"✓ Algoritmo de hash cambiado a: {algorithm}")
    
    def _calcular_hash(self, data):
        if self.hash_algorithm == 'sha256':
            return hashes.Hash(hashes.SHA256())
        elif self.hash_algorithm.startswith('fnv'):
            bits = 32 if '32' in self.hash_algorithm else 64
            
            if 'fnv1a' in self.hash_algorithm:
                hash_value = FNV1Hash.fnv1a(data, bits)
            else:
                hash_value = FNV1Hash.fnv1(data, bits)
            
            return hash_value.to_bytes(bits // 8, byteorder='big')
        else:
            raise ValueError("Algoritmo de hash no soportado")
    
    def _get_padding_scheme(self):
        if self.hash_algorithm == 'sha256':
            return padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ), hashes.SHA256()
        else:
            return padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ), hashes.SHA256()
    
    def generar_par_claves(self, tamaño_clave=2048):
        print("Generando par de claves...")
        self.private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=tamaño_clave
        )
        self.public_key = self.private_key.public_key()
        print("✓ Par de claves generado exitosamente")
        return self.private_key, self.public_key
    
    def guardar_claves(self, nombre_archivo_privada="clave_privada.pem", 
                      nombre_archivo_publica="clave_publica.pem"):
        if self.private_key is None or self.public_key is None:
            raise ValueError("Primero debe generar las claves")
        
        with open(nombre_archivo_privada, "wb") as f:
            f.write(self.private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption()
            ))
        
        with open(nombre_archivo_publica, "wb") as f:
            f.write(self.public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            ))
        
        print(f"✓ Claves guardadas en '{nombre_archivo_privada}' y '{nombre_archivo_publica}'")
    
    def cargar_clave_privada(self, archivo_clave):
        with open(archivo_clave, "rb") as f:
            self.private_key = serialization.load_pem_private_key(
                f.read(),
                password=None
            )
        print(f"✓ Clave privada cargada desde '{archivo_clave}'")
    
    def cargar_clave_publica(self, archivo_clave):
        with open(archivo_clave, "rb") as f:
            self.public_key = serialization.load_pem_public_key(
                f.read()
            )
        print(f"✓ Clave pública cargada desde '{archivo_clave}'")
    
    def calcular_hash_archivo(self, archivo_entrada):
        if not os.path.exists(archivo_entrada):
            raise FileNotFoundError(f"El archivo '{archivo_entrada}' no existe")
        
        with open(archivo_entrada, "rb") as f:
            datos = f.read()
        
        if self.hash_algorithm == 'sha256':
            hash_obj = hashlib.sha256(datos)
            hash_value = hash_obj.hexdigest()
        else:
            bits = 32 if '32' in self.hash_algorithm else 64
            if 'fnv1a' in self.hash_algorithm:
                hash_int = FNV1Hash.fnv1a(datos, bits)
            else:
                hash_int = FNV1Hash.fnv1(datos, bits)
            hash_value = hex(hash_int)
        
        print(f"Hash ({self.hash_algorithm}) de '{archivo_entrada}': {hash_value}")
        return hash_value
    
    def firmar_archivo(self, archivo_entrada, archivo_salida=None):
        if self.private_key is None:
            raise ValueError("Primero debe cargar una clave privada")
        
        if not os.path.exists(archivo_entrada):
            raise FileNotFoundError(f"El archivo '{archivo_entrada}' no existe")
        
        with open(archivo_entrada, "rb") as f:
            datos = f.read()
        
        print(f"Firmando archivo '{archivo_entrada}' con {self.hash_algorithm}...")
        
        self.calcular_hash_archivo(archivo_entrada)
        
        padding_scheme, hash_obj = self._get_padding_scheme()
        
        firma = self.private_key.sign(
            datos,
            padding_scheme,
            hash_obj
        )
        
        if archivo_salida is None:
            archivo_salida = archivo_entrada + ".firma"
        
        with open(archivo_salida, "wb") as f:
            f.write(firma)
        
        print(f"✓ Firma guardada en '{archivo_salida}'")
        return firma
    
    def verificar_firma(self, archivo_original, archivo_firma):
        if self.public_key is None:
            raise ValueError("Primero debe cargar una clave pública")
        
        if not os.path.exists(archivo_original):
            raise FileNotFoundError(f"El archivo '{archivo_original}' no existe")
        
        if not os.path.exists(archivo_firma):
            raise FileNotFoundError(f"El archivo de firma '{archivo_firma}' no existe")
        
        with open(archivo_original, "rb") as f:
            datos_originales = f.read()
        
        with open(archivo_firma, "rb") as f:
            firma = f.read()
        
        print(f"Verificando firma para '{archivo_original}'...")
        
        self.calcular_hash_archivo(archivo_original)
        
        try:
            padding_scheme, hash_obj = self._get_padding_scheme()
            
            self.public_key.verify(
                firma,
                datos_originales,
                padding_scheme,
                hash_obj
            )
            print("✓ FIRMA VÁLIDA: El archivo es auténtico y no ha sido modificado")
            return True
            
        except InvalidSignature:
            print("✗ FIRMA INVÁLIDA: El archivo ha sido modificado o la firma es incorrecta")
            return False

def mostrar_menu():
    print("\n" + "="*50)
    print("          SISTEMA DE FIRMA DIGITAL")
    print("="*50)
    print("1. Generar nuevo par de claves")
    print("2. Cambiar algoritmo de hash")
    print("3. Calcular hash de archivo")
    print("4. Firmar un archivo")
    print("5. Verificar firma de archivo")
    print("6. Salir")
    print("-"*50)

def main():
    firma_digital = FirmaDigital()
    
    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción (1-6): ").strip()
        
        if opcion == "1":
            try:
                firma_digital.generar_par_claves()
                firma_digital.guardar_claves()
            except Exception as e:
                print(f"Error: {e}")
        
        elif opcion == "2":
            try:
                print("\nAlgoritmos de hash disponibles:")
                print("1. SHA-256 (estándar, recomendado)")
                print("2. FNV-1 32-bit")
                print("3. FNV-1 64-bit")
                print("4. FNV-1a 32-bit (mejor distribución)")
                print("5. FNV-1a 64-bit (mejor distribución)")
                
                algo_opcion = input("Seleccione algoritmo (1-5): ").strip()
                algoritmos = {
                    '1': 'sha256',
                    '2': 'fnv1_32',
                    '3': 'fnv1_64',
                    '4': 'fnv1a_32',
                    '5': 'fnv1a_64'
                }
                
                if algo_opcion in algoritmos:
                    firma_digital.set_hash_algorithm(algoritmos[algo_opcion])
                else:
                    print("Opción inválida. Usando SHA-256 por defecto.")
                    firma_digital.set_hash_algorithm('sha256')
                    
            except Exception as e:
                print(f"Error: {e}")
        
        elif opcion == "3":
            try:
                archivo = input("Ingrese la ruta del archivo: ").strip()
                firma_digital.calcular_hash_archivo(archivo)
            except Exception as e:
                print(f"Error al calcular hash: {e}")
        
        elif opcion == "4":
            try:
                archivo = input("Ingrese la ruta del archivo a firmar: ").strip()
                clave_privada = input("Ingrese la ruta de la clave privada (ENTER para usar la actual): ").strip()
                
                if clave_privada:
                    firma_digital.cargar_clave_privada(clave_privada)
                elif firma_digital.private_key is None:
                    print("Error: No hay clave privada cargada. Genere o cargue una clave primero.")
                    continue
                
                archivo_salida = input("Ingrese la ruta para guardar la firma (ENTER para automático): ").strip()
                if not archivo_salida:
                    archivo_salida = None
                
                firma_digital.firmar_archivo(archivo, archivo_salida)
                
            except Exception as e:
                print(f"Error al firmar: {e}")
        
        elif opcion == "5":
            try:
                archivo_original = input("Ingrese la ruta del archivo original: ").strip()
                archivo_firma = input("Ingrese la ruta del archivo de firma: ").strip()
                clave_publica = input("Ingrese la ruta de la clave pública (ENTER para usar la actual): ").strip()
                
                if clave_publica:
                    firma_digital.cargar_clave_publica(clave_publica)
                elif firma_digital.public_key is None:
                    print("Error: No hay clave pública cargada. Genere o cargue una clave primero.")
                    continue
                
                firma_digital.verificar_firma(archivo_original, archivo_firma)
                
            except Exception as e:
                print(f"Error al verificar: {e}")
        
        elif opcion == "6":
            print("¡Hasta luego!")
            break
        
        else:
            print("Opción inválida. Por favor, seleccione 1-6.")

if __name__ == "__main__":
    print("Sistema de Firma Digital con FNV-1")
    print("Nota: Requiere la librería 'cryptography'")
    print("Instalar con: pip install cryptography")
    print()
    main()