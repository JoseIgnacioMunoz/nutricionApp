# BIENVENID@ AL CÓDIGO DE MI APLICACIÓN NUTRICIONAL!
# AUTOR: JOSÉ IGNACIO MUÑOZ SOTELO
#API: SPOONACULAR API

import requests # Biblioteca requests para hacer solicitudes a la API de Spoonacular
import os   # Para la función de limpiar la terminal segun el Sistema Operativo
apiKey = "64e9a5cb1b1f41daa6a4b3a8c572d2dc"
urlBase = "https://api.spoonacular.com/recipes"  #E URL base para todas las solicitudes que haremos a la API
noDisponible = 'Information not available'  # Lo usaremos para cuando no se encuentre, por ejemplo, un nutriente, ingrediente...

OK200 = 200 # Constante para comprobar si la respuesta de la API es 200 OK
UMBRAL50 = 50


# Limpiar la terminal antes de la ejecución del menú. Fuente de información: https://stackoverflow.com/questions/2084508/clear-terminal-in-python

if os.name == 'nt':    # Windows
    os.system('cls')  
else:                  # Linux, macOS
    os.system('clear')  

#--------Función menú---------

def menu():

    salir=False
    while salir==False:
        
        print("-------------------------------------------------")
        print("\nMenu:\n")
        print("1. Search for recipes by ingredients.")
        print("2. Get ingredients from a recipe.")
        print("3. Get nutrients from a recipe.")
        print("4. Exit.")
        opcion = input("\nGo ahead, choose an option! - ")
        print("\n-------------------------------------------------")

        if opcion == "1":
            recetasPorIngredientes()
        elif opcion == "2":
            mostrarIngredientesReceta()
        elif opcion == "3":
            mostrarNutrientesReceta()
        elif opcion == "4":
            print("Goodbye!")
            salir=True
        else:
            print("Sorry, that option is out of our reach. Please choose from 1 to 4. (; ")


#------1º Búsqueda de recetas que contengan ciertos ingredientes.

def recetasPorIngredientes():

    ingredientes = input("Enter ingredients separated by commas: ")
    numRecetas = input("Number of recipes to get: ")

    # Parámetros para la url

    parametros = {      #Variable que guardará el diccionario de parámetros a pasar al método requests.get
            "apiKey": apiKey,
            "ingredients":  ingredientes,  # Ingredientes (la API espera que estén separados por comas)
            "number": numRecetas     # Cantidad de recetas a obtener
    }

    terminacionUrl = "/findByIngredients"

    respuesta = requests.get(urlBase + terminacionUrl, params=parametros)    # Se guarda la respuesta para comprobarla y manejar los datos contenidos en ella

    if respuesta.status_code == OK200:    #Aquí vemos si devuelve 200 OK con el status_code
            recetas = respuesta.json()    # Respuesta de formato json a objeto Python
            if recetas:                   # Si hay recetas...
                print("\nYay! It looks like there are recipes for you!\n")
                i = 1   #i se incrementará para hacer una lista ordenada
                for receta in recetas:      #Iteramos los objetos receta
                    print(f"{i}. {receta['title']}")    # Lista ordenada de titulos de recetas          
                    
                    i += 1
            else:   
                print("No recipes were found with the provided ingredients.")
    else:
            print("Recipes could not be found. We're sorry!")   #Códigos de error. Puede ser por la cuota de la API o porque no haya conexion.

#Función auxiliar. Devuelve id y nombre de una receta. (Véase su uso en las siguientes dos funciones)

def obtenerIdYNombreReceta():

    nombreReceta = input("What is the recipe? \n")

    # Parametros a pasar en la url
    parametros = {
        "apiKey": apiKey,
        "number": 1,
        "query": nombreReceta
    }

    terminacionUrl = "/autocomplete"

    respuesta = requests.get(urlBase + terminacionUrl, params=parametros)      #LA API DEVUELVE UNA LISTA DE RECETAS AUTOCOMPLETADAS A PARTIR DE LA BÚSQUEDA

    if respuesta.status_code == OK200: 
        recetas = respuesta.json()

        if recetas and len(recetas) > 0:    #Devuelve una lista de recetas. Miramos si está vacía
            idReceta = recetas[0]['id']     #Solo quiero que me devuelva el id y el nombre de la primera receta de la lista
            tituloReceta = recetas[0]['title']
            return idReceta, tituloReceta
        else:
            print("We tried, but we couldn't find that recipe. :( ")
            return None, None   #Tuve problemas con el control de errores, y era porque no puse que devolviera None, None.
    else:
        print("There was a problem searching for the recipe.")
        return None, None

#------2º Devuelve los ingredientes que se usan en una receta.

