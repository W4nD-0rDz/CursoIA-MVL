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
#Forma de mutación: mutación adaptativa o heurística basada en frecuencia

import random
import statistics as st
from collections import Counter
from fuzzywuzzy import fuzz

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

#METODOS INICIALES
    def ingresarPalabra(self): 
        while True:
            palabra = input("Ingresá una palabra de 4 letras: ").lower()
            if len(palabra) == self.longPalabra:
                if all(letra in self.abecedario for letra in palabra):
                    self.palabraTarget = palabra
                    break
            print("Palabra inválida. Intentá nuevamente.")
    
    def cargarAbecedarioPonderado(self, generacion):
        #Ver de agregar las letras de las palabras con un fuzzy distinto de 0 (al menos en el ciclo 1 a 3)
        self.mejoresPalabras.extend(self.seleccionarPalabras(generacion))
        todasLetras=''
        listaPalabras=[]
        for tupla in self.mejoresPalabras:
            diccionario = tupla[0]
            palabra = list(diccionario.keys())[0]#extrae las palabras del diccionario
            listaPalabras.append(palabra)
        todasLetras = "".join(listaPalabras)
        for letra, frecuencia in Counter(todasLetras).items():
            if frecuencia > 3: #la misma letra tantas veces como aparece en las palabras seleccionadas
                self.abecedarioPonderado.extend([letra] * frecuencia)

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
    
    def evaluarCodeEnTupla(tupla):
        diccionario = tupla[0]
        code = list(diccionario.values())
        return sum(code)
    
    def evaluarFuzzyEnGeneracion(self, generacion):
        #fuzzy 0-100, entonces si hay 1 letra de 4 da 25.
        listaFuzzy = [tupla[1] for tupla in generacion]
        #tamaño de la generación = 10
        return st.mean(listaFuzzy)
    
    # def evaluarPosicion(self, tupla):
    #     sumaLetrasOk = 0
    #     diccionario = tupla[0]
    #     palabra = list(diccionario.keys())[0]
    #     code = diccionario[palabra]
    #     sumaLetrasOk += sum(code)
    #     return sumaLetrasOk
    
