"""
Publicado: 5 sept 2023 (Última modificación: 22 mar)
Asignado
1. Importar el csv como matriz en python.
2. Eliminar de la matriz a los jugadores que no posean fotos.
3. Imprimir un mensaje indicando aquellos jugadores que posean foto en blanco y negro. 
(escala de grises)
4. Que el programa muestre un menu que le pida al usuario que indique que desea hacer: 
ver un jugados, ver todos o borrar un jugador.
5. Si selecciona ver un jugador, el sistema le pedirá el número de camiseta y que lo imprima 
en pantalla con su nombre por como título y sin mostrar los ejes.
6. Si selecciona ver todos, mostrar en una sola impresión a todos los jugadores.
7. Si decide borrar un jugador, pedirle el nombre y el apellido. Borrar su foto de la carpeta
 y eliminarlo de la matriz. También borrarlo del archivo csv original.
"""

import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from fuzzywuzzy import fuzz
from matplotlib.gridspec import GridSpec
import pandas as pd
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import os
import shutil

csv = "⭐⭐⭐ARGENTINA⭐⭐⭐"
afa = pd.read_csv("argentina.csv")
afa['num'] = pd.to_numeric(afa['num'], errors='coerce')
afa = afa.dropna(subset=['num'])  # elimina filas como DT o AC
afa['num'] = afa['num'].astype(int)  # opcional: convierte a enteros si ya no hay NaNs

##################################################FUNCIONES############################################################
#RGB = 3, escalaGrises = 2
def contarCanales(imagen):
    if len(imagen.shape) == 2:
        return 1  # escala de grises (un canal)
    elif len(imagen.shape) == 3:
        return imagen.shape[2]  # cantidad de canales (3 o 4)
    else:
        return 0  # formato inesperado


def identificarGrises():
    df = afa
    for _, fila in df.iterrows():
        archivo = f"{fila['nombre'].lower()} {fila['apellido'].lower()}.jpg"
        ruta_imagen = os.path.join("imagenes/fotos", archivo)
        if os.path.exists(ruta_imagen):
            try:
                imagen = Image.open(ruta_imagen)
                imagen_np = np.array(imagen)
                canales = contarCanales(imagen_np)
                if canales == 1:
                    print(f"El archivo {archivo} está en escala de grises.")
                # elif canales == 3:
                #     print(f"{nombre_archivo} está en RGB.")
                # else:
                #     print(f"{nombre_archivo}: formato no reconocido.")
            except Exception as e:
                print(f"Error al procesar {archivo}: {e}")
        else:
            print(f"{archivo} no encontrado.")

def obtenerRutasFotos(jugadores_df, carpeta_fotos):
    rutas = []
    for _, row in jugadores_df.iterrows():
        nombre_archivo = f"{row['nombre'].lower()} {row['apellido'].lower()}.jpg"
        ruta = os.path.join(carpeta_fotos, nombre_archivo)
        if os.path.exists(ruta):
            rutas.append((ruta, row['nombre'] + " " + row['apellido']))
    return rutas

def ubicarJugador():
    try:
        numero = int(input("Indique el número de la camiseta del jugador: "))
    except ValueError:
        print("Número inválido.")
        return None, None
    fila = afa[afa['num'] == numero]
    if fila.empty:
        print(f"No se encontró jugador con número {numero}.")
        return None, None

    nombre = fila.iloc[0]['nombre']
    apellido = fila.iloc[0]['apellido']
    jugador = f"{nombre} {apellido}".lower()
    carpeta = "imagenes/fotos/"
    archivo = jugador + ".jpg"
    return carpeta, archivo

def clasificarImagenesXForma(rutas):
    clasificadas = []
    for ruta, nombre in rutas:
        with Image.open(ruta) as img:
            ancho, alto = img.size
            proporcion = ancho / alto
            if proporcion > 1.2:
                forma = "ancha"
            elif proporcion < 0.8:
                forma = "alta"
            else:
                forma = "cuadrada"
            clasificadas.append((ruta, nombre, forma))
    return clasificadas

