#1. Ejecutar el generador de imágenes de entrenamiento (circulo, triangulo, cuadrado) -> Clasificador1.py
#2. Crear una red neuronal de clasificación
#2.1 Datos de entrada: una neurona por cada pixel. La imagen normalizada tipo L, (x, y, colorgray)
#       color gray puede ser entre 0 y 255 por cada pixel para imagenes en escala de grises.
#2.2 Tipo de Red: red densa igual a la que se utilizó anteriormente
#2.3 Agregar complejidad a problemas no lineales: capas ocultas y funciones de activación (relu, softmax)
#2.4 La red debe tener:
# Una capa de entrada con 50x50 neuronas
# Dos capas ocultas de 50 neuronas cada una, con función de activación RELU
# Una capa de salida de 3 neuronas con función de activación softmax (para gráfica)

import tensorflow as tf
import os
import numpy as np
import cv2
from sklearn.model_selection import train_test_split
import random
import matplotlib.pyplot as plt

class ClasificadorForma:
    def __init__(self, carpeta_imagenes, tamano=(50, 50)):
        self.carpeta = carpeta_imagenes
        self.clases = {"triangulo": 0, "cuadrado": 1, "circulo": 2}
        self.tamano = tamano
        self.modelo = None

    def determinar_clase(self, numero):
        if 1<= numero <=450:
            return "circulo"
        elif 451 <= numero <=900:
            return "cuadrado"
        elif 901 <= numero <= 1350:
            return "triangulo"
        else:
            return None

    def cargar_datos(self):
        imagenes = []
        etiquetas = []

        for nombre_archivo in os.listdir(self.carpeta):
            if not nombre_archivo.endswith(".png"):
                continue

            numero = int(os.path.splitext(nombre_archivo)[0])
            clase = self.determinar_clase(numero)
            if clase is None:
                continue

            ruta = os.path.join(self.carpeta, nombre_archivo)
            imagen = cv2.imread(ruta, cv2.IMREAD_GRAYSCALE)
            if imagen is None:
                continue
            if imagen.shape != self.tamano:
                continue
            arreglo = imagen.astype(np.float32)/255.0 #normaliza el color a un valor entre 0 y 1
            arr = arreglo.reshape((50,50,1)) #formato requerido por TensorFlow
            imagenes.append(arr)

            etiqueta_idx = self.clases[clase]
            etiquetas.append(etiqueta_idx)
        
        return np.array(imagenes), np.array(etiquetas)

    def construir_modelo(self):
        self.modelo = tf.keras.Sequential([
            tf.keras.layers.Flatten(input_shape=(*self.tamano, 1)), #capa de entrada 50*50 con 1 solo color
            tf.keras.layers.Dense(128, activation='relu'),
            tf.keras.layers.Dense(64, activation='relu'),
            tf.keras.layers.Dense(len(self.clases), activation='softmax') #capa de salida con tantas neuronas como clases hay
        ])
        self.modelo.compile(optimizer='adam',
                            loss='sparse_categorical_crossentropy',
                            metrics=['accuracy'])

    def entrenar(self, x, y, epochs=20, batch_size=32):
        x_train, x_val, y_train, y_val = train_test_split(x, y, test_size=0.2)
        historial = self.modelo.fit(x_train, y_train, epochs=epochs, batch_size=batch_size,
                        validation_data=(x_val, y_val))
        self.mostrar_perdida(historial)
        
    def mostrar_perdida(self, historial):
        plt.figure(figsize=(8, 4))
        plt.plot(historial.history["loss"])
        plt.xlabel("Época")
        plt.ylabel("Pérdida (loss)")
        plt.title("Evolución del aprendizaje")
        plt.grid(True)
        plt.show()

    def guardar_modelo(self, ruta_salida):
        if self.modelo is None:
            raise RuntimeError("Error: el modelo no fue construido. Llamá a construir_modelo() primero.")
        self.modelo.save(ruta_salida)

##############################################################################################

    def cargar_modelo(self, ruta_modelo):
        self.modelo = tf.keras.models.load_model(ruta_modelo)

    def clasificar_imagen_color(self, ruta_imagen):
        if self.modelo is None:
            raise RuntimeError("El modelo no está cargado ni entrenado.")
        
        imagen_color = cv2.imread(ruta_imagen)
        if imagen_color is None:
            print("No se pudo leer la imagen:", ruta_imagen)
            return
        imagen_gris = cv2.cvtColor(imagen_color, cv2.COLOR_BGR2GRAY)
        imagen_redimensionada = cv2.resize(imagen_gris, self.tamano)
        entrada = imagen_redimensionada.astype(np.float32)/255.0
        entrada = entrada.reshape((1, *self.tamano, 1))

        pred = self.modelo.predict(entrada, verbose=0)
        idx = np.argmax(pred)
        nombre_clase = [k for k, v in self.clases.items() if v == idx][0]
        prob = pred[0][idx]
        return nombre_clase, prob
    
    def mostrar_prediccion(self, ruta_imagen):
        resultado = self.clasificar_imagen_color(ruta_imagen)
        if resultado is None:
            return
        nombre_clase, prob = resultado
        imagen = cv2.imread(ruta_imagen)
        if imagen is None:
            print("No se pudo leer la imagen:", ruta_imagen)
            return
        
        # Agrandar la imagen para visualizar mejor (por ejemplo, al 200%)
        factor_escala = 2  # Cambiá esto para agrandar más o menos
        ancho = imagen.shape[1] * factor_escala
        alto = imagen.shape[0] * factor_escala
        imagen = cv2.resize(imagen, (ancho, alto), interpolation=cv2.INTER_LINEAR)
        
        texto = f"{nombre_clase} ({prob*100:.1f}%)"
        cv2.putText(
            imagen, texto, org=(10, alto - 20),
            fontFace=cv2.FONT_HERSHEY_SIMPLEX,
            fontScale=0.8,  # Ajustado a la imagen ampliada
            color=(200,200,0), thickness=2, lineType=cv2.LINE_AA
            )
        cv2.imshow("Predicción", imagen)
        cv2.waitKey(0)
        cv2.destroyAllWindows
    
    def mostrar_varias_predicciones(self, carpeta, cantidad=5):
        archivos = [f for f in os.listdir(carpeta) if f.endswith(".png")]
        if not archivos:
            print("No se encontraron imágenes en la carpeta:", carpeta)
            return
        seleccionadas = random.sample(archivos, min(cantidad, len(archivos)))

        for nombre_archivo in seleccionadas:
            ruta = os.path.join(carpeta, nombre_archivo)
            self.mostrar_prediccion(ruta)



##############################################################################################################
if __name__ == "__main__":
    clasificador = ClasificadorForma("imagenes/simples/entrenamiento")
    x, y = clasificador.cargar_datos()
    clasificador.construir_modelo()
    clasificador.entrenar(x, y)
    clasificador.guardar_modelo("modelo_clasificador_formas.keras")

    clasificador.cargar_modelo("modelo_clasificador_formas.keras")
    clasificador.mostrar_prediccion("imagenes/simples/circulo_amarillo_sobre_rojo.png")
    clasificador.mostrar_varias_predicciones("imagenes/simples", cantidad=5)