#METODOS DE GENERACION DE PALABRAS    
    def generarPalabraAleatoria(self):
        for _ in range(self.longPalabra):
            return ''.join(random.choice(self.abecedario))
        
    def generarPalabraPonderada(self, cantidad):
        palabrasPonderadas = []
        #Ordenar las palabrasSeleccionadas por la cantidad de 1 en el code
        self.palabrasSeleccionadas.sort(key=self.evaluarCodeEnTupla, reverse=True)

        while len(palabrasPonderadas) < cantidad:
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
                            letrasResultantes[i] = random.choice(self.abecedarioPonderado)
                        else:
                            letrasResultantes[i] = random.choice(self.abecedario)

                palabraPonderada = "".join(palabraTemporal)
                palabrasPonderadas.append(palabraPonderada)
                if len(palabrasPonderadas) >= cantidad:
                    break                                         
        return palabrasPonderadas

    def generarPalabraWordle(self, cantidad):
        palabrasWordle = []
        letrasFijas = [None] * self.longPalabra
        while len(palabrasWordle) <= cantidad:
            for tupla in self.mejoresPalabras:
                diccionario = tupla[0]
                palabra = list(diccionario.keys())[0]
                code = list(diccionario.values())[0]

                for i, flag in enumerate(code):
                    if flag == 1:
                        if letrasFijas[i] is None:
                            letrasFijas[i] = palabra[i]
                
                for _ in range(self.tamGeneracion//4): #Proporción de la generación de mutación Wordle
                    letrasWordle = []
                    palabraWordle = ""
                    for i in range(self.longPalabra):
                        if letrasFijas[i] is not None:
                            letrasWordle.append(letrasFijas[i])
                        else:
                            if self.abecedarioPonderado and random.random() < 0.7:
                                letrasWordle.append(random.choice(self.abecedarioPonderado))
                            else:
                                letrasWordle.append(random.choice(self.abecedario))
                    palabraWordle = "".join(letrasWordle)
                    palabrasWordle.append(palabraWordle)            
        return palabrasWordle

    # def generarPalabra(self,palabraTupla,fuente):
    #     #palabras sin antecesores
    #     if not palabraTupla:
    #             return ''.join(random.choice(fuente) for _ in range(self.longPalabra))
    #     #palabras con antecesores, mutación guiada (x medio de abecedarioPonderado)
    #     elif palabra:
    #         diccionario = palabraTupla[0]
    #         palabra = list(diccionario.keys())[0]
    #         code = diccionario[palabra]
    #         intento=''
    #         for i in range(len(code)):
    #             if code[i] == 1:
    #                 intento += palabra[i]
    #             else:
    #                 intento += random.choice(random.shuffle(fuente))
    #         return intento

#METODOS DE ALMACENAJE
    def llenarListaPalabras(self):
        if self.ciclo == 0:
            fuente = self.abecedario
        elif self.ciclo > 0 and self.mejoresPalabras:
            fuente = self.abecedarioPonderado
            for palabraTupla in self.mejoresPalabras:
                self.listaPalabras.extend([self.generarPalabra(palabraTupla,fuente) for _ in range(self.tamGeneracion)])
        elif self.ciclo > 0 and not self.mejoresPalabras:
            self.listaPalabras = [self.generarPalabra(palabraTupla,fuente) for _ in range(self.tamGeneracion)]
    
    def generarTuplas(self, listaPalabras):
        tuplas = []
        for palabra in listaPalabras:
            code = self.evaluarPosicion(palabra)
            fuzzyIndex = self.evaluarFuzzy(palabra)
            palabraDiccionario = {palabra:code}
            palabraTupla = (palabraDiccionario, fuzzyIndex)
            tuplas.append(palabraTupla)
        return tuplas
    
    def almacenarTuplas(self,tuplas):
        self.generacion.extend(tuplas)

    def almacenarGeneracion(self, generacion):
        self.historial.extend(generacion)

#METODOS DE SELECCION
    def ponderarPalabras(self, generacion):
        candidatas = [tupla for tupla in generacion if tupla[1] >= self.evaluarFuzzy(generacion)] # 1. Ver cuántas palabras tienen FuzzyIndex ≥ promedio de la generación
        palabrasSeleccionadas = sorted(
            candidatas,
            key=lambda x: (sum(list(x[0].values())[0])),  # 2. ordenarlas según la cantidad de 1s en code
            reverse=True
        )
        self.palabrasSeleccionadas.extend(palabrasSeleccionadas) # Las almacena en la lista de palabrasSeleccionadas
        
    def seleccionarPalabras(self, generacion):
        candidatas = [tupla for tupla in generacion if self.evaluarCodeEnTupla(tupla) >= 1] # 1. Si tiene una o más letras en la posición correcta
        mejoresPalabras = sorted(
            candidatas,
            key=lambda x: (sum(list(x[0].values())[0])),  # 2. ordenarlas según la cantidad de 1s en code
            reverse=True
        )
        
        for tupla in mejoresPalabras:
            if self.verificarExistencia(tupla): # Agregar solo las palabras que no estén ya en self.palabrasSeleccionadas
                self.mejoresPalabras.extend(tupla) # Las almacena en la lista de palabrasSeleccionadas

#METODOS DE JUEGO Y ADAPTACION
    def controlador(self):
        """
        Retorna un diccionario con la proporción de uso de cada estrategia
        basada en el ciclo actual, el progreso de fuzzyIndex y mejoresPalabras.
        """
        # Ciclo 0: todo aleatorio
        if self.ciclo == 0:
            return {
                "aleatoria": 1.0, "ponderada": 0.0, "wordle": 0.0
            }

        fuzzy_actual = self.fuzzyIndexGeneracion[-1] if self.fuzzyIndexGeneracion else 0
        fuzzy_anterior = self.fuzzyIndexGeneracion[-2] if len(self.fuzzyIndexGeneracion) > 1 else 0
        cantidad_mejores = len(self.mejoresPalabras)

        # Ciclo 1
        if self.ciclo == 1:
            if fuzzy_actual == 0:
                return { 
                    "aleatoria": 1.0, "ponderada": 0.0, "wordle": 0.0
                }
            elif cantidad_mejores >= 1:
                return {
                    "aleatoria": 0.75, "ponderada": 0.15, "wordle": 0.10
                }

        # Ciclos posteriores
        if fuzzy_actual > fuzzy_anterior:
            if cantidad_mejores == len(set(self.mejoresPalabras)):
                # Aumenta el fuzzyIndex, pero no crecen los buenos resultados
                return {
                    "aleatoria": 0.65, "ponderada": 0.25, "wordle": 0.10
                }
            else:
                # Aumenta fuzzyIndex y también aparecen más buenas
                return {
                    "aleatoria": 0.50, "ponderada": 0.25, "wordle": 0.25
                }

        # Si el fuzzyIndex no mejora y no hay nuevas buenas
        return {
            "aleatoria": 0.80, "ponderada": 0.10, "wordle": 0.10
        }

    def jugar(self):
        print("🎯 BIENVENIDO AL JUEGO DE ADIVINAR LA PALABRA 🎯")
        # 1. Pedir el ingreso de la palabra objetivo
        self.ingresarPalabra()  
        # 2. Inicializar ciclo y limpiar historial
        self.ciclo = 0
        self.historial = []

###########################################################################################
# FIN DE LA CLASE #
###########################################################################################
juego = wordGesser()
juego.jugar()
        
