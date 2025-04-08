# Urban Routes QA Project

## Descripción del Proyecto

Este proyecto de automatización de pruebas se diseñó para validar la funcionalidad de la aplicación web Urban Routes, una plataforma para solicitar taxis. El objetivo de los tests es asegurar que el flujo completo de la aplicación funcione correctamente: desde configurar las direcciones, seleccionar la tarifa (por ejemplo, "Comfort"), iniciar sesión mediante la verificación del número de teléfono, agregar el método de pago (incluyendo el proceso de agregar tarjeta de crédito) hasta confirmar el pedido de taxi.  
  
La implementación sigue el patrón **Page Object Model (POM)** para organizar los tests y facilitar su mantenimiento, separando la lógica de interacción con los elementos de la interfaz de los propios escenarios de prueba.

## Tecnologías y Técnicas Utilizadas

- **Selenium WebDriver:** Automatiza la interacción con el navegador para simular la actividad de un usuario en la aplicación.
- **Python:** Lenguaje de programación utilizado para desarrollar los tests.
- **Page Object Model (POM):** Patrón de diseño para encapsular los elementos y métodos de interacción de cada página, facilitando la reutilización y mantenimiento del código.
- **Google Chrome y Chrome WebDriver:** Navegador y driver utilizados para ejecutar las pruebas.
- **Git & GitHub:** Para la gestión de versiones y la colaboración, facilitando la revisión y actualización del código.

## Instrucciones para Ejecutar las Pruebas

1. **Clonar el repositorio:**

   Abre tu terminal y clona el repositorio (asegúrate de usar tu propio nombre de usuario en lugar de `username`):

   ```bash
   git clone git@github.com:TU_USUARIO/qa-project-Urban-Routes-es.git
Crear y activar el entorno virtual:

Dirígete al directorio del proyecto y crea el entorno virtual:

Copiar
cd qa-project-Urban-Routes-es
python -m venv .venv
Activa el entorno virtual:

En Windows:
Copiar
.\.venv\Scripts\activate
En macOS/Linux:

Copiar
source .venv/bin/activate
Instalar las dependencias:

Si el proyecto incluye un archivo requirements.txt, ejecuta:

Copiar
pip install -r requirements.txt
Si no, asegúrate de que selenium esté instalado:

Copiar
pip install selenium
Configurar la URL de la aplicación (si es necesario):

Revisa el archivo data.py y actualiza la variable urban_routes_url con la URL correcta si hubiese cambios.

Ejecutar las pruebas:

Puedes ejecutar las pruebas directamente desde PyCharm o desde la terminal. Por ejemplo, para ejecutar el script principal:

Copiar
python main.py
O, si utilizas un framework de testing como PyTest:

Copiar
pytest