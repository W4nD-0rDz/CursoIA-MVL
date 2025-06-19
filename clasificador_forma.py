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

import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2' #Reduce el "ruido" en la consola
import numpy as np
import cv2
from PIL import Image
import pandas as pd
import tensorflow as tf
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt

class EntrenadorModelo:
    def __init__(self, carpeta_entrenamiento):
        self.carpeta = carpeta_entrenamiento
        self.X = []
        self.y = []
        self.modelo = None
        self.mapeo_etiquetas = {"triangulo": 0, "cuadrado": 1, "circulo": 2}
    
    # Normalizar imágenes:
    def normalizar_imagenes(self, carpeta_origen, carpeta_destino):
        os.makedirs(carpeta_destino, exist_ok=True)
        contador = 1
        for nombre_archivo in os.listdir(carpeta_origen):
            if not nombre_archivo.endswith(".png"):
                continue
            ruta = os.path.join(carpeta_origen, nombre_archivo)
            img = Image.open(ruta).convert("L")
            img_redimensionada = img.resize((30, 30), Image.BICUBIC)
            nombre_salida = f"{contador}.png"
            img_redimensionada.save(os.path.join(carpeta_destino, nombre_salida))
            contador += 1
        print(f"{contador - 1} imágenes normalizadas guardadas en {carpeta_destino}.")

    # Cargar imágenes desde carpeta.
    def cargar_datos(self):
        for nombre_archivo in os.listdir(self.carpeta):
            if not nombre_archivo.endswith(".png"):
                continue

            ruta = os.path.join(self.carpeta, nombre_archivo)  # ✅ Definir primero
            print("Leyendo:", nombre_archivo)

            imagen = Image.open(ruta).convert("L")
            imagen_np = np.asarray(imagen)
            print("Promedio de gris:", np.mean(imagen_np))

            try:
                forma = self.detectar_forma(ruta)
                print(f"→ Imagen: {nombre_archivo}, forma detectada: {forma}")
            except Exception as e:
                print(f"No se pudo detectar forma en {nombre_archivo}: {e}")
                continue
            if forma not in self.mapeo_etiquetas:
                print(f"Forma desconocida '{forma}' en archivo {nombre_archivo}")
                continue

            # Convertir a arrays numpy de 30x30 → aplanar a (900,).
            imagen = imagen.resize((30, 30))  # Ya fue convertida a "L" antes
            arreglo = np.asarray(imagen).flatten() / 255.0

            self.X.append(arreglo)
            self.y.append(self.mapeo_etiquetas[forma])

        self.X = np.array(self.X)
        self.y = tf.keras.utils.to_categorical(self.y, num_classes=3)
        print(f"{len(self.X)} imágenes cargadas y etiquetas asignadas.")
 
    # Detectar la forma de la imagen
    def detectar_forma(ruta_imagen):
        imagen = cv2.imread(ruta_imagen, cv2.IMREAD_GRAYSCALE)
        if imagen is None:
            raise ValueError(f"No se pudo abrir la imagen en {ruta_imagen}")
        
        # Invertimos si la figura es blanca sobre fondo blanco (caso común)
        if np.mean(imagen) > 127:
            _, imagen = cv2.threshold(imagen, 200, 255, cv2.THRESH_BINARY_INV)
        else:
            _, imagen = cv2.threshold(imagen, 50, 255, cv2.THRESH_BINARY)
        # Buscar contornos
        contornos, _ = cv2.findContours(imagen, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        if not contornos:
            raise ValueError("No se encontraron contornos")
        
        contorno = max(contornos, key=cv2.contourArea)
        aprox = cv2.approxPolyDP(contorno, 0.04 * cv2.arcLength(contorno, True), True)
        lados = len(aprox)
        if lados == 3:
            return "triangulo"
        elif lados == 4:
            return "cuadrado"
        else:
            return "circulo"

    # Crear modelo
    def construir_modelo(self):
        self.modelo = tf.keras.Sequential([
            tf.keras.layers.Dense(128, activation='relu', input_shape=(900,)),
            tf.keras.layers.Dense(64, activation='relu'),
            tf.keras.layers.Dense(3, activation='softmax')
        ])
        self.modelo.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
        print("modelo compilado.")

    # Entrenar modelo
    def entrenar_modelo(self, epochs=100, batch_size=16):
        x_train, x_val, y_train, y_val = train_test_split(self.X, self.y, test_size=0.2)
        historial = self.modelo.fit(x_train, y_train, epochs=epochs, batch_size=batch_size, validation_data=(x_val, y_val))
        # Mostrar gráfico de pérdida
        self.mostrar_perdida(historial)

    # Mostrar el desempeño del modelo
    def mostrar_perdida(self, historial):
        plt.figure(figsize=(8, 4))
        plt.plot(historial.history["loss"])
        plt.xlabel("Época")
        plt.ylabel("Pérdida (loss)")
        plt.title("Evolución del aprendizaje")
        plt.grid(True)
        plt.show()

    # Guardar modelo (model.save("modelo_clasificador_forma.keras"))
    def guardar_modelo(self, nombre_archivo="modelo_clasificador_forma.keras"):
        self.modelo.save(nombre_archivo)
        print(f"Modelo guardado como {nombre_archivo}")

#########################################################################################################################
if __name__ == "__main__":
    entrenador = EntrenadorModelo("imagenes/simples/entrenamiento")
    entrenador.normalizar_imagenes("imagenes/simples", "imagenes/simples/entrenamiento")
    entrenador.cargar_datos()
    entrenador.construir_modelo()
    entrenador.entrenar_modelo()
    entrenador.guardar_modelo()