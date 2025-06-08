"""
Del siguiente enunciado ir haciendo solo lo que vimos en la clase... el resto lo terminamos la clase que viene:
1. Importar el archivo nba.csv adjunto en un programa de python.
2. Modificar el campo nombre por jugador e imprimir el dataframe.
3. Imprimirle un mensaje al usuario en el que se le pida que indique que desea hacer: Ver todos los jugadores, ver detalle por jugador,  ver el puntaje general o graficar
4. Si desea ver los jugadores, imprimirle solo los nombres de los jugadores.
5. Si desea ver detalle, pedirle el nombre del jugador y mostrarle todos sus datos.
6. Si desea ver el puntaje general, calcular la madia de los puntos de los jugadores.
7. Si quiere graficar, mostrarle el gráfico de puntos por jugador en una tamaño de 
    10x10 color verde con los textos indicativos.
"""
import statistics as st
import pandas as pd
import matplotlib.pyplot as plt
import tabulate

csv = "NBA"
nba=pd.read_csv("nba.csv")
nba.rename(columns = {"nombre":"jugador"}, inplace=True)
"""nba.to_csv("nba.csv", index=False)"""
#print(nba.to_markdown())
#print(nba.dtypes)

###FUNCIONES DE IMPRESIÓN###
def verJugadores():
    for i, row in nba.iterrows():
        print(row["jugador"].upper())

def verColumnas1_2():
    for i, row in nba.iterrows():
        print(f'N° {row["pos"]}: {row["jugador"].capitalize()}')

def verJugador(id):
    # Filtra el DataFrame para encontrar la fila donde la posición coincida
    jugador = nba[nba["pos"] == int(id)]
    if not jugador.empty:
        # Imprime los datos de la fila: posición, jugador y puntos
        print(f"Posición: {jugador['pos'].values[0]}, Jugador: {jugador['jugador'].values[0].capitalize()}, Puntos: {jugador['puntos'].values[0]}")
        print("")
    else:
        print("No se encontró ningún jugador con ese número.")

def verGrafico():
    nbaGraf = identificarDuplicados(nba) 
    nbaGraf.sort_values("puntos", ascending=True) #<-- ordena lo que recibe del identificador de duplicados
    x = nbaGraf["Label"].str.capitalize() #<-- mayúscula a los nombres de los jugadores
    y = nbaGraf["puntos"]

    #Esto es necesario para usar el matplotlib directamente. En el archivo Clase2 está la versión para pyplot    
    fig, ejes = plt.subplots(figsize=(10,8), facecolor=('white'))  
    # A partir de acá se cambian las características del gráfico
    ejes.set_facecolor('lightgray')  
    ejes.bar( x,y, color=('lightgreen'), edgecolor=('green'), width=0.5)
    ejes.set_title("Puntaje General de Jugadores NBA", fontsize=16, fontweight="heavy")
    ejes.set_xlabel("Jugador", fontsize=12)
    ejes.set_ylabel("Puntaje", fontsize=12)
    ejes.set_xticklabels(x, rotation=0, ha='center', fontsize=10, fontweight='bold', color='darkgreen')
    ejes.set_yticklabels(y, rotation=45, ha='center', fontsize=12, fontweight='normal', color='darkgreen')
    ejes.tick_params(axis='x', pad=15)
    ejes.tick_params(axis='y', pad=20)

    fig.tight_layout()
    plt.show(block=True) #<-- block=True bloquea la ventana del gráfico (hay que reiniciar el juego para que se modifique NO es interactivo)
                         # para que sea interactivo: plt.ion() [arriba del todo el algoritmo] y luego puede ser .show(block=False) o .draw()  

###FUNCIONES DE ACCION###
def elegirJugador():
    print("Elija un jugador del listado: ")
    verColumnas1_2()
    posicionesValidas = nba["pos"].astype(str).tolist() 
    id = input("Ingrese el número de un jugador: ")
    # Se repite mientras no se ingrese un número válido
    while id not in posicionesValidas:
        print("Número inválido. Intente nuevamente.")
        id = input("Ingrese el número de un jugador: ")
    verJugador(id)

def verPuntajeGeneral():
    puntaje_promedio = st.mean(nba["puntos"])
    print("Puntaje promedio por jugador:", puntaje_promedio)

def identificarDuplicados(df):
    df = df.copy()
    df["Label"] = df["jugador"]
    contador = {}
    for i in range(len(df)):
        nombre = df.loc[i, "Label"]
        if nombre in contador:
            contador[nombre] += 1
            df.loc[i, "Label"] = f"{nombre}-{contador[nombre]}"
        else:
            contador[nombre] = 0
    return df

def salir():
    print("Gracias por visitar", csv, "\n Hasta pronto!!")
    exit()
    
###MENU###
#Diccionario que contiene las funcionalidades a las que puede acceder en usuario
menuUsuario = {
    "1": ("Ver jugadores", verJugadores),
    "2": ("Ver detalle por jugador", elegirJugador),
    "3": ("Ver puntaje general", verPuntajeGeneral),
    "4": ("Graficar", verGrafico),
    "0": ("Salir", salir)
}

#Función que muestra el diccionario menu
def mostrarMenuUsuario():
    for opcion, (descripcion, _) in menuUsuario.items():
        print(f"{opcion}. {descripcion}")
#Función que encapsula las funcionalidades del algoritmo
def ejecutarMenuUsuario():
    print("")
    print("BIENVENIDO A", csv)
    print("")
    while True:
        print("Elija una opción de entre las siguientes:")
        mostrarMenuUsuario()
        opcion = input("Opción: ").strip()
        print("")
        if opcion in menuUsuario:
            _, funcion = menuUsuario[opcion]
            funcion()
            if opcion == "0":
                break
        else:
            print("Opción inválida. Intente nuevamente.")
    
ejecutarMenuUsuario()
