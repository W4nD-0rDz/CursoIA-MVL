import random
import statistics as st

# Definimos la clase Individuo
class Individuo:
    #Constructor
    def __init__(self):
        self.fuerza = random.randint(0, 3)
        self.inteligencia = random.randint(0, 3)
        self.velocidad = random.randint(0, 3)
        self.aptitud = self.fuerza + self.inteligencia + self.velocidad

    def actualizarAptitud(self):
        self.aptitud = self.fuerza + self.inteligencia + self.velocidad

    #Genera los atributos al azar (refuerza lo que genera el constructor)
    def mutar(self):
        gen_a_mutar = random.choice(['fuerza', 'inteligencia', 'velocidad'])
        if gen_a_mutar == 'fuerza':
            self.fuerza = random.randint(0, 3)
        elif gen_a_mutar == 'inteligencia':
            self.inteligencia = random.randint(0, 3)
        elif gen_a_mutar == 'velocidad':
            self.velocidad = random.randint(0, 3)
        self.actualizarAptitud()
    
    #Genera los atributos al azar en base a los de los padres
       
    #debe marcarse como método estático porque no depende de una instancia específica (no usa self).
    # Opera sobre dos objetos Individuo (los padres) y devuelve un nuevo Individuo (el hijo).
    # Se marca como estático para indicar que es una función relacionada con la clase,
    # pero que no modifica ni necesita acceder a atributos de una instancia particular.
    @staticmethod
    def cruzar(madre, padre):
        hijo = Individuo.__new__(Individuo)
        hijo.fuerza = random.choice([madre.fuerza, padre.fuerza])
        hijo.inteligencia = random.choice([madre.inteligencia, padre.inteligencia])
        hijo.velocidad = random.choice([madre.velocidad, padre.velocidad])
        hijo.actualizarAptitud()
        return hijo

    #Muestra los atributos de cada individuo
    def __repr__(self):
        return f"(F:{self.fuerza}, I:{self.inteligencia}, V:{self.velocidad}, A:{self.aptitud})"
    
###########################################################################################
# FIN DE LA CLASE #
###########################################################################################

historial = []
tamano = 5


# Crear la población
def poblar(tamano):
    poblacion = []
    for i in range(tamano):
        individuo = Individuo()
        poblacion.append(individuo)
    return poblacion

#OPT: una función que permita aumentar la diversidad:
#Calcula desviaciones = cuán distinto es un ind respecto de la media de la generación
def aumentarDiversidad(poblacion):
    fuerzas = [ind.fuerza for ind in poblacion]
    inteligencias = [ind.inteligencia for ind in poblacion]
    velocidades = [ind.velocidad for ind in poblacion]

    media_fuerza = st.mean(fuerzas)
    desv_fuerza = st.stdev(fuerzas) if len(fuerzas) > 1 else 0
    media_inteligencia = st.mean(inteligencias)
    desv_inteligencia = st.stdev(inteligencias) if len(inteligencias) > 1 else 0
    media_velocidad = st.mean(velocidades)
    desv_velocidad = st.stdev(velocidades) if len(velocidades) > 1 else 0

    def diversidad_ind(ind):
        d_f = abs(ind.fuerza - media_fuerza) / desv_fuerza if desv_fuerza != 0 else 0
        d_i = abs(ind.inteligencia - media_inteligencia) / desv_inteligencia if desv_inteligencia != 0 else 0
        d_v = abs(ind.velocidad - media_velocidad) / desv_velocidad if desv_velocidad != 0 else 0
        return d_f + d_i + d_v
    return diversidad_ind

#Se eligen a los "mejores" de la generación para reproducir
def seleccionar(poblacion):
    def aptitud_madre(ind):
        return 0.2*ind.fuerza + 0.5* ind.inteligencia + 0.3*ind.velocidad
    def aptitud_padre(ind):
        return 0.5*ind.fuerza + 0.2* ind.inteligencia + 0.3*ind.velocidad
    
    diversidad_ind = aumentarDiversidad(poblacion)

    # Ordenar candidatos combinando aptitud y diversidad para madre
    candidatos_madre = sorted(
        poblacion,
        key=lambda ind: (aptitud_madre(ind), diversidad_ind(ind)),
        reverse=True
    )
    madre = candidatos_madre[0]

        # Filtramos a la madre del conjunto de candidatos a padre
    poblacion_sin_madre = [ind for ind in poblacion if ind != madre]

    # Ordenar candidatos combinando aptitud y diversidad para padre
    candidatos_padre = sorted(
        poblacion_sin_madre,
        key=lambda ind: (aptitud_padre(ind), diversidad_ind(ind)),
        reverse=True
    )
    padre = candidatos_padre[0]
    return madre, padre

# Crear generación
def reproducir(tamano, poblacion):
    madre, padre = seleccionar(poblacion)
    print("Madre: ", madre, "\nPadre: ", padre)
    generacion = []
    for i in range(tamano):
        individuo = Individuo.cruzar(madre, padre)
        #Para evitar convergencia prematura, que los hijos sean demasiado parecidos a los padres
        difP1 = abs(madre.aptitud - individuo.aptitud)
        difP2 = abs(padre.aptitud - individuo.aptitud)
        aptitudes = [madre.aptitud, padre.aptitud, individuo.aptitud]

        if st.stdev(aptitudes) < 0.75:
            if st.mean([difP1, difP2]) < 0.9:
                individuo.mutar()
        generacion.append(individuo)
    return generacion

# Elegir al mejor
def premiar(generacion):
    #ultimaGen = historial[len(historial)-1]
    #ultimaGen = historial[-1]
    return max(generacion, key=lambda ind: ind.aptitud)
    
# Mostrar la generación
def mostrar(grupo):
    for ind in grupo:
        print(ind)

# Repetir el ciclo
def repetir(ciclos):
    poblacion = poblar(tamano)
    print("Generación inicial:")
    mostrar(poblacion)
    historial.append(poblacion)
    for k in range(int(ciclos)):
        print(f"Generación {k+1}:")
        generacion = reproducir(tamano, poblacion)
        mostrar(generacion)
        historial.append(generacion)
        poblacion = generacion
    

ciclos = input("Por favor elija la cantidad de veces que se repite el ciclo: ")
repetir(ciclos)
mejor = premiar([ind for generacion in historial for ind in generacion])
print("El mejor individuo de la generación es ", mejor)
