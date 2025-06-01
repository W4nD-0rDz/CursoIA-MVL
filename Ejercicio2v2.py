"""
Desarrollar un programa que le pida un usuario una palabra de cuatro letras 
    y la adivine por medio de un algoritmo genético. Para ello:
1. Importar la función choice de la librería random.
2. Importar la función fuzz de la librería fuzzywuzzy (previamente instalada desde CMD)
3. Declarar una lista con todos los caracteres el abecedario.
4. Pedirle al usuario que ingrese una palabra de cuatro caracteres. 
    En caso que ingrese un largo incorrecto pedírselo nuevamente.
5. Desarrollar el algoritmo genético para intentar acercarse lo más posible al resultado.
"""
#Forma de mutación: mutación adaptativa
import random
import statistics as st
from collections import Counter
from fuzzywuzzy import fuzz
import pandas as pd
import matplotlib.pyplot as plt

class wordGesser:
    def __init__(self):
        self.abecedario = list("abcdefghijklmnopqrstuvwxyz")
        self.abecedarioPonderado = []
        self.limCiclos = 20
        self.ciclo = 0
        self.tamGeneracion = 10
        self.palabraTarget = ""
        self.longPalabra = 4
        self.fuzzyIndexGeneracion = []
        self.limiteLetras = 10
        self.listaPalabras = [] #este se renueva en cada ciclo, guarda strings
        self.historial = [] #acumula cada generación (lista de listas de tuplas)
        self.generacion = [] #acumula (lista de tuplas que contienen: ({palabra:[c,o,d,e]}, FuzzyIndex) (una vez generada no se modifica)
        self.palabrasSeleccionadas = [] #lista de tuplas ({"palabra":[c,o,d,e]}, FuzzyIndex) seleccionadas en función de 1. FuzzyIndex > 25
        self.mejoresPalabras = [] #lista de tuplas ({"palabra":[c,o,d,e]}, FuzzyIndex) seleccionadas en función de 1. FuzzyIndex > 25 y 2. code (si contiene 1)
        self.resumenEstadistico = []

#METODOS INICIALES
    def ingresarPalabra(self): 
        while True:
            palabra = input("Ingresá una palabra de 4 letras: ").lower()
            if len(palabra) == self.longPalabra:
                if all(letra in self.abecedario for letra in palabra):
                    self.palabraTarget = palabra
                    break
            print("Palabra inválida. Intentá nuevamente.")
    
    def cargarAbecedarioPonderado(self):
        #Ver de agregar las letras de las palabras con un fuzzy distinto de 0 (al menos en el ciclo 1 a 3)
        todasLetras=''
        listaPalabras=[]
        for tupla in self.palabrasSeleccionadas:
            diccionario = tupla[0]
            palabra = list(diccionario.keys())[0]#extrae las palabras del diccionario
            listaPalabras.append(palabra)
        todasLetras = "".join(listaPalabras)
        for letra, frecuencia in Counter(todasLetras).items():
            if frecuencia > 3: 
                self.abecedarioPonderado.extend([letra] * frecuencia) #la misma letra tantas veces como aparece en las palabras seleccionadas

#METODOS DE EVALUACION
    def verificarExistencia(self, tupla):
        return tupla not in self.mejoresPalabras

    def evaluarFuzzyEnPalabra(self, palabra):
        return fuzz.ratio(palabra, self.palabraTarget)
    
    def analizarPosicion(self, palabra):
        code = []
        for i in range(self.longPalabra):
            if palabra[i] == self.palabraTarget[i]:
                code.append(1)
            else:
                code.append(0)
        return code
    
    def evaluarCodeEnTupla(self, tupla):
        diccionario = tupla[0]
        code = list(diccionario.values())[0]
        return sum(code)
    
    def evaluarFuzzyEnGeneracion(self):
        listaFuzzy = [tupla[1] for tupla in self.generacion]
        return st.mean(listaFuzzy)
        
