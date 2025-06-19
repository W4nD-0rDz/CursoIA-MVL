import os
import cv2
import numpy as np
import random

# GENERADOR DE IMAGENES NORMALIZADAS PARA ENTRENAMIENTO
# carpeta_origen = "imagenes/simples"
# carpeta_destino = "imagenes/simples/entrenamiento"
# os.makedirs(carpeta_destino, exist_ok=True)

# TAM_ORIGINAL = 100
# TAM_FINAL = 30
# COPIAS = 5
# contador = 1

# def detectar_color_fondo(imagen_bgr):
#     return imagen_bgr[0,0].tolist() #devuelve[B, G, R]

# def rotar_con_cv2(imagen, angulo, fondo_color):
#     h, w = imagen.shape[:2]
#     centro = (w//2, h//2)
#     M = cv2.getRotationMatrix2D(centro, angulo, 1.0)
#     rotada = cv2.warpAffine(imagen, M, (w, h), borderValue=fondo_color)
#     return rotada

# def desplazar_con_cv2(imagen, dx, dy, fondo_color):
#     h, w = imagen.shape[:2]
#     M = np.float32([[1, 0, dx], [0, 1, dy]])
#     desplazada = cv2.warpAffine(imagen, M, (w,h), borderValue=fondo_color)
#     return desplazada

# def hacer_gris(imagen_bgr):
#     return cv2.cvtColor(imagen_bgr, cv2.COLOR_BGR2GRAY)

# def detectar_BGR(imagen):
#     return len(imagen.shape) == 3 and imagen.shape[2] == 3

# def transformar_con_cv2(imagen):
#     if detectar_BGR(imagen):
#         fondo_color = detectar_color_fondo(imagen)
#         angulo = random.choice([45, 60, 90, 120, 135])
#         dx = random.randint(-25, 25) #1/4 tamaño original
#         dy = random.randint(-25, 25) #1/4 tamaño original
        
#         # Elegir transformación al azar
#         opcion = random.choice(["rotar", "desplazar", "ambas"])

#         if opcion == "rotar":
#             imagen = rotar_con_cv2(imagen, angulo, fondo_color)
#         elif opcion == "desplazar":
#             imagen = desplazar_con_cv2(imagen, dx, dy, fondo_color)
#         elif opcion == "ambas":
#             imagen = rotar_con_cv2(imagen, angulo, fondo_color)
#             imagen = desplazar_con_cv2(imagen, dx, dy, fondo_color)
        
#     if detectar_BGR(imagen):
#         imagen = hacer_gris(imagen)
#     return imagen
    
# def reducir_con_cv2(imagen):
#     return cv2.resize(imagen, (TAM_FINAL, TAM_FINAL), interpolation=cv2.INTER_AREA)

# def llenar_entrenamiento(ruta_imagen):
#     global contador
#     imagen = cv2.imread(ruta_imagen)
#     for i in range(COPIAS):
#         imagen_transformada = transformar_con_cv2(imagen)
#         imagen_reducida = reducir_con_cv2(imagen_transformada)
#         nombre_salida = os.path.join(carpeta_destino, f"{contador}.png")
#         cv2.imwrite(nombre_salida, imagen_reducida)
#         print(f"Guardado: {nombre_salida}")
#         contador +=1


# for archivo in os.listdir(carpeta_origen):
#     if archivo.lower().endswith(".png"):
#         ruta = os.path.join(carpeta_origen, archivo)
#         llenar_entrenamiento(ruta)
        




    






