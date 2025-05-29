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

###########################################################################################
# INICIO DE LA CLASE #
###########################################################################################
class wordGesser:
    def __init__(self):
        self.abecedario = list("abcdefghijklmnopqrstuvwxyz")
        self.abecedarioPonderado = []
        self.limCiclos = 20
        self.tamGeneracion = 10
        self.palabraTarget = ""
        self.longPalabra = 4
        self.gradoMutacion = 0.1
        self.limiteLetras = 8
        self.listaPalabras = []
        self.generacion = []
        self.historial = []
        self.historialAbecedarios = []
        self.ciclo = 0

    def esValida(self,palabra):
        if len(palabra) == self.longPalabra:
            if all(letra in self.abecedario for letra in palabra):
                return True
        return False
    
    def validarPalabra(self):
        for palabra, _ in self.generacion:
            if palabra == self.palabraTarget:
                return True
        return False
    
    def ingresarPalabra(self): 
        while True:
            palabra = input("Ingresá una palabra de 4 letras: ").lower()
            if self.esValida(palabra):
                self.palabraTarget = palabra
                break
            print("Palabra inválida. Intentá nuevamente.")

    def generarPalabra(self):
        if self.ciclo == 0 or self.evaluarGeneracion() < 0.25:
            return ''.join(random.choice(self.abecedario) for _ in range(len(self.palabraTarget)))
        else:
            return ''.join(
            random.choice(self.abecedarioPonderado 
                          if random.random() > self.gradoMutacion 
                          else self.abecedario)
            for _ in range(self.longPalabra)
        )

    def llenarListaPalabras(self):
        self.listaPalabras = [self.generarPalabra() for _ in range(self.tamGeneracion)]

    def construirGeneracion(self):
        self.generacion = []
        for palabra in self.listaPalabras:
            puntaje = self.evaluarPalabra(palabra)
            self.generacion.append((palabra, puntaje))
        
    def seleccionarMejores(self):
        umbral = self.evaluarGeneracion()
        puntuados = sorted(
            self.generacion,
            key=lambda x: x[1],
            reverse=True
        )
        puntuadosFiltrados = [p for p in puntuados if p[1] >= umbral]
        if len(puntuadosFiltrados) < self.tamGeneracion // 2:
            puntuadosFiltrados = puntuados[:self.tamGeneracion]

        mejores = [p[0] for p in puntuadosFiltrados[:self.tamGeneracion//5]]
        resto = [p[0] for p in puntuadosFiltrados[self.tamGeneracion//3:]]
        random.shuffle(resto)
        palabrasSeleccionadas = mejores + resto
        self.listaPalabras = [p[0] for p in palabrasSeleccionadas[:self.tamGeneracion]]

    def evaluarPalabra(self, palabra):
        puntos = 0
        letrasTarget = list(self.palabraTarget)
        letrasCandidata = list(palabra)
        for i in range(self.longPalabra):
            if letrasCandidata[i] == letrasTarget[i]:
                puntos += 1
                letrasTarget[i] = None
                letrasCandidata[i] = None
        for i in range(self.longPalabra):
            if letrasCandidata[i] is not None and letrasCandidata[i] in letrasTarget:
                puntos += 0.5
                idx = letrasTarget.index(letrasCandidata[i])
                letrasTarget[idx] = None
        return puntos

    def evaluarGeneracion(self):
        puntajes = [p[1] for p in self.generacion]
        return st.mean(puntajes) if puntajes else 0

    def cargarAbecedarioPon(self):
        todasLetras = "".join(self.listaPalabras)
        frecuencias = Counter(todasLetras)
        letrasFrecuentes = frecuencias.most_common(self.limiteLetras)
        self.abecedarioPonderado = []
        for letra, frecuencia in letrasFrecuentes:
            #la misma letra tantas veces como aparece en las palabras seleccionadas
            self.abecedarioPonderado.extend([letra] * frecuencia) 
        self.historialAbecedarios.append(self.abecedarioPonderado[:])
    
    def __str__(self):
        BOLD = "\033[1m"
        RESET = "\033[0m"
        salida = "\n📜 HISTORIAL COMPLETO DE GENERACIONES:"
        for i, generacion in enumerate(self.historial):
            salida += f"\n🌀 Generación {i+1}:"
            if i == 0:
                salida += "\n   🔤 Abecedario Ponderado: N/A (Generación aleatoria inicial)"
            else:
                # El abecedario que se usó para crear generación i
                abecedario_gen = self.historialAbecedarios[i-1]  
                resumen = Counter(abecedario_gen)
                salida += f"\n   🔤 Abecedario Ponderado: {dict(sorted(resumen.items()))}"
            promedio = self.evaluarGeneracion()
            salida += f"\n   📊 Promedio de la generación: {promedio:.2f}"
            for palabra, puntaje in generacion:
                if puntaje > promedio:
                    salida += f"\n   - {BOLD}{palabra}{RESET} | Puntaje: {puntaje}"
                else:
                    salida += f"\n   - {palabra} | Puntaje: {puntaje}"
        return salida                

    def jugar(self):
        print("🎯 BIENVENIDO AL JUEGO DE ADIVINAR LA PALABRA 🎯")
        # 1. Pedir el ingreso de la palabra objetivo
        self.ingresarPalabra()  
        # 2. Inicializar ciclo y limpiar historial
        self.ciclo = 0
        self.historial = []
        # 3. Repetir el ciclo hasta el límite de ciclos 
        while self.ciclo <= self.limCiclos:
            if self.ciclo > 0:
                # 3.4 Cargar abecedario ponderado
                self.cargarAbecedarioPon()
            self.llenarListaPalabras()
            # 3.1. Evaluar cada palabra y completar la generación
            self.construirGeneracion()
            # 3.2. Guardar la generación en el historial
            self.historial.append(self.generacion)
            # 3.3. Verificar si alguna palabra es igual a la palabra objetivo
            if self.validarPalabra():
                print(f"\n✅ ¡Palabra '{self.palabraTarget.upper()}' adivinada en el ciclo {self.ciclo}!")
                print(self)
                break
            else:
                # 3.3.1 Seleccionar las mejores palabras (por puntaje)
                self.seleccionarMejores()
                # 3.3.2 Pasar al sig. ciclo
                self.ciclo += 1
        else:
            print(f"\n🛑 No se adivinó la palabra en {self.limCiclos} ciclos.")
            print(self)                                                                                                                     
   
###########################################################################################
# FIN DE LA CLASE #
###########################################################################################
juego = wordGesser()
juego.jugar()