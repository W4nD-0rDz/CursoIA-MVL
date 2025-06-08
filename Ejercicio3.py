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
import os
from PIL import Image
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from fuzzywuzzy import fuzz
import pandas as pd
from pathlib import Path
import math
import numpy as np
from time import sleep

class Jugador:
    def __init__(self, nombre, apellido, rol, ruta_foto):
        self.nombre = nombre
        self.apellido = apellido
        self.rol = rol
        self.ruta_foto = ruta_foto
    
    def tiene_foto(self):
        return os.path.isfile(self.ruta_foto)
    
    def es_gris(self):
        if not self.tiene_foto():
            return False
        try:
            with Image.open(self.ruta_foto) as img:
                return img.mode == 'L'
        except:
            return False

    def mostrar_jugador(self):
        nombre_completo = f"{self.nombre} {self.apellido}".title()
        if not self.tiene_foto():
            print(f"No se puede mostrar la foto de {nombre_completo}")
            return
        try:
            img = Image.open(self.ruta_foto)
            plt.imshow(img, cmap='gray' if self.es_gris() else None)
            plt.axis('off')
            plt.title(nombre_completo, fontsize=10)
            plt.tight_layout()
            plt.show()
        except Exception as e:
            print(f"Error al mostrar la imagen: {e}")

class Plantel:
    def __init__(self, csv_path, dir_fotos):
        self.csv_path = csv_path
        self.dir_fotos = dir_fotos
        self.jugadores = []
    
    def guardar_csv(self):
        datos = []
        for j in self.jugadores:
            datos.append({
                "num": j.rol,
                "nombre": j.nombre,
                "apellido": j.apellido
            })
        df = pd.DataFrame(datos)
        df.to_csv(self.csv_path, index = False)
        #print("Archivo csv actualizado")

    def cargar(self):
        df = pd.read_csv(self.csv_path)
        for _, fila in df.iterrows():
            nombre = fila["nombre"]
            apellido = fila["apellido"]
            rol = str(fila["num"])
            archivo =  f"{fila['nombre'].lower()} {fila['apellido'].lower()}.jpg"
            ruta_foto = os.path.join(self.dir_fotos, archivo)
            jugador = Jugador(nombre, apellido, rol, ruta_foto)
            self.jugadores.append(jugador)

    def filtrar_sin_foto(self):
        """Elimina de la lista los jugadores que no tengan foto."""
        jugadores_con_foto = []
        for jugador in self.jugadores:
            if not jugador.tiene_foto():
                print("⬛ Jugador sin foto eliminado:")
                nombre_completo = f"{jugador.nombre} {jugador.apellido}".title()
                print(f"{nombre_completo}") 
                sleep(0.8)
            else:
                jugadores_con_foto.append(jugador)
        self.jugadores = jugadores_con_foto
        self.guardar_csv()
        print("Archivo argentina.csv actualizado")

    def mostrar_grises(self):
        jugadores_grises = [ j for j in self.jugadores if j.tiene_foto() and j.es_gris()]
        if not jugadores_grises:
            print("No hay jugadores con foto en escala de grises.")
        else:
            print("Integrantes del plantel cuya foto está en escala de grises:")
            for jugador in jugadores_grises:
                nombre_completo = f"{jugador.nombre} {jugador.apellido}".title()
                print(f"{nombre_completo}")
                jugador.mostrar_jugador()


    def buscar_por_numero(self, numero):
        for jugador in self.jugadores:
            if jugador.rol.isdigit() and jugador.rol == str(numero):
                return jugador
        return None

    def buscar_por_nombre_apellido(self, nombre, apellido):
        mejor_coincidencia = None
        mejor_puntaje = 0

        entrada = f"{nombre} {apellido}".lower()

        for jugador in self.jugadores:
            candidato = f"{jugador.nombre} {jugador.apellido}".lower()
            puntaje = fuzz.partial_ratio(candidato, entrada)

            if puntaje > mejor_puntaje:
                mejor_puntaje = puntaje
                mejor_coincidencia = jugador
        
        if mejor_puntaje >= 85:
            return mejor_coincidencia
        else:
            print(f"No se encontró coincidencia suficiente (score={mejor_puntaje})")
            return None

    def borrar(self):
        nombre = input("Ingrese el nombre del jugador a borrar: ").strip().lower()
        apellido = input("Ingrese el apellido del jugador a eliminar: ").strip().lower()
        
        jugador = self.buscar_por_nombre_apellido(nombre, apellido)
        if not jugador:
            print("Jugador no encontrado.")
            return
        
        confirmar = input(f"¿Está seguro de eliminar a {jugador.nombre} {jugador.apellido}? (s/n): ").strip().lower()
        if confirmar != 's':
            print("Operación cancelada.")
            return
        
        self.jugadores.remove(jugador)
        
        ruta = Path(jugador.ruta_foto)
        if ruta.exists():
            ruta.unlink()
            print("Foto eliminada.")
        else:
            print("La foto no existe o ya fue eliminada")

        self.guardar_csv()
        print("jugador eliminado del CSV.")
        
    def calcular_grilla(self):
        jugadores_con_foto = [j for j in self.jugadores
                              if j.rol.isdigit() and j.tiene_foto()]
        modulos = len(jugadores_con_foto)
        filas = math.ceil(math.sqrt(modulos*0.8))
        columnas = math.ceil(modulos/filas)
        return columnas, filas, modulos
        
    def mostrar_jugadores(self):
        jugadores_con_foto = [
        j for j in self.jugadores
        if j.rol.isdigit() and j.tiene_foto()
        ]
    
        if not jugadores_con_foto:
            print("No hay jugadores con foto para mostrar.")
            return
        
        columnas, filas, modulos = plantel.calcular_grilla()
        fig, ejes = plt.subplots(filas, columnas, figsize=(columnas*3.5, filas*2.5))
        fig.suptitle("ARGENTINA", fontsize=16)
        ejes = ejes.flatten() if modulos > 1 else [ejes]

        # for i, jugador in enumerate(jugadores_con_foto):
        #     nombre_completo = f"{jugador.nombre} {jugador.apellido}".title()
        #     img = mpimg.imread(jugador.ruta_foto)
        #     ejes[i].imshow(img)
        #     ejes[i].axis('off')
        #     ejes[i].set_title(nombre_completo, fontsize=9)

        # # Ocultar los ejes restantes (vacíos)
        # for j in range(len(jugadores_con_foto), len(ejes)):
        #     ejes[j].axis('off')



        for i, jugador in enumerate(jugadores_con_foto):
            for j in range(len(jugadores_con_foto), len(ejes)):
                ejes[j].axis('off')
                nombre_completo = f"{jugador.nombre} {jugador.apellido}".title()
                img = mpimg.imread(jugador.ruta_foto)
                ejes[i].imshow(img)
                ejes[i].axis('off')
                ejes[i].text(0.5, -0.1, nombre_completo,
                            ha='center', va='top', transform=ejes[i].transAxes,
                            fontsize=9)
                            
        plt.tight_layout()
        plt.show()