def calcularTamanoGrilla(clasificadas):
    modulos = 0
    for _, _, forma in clasificadas:
        if forma == "cuadrada":
            modulos += 1
        else:
            modulos += 2
    columnas = 4
    filas = -(-modulos // columnas)  # redondeo hacia arriba
    return filas, columnas

#######################################################################################################################
def mostrarJugador():
    carpeta, archivo = ubicarJugador()
    if carpeta is None or archivo is None:
        return
    ruta = os.path.join(carpeta, archivo)
    if not os.path.exists(ruta):
        print(f"No se encontró la foto de {archivo}.")
        return
    
    try:
        img = Image.open(ruta)
    except Exception as e:
        print(f"Error al abrir la imagen: {e}")
        return
    
    nombreSinExtension = os.path.splitext(archivo)[0]
    draw = ImageDraw.Draw(img)
    try:
        fuente = ImageFont.truetype("arial.ttf", 20)
    except:
        fuente = ImageFont.load_default()
    
    ancho, alto = img.size
    anchoTxt, altoTxt = draw.textsize(nombreSinExtension, font=fuente)
    x = (ancho - anchoTxt) // 2
    y = (alto - altoTxt) - 10

    draw.text((x,y), nombreSinExtension, fill="red", font=fuente)
    img.show()

def mostrarGrillaImagenes(clasificadas, filas, columnas):
    fig = plt.figure(figsize=(columnas * 2.5, filas * 2.5))
    gs = fig.add_gridspec(filas, columnas)
    ocupado = [[False]*columnas for _ in range(filas)]

    def buscar_lugar(ancho, alto):
        for r in range(filas - alto + 1):
            for c in range(columnas - ancho + 1):
                if all(not ocupado[r+i][c+j] for i in range(alto) for j in range(ancho)):
                    for i in range(alto):
                        for j in range(ancho):
                            ocupado[r+i][c+j] = True
                    return r, c
        return None, None

    for ruta, nombre, forma in clasificadas:
        img = Image.open(ruta)
        img_array = np.array(img)
        if forma == "cuadrada":
            alto, ancho = 1, 1
        elif forma == "ancha":
            alto, ancho = 1, 2
        else:
            alto, ancho = 2, 1
        r, c = buscar_lugar(ancho, alto)
        if r is not None:
            ax = fig.add_subplot(gs[r:r+alto, c:c+ancho])
            ax.imshow(img_array)
            ax.set_title(nombre, fontsize=8)
            ax.axis('off')

    plt.tight_layout()
    plt.show()

def mostrarJugadores():
    df = afa
    rutas = obtenerRutasFotos(df, "imagenes/fotos")
    clasificadas = clasificarImagenesXForma(rutas)
    filas, columnas = calcularTamanoGrilla(clasificadas)
    mostrarGrillaImagenes(clasificadas, filas, columnas)


###############################################ELIMINA DEFINITIVAMENTE#################################################
# def eliminarJugador():
#     nombre = str(input("Indique el nombre del jugador: ")).lower()
#     apellido = str(input("Indique el apellido del jugador: ")).lower()
#     jugador = nombre+" "+apellido
#     #Con una excepción, por si el archivo no se encuentra:
#     try:
#         os.unlink("imagenes/fotos/"+jugador+".jpg")
#         print("Se ha eliminado "+jugador+" de la lista.")
#     except FileNotFoundError:
#         print("Jugador no encontrado.")

def eliminarRegistrosSinFotoFuzzy(limite=90):
    ruta_csv = "argentina.csv"
    carpetaFotos = "imagenes/fotos"

    df = pd.read_csv(ruta_csv)
    archivos_fotos = [f.lower().replace(".jpg", "") 
        for f in os.listdir(carpetaFotos) if f.endswith(".jpg")]

    def tiene_foto(nombre, apellido):
        nombre_completo = f"{nombre.lower()} {apellido.lower()}"
        puntajes = [fuzz.partial_ratio(nombre_completo, archivo) for archivo in archivos_fotos]
        return max(puntajes, default=0) >= limite
    
    dfFiltrado = df[df.apply(lambda row:tiene_foto(row["nombre"], row["apellido"]), axis=1)]
    eliminados = len(df) - len(dfFiltrado)
    df = dfFiltrado

    dfFiltrado.to_csv(ruta_csv, index=False)
    print(f"Se eliminaron {eliminados} registros sin foto")

###############################################ELIMINA TEMPORARIAMENTE#################################################
def eliminarJugador():
    nombre = input("Indique el nombre del jugador: ").strip().lower()
    apellido = input("Indique el apellido del jugador: ").strip().lower()
    jugador = f"{nombre} {apellido}"
    origen = f"imagenes/fotos/{jugador}.jpg"
    destino = f"imagenes/eliminados/{jugador}.jpg"

    try:
        if not os.path.exists("imagenes/eliminados"): 
            os.makedirs("imagenes/eliminados") 
        shutil.move(origen, destino) 
        print(f"Se ha eliminado {jugador} de la lista (movido a eliminados).")
    except FileNotFoundError:
        print("Jugador no encontrado.")

def eliminarJugador():
    nombre = input("Indique el nombre del jugador: ").strip().lower()
    apellido = input("Indique el apellido del jugador: ").strip().lower()
    jugador = f"{nombre} {apellido}"
    origen_foto = f"imagenes/fotos/{jugador}.jpg"
    destino_foto = f"imagenes/eliminados/{jugador}.jpg"

    try:
        # Mover foto a carpeta "eliminados"
        if os.path.exists(origen_foto):
            if not os.path.exists("imagenes/eliminados"):
                os.makedirs("imagenes/eliminados")
            shutil.move(origen_foto, destino_foto)
            print(f"Foto de {jugador} movida a eliminados.")
        else:
            print("Foto no encontrada.")

        # Eliminar del CSV
        df = afa
        eliminado = df[(df["nombre"].str.lower() == nombre) & (df["apellido"].str.lower() == apellido)]

        if eliminado.empty:
            print("Registro no encontrado en el CSV.")
            return

        df = df.drop(eliminado.index)
        df.to_csv("argentina.csv", index=False)

        if os.path.exists("imagenes/eliminados.csv"):
            df_elim = pd.read_csv("imagenes/eliminados.csv")
            df_elim = pd.concat([df_elim, eliminado], ignore_index=True)
        else:
            df_elim = eliminado

        df_elim.to_csv("imagenes/eliminados.csv", index=False)
        print(f"Registro de {jugador} eliminado del CSV.")

    except Exception as e:
        print("Error al eliminar al jugador:", e)
#########################RESTAURA###############################################################################
def restaurarTodo():
    # Restaurar imágenes
    origen_img = "imagenes/eliminados"
    destino_img = "imagenes/fotos"

    if os.path.exists(origen_img):
        for archivo in os.listdir(origen_img):
            ruta_origen = os.path.join(origen_img, archivo)
            ruta_destino = os.path.join(destino_img, archivo)
            shutil.move(ruta_origen, ruta_destino)
        print("Se han restaurado las imágenes eliminadas.")
    else:
        print("No hay imágenes para restaurar.")

    # Restaurar registros CSV
    eliminados_csv = "eliminados.csv"
    original_csv = "argentina.csv"

    if os.path.exists(eliminados_csv):
        df = pd.read_csv(original_csv)
        df_elim = pd.read_csv(eliminados_csv)
        df = pd.concat([df, df_elim], ignore_index=True)
        df.to_csv(original_csv, index=False)
        os.remove(eliminados_csv)
        print("Se han restaurado los jugadores al CSV.")
    else:
        print("No hay registros de jugadores para restaurar.")

def salir():
    print("Gracias por visitar", csv, "\n Hasta pronto!!")
    exit()
    

###MENU###
#Diccionario que contiene las funcionalidades a las que puede acceder en usuario
menuUsuario = {
    "1": ("Ver jugador", mostrarJugador),
    "2": ("Ver todos los jugadores", mostrarJugadores),
    "3": ("Eliminar jugador", eliminarJugador),
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
    eliminarRegistrosSinFotoFuzzy()
    identificarGrises()
    while True:
        print("Elija una opción de entre las siguientes:")
        mostrarMenuUsuario()
        opcion = input("Opción: ").strip()
        print("")
        if opcion in menuUsuario:
            _, funcion = menuUsuario[opcion]
            funcion()
            if opcion == "0":
                restaurarTodo() #Restaura lo eliminado durante la ejecución
                break
        else:
            print("Opción inválida. Intente nuevamente.")

ejecutarMenuUsuario()





#METODOS EXPERIMENTALES:

# def clasificar_forma_imagenes(self):
#         clasificados = []
#         for jugador in self.jugadores:
#             if not jugador.tiene_foto():
#                 continue
#             try:
#                 with Image.open(jugador.ruta_foto) as img:
#                     ancho, alto = img.size
#                     proporcion = ancho/alto
#                     if proporcion > 1.2:
#                         forma = "ancha"
#                     elif proporcion < 0.8:
#                         forma = "alta"
#                     else:
#                         forma = "cuadrada"
#                         clasificados.append((jugador, forma))
#             except Exception as e:
#                 print(f"Error al abrir imagen de {jugador.nombre} {jugador.apellido}: {e}")
#         return clasificados
    
#     def calcular_grilla(self, clasificados, columnas=5):
#         modulos = 0
#         for _, forma in clasificados:
#             if forma == "cuadrada":
#                 modulos +=1
#             else:
#                 modulos +=2
#         filas = int(math.ceil(modulos/columnas * 1.2))
#         return filas, columnas
    
#     def mostrar_grilla(self, clasificados, filas, columnas):
#         figura = plt.figure(figsize = (columnas * 3, filas * 3))
#         gs = figura.add_gridspec(filas, columnas)
#         ocupado = [[False]*columnas for _ in range(filas)]

#         def buscar_lugar(ancho, alto):
#             for r in range(filas - alto + 1):
#                 for c in range(columnas - ancho + 1):
#                     if all(not ocupado[r+i][c+j] for i in range(alto) for j in range(ancho)):
#                         for i in range(alto):
#                             for j in range(ancho):
#                                 ocupado[r+i][c+j] = True
#                         return r, c
#             return None, None
        
#         for jugador, forma in clasificados:
#             try:
#                 img = Image.open(jugador.ruta_foto)
#             except:
#                 continue
#             img_array = np.array(img)

#             if forma == "cuadrada":
#                 alto, ancho = 1, 1
#             elif forma == "ancha":
#                 alto, ancho = 1, 2
#             else:
#                 alto, ancho = 2, 1
            
#             r, c = buscar_lugar(ancho, alto)
#             if r is not None:
#                 ax = figura.add_subplot(gs[r:r+alto, c:c+ancho])
#                 ax.imshow(img_array)
#                 nombre_completo = jugador.nombre.capitalize() + " " + jugador.apellido.capitalize()
#                 ax.set_title(nombre_completo, fontsize=10)
#                 ax.axis('off')
        
#         plt.tight_layout()
#         plt.show()
    
#     def mostrar_jugadores(self):
#         clasificados = self.clasificar_forma_imagenes()
#         if not clasificados:
#             print("No hay imágenes válidas para mostrar.")
#             return
#         filas, columnas = self.calcular_grilla(clasificados)
#         self.mostrar_grilla(clasificados, filas, columnas)