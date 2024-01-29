# nutricionApp


Bienvenido/a! A lo largo de este archivo podrás descubrir el funcionamiento, la ejecución y las carácterísticas de mi app de nutrición (;

NutricionApp es una aplicación de línea de comandos que te permite buscar recetas, obtener información nutricional e ingredientes de recetas, y explorar sus beneficios y riesgos nutricionales. Esta aplicación está abastecida por una gran base de datos nutricionales de la mano de la API web de Spoonacular (https://spoonacular.com/food-api).

## **Requisitos**

Para poder ejecutar la aplicación, comenzaremos clonando o descargando el repositorio nutricionApp en el equipo.

**Recomendación**: En las indicaciones siguientes, se explicará como instalar las dependencias de nutricionApp. Para un aislamiento de estas y una máxima compatibilidad se recomienda el uso de un entorno virtual. He proporcionado en el repositorio una carpeta ("entornoVirtual") para que se cree ahí el entorno virtual. Personalmente, **Virtualenvwrapper** es el que yo he utilizado. Para ver cómo se instala, puedes usar esta url: https://virtualenvwrapper-docs-es.readthedocs.io/es/latest/install.html

Una vez tengamos el repositorio, lo siguiente será tener Python y ciertas bibliotecas instaladas. En cuanto a la versión, se recomienda utilizar **Python 3.10.12** para garantizar la compatibilidad total. Puedes descargar Python desde el sitio web oficial python.org. Comprueba que Python esté correctamente instalado ejecutando el siguiente comando en tu terminal: **python --version**.

A continuación, deberás instalar las bibliotecas de las que depende esta app Python. Para ello, he proporcionado un archivo **nutricionApp/app/requirements.txt**. Dirígete en tu terminal hacia la ruta en la que se encuentra requirements.txt y ejecuta el siguente comando: **pip install -r requirements.txt**. Con esto, ya habrás instalado todas las bibliotecas necesarias para usar el programa.

## **Ejecución**

Ahora que tenemos los requisitos, ya puedes ejecutar la app. Desde el directorio **nutricionApp/app**, ejecuta el siguiente comando: **python principal.py**.

## **Uso**

La aplicación ofrece las siguientes características:

1. **Búsqueda de recetas por ingredientes**: Permite buscar recetas que contengan ciertos ingredientes.
2. **Obtener ingredientes de una receta**: Proporciona una lista de ingredientes para una receta específica.
3. **Obtener nutrientes de una receta**: Muestra información nutricional para una receta, incluyendo calorías, grasas, proteínas y más.
4. **Salir**: Cierra la aplicación.

Nota: he implementado el autocompletado para la búsqueda de recetas.

Sigue las instrucciones de la línea de comandos y disfruta de la comida sazonada con Python!

## **Imagen Docker**

Si tienes docker y deseas ejecutar la aplicación en un contenedor, estás de suerte! Solo dirígete hacia la terminal y ejecuta **sudo docker run -it ignacio22/nutricion** y ya tendrás preparado todo para tí! 

Si estás en Windows, considera ejecutar el **símbolo del sistema como administrador**.

Nota: tienes el archivo **Dockerfile** que se ha usado a tu entera disposición en el repositorio.

Guía para instalar docker: https://docs.docker.com/engine/install/

## **Términos y licencia de Spoonacular API**

https://spoonacular.com/food-api/terms