def mostrarIngredientesReceta():

    idReceta, nombreReceta= obtenerIdYNombreReceta() #  Se necesita el id para obtener los ingredientes de la receta

    if idReceta:
        # Parámetros a pasar en la url
        parametros = {
            "apiKey": apiKey,
        }

        url = f"{urlBase}/{idReceta}/ingredientWidget.json" #Proporciona ingredientes por ID de receta, por eso se crea obtenerIdYNombreReceta()
        respuesta = requests.get(url, params=parametros)

        if respuesta.status_code == OK200:
            ingredientes = respuesta.json()

            if "ingredients" in ingredientes:
                print(f"\nIngredients in {nombreReceta}:")     # Pongo el nombreReceta para controlar el autocompletado. Te animo a que pruebes a poner "fish and"
                for ingrediente in ingredientes["ingredients"]: #Recorrido de ingredientes
                    nombre = ingrediente['name']                #Ejemplo: garlic
                    cantidad = ingrediente['amount']['metric']  #Cantidad y su métrica
                    print(f"{nombre} = {cantidad['value']} {cantidad['unit']}") #Valor de la cantidad y unidad métrica
            else:
                print("No ingredients were found for this recipe.")
        else:
            print("There was a problem getting the ingredients.")

#------3º Devuelve los nutrientes de una receta.

def mostrarNutrientesReceta():   

    idReceta, nombreReceta= obtenerIdYNombreReceta() # Se necesita el id para obtener los nutrientes de la receta

    url = f"https://api.spoonacular.com/recipes/{idReceta}/nutritionWidget.json"    # URL para acceder a la info nutricional mediante id
    parametros = {
        "apiKey": apiKey,
    }

    respuesta = requests.get(url, params=parametros)

    if respuesta.status_code == OK200:
            
            infoNutricional = respuesta.json()
            print(f"Nutritional Information for {nombreReceta}: \n")

            # Creación e inicialización de las variables que contendrán información nutricional:
            calorias = infoNutricional.get('calories', noDisponible)
            grGrasa = infoNutricional.get('fat', noDisponible)
            hidratos = infoNutricional.get('carbs', noDisponible) 
            grProteina = infoNutricional.get('protein', noDisponible)

            for nutriente in infoNutricional.get('bad'):    # Grasas saturadas está anidado a la lista de elementos "bad", por eso la recorremos y buscamos el título "Satured Fat"
                if nutriente.get('title') == 'Saturated Fat':
                    grGrasaSaturada = nutriente.get('amount', noDisponible)
                    break   # No queda más remedio que utilizar el break para que no recorra toda la lista
            
            for nutriente in infoNutricional.get('bad'):    # Lo mismo de las grasas saturadas lo hacemos con el azúcar.
                if nutriente.get('title') == 'Sugar':
                    azucar = nutriente.get('amount', noDisponible)
                    break

            for nutriente in infoNutricional.get('bad'):    # También con el sodio
                if nutriente.get('title') == 'Sodium':
                    sodio = nutriente.get('amount', noDisponible)
                    break

            for nutriente in infoNutricional.get('good'):   # Lo mismo, pero esta vez, "fibra", está en la lista "good"
                if nutriente.get('title') == 'Fiber':
                    fibra = nutriente.get('amount', noDisponible)
                    break

            #Mostramos los nutrientes

            print("Calories:", calorias, "kcal")
            print("Total Fat:", grGrasa)
            print("Saturated Fat:", grGrasaSaturada)
            print("Carbohydrates:", hidratos)
            print("Sugar:", azucar)
            print("Protein:", grProteina)
            print("Fiber:", fibra)
            print("Sodium:", sodio)

            # Mostrar beneficios y riesgos nutricionales 

            mostrarBeneficios(infoNutricional)
            mostrarRiesgos(infoNutricional)
   

def mostrarBeneficios(infoNutricional):     # Beneficios 
    
    nutrientesBuenos = infoNutricional.get('nutrients', [])

    for nutriente in infoNutricional.get('good'):   # Buscamos en la lista de nutrientes favorables
        nombre = nutriente.get('title', noDisponible)
        porcentajeDiario = nutriente.get('percentOfDailyNeeds', noDisponible)
        if porcentajeDiario > UMBRAL50:     # 50 %
            print(f"This recipe is rich in {nombre} ({porcentajeDiario}% of daily needs).")

def mostrarRiesgos(infoNutricional):        # Riesgos 

    nutrientesMalos = infoNutricional.get('nutrients', [])  

    for nutriente in infoNutricional.get('bad'):    # Buscamos en la lista de nutrientes desfavorables
        nombre = nutriente.get('title', noDisponible)
        porcentajeDiario = nutriente.get('percentOfDailyNeeds', noDisponible)
        if porcentajeDiario > UMBRAL50:     #50%
            print(f"Warning: this recipe has {porcentajeDiario}% of daily needs for {nombre}.")
       
menu()
