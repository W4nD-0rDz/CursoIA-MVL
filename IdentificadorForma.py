import os
import random
import cv2
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import pandas as pd

def detectar_forma(imagen_np):
    # cv2.imshow("Imagen original", imagen_np)
    # cv2.waitKey(0)

    # Asegurar que la figura sea blanca sobre fondo negro
    imagen_np = invertir_si_es_necesario(imagen_np)
    
    #Ecualizar la imagen
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    imagen_ecualizada = clahe.apply(imagen_np)

    #Aplicar suavizado:
    imagen_suavizada = cv2.GaussianBlur(imagen_ecualizada, (3,3),0)
    # cv2.imshow("Imagen suavizada", imagen_suavizada)
    # cv2.waitKey(0)
    
    #Binarizar la imagen
    media = np.mean(imagen_suavizada)
    invertir = media > 127 #Si el fondo es claro, se invierte
    modo = cv2.THRESH_BINARY_INV if invertir else cv2.THRESH_BINARY
    _, imagen_binaria = cv2.threshold(imagen_suavizada, 0, 255, modo + cv2.THRESH_OTSU)
    # cv2.imshow("Imagen binarizada", imagen_binaria)
    # cv2.waitKey(0)

    #Detectar contornos
    contornos, _ = cv2.findContours(imagen_binaria, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contornos:
        return "No se detectaron contornos"
    contorno = max(contornos, key= cv2.contourArea)
        # # Calculo de perímetro y área
    perimetro = cv2.arcLength(contorno, True)
    area = cv2.contourArea(contorno)
        # # Aproximar contorno para simplificar la forma
    epsilon = 0.01 * cv2.arcLength(contorno, True)
    aprox = cv2.approxPolyDP(contorno, epsilon, True)
    lados = len(aprox)
    # print(f"Lados detectados: {lados}")
        # # Mostrar contorno dibujado
    # imagen_dibujo = imagen_np.copy()
    # imagen_dibujo = cv2.drawContours(imagen_dibujo, [aprox], -1, (0,0,0), 1)
    # imagen_grande = cv2.resize(imagen_dibujo, (300, 300), interpolation=cv2.INTER_NEAREST)
    # cv2.imshow("Contorno detectado", imagen_grande)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    #Cálculo de índice de circularidad
    circularidad = 0
    if perimetro > 0:
        circularidad = 4 * np.pi * (area / (perimetro * perimetro))

    #Cálculo de Hu Moments
    momentos = cv2.moments(contorno)
    hu = cv2.HuMoments(momentos)
    hu_log = -np.sign(hu) * np.log10(np.abs(hu) + 1e-10)

    forma = clasificar_forma(lados, circularidad, hu_log)
    return lados, perimetro, area, circularidad, hu_log.flatten(), forma

def invertir_si_es_necesario(imagen_np):
    h, w = imagen_np.shape

    # Obtener el color promedio del fondo (esquinas)
    esquinas = [
        imagen_np[0, 0],
        imagen_np[0, w-1],
        imagen_np[h-1, 0],
        imagen_np[h-1, w-1]
    ]
    centro = [h//2, w//2]
    fondo_promedio = np.mean(esquinas)
    figura_promedio = np.mean(centro)

    # Si el fondo es mucho más claro que la figura, invertir
    if fondo_promedio - figura_promedio > 15:  # margen ajustable
        return cv2.bitwise_not(imagen_np)
    return imagen_np


def clasificar_forma(lados, circularidad, hu):
    if lados >= 8 and circularidad > 0.85:
        return "circulo"
    elif (lados == 4 and 0.75 < circularidad < 0.79) or (hu[0] > 0.76 and hu[1] < 0.01):
        return "cuadrado"
    elif 2 <= lados <= 5 and hu[4] < -7 and hu[5] < -5:
        return "triangulo"
    else:
        return "forma no reconocida"

def dar_forma_real(nombre_archivo):
    numero = int(nombre_archivo.split('.')[0])
    if numero > 0 and numero <= 450:
        return "circulo"
    if numero >= 451 and numero <=900:
        return "cuadrado"
    if numero >= 901:
        return "triangulo"
# --------------------------
# PRUEBA SOBRE UN LOTE DE IMAGENES
# --------------------------

resultados = []
carpeta ="imagenes/simples/entrenamiento"
imagenes = [f for f in os.listdir(carpeta) if f.endswith('.png')]

def almacenar_resultados():
    muestra = random.sample(imagenes, 50)
    for nombre in muestra:
        ruta = os.path.join(carpeta, nombre)
        imagen_pil = Image.open(ruta).convert('L')
        imagen_np = np.array(imagen_pil)
        forma_por_orden = dar_forma_real(nombre)
        lados, perimetro, area, circularidad, hu, forma = detectar_forma(imagen_np)
        resultados.append({
            "nombre": nombre,
            "lados": lados,
            "perimetro": perimetro,
            "area": area,
            "circularidad": circularidad,
            **{f"hu{i}": hu[i] for i in range(7)},
            "forma_detectada": forma,
            "forma_real": forma_por_orden
        })

almacenar_resultados()
df = pd.DataFrame(resultados)
df_errores = df[df["forma_detectada"] != df["forma_real"]]
df_errores.to_csv("errores_clasificacion.csv", index=False)
coinciden = df[df["forma_detectada"].str.lower() == df["forma_real"].str.lower()]

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)

print("")
print(df.to_string(index=True))
print(f"✅ Coincidencias correctas: {len(coinciden)} de {len(df)} imágenes")