#METODOS DE GENERACION DE PALABRAS    
    def generarPalabraAleatoria(self, cantidad):
        return [
            ''.join(random.choice(self.abecedario) for _ in range(self.longPalabra))
            for _ in range(int(cantidad))
        ]
        
    def generarPalabraPonderada(self, cantidad):
        palabrasPonderadas = []
        #Ordenar las palabrasSeleccionadas por la cantidad de 1 en el code
        self.palabrasSeleccionadas.sort(key=self.evaluarCodeEnTupla, reverse=True)

        while len(palabrasPonderadas) < int(cantidad):
            for tupla in self.palabrasSeleccionadas:
                diccionario = tupla[0]
                palabra = list(diccionario.keys())[0]
                code = list(diccionario.values())[0]
                
                letrasResultantes = []
                for i, flag in enumerate(code):
                    if flag == 1:
                        letrasResultantes.append(palabra[i])
                    else:
                        letrasResultantes.append(None)
                
                palabraTemporal = []
                for i, letra in enumerate(letrasResultantes):
                    if letra is not None:
                        palabraTemporal.append(letra)
                    else:
                        if self.abecedarioPonderado:
                            palabraTemporal.append(random.choice(self.abecedarioPonderado))
                        else:
                            palabraTemporal.append(random.choice(self.abecedario))

                palabraPonderada = "".join(palabraTemporal)
                palabrasPonderadas.append(palabraPonderada)
                if len(palabrasPonderadas) >= cantidad:
                    break                                         
        return palabrasPonderadas

    def generarPalabraWordle(self, cantidad):

        palabrasWordle = []
        letrasFijas = [None] * self.longPalabra
        
        for tupla in self.mejoresPalabras:
            diccionario = tupla[0]
            palabra = list(diccionario.keys())[0]
            code = list(diccionario.values())[0]

            for i, flag in enumerate(code):
                if flag == 1:
                    if letrasFijas[i] is None:
                        letrasFijas[i] = palabra[i]
        while len(palabrasWordle) < int(cantidad):
            letras = []
            for i in range(self.longPalabra):
                if letrasFijas[i] is not None:
                    letras.append(letrasFijas[i])
                elif self.abecedarioPonderado and random.random() < 0.7:
                    letras.append(random.choice(self.abecedarioPonderado))
                else:
                    letras.append(random.choice(self.abecedario))
            palabra = "".join(letras)
            palabrasWordle.append(palabra)

        return palabrasWordle
    
    def generarPalabras(self, variables):
        aleatoria = int(self.tamGeneracion * variables["aleatoria"])
        ponderada = int(self.tamGeneracion * variables["ponderada"])
        wordle = int(self.tamGeneracion * variables["wordle"])

        #Por si falta alguna palabra:
        total = aleatoria + ponderada + wordle
        diferencia = self.tamGeneracion - total
        aleatoria += diferencia

        listaPalabrasAleatorias = self.generarPalabraAleatoria(aleatoria)
        listaPalabrasPonderadas = self.generarPalabraPonderada(ponderada)
        listaPalabrasWordle = self.generarPalabraWordle(wordle)

        listaPalabras = listaPalabrasAleatorias + listaPalabrasPonderadas + listaPalabrasWordle
        self.listaPalabras = listaPalabras

#METODOS DE ALMACENAJE
    def generarTuplas(self):
        tuplas = []
        for palabra in self.listaPalabras:
            code = self.analizarPosicion(palabra)
            fuzzyIndex = self.evaluarFuzzyEnPalabra(palabra)
            palabraDiccionario = {palabra: code}

            palabraTupla = (palabraDiccionario, fuzzyIndex)
            tuplas.append(palabraTupla)
        return tuplas
    
    def almacenarTuplas(self):
        self.generacion = self.generarTuplas()
        
    def almacenarGeneracion(self):
        self.historial.append(self.generacion)
        self.fuzzyIndexGeneracion.append(self.evaluarFuzzyEnGeneracion())
    
    def registrar(self, cantidad1, cantidad2):
        cantidadPalabrasNuevas = cantidad1 - cantidad2
        fuzzyIndex = self.evaluarFuzzyEnGeneracion()
        self.resumenEstadistico.append((fuzzyIndex, cantidadPalabrasNuevas))

#METODOS DE SELECCION
    def ponderarPalabras(self):
        promedio = self.evaluarFuzzyEnGeneracion()
        candidatas = [tupla for tupla in self.generacion if tupla[1] >= promedio] # 1. almacena solo las que tienen FuzzyIndex ≥ promedio de la generación
        palabrasPonderadas = sorted(
            candidatas,
            key=lambda x: (sum(list(x[0].values())[0])),  # 2. ordenarlas según la cantidad de 1s en code
            reverse=True
        )
        self.palabrasSeleccionadas.extend(palabrasPonderadas) # Las almacena en la lista de palabrasSeleccionadas
        
    def seleccionarPalabras(self):
        cantidadPrevia = len(self.mejoresPalabras)
        candidatas = [tupla for tupla in self.generacion if self.evaluarCodeEnTupla(tupla) >= 1] # 1. Si tiene una o más letras en la posición correcta
        mejoresPalabras = sorted(
            candidatas,
            key=lambda x: (sum(list(x[0].values())[0])),  # 2. ordenarlas según la cantidad de 1s en code
            reverse=True
        )
        for tupla in mejoresPalabras:
            if self.verificarExistencia(tupla): # Agregar solo las palabras que no estén ya en self.palabrasSeleccionadas
                self.mejoresPalabras.append(tupla) # Las almacena en la lista de palabrasSeleccionadas
        cantidadActual = len(self.mejoresPalabras)

        #Datos para la estadística
        self.registrar(cantidadActual, cantidadPrevia)
           
