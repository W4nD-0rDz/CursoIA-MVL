"""
Del siguiente enunciado ir haciendo solo lo que vimos en la clase... el resto lo terminamos la clase que viene:
1. Importar el archivo nba.csv adjunto en un programa de python.
2. Modificar el campo nombre por jugador e imprimir el dataframe.
3. Imprimirle un mensaje al usuario en el que se le pida que indique que desea hacer: Ver todos los jugadores, ver detalle por jugador,  ver el puntaje general o graficar
4. Si desea ver los jugadores, imprimirle solo los nombres de los jugadores.
5. Si desea ver detalle, pedirle el nombre del jugador y mostrarle todos sus datos.
6. Si desea ver el puntaje general, calcular la madia de los puntos de los jugadores.
7. Si quiere graficar, mostrarle el gráfico de puntos por jugador en una tamaño de 10x10 color verde con los textos indicativos.
"""
import statistics as st
import pandas as pd
import tabulate

csv = "NBA"
nba=pd.read_csv("nba.csv")
nba.rename(columns = {"nombre":"jugador"}, inplace=True)
"""nba.to_csv("nba.csv", index=False)"""
#print(nba.to_markdown())

#print(nba.dtypes)

#Funciones de impresión:
def verJugadores():
    for i, row in nba.iterrows():
        print(row["jugador"].upper())
def verColumnas1_2():
    for i, row in nba.iterrows():
        print(f'N° {row["pos"]}: {row["jugador"].capitalize()}')
def verJugador(id):
    # Filtra el DataFrame para encontrar la fila donde la posición coincida
    jugador = nba[nba["pos"] == int(id)]  # Asegúrate de que 'id' sea tratado como un número entero
    if not jugador.empty:
        # Imprime los datos de la fila, mostrando la posición, jugador y puntos
        print(f"Posición: {jugador['pos'].values[0]}, Jugador: {jugador['jugador'].values[0].capitalize()}, Puntos: {jugador['puntos'].values[0]}")
        print("")
    else:
        print("No se encontró ningún jugador con ese número.")


#Funciones de acción:
def elegirJugador():
    print("Elija un jugador del listado: ")
    verColumnas1_2()
    posiciones_validas = nba["pos"].astype(str).tolist() 
    id = input("Ingrese el número de un jugador: ")
    # Se repite mientras no se ingrese un número válido
    while id not in posiciones_validas:
        print("Número inválido. Intente nuevamente.")
        id = input("Ingrese el número de un jugador: ")
    verJugador(id)
def verPuntajeGeneral():
    puntaje_promedio = st.mean(nba["puntos"])
    print("Puntaje promedio por jugador:", puntaje_promedio)
#def graficar():
def salir():
    print("Gracias por visitar", csv, "\n Hasta pronto!!")
    exit()
    
###MENU###
#Diccionario que contiene las funcionalidades a las que puede acceder en usuario
menuUsuario = {
    "1": ("Ver jugadores", verJugadores),
    "2": ("Ver detalle por jugador", elegirJugador),
    "3": ("Ver puntaje general", verPuntajeGeneral),
    #"4": ("Graficar", verGrafico),
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