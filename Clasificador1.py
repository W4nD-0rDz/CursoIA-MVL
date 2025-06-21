import cv2
import numpy as np
import random
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2' #Reduce el "ruido" en la consola
import numpy as np
from PIL import Image
import tensorflow as tf

# GENERADOR DE IMAGENES NORMALIZADAS PARA ENTRENAMIENTO
carpeta_origen = "imagenes/simples"
carpeta_destino = "imagenes/simples/entrenamiento"
os.makedirs(carpeta_destino, exist_ok=True)

TAM_ORIGINAL = 100
TAM_FINAL = 50
COPIAS = 5
contador = 1

def detectar_color_fondo(imagen_bgr):
    return imagen_bgr[0,0].tolist() #devuelve[B, G, R]

def rotar_con_cv2(imagen, angulo, fondo_color):
    h, w = imagen.shape[:2]
    centro = (w//2, h//2)
    M = cv2.getRotationMatrix2D(centro, angulo, 1.0)
    rotada = cv2.warpAffine(imagen, M, (w, h), borderValue=fondo_color)
    return rotada

def desplazar_con_cv2(imagen, dx, dy, fondo_color):
    h, w = imagen.shape[:2]
    M = np.float32([[1, 0, dx], [0, 1, dy]])
    desplazada = cv2.warpAffine(imagen, M, (w,h), borderValue=fondo_color)
    return desplazada

def hacer_gris(imagen_bgr):
    return cv2.cvtColor(imagen_bgr, cv2.COLOR_BGR2GRAY)

def detectar_BGR(imagen):
    return len(imagen.shape) == 3 and imagen.shape[2] == 3

def transformar_con_cv2(imagen):
    if detectar_BGR(imagen):
        fondo_color = detectar_color_fondo(imagen)
        angulo = random.choice([30, 60, 90, 120])
        dx = random.randint(-15, 15)
        dy = random.randint(-15, 15)
        
        # Elegir transformación al azar
        opcion = random.choice(["rotar", "desplazar", "ambas"])

        if opcion == "rotar":
            imagen = rotar_con_cv2(imagen, angulo, fondo_color)
        elif opcion == "desplazar":
            imagen = desplazar_con_cv2(imagen, dx, dy, fondo_color)
        elif opcion == "ambas":
            imagen = rotar_con_cv2(imagen, angulo, fondo_color)
            imagen = desplazar_con_cv2(imagen, dx, dy, fondo_color)
        
    if detectar_BGR(imagen):
        imagen = hacer_gris(imagen)
    return imagen
    
def reducir_con_cv2(imagen):
    return cv2.resize(imagen, (TAM_FINAL, TAM_FINAL), interpolation=cv2.INTER_AREA)

def llenar_entrenamiento(ruta_imagen):
    global contador
    imagen = cv2.imread(ruta_imagen)
    for i in range(COPIAS):
        imagen_transformada = transformar_con_cv2(imagen)
        imagen_reducida = reducir_con_cv2(imagen_transformada)
        nombre_salida = os.path.join(carpeta_destino, f"{contador}.png")
        cv2.imwrite(nombre_salida, imagen_reducida)
        print(f"Guardado: {nombre_salida}")
        contador +=1

for archivo in os.listdir(carpeta_origen):
    if archivo.lower().endswith(".png"):
        ruta = os.path.join(carpeta_origen, archivo)
        llenar_entrenamiento(ruta)
        

# ENTRENADOR DE MODELO de CLASIFICADOR
# class EntrenadorModelo:
#     #Inicialización:
#     def __init__(self, carpeta_entrenamiento):
#         self.carpeta = carpeta_entrenamiento
#         self.X = []
#         self.y = []
#         self.modelo = None
#         self.mapeo_etiquetas = {"triangulo": 0, "cuadrado": 1, "circulo": 2}
    
#     #Cargar los datos
#     def cargar_datos(self):
#         for nombre_archivo in os.listdir(self.carpeta):
#             if not nombre_archivo.endswith(".png"):
#                 continue
#             ruta = os.path.join(self.carpeta, nombre_archivo)  # ✅ Definir primero
#             print("Leyendo:", nombre_archivo)

#             imagen = Image.open(ruta).convert("L")
#             imagen_np = np.asarray(imagen)

#             try:
#                 forma = detectar_forma(imagen_np)
#                 print(f"Forma: {forma}")
#             except Exception as e:
#                 print(f"No se pudo detectar forma en {nombre_archivo}: {e}")
#                 continue

#             if forma not in self.mapeo_etiquetas:
#                 print(f"Forma desconocida '{forma}' en archivo {nombre_archivo}")
#                 continue

#             arreglo = imagen_np.flatten()/255.0

#             self.X.append(arreglo)
#             self.y.append(self.mapeo_etiquetas[forma])
        
#         self.X=np.array(self.X)
#         self.y=tf.keras.utils.to_categorical(self.y, num_clases=3)

#     #Identifica la cantidad de lados y en función de eso asigna una forma
#     def detectar_forma(imagen_np):
#         #hacer imagen binaria, blanco/negro
#         _, binaria = cv2.threshold(imagen_np, 128, 255, cv2.THRESH_BINARY_INV)
#         #buscar contornos
#         contornos, _ = cv2.findContours(binaria, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

#         if not contornos:
#             raise ValueError("No se encontraron contornos")
        
#         contorno = max(contornos, key=cv2.contourArea)
#         perimetro = cv2.arcLength(contorno, True)
#         aprox = cv2.approxPolyDP(contorno, 0.04 * perimetro, True)
#         lados = len(aprox)

#         if lados == 3:
#             return "triangulo"
#         elif lados == 4:
#             return "cuadrado"
#         elif lados > 6:
#             return "circulo"
#         else:
#             raise ValueError(f"No se pudo clasificar la forma (lados = {lados})")
            



    






