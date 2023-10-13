import requests #Importamos la biblioteca requests para hacer solicitudes a la API de Spoonacular.
import json

apiKey = "64e9a5cb1b1f41daa6a4b3a8c572d2dc"

urlInicial = "https://api.spoonacular.com/recipes"  #Esta en principio es la url base que voy a utilizar



terminacionUrl = "/findByIngredients"
parametros = {      #Variable que guardará el diccionario de parámetros a pasar al método requests.get
        "apiKey": apiKey,
        "ingredients": "milk, berries",  # Ingredientes (la API espera que estén separados por comas)
        "number": 5     # Cantidad de recetas a obtener
}


respuesta = requests.get(urlInicial + terminacionUrl, params=parametros)    #Se usará para control de respuesta de la API

if respuesta.status_code == 200:    #Aquí vemos si devuelve 200 OK con el status_code
        recetas = respuesta.json()      # Respuesta de formato json a objeto Python
        if recetas:
            for receta in recetas:      #Iteramos los objetos receta
             print(f"Nombre: {receta['title']}")
             print("")
else:
        print("No se pudieron buscar recetas. Lo lamentamos!", respuesta.status_code)   #Códigos de error. Puede ser por la cuota de la API o porque no haya conexion.