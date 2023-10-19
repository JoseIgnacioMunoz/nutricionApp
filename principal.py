import requests #Importamos la biblioteca requests para hacer solicitudes a la API de Spoonacular.
import json
import os
apiKey = "64e9a5cb1b1f41daa6a4b3a8c572d2dc"
urlBase = "https://api.spoonacular.com/recipes"  #Esta en principio es la url base que voy a utilizar
OK200 = 200
UMBRAL50 = 50


#Función para limpiar la terminal antes de la ejecución del menú. Fuente de información: https://stackoverflow.com/questions/2084508/clear-terminal-in-python

def limpiar_pantalla():
    if os.name == 'nt':     #Para windows
        os.system('cls')  
    else:                   #Para linux, macOS
        os.system('clear')  

limpiar_pantalla()

#--------Función menú---------
def menu():

    salir=False
    while salir==False:
        
        print("-------------------------------------------------")
        print("\nMenú:\n")
        print("1. Búsqueda de recetas por ingredientes.")
        print("2. Obtener ingredientes de una receta.")
        print("3. Obtener nutrientes de una receta")
        print("4. Salir")
        opcion = input("\nElige una opción: ")
        print("\n-------------------------------------------------")

        if opcion == "1":
            recetasPorIngredientes()
        elif opcion == "2":
            mostrarIngredientesReceta()
        elif opcion == "3":
            mostrarNutrientesReceta()
        elif opcion == "4":
            print("¡Hasta luego!")
            salir=True
        else:
            print("Opción no válida. Por favor, elige una opción del 1 al 4.")


#------1º Búsqueda de recetas que contengan ciertos ingredientes.
def recetasPorIngredientes():

    ingredientes = input("Ingresa los ingredientes separados por comas: ")
    numRecetas = input("Número de recetas a obtener: ")

    # Parámetros para la url
    parametros = {      #Variable que guardará el diccionario de parámetros a pasar al método requests.get
            "apiKey": apiKey,
            "ingredients":  ingredientes,  # Ingredientes (la API espera que estén separados por comas)
            "number": numRecetas     # Cantidad de recetas a obtener
    }

    respuesta = requests.get(urlBase + "/findByIngredients", params=parametros)    #Se usará para control de respuesta de la API

    if respuesta.status_code == OK200:    #Aquí vemos si devuelve 200 OK con el status_code
            recetas = respuesta.json()      # Respuesta de formato json a objeto Python
            if recetas:
                print("\nYuju! Parece que hay recetas para ti!\n")
                i = 1   #i se incrementará para hacer una lista ordenada
                for receta in recetas:      #Iteramos los objetos receta
                    print(f"{i}. {receta['title']}")    # Lista ordenada de titulos de recetas
                    #idReceta=receta['id']
                    #informacionNutricional = mostrarInfoNutrientes(idReceta)          
                    
                    i += 1
            else:   
                print("No se encontraron recetas con los ingredientes proporcionados.")
    else:
            print("No se pudieron buscar recetas. Lo lamentamos!", respuesta.status_code)   #Códigos de error. Puede ser por la cuota de la API o porque no haya conexion.


#------2º Devuelve los ingredientes que se usan en una receta.
def mostrarIngredientesReceta():

    idReceta, nombreReceta= obtenerIdYNombreReceta() # Almacenamiento de lo devuelto en dicha función

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
                print(f"\nIngredientes de {nombreReceta}:")     #Si busco "fish and" se autocompletará como "fish and chips". Pongo el nombreReceta para controlar el autocompletado
                for ingrediente in ingredientes["ingredients"]: #Recorrido de ingredientes
                    nombre = ingrediente['name']                #Ejemplo: garlic
                    cantidad = ingrediente['amount']['metric']  #Cantidad y su métrica
                    print(f"{nombre} = {cantidad['value']} {cantidad['unit']}") #Valor de la cantidad y unidad métrica
            else:
                print("No se encontraron ingredientes para esta receta.")
        else:
            print("Hubo un problema al obtener los ingredientes.")

#------3º Devuelve los nutrientes de una receta.

