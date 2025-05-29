"""Un algoritmo genético (AG) es un tipo de algoritmo de búsqueda y optimización inspirado en la 
evolución biológica. Su objetivo es encontrar soluciones aproximadas a problemas complejos, 
imitando el proceso de selección natural: los mejores, los más aptos, sobreviven, se reproducen, y sus "hijos" 
(nuevas soluciones) se prueban a ver si mejoran."""

# 🧬 ¿Cómo funciona un algoritmo genético?
# 1. Inicialización: Se genera una población inicial aleatoria de posibles soluciones.
import random

poblacion = 5
seleccion = 2
generaciones = 3
individuos = []

for i in range(poblacion):
    fuerza = random.randint(1, 3)
    intel = random.randint(1, 3)
    vel = random.randint(1, 3)
    aptitud = fuerza + intel + vel
    individuo = [fuerza, intel, vel, aptitud]
    individuos.append(individuo)
print("Primera generación:", individuos)

# 2. Evaluación (aptitud): Se mide qué tan buena es cada solución con una función de aptitud (fitness).
def seleccionar():
    global seleccionados
    seleccionados = []
    for k in range(seleccion):
        max_aptitud = 0
        for i in individuos:
            if i[3] > max_aptitud:
                max_aptitud = i[3]
                indice = individuos.index(i)
        seleccionados.append(individuos[indice])
        individuos[indice] = [0, 0, 0, 0]  # eliminamos temporalmente al mejor para no repetirlo

    print("Seleccionados:", seleccionados)

# 3. Reproducción (crear nueva población a partir de los mejores)
def heredar():
    global individuos
    individuos = []
    for i in range(poblacion):
        fuerza = random.choice([seleccionados[0][0], seleccionados[1][0]])
        intel = seleccionados[random.randint(0, 1)][1]
        vel = random.randint(1, 3)  #la velocidad muta aleatoriamente
        aptitud = fuerza + intel + vel
        individuo = [fuerza, intel, vel, aptitud]
        individuos.append(individuo)

    print("Nueva generación:", individuos)

# 4. Ejecutar por varias generaciones
for i in range(generaciones - 1):
    seleccionar()
    heredar()

# 5. Mostrar el mejor individuo final
max_aptitud = 0
for i in individuos:
    if i[3] > max_aptitud:
        max_aptitud = i[3]
        indice = individuos.index(i)

print("Mejor individuo final:", individuos[indice])