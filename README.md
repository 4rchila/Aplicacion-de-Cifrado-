# Aplicacion-de-Cifrado-
Un programa hecho en python para cifrar datos de forma Asimétrica y una Firma digital 


Funcionamiento del sistema:

El sistema cuenta con 3 opciones las cuales ejecutan las siguientes acciones:
1. Gestión de claves
2. Cifrado y descifrado
3. Firma digital

## Gestión de claves
En esta opción se muestran 3 botones, el primero es para cargar la clave privada, luego otro para la clave pública y finalmente el botón que genera y guarda las claves resultantes. Basta con añadir estos archivos para que devuleva e ingresar el nombre para las claves.

## Cifrado y descifrado
En este menú el primer paso es cargar las claves para el cifrado, seguido de ello se carga el archivo a cifrar en el programa para finalmente presionar el botón para cifrar el archivo en función de la clave precargada. Es obligatorio cargar las claves antes de iniciar cualquier otro proceso.

## Firma digital

La firma digital es un mecanismo criptográfico por el cual se verifica la autenticidad de un documento o archivo al firmarlo digitalmente, esto con el fin que quien reciba el documento pueda corroborar que no tuvo modificación.

Para emplear esta función se abre un menú el cual al inicio solicita una llave pública o privada. Esta puede ser una externa o así, si el usuario prefiere, el sistema contiene embedido un creador de claves automático. 
Tras cargar las claves, se solicita el archivo a firmar y este se carga desde el sistema del usuario. Para firmar, basta con presionar en "Firmar archivo" para realizar la acción y así encriptar el archivo con su firma.
Finalmente, para verificar la autenticidad del archivo se debe ingresar tanto el archivo original como el firmado para que el sistema compare si este es verídico o no, devolviendo los resultados en pantalla.

Enlace al GitHub: https://github.com/4rchila/Aplicacion-de-Cifrado-