def mostrarNutrientesReceta():    #se usará para la opcion 2 del menu. (Obtener nutrientes de una receta mediante el id que devuelve la funcion de la api de autocompletar recetas)

    idReceta, nombreReceta= obtenerIdYNombreReceta() # Almacenamiento de lo devuelto en dicha función

    url = f"https://api.spoonacular.com/recipes/{idReceta}/nutritionWidget.json"

    parametros = {
        "apiKey": apiKey,
    }

    respuesta = requests.get(url, params=parametros)

    if respuesta.status_code == OK200:
            
            infoNutricional = respuesta.json()
            print(f"Información Nutricional de {nombreReceta}: \n")

            # Creación e inicialización de las variables que contendrán información nutricional:
            calorias = infoNutricional.get('calories', 'Información no disponible')
            grGrasa = infoNutricional.get('fat', 'Información no disponible')
            hidratos = infoNutricional.get('carbs', 'Información no disponible') #Hidratos de carbono 
            grProteina = infoNutricional.get('protein', 'Información no disponible')

            for nutriente in infoNutricional.get('bad'):    # Grasas saturadas está anidado a la lista de elementos "bad", por eso la recorremos y buscamos el título "Satured Fat"
                if nutriente.get('title') == 'Saturated Fat':
                    grGrasaSaturada = nutriente.get('amount', 'Información no disponible')
                    break   # No queda más remedio que utilizar el break para que no recorra toda la lista
            
            for nutriente in infoNutricional.get('bad'):    # Lo mismo de las grasas saturadas lo hacemos con el azúcar.
                if nutriente.get('title') == 'Sugar':
                    azucar = nutriente.get('amount', 'Información no disponible')
                    break

            for nutriente in infoNutricional.get('bad'):    # Lo mismo de las grasas saturadas lo hacemos con el sodio.
                if nutriente.get('title') == 'Sodium':
                    sodio = nutriente.get('amount', 'Información no disponible')
                    break

            for nutriente in infoNutricional.get('good'):   # Lo mismo, pero esta vez, "fibra", está en la lista "good"
                if nutriente.get('title') == 'Fiber':
                    fibra = nutriente.get('amount', 'Información nutricional no disponible')
                    break

            #Mostramos los nutrientes

            print("Calorías:", calorias, "kcal")
            print("Grasas totales:", grGrasa)
            print("Grasas saturadas:", grGrasaSaturada)
            print("Hidratos de carbono:", hidratos)
            print("Azúcar:", azucar)
            print("Proteína:", grProteina)
            print("Fibra:", fibra)
            print("Sodio:", sodio)
            
    else:
        print("Lo intentamos pero no pudimos encontrar la información de esa receta :(")

    mostrarBeneficios(infoNutricional)
    mostrarRiesgos(infoNutricional)

def mostrarBeneficios(infoNutricional):     # Beneficios de la receta
    
    nutrientesBuenos = infoNutricional.get('nutrients', [])

    for nutriente in infoNutricional.get('good'):   # Buscamos en la lista de nutrientes favorables
        nombre = nutriente.get('title', 'Información no disponible')
        porcentajeDiario = nutriente.get('percentOfDailyNeeds', 'Información no disponible')
        if porcentajeDiario > UMBRAL50:
            print(f"Esta receta es rica en {nombre} ({porcentajeDiario}% de necesidades diarias).")

def mostrarRiesgos(infoNutricional):        # Riesgos de la receta

    nutrientesMalos = infoNutricional.get('nutrients', [])  

    for nutriente in infoNutricional.get('bad'):    # Buscamos en la lista de nutrientes desfavorables
        nombre = nutriente.get('title', 'Información no disponible')
        porcentajeDiario = nutriente.get('percentOfDailyNeeds', 'Información no disponible')
        if porcentajeDiario > UMBRAL50:
            print(f"Avertencia: esta receta tiene un {porcentajeDiario}% de necesidades diarias de {nombre}.")

#Función auxiliar. Devuelve id y nombre de una receta

def obtenerIdYNombreReceta():
    nombreReceta = input("¿Cuál es la receta? \n")

    # Parametros a pasar en la url
    parametros = {
        "apiKey": apiKey,
        "number": 1,
        "query": nombreReceta
    }

    respuesta = requests.get(urlBase + "/autocomplete", params=parametros)      #LA API DEVUELVE UNA LISTA DE RECETAS AUTOCOMPLETADAS A PARTIR DE LA BÚSQUEDA

    if respuesta.status_code == OK200:    #Control de respuesta
        recetas = respuesta.json()

        if recetas and len(recetas) > 0:    #Devuelve una lista de recetas. Miramos si está vacía
            idReceta = recetas[0]['id']     #Solo quiero que me devuelva el id y el nombre de la primera de la lista
            tituloReceta = recetas[0]['title']
            return idReceta, tituloReceta
        else:
            print("Lo intentamos pero no pudimos encontrar esa receta :( ")
            return None, None   #Tuve problemas con el control de errores, y era porque no puse que devolviera None, None.
    else:
        print("Hubo un problema al buscar la receta.")
        return None, None
       
menu()



