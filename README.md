# qa-project-Urban-Routes-es

## Descripción del Proyecto

Este proyecto forma parte del Bootcamp en QA Engineer y tiene como objetivo automatizar pruebas funcionales de la aplicación web Urban Routes.  
La automatización se implementa en Python utilizando Selenium WebDriver y se organiza aplicando el patrón Page Object Model (POM).  
El flujo automatizado abarca desde la configuración de la ruta y la selección de la tarifa hasta la confirmación final del pedido del taxi, incluyendo:

- **Configuración de la ruta y selección de tarifa:**  
  Ingreso de datos de origen y destino, y selección de la tarifa "Comfort".

- **Autenticación mediante teléfono:**  
  Ingreso del número de teléfono y el código SMS (capturado a través de los logs de rendimiento).

- **Agregación de tarjeta de crédito:**  
  Apertura del modal de “Método de pago”, ingreso del número de tarjeta y CVV (forzando la pérdida de foco para activar el botón "Agregar"), y cierre del modal.

- **Ingreso de un mensaje para el conductor:**  
  Se activa la sección para escribir el mensaje y se ingresa el contenido.

- **Selección de requisitos y pedido:**  
  Se activa automáticamente el contenedor de requisitos, donde se habilita la opción de “manta y pañuelos” y se agregan 2 helados mediante el contador, seguido por un clic en "Reservar".  
  Finalmente, se confirma el pedido y se solicita el taxi.

## Estructura del Proyecto

El proyecto se divide en los siguientes archivos:

- **data.py**  
  Contiene las variables de configuración y datos de prueba (URL del servidor, direcciones, número de teléfono, datos de la tarjeta, mensaje, etc.).

- **helpers.py**  
  Incluye funciones de apoyo, como `slow_type` y `retrieve_phone_code`, que facilitan la interacción con la aplicación.

- **pages.py**  
  Define la clase `UrbanRoutesPage`, que contiene los selectores y métodos para interactuar con cada parte de la interfaz de Urban Routes siguiendo el patrón POM.  
  El método `__init__` se utiliza aquí para inicializar el driver en la instancia de página (esto es estándar en POM).

- **test_main.py**  
  Contiene la clase `TestUrbanRoutes` con todos los métodos de test individuales.  
  La clase utiliza los métodos `setup_class` y `teardown_class` (sin un constructor `__init__`) para que pytest gestione la creación de la única instancia de Chrome en la que se ejecutan todas las pruebas.

## Tecnologías y Técnicas Utilizadas

- **Python:** Lenguaje de programación principal.  
- **Selenium WebDriver:** Librería para automatizar pruebas y la interacción con el navegador.  
- **ChromeDriver:** Controlador para automatizar Google Chrome.  
- **Page Object Model (POM):** Patrón de diseño que facilita la mantenibilidad del código al separar la lógica de interacción con la interfaz de la lógica de validación.  
- **PyTest:** Framework para la ejecución y organización de pruebas en Python.

## Instrucciones para Ejecutar las Pruebas

### Preparación del Proyecto

1. **Clonar el repositorio**  
   Asegúrate de tener una copia local del repositorio:
   
       git clone git@github.com:tu-usuario/qa-project-Urban-Routes-es.git

## Estructura de archivos
qa-project-Urban-Routes-es/
├── data.py
├── helpers.py
├── pages.py
└── test_main.py

## Configurar el entorno virtual
         python -m venv .venv

## En Windows (PowerShell):
         .\.venv\Scripts\Activate.ps1

## Instalar dependencias
          pip install selenium

## Configurar los datos
# data.py
urban_routes_url = "https://cnt-f77e12c2-30d6-4786-83ff-0e3e067a0751.containerhub.tripleten-services.com?lng=es"
address_from = "East 2nd Street, 601"
address_to = "1300 1st St"
phone_number = "+1 123 123 12 12"
card_number = "435465456768687687"
card_code = "44"
message_for_driver = "Muéstrame el camino al museo"

## Ejecución de las Pruebas
Desde la Terminal
Navega hasta la carpeta raíz del proyecto.

Ejecuta los tests con pytest:

          pytest

