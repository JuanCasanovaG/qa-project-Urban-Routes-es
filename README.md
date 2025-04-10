<<<<<<< HEAD
qa-project-Urban-Routes-es
Descripción del Proyecto
Este proyecto forma parte del Bootcamp en QA Engineer y tiene como objetivo automatizar pruebas funcionales de la aplicación web Urban Routes.
La automatización se implementa utilizando Selenium WebDriver en Python, aplicando el patrón Page Object Model (POM) para separar la lógica de interacción con la página de la lógica de pruebas.
El flujo automatizado abarca desde la configuración de la ruta y selección de tarifa hasta la confirmación final del pedido del taxi. Entre las acciones automatizadas se encuentran:

Configuración de la ruta y selección de tarifa:
* Ingreso de los datos de origen y destino, y selección de la tarifa "Comfort" para el servicio.

Autenticación mediante teléfono:
* Ingreso del número de teléfono y del código SMS, utilizando métodos que capturan el código mediante los logs de rendimiento.

Agregar una tarjeta de crédito:
* Se abre el modal "Método de pago" y, desde allí, el modal "Agregar tarjeta" para ingresar el número de la tarjeta y el CVV. Se fuerza la pérdida de foco para activar el botón "Agregar", luego se cierra el modal de "Método de pago".

Ingreso de un mensaje al conductor:
* Se accede a la sección de mensaje para el conductor y se ingresa el mensaje correspondiente.

Selección de requisitos y confirmación del pedido:
* Se activa la opción de “manta y pañuelos”, se agregan 2 helados mediante el contador y, finalmente, se hace clic en el botón "Reservar". Una vez completadas estas acciones, se confirma el pedido y se solicita el taxi.

Tecnologías y Técnicas Utilizadas
* Python: Lenguaje de programación principal.
* Selenium WebDriver: Librería para automatizar pruebas y la interacción con el navegador.
* ChromeDriver: Controlador para automatizar Google Chrome.
* Page Object Model (POM): Patrón de diseño que permite organizar el código de pruebas separando la lógica de interacción con la interfaz de la lógica de verificación.
* Pausas temporales (time.sleep): Utilizadas para esperar a que se completen acciones asíncronas en la interfaz.
Instrucciones para Ejecutar las Pruebas
Clonar el repositorio

Asegúrate de tener una copia local del repositorio:

git clone git@github.com:tu-usuario/qa-project-Urban-Routes-es.git
Abrir el proyecto en PyCharm
=======
# qa-project-Urban-Routes-es

## Descripción del Proyecto

Este proyecto forma parte del Bootcamp en QA Engineer y tiene como objetivo automatizar pruebas funcionales de la aplicación web Urban Routes.  
La automatización se implementa utilizando Selenium WebDriver en Python, aplicando el patrón Page Object Model (POM) para separar la lógica de interacción con la página de la lógica de pruebas.  
El flujo automatizado abarca desde la configuración de la ruta y selección de tarifa hasta la confirmación final del pedido del taxi. Entre las acciones automatizadas se encuentran:

- **Configuración de la ruta y selección de tarifa:**  
  Ingreso de los datos de origen y destino, y selección de la tarifa "Comfort" para el servicio.

- **Autenticación mediante teléfono:**  
  Ingreso del número de teléfono y del código SMS, utilizando métodos que capturan el código mediante los logs de rendimiento.

- **Agregar una tarjeta de crédito:**  
  Se abre el modal "Método de pago" y, desde allí, el modal "Agregar tarjeta" para ingresar el número de la tarjeta y el CVV. Se fuerza la pérdida de foco para activar el botón "Agregar", luego se cierra el modal de "Método de pago".

- **Ingreso de un mensaje al conductor:**  
  Se accede a la sección de mensaje para el conductor y se ingresa el mensaje correspondiente.

- **Selección de requisitos y confirmación del pedido:**  
  Se activa la opción de “manta y pañuelos”, se agregan 2 helados mediante el contador y, finalmente, se hace clic en el botón "Reservar". Una vez completadas estas acciones, se confirma el pedido y se solicita el taxi.

## Tecnologías y Técnicas Utilizadas

- **Python:** Lenguaje de programación principal.
- **Selenium WebDriver:** Librería para automatizar pruebas y la interacción con el navegador.
- **ChromeDriver:** Controlador para automatizar Google Chrome.
- **Page Object Model (POM):** Patrón de diseño que permite organizar el código de pruebas separando la lógica de interacción con la interfaz de la lógica de verificación.
- **Pausas temporales (time.sleep):** Utilizadas para esperar a que se completen acciones asíncronas en la interfaz.

## Instrucciones para Ejecutar las Pruebas

1. **Clonar el repositorio**

   Asegúrate de tener una copia local del repositorio:
   
       git clone git@github.com:tu-usuario/qa-project-Urban-Routes-es.git

2. **Abrir el proyecto en PyCharm**
>>>>>>> 4a3b8a76f2e37eb94ef237ebdebef31b64c2e6f7

En PyCharm, selecciona File → Open y carga la carpeta del proyecto.

Configurar el entorno virtual

<<<<<<< HEAD
    python -m venv .venv
=======
      python -m venv .venv

>>>>>>> 4a3b8a76f2e37eb94ef237ebdebef31b64c2e6f7
Activa el entorno:

En PowerShell (Windows):

<<<<<<< HEAD
    .\.venv\Scripts\Activate.ps1
Instalar dependencias
Instala la librería Selenium:

    pip install selenium
    pip install pytest
Ejecutar el Flujo Completo de Pruebas
El flujo completo de pruebas se encuentra en el archivo main.py. Para ejecutarlo, dar clic en el boton Run, o clic derecho al arhivo main 'Run':

    Ejececutar desde el Run 'main' (Boton ">")
Esto ejecutará todo el flujo automatizado que abarca:
=======
     .\.venv\Scripts\Activate.ps1

3. **Instalar dependencias**

Instala la librería Selenium:

      pip install selenium

4. **Ejecutar el Flujo Completo de Pruebas**

El flujo completo de pruebas se encuentra en el archivo main.py. Para ejecutarlo, desde la terminal (dentro del entorno virtual) escribe:

      python main.py o  Ejececutar desde el Run 'main' (Boton ">")

* Esto ejecutará todo el flujo automatizado que abarca:
>>>>>>> 4a3b8a76f2e37eb94ef237ebdebef31b64c2e6f7

* Configuración de la ruta y selección de tarifa.

* Autenticación con teléfono (ingreso de número y código SMS).

* Agregar tarjeta de crédito y cierre del modal de "Método de pago".

* Ingreso del mensaje para el conductor.

* Selección de requisitos (activación de manta y pañuelos, agregar 2 helados y clic en "Reservar").

* Confirmación final del pedido y solicitud del taxi.