class Menu:
    def __init__(self, plantel):
        self.plantel = plantel
        self.nombre_menu = "⭐⭐⭐ARGENTINA⭐⭐⭐"
        self.opciones = {
            "1": ("Ver jugador", self.ver_jugador),
            "2": ("Ver todos los jugadores", self.mostrar_jugadores),
            "3": ("Eliminar jugador", self.eliminar_jugador),
            "0": ("Salir", self.salir)
        }
        self.salida = False

    def mostrar_menu(self):
        print("\nMenú:")
        for clave, (desc, _) in self.opciones.items():
            print(f"{clave}. {desc}")

    def ejecutar(self):
        print(f"\n{self.nombre_menu}")
        self.borrar_sin_foto()
        self.mostrar_grises()
        while not self.salida:
            self.mostrar_menu()
            opcion = input("Opción: ").strip()
            if opcion in self.opciones:
                _, funcion = self.opciones[opcion]
                funcion()
            else:
                print("Opción inválida. Intente nuevamente.")
    
    def borrar_sin_foto(self):
        self.plantel.filtrar_sin_foto()

    def mostrar_grises(self):
        self.plantel.mostrar_grises()

    def ver_jugador(self):
        while True:
            entrada = input("Elija un jugador por número de camiseta (o escriba 'salir'): ").strip()
            if entrada.lower() == 'salir':
                break
            if not entrada.isdigit():
                print("Ingrese un número de camiseta válido")
                continue
            jugador = self.plantel.buscar_por_numero(entrada)
            if jugador:
                jugador.mostrar_jugador()
                break
            else:
                print("Jugador no encontrado. Intente nuevamente")

    def mostrar_jugadores(self):
        self.plantel.mostrar_jugadores()

    def eliminar_jugador(self):
        self.plantel.borrar()

    def salir(self):
        print(f"{self.nombre_menu}")
        exit()
        self.salida = True

#########################################################################

if __name__ == "__main__":
    ruta_csv = "argentina.csv"
    carpeta_fotos = r"imagenes/fotos"
    
    plantel = Plantel(ruta_csv, carpeta_fotos)
    plantel.cargar()
    
    menu = Menu(plantel)
    menu.ejecutar()
      
# plantel = Plantel("argentina.csv", "imagenes/fotos")
# plantel.cargar()
# plantel.mostrar_jugadores()
