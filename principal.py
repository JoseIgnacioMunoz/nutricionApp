import requests #Importamos la biblioteca requests para hacer solicitudes a la API de Spoonacular.
import json
import os
apiKey = "64e9a5cb1b1f41daa6a4b3a8c572d2dc"
urlInicial = "https://api.spoonacular.com/recipes"  #Esta en principio es la url base que voy a utilizar


#-------Función para limpiar la terminal antes de la ejecución del menú. Fuente de información: https://stackoverflow.com/questions/2084508/clear-terminal-in-python

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
        print("2. Obtener nutrientes de una receta.")
        print("3. Mostrar riesgos y beneficios de una receta.")
        print("4. Receta aleatoria (desayuno/almuerzo/cena).")
        print("5. Salir")
        opcion = input("\nElige una opción: ")
        print("\n-------------------------------------------------")

        if opcion == "1":
            recetasPorIngredientes()
        #elif opcion == "2":
           # obtenerNutrientesDeReceta()
        #elif opcion == "3":
            # mostrarRiesgosYBeneficios()
        #elif opcion == "4":
            #recetaAleatoria()
        elif opcion == "5":
            print("¡Hasta luego!")
            salir=True
        else:
            print("Opción no válida. Por favor, elige una opción del 1 al 5.")

def recetasPorIngredientes():

    
    ingredientes = input("Ingresa los ingredientes separados por comas: ")
    numRecetas = input("Número de recetas a obtener: ")

    parametros = {      #Variable que guardará el diccionario de parámetros a pasar al método requests.get
            "apiKey": apiKey,
            "ingredients":  ingredientes,  # Ingredientes (la API espera que estén separados por comas)
            "number": numRecetas     # Cantidad de recetas a obtener
    }

    respuesta = requests.get(urlInicial + "/findByIngredients", params=parametros)    #Se usará para control de respuesta de la API

    if respuesta.status_code == 200:    #Aquí vemos si devuelve 200 OK con el status_code
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


menu()



