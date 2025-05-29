import random
from random import randint

poblacion=5
seleccion=2
generaciones=3
individuos=[]

for i in range(poblacion):
    fuerza=random.randint(1,3)
    intel=random.randint(1,3)
    vel=random.randint(1,3)
    aptitud=fuerza+intel+vel
    individuo=[fuerza,intel,vel,aptitud]
    individuos.append(individuo)

print("la primer generacion es" , individuos)


def seleccionar():
    global seleccionados
    seleccionados=[]
    for k in range(seleccion):
        max=0
        for i in individuos:
            if i[3]>max:
                max=i[3]
                indice=individuos.index(i) #1
        seleccionados.append(individuos[indice])
        individuos[indice]=[0,0,0,0]
    print("los seleccionados son:" , seleccionados)

def heredar():
    global individuos
    individuos=[]
    for i in range (poblacion):
        fuerza =seleccionados[random.randint(0,1)][0]
        intel=seleccionados[random.randint(0,1)][1]
        vel=random.randint(1,3)
        aptitud=fuerza+intel+vel
        individuo=[fuerza,intel,vel,aptitud]
        individuos.append(individuo)
    print("La siguiente poblacion es", individuos)

for i in range(generaciones-1):  #2
    seleccionar()
    heredar()

#individuos=[[1, 3, 2, 6], [1, 3, 3, 7], [3, 3, 3, 9], [3, 3, 2, 8], [3, 3, 1, 7]]

max=0
for i in individuos:
    if i[3]>max:
        max=i[3]
        indice=individuos.index(i) #2

print(individuos[indice])