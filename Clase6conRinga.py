#Clasificador de imágenes con Py y TensorFlow
#https://www.youtube.com/watch?v=j6eGHROLKP8&list=PLZ8REt5zt2Pn0vfJjTAPaDVSACDvnuGiG&index=3&t=46s

#0. Generador de imágenes de entrenamiento. Genera figuras de colores.
from PIL import Image, ImageDraw
import math
import os
import random

# # Diccionario de Colores
# colores = {
#     "rojo": (255, 0, 0),
#     "azul": (0, 0, 255),
#     "amarillo": (255, 255, 0),
#     "naranja": (255, 165, 0),
#     "verde": (0, 128, 0),
#     "violeta": (128, 0, 128),
#     "blanco":(255, 255, 255),
#     "negro":(0, 0, 0),
#     "gris128": (128, 128, 128),
#     "gris64": (64, 64, 64),
# }

# # Dimensiones de imagen y figura
# TAM = 100
# CENTRO = (TAM // 2, TAM // 2)
# LADO = 70  # lado de cuadrado o base del triángulo
# ALTURA_TRIANGULO = int((math.sqrt(3) / 2) * LADO)
# FORMATO = "png"

# def dibujar_circulo(draw, color):
#     radio = LADO // 2
#     x0 = CENTRO[0] - radio
#     y0 = CENTRO[1] - radio
#     x1 = CENTRO[0] + radio
#     y1 = CENTRO[1] + radio
#     draw.ellipse((x0, y0, x1, y1), fill=color)
    
# def dibujar_cuadrado(draw, color):
#     x0 = CENTRO[0] - LADO // 2
#     y0 = CENTRO[1] - LADO // 2
#     x1 = CENTRO[0] + LADO // 2
#     y1 = CENTRO[1] + LADO // 2
#     draw.rectangle([x0, y0, x1, y1], fill=color)

# def dibujar_triangulo(draw, color):
#     x = CENTRO[0]
#     y = CENTRO[1]
#     # triángulo equilátero centrado
#     p1 = (x, y - ALTURA_TRIANGULO // 2)  # vértice superior
#     p2 = (x - LADO // 2, y + ALTURA_TRIANGULO // 2)  # inferior izq
#     p3 = (x + LADO // 2, y + ALTURA_TRIANGULO // 2)  # inferior der
#     draw.polygon([p1, p2, p3], fill=color)

# # Diccionario de formas
# dibujantes = {
#     "cuadrado": dibujar_cuadrado,
#     "triangulo": dibujar_triangulo,
#     "circulo": dibujar_circulo
# }

# # Valida si la imagen está en escala de grises (R=G=B)
# def es_gris(imagen_rgb):
#     pixeles = imagen_rgb.getdata()
#     for r, g, b in pixeles:
#         if r != g or g != b:
#             return False
#     return True

# #Define la mezcla de colores:
# def get_nombre_color(valor_rgb):
#     for nombre, valor in colores.items():
#         if valor == valor_rgb:
#             return nombre
#     return "desconocido"

# # Función general para crear imagen
# def crear_figura(nombre_figura, color_figura_nombre, fondo_nombre):
#     color_figura_rgb = colores[color_figura_nombre]
#     fondo_rgb = colores[fondo_nombre]

#     img = Image.new("RGB", (TAM, TAM), fondo_rgb)
#     draw = ImageDraw.Draw(img)
#     dibujantes[nombre_figura](draw, color_figura_rgb)

#     # Convertir a escala de grises si corresponde
#     if es_gris(img):
#         img = img.convert("L")

#     carpeta = "imagenes/simples"
#     img.save(f"{carpeta}/{nombre_figura}_{color_figura_nombre}_sobre_{fondo_nombre}.{FORMATO}")

# # Bucle general
# for nombre_figura in dibujantes:
#     for color_figura_nombre in colores:
#         for fondo_nombre in colores:
#             if color_figura_nombre == fondo_nombre:
#                 continue  # evita fondo igual al color de figura
#             crear_figura(nombre_figura, color_figura_nombre, fondo_nombre)
#########################################################################################################################
#1. Es un PROBLEMA DE CLASIFICACION: 
# recibe una entrada (imágen), debe retornar la clase a la que pertenece
#2. Se supone:
# capa de entrada con una neurona por cada pixel (100x100xRGB) = 30000 neuronas
# capa de salida con una neurona por cada clase (triangulo rojo, cuadrado azul, etc. 3*10) = 30 neuronas
#3. Para simplificar el problema:
# seleccionar imágenes tipo "L"
# se giran, desplazan y reducen a 30x30 pixeles
# la capa de entrada tendrá 30*30*1 neuronas= 900
# la capa de salida tendré 3 neuronas (circulo, triángulo cuadrado)
# Se entrenará el modelo con 180 imágenes modificadas y almacenadas en imagenes/simples/entrenamiento
#########################################################################################################################
# #Configuracion para generación de imágenes de entrenamiento:
# carpeta_origen = "imagenes/simples"
# carpeta_destino = "imagenes/simples/entrenamiento"
# os.makedirs(carpeta_destino, exist_ok=True)

# TAM_ORIGINAL = 100
# TAM_FINAL = 30
# COPIAS = 5
# formato_salida = "png"
# contador = 1

# for nombre_archivo in os.listdir(carpeta_origen):
#     if not nombre_archivo.endswith(".png"):
#         continue
#     ruta = os.path.join(carpeta_origen, nombre_archivo)
#     imagen = Image.open(ruta)
#     if imagen.mode != "L":
#         continue
#     for i in range(COPIAS):
#         fondo = Image.new("L", (TAM_ORIGINAL, TAM_ORIGINAL), 255)
#         angulo = random.randint(45,125)
#         rotada = imagen.rotate(angulo, expand = False, fillcolor=255)
#         dx = random.randint(-15,15)
#         dy = random.randint(-15, 15)
#         fondo.paste(rotada, (dx, dy))
#         final = fondo.resize((TAM_FINAL, TAM_FINAL), Image.BICUBIC)

#         salida = os.path.join(carpeta_destino, f"{contador}.{formato_salida}")
#         final.save(salida)
#         contador +=1