#METODOS DE MUESTRA/IMPRESION
    def __str__(self):
        BOLD = "\033[1m"
        RESET = "\033[0m"
        salida = "\n📜 HISTORIAL COMPLETO DE GENERACIONES:"

        for i, generacion in enumerate(self.historial):
            salida += f"\n🌀 Generación {i+1}:"
            promedio = float(self.fuzzyIndexGeneracion[i])
            salida += f"\n   📊 Promedio de la generación: {promedio:.2f}"
            generacionOrdenada = sorted(generacion, key=lambda t:t[1], reverse=True)

            for tupla in generacionOrdenada:
                diccionario = tupla[0]
                palabra = next(iter(diccionario)) #Hace lo mismo que: list(diccionario.keys())[0]
                scoring = self.evaluarCodeEnTupla(tupla)
                fuzzyIndex = tupla[1]
                if scoring >= 1:
                    salida += f"\n  - {BOLD}{palabra}{RESET} | Code: {scoring} | Fuzzy: {fuzzyIndex:.2f}"
                else:
                    salida += f"\n  - {palabra} | Code: {scoring} | Fuzzy: {fuzzyIndex:.2f}"
        
        return salida

    def mostrarEstadistica(self):
        df = pd.DataFrame(self.resumenEstadistico, columns=["fuzzyIndex", "cantidad"])
        print(df.describe())

    def graficarEstadistica(self):
        df = pd.DataFrame(self.resumenEstadistico, columns=["fuzzyIndex", "cantidad"])
        df["generacion"] = df.index + 1
        
        plt.figure(figsize=(10, 5))
        #plt.scatter(x,y)
        plt.scatter(df["generacion"], df["fuzzyIndex"], color="blue", label="Índice Fuzzy promedio")
        plt.scatter(df["generacion"], df["cantidad"], color="green", label="Cantidad de Palabras Buenas")
        plt.xlabel("Generación")
        plt.ylabel("Valores")
        plt.title("Evolución del Índice Fuzzy y la cantidad de mejores candidatas por cada generación")
        plt.legend()
        plt.grid(True)
        plt.xticks(df["generacion"])  # fuerza a mostrar solo los valores enteros del índice
        plt.tight_layout()
        plt.show()

#METODOS DE JUEGO Y ADAPTACION
    def controlar(self):
        """
        El controlador devuelve un diccionario con la proporción de aplicación de cada método de generación de palabras
        Se basa en la evolución de las variables que se almacenan por fuera de cada generación:
        self.fuzzyIndexGeneracion = []
        self.mejoresPalabras = []
        """
        # Ciclo 0: todo aleatorio
        if self.ciclo == 0:
            return {"aleatoria": 1.0, "ponderada": 0.0, "wordle": 0.0}

        fuzzy_actual = self.fuzzyIndexGeneracion[-1] if self.fuzzyIndexGeneracion else 0
        fuzzy_anterior = self.fuzzyIndexGeneracion[-2] if len(self.fuzzyIndexGeneracion) > 1 else 0
        cantidadMejores = len(self.mejoresPalabras)

        # Ciclo 1
        if self.ciclo == 1:
            if fuzzy_actual == 0:
                return {"aleatoria": 1.0, "ponderada": 0.0, "wordle": 0.0}
            elif cantidadMejores >= 1:
                return { "aleatoria": 0.75, "ponderada": 0.15, "wordle": 0.10}

        # Ciclos posteriores
        if fuzzy_actual > fuzzy_anterior: #Si mejora el fuzzy.ratio de la generacion
            cantidadMejoresPalabras = len(self.mejoresPalabras)
            cantidadPalabrasUnicas = len(set([list(tupla[0].keys())[0] for tupla in self.mejoresPalabras]))
            if cantidadMejoresPalabras == cantidadPalabrasUnicas:
                # Aumenta el fuzzyIndex, pero no aumentan las palabras nuevas entre las mejores
                return {"aleatoria": 0.65, "ponderada": 0.25, "wordle": 0.10}
            else:
                # Aumenta fuzzyIndex y también aparecen más buenas
                return {"aleatoria": 0.50, "ponderada": 0.25, "wordle": 0.25}

        # Si el fuzzyIndex no mejora y no hay nuevas buenas
        return {"aleatoria": 0.80, "ponderada": 0.10, "wordle": 0.10}

    def jugar(self):
        print("🎯 BIENVENIDO AL JUEGO DE ADIVINAR LA PALABRA 🎯")
        self.ingresarPalabra()  
        self.ciclo = 0
        
        while self.ciclo < self.limCiclos:
            variables = self.controlar()
            self.generarPalabras(variables)
            self.almacenarTuplas()
            self.almacenarGeneracion()
            self.ponderarPalabras()
            self.seleccionarPalabras()
            self.cargarAbecedarioPonderado()
            palabrasGeneradas = [list(t[0].keys())[0] for t in self.generacion]
            if self.palabraTarget in palabrasGeneradas:
                print(f"\n🎉 ¡La palabra {self.palabraTarget.upper()} fue adivinada en el ciclo {self.ciclo + 1}!")
                print("Promedios FUZZY por generación: ", self.fuzzyIndexGeneracion)
                break  
            self.ciclo += 1
        else:
            print(f"\n🧪 Se alcanzó el límite de ciclos. La palabra era: {self.palabraTarget.upper()}")

        # Mostrar resumen final
        print(self)
        self.mostrarEstadistica()
        self.graficarEstadistica() 

###########################################################################################
# FIN DE LA CLASE #
###########################################################################################
juego = wordGesser()
juego.jugar()