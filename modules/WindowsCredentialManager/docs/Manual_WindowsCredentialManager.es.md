# Windows Credential Manager
  
Obtiene las credenciales desde el administrador de credenciales de Windows  

*Read this in other languages: [English](Manual_WindowsCredentialManager.md), [Español](Manual_WindowsCredentialManager.es.md), [Portugués](Manual_WindowsCredentialManager.pr.md)*
  
![banner](imgs/Banner_WindowsCredentialManager.png)
## Como instalar este módulo
  
__Descarga__ e __instala__ el contenido en la carpeta 'modules' en la ruta de Rocketbot.  


## Como usar este módulo
1. Escribir en el buscador de Windows "Administrador de credenciales" y abrirlo
2. Hacer click en "Credenciales de Windows"
3. En la sección de Credenciales genéricas hacer click en "Agregar una credencial genérica"
4. Deberás completar la información con una dirección de red, nombre de usuario y contraseña (Pueden ser los valores que quieras).
5. En el comando de Rocketbot deberás escribir el nombre de la dirección de red para poder obtener sus valores.


## Descripción de los comandos

### Obtener credenciales
  
Obtener credenciales de usuario y contraseña del baúl de credenciales de Windows
|Parámetros|Descripción|ejemplo|
| --- | --- | --- |
|Dirección de red o Internet|Dirección de red o Internet de la credencial genérica|rocketbot.com|
|Asignar resultado usuario a variable|Asigna el usuario de la credencial a una variable|Variable 1|
|Asignar resultado password a variable|Asigna la contraseña de la credencial a una variable|Variable 2|
