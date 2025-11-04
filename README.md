# Aplicación de Cifrado

Un programa desarrollado en Python para cifrar datos de forma asimétrica y para la creación de firmas digitales.

## Funcionamiento del Sistema

El sistema ofrece tres opciones principales:

1. **Gestión de Claves**
2. **Cifrado y Descifrado**
3. **Firma Digital**

## Gestión de Claves

En esta opción, se presentan tres botones:

- **Cargar Clave Privada**: Permite cargar la clave privada necesaria para el cifrado y la firma.
- **Cargar Clave Pública**: Permite cargar la clave pública correspondiente.
- **Generar y Guardar Claves**: Este botón genera nuevas claves y las guarda en el sistema. Solo es necesario añadir los archivos y proporcionar un nombre para las claves.

## Cifrado y Descifrado

Para cifrar y descifrar archivos, sigue estos pasos:

1. **Cargar las Claves**: Es obligatorio cargar las claves antes de proceder con cualquier otro proceso.
2. **Seleccionar el Archivo**: Carga el archivo que deseas cifrar.
3. **Cifrar el Archivo**: Presiona el botón correspondiente para cifrar el archivo utilizando las claves previamente cargadas.

## Firma Digital

La firma digital es un mecanismo criptográfico que verifica la autenticidad de un documento o archivo al firmarlo digitalmente, permitiendo al receptor comprobar que no ha habido modificaciones.

Para utilizar esta función:

1. **Seleccionar Llave**: Se abrirá un menú que solicita una llave pública o privada. Puedes usar una llave externa o, si lo prefieres, el sistema incluye un generador de claves automático.
2. **Cargar el Archivo a Firmar**: Selecciona el archivo desde tu sistema.
3. **Firmar el Archivo**: Presiona "Firmar archivo" para realizar la acción y encriptar el archivo con tu firma.
4. **Verificar Autenticidad**: Para comprobar la autenticidad, ingresa tanto el archivo original como el firmado. El sistema comparará ambos y devolverá los resultados en pantalla.

## Enlace al GitHub

[Repositorio de GitHub](https://github.com/4rchila/Aplicacion-de-Cifrado-)

---

**Autores:**

- German Juan Carlos Archila Batz - 1526824
- Rodrigo Gabriel Pérez Vásquez - 1576224