"""
Realizar un bucle que muestre aleatoriamente una de las tres imágenes de los semáforos adjuntos por intervalos de 2 segundos.
En cada vuelta el sistema deberá reconocer el estado del semáforo e imprimir según corresponda:
Semáforo en rojo! - Detenerse!
Semáforo en amarillo - Atención!
Semáforo en verde - Avanzar!
"""

import tensorflow as tf
import os
import numpy as np
import cv2
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import random
import re
import time


class ClasificadorColor:
    def __init__(self, carpeta_imagenes="imagenes/semaforo", tamano=(60, 100)): #ancho, alto
        self.carpeta = carpeta_imagenes
        self.tamano = tamano
        self.clases = {"rojo":0, "amarillo":1, "verde":2}
        self.modelo = None
 
    def determinar_color(self, nombre_archivo):
        match = re.match(r"(\d+)", nombre_archivo)
        if not match:
            return None

        numero = int(match.group(1))
        return {1: "rojo", 2: "amarillo", 3: "verde"}.get(numero, None)
    
    def cargar_datos(self):
        imagenes = []
        etiquetas = []
        for nombre_archivo in os.listdir(self.carpeta):
            if not nombre_archivo.endswith(".png"):
                continue
            try:
                clase = self.determinar_color(nombre_archivo)
                if clase is None:
                    continue
            except:
                continue

            ruta = os.path.join(self.carpeta, nombre_archivo)
            imagen = cv2.imread(ruta, cv2.IMREAD_COLOR)
            if imagen is None:
                continue
            imagen_redimensionada = cv2.resize(imagen, self.tamano)
            imagen_normalizada = imagen_redimensionada.astype(np.float32)/255.0
            imagenes.append(imagen_normalizada)
            etiquetas.append(self.clases[clase])
        
        return np.array(imagenes), np.array(etiquetas)
  
    def aumentar_datos(self, carpeta_destino="imagenes/semaforo/imagenes_aumentadas", cantidad_por_imagen=40):
        if not os.path.exists(carpeta_destino):
            os.makedirs(carpeta_destino)
        
        codigo = {"rojo": 1, "amarillo": 2, "verde": 3}

        for nombre_archivo in os.listdir(self.carpeta):
            if not nombre_archivo.endswith(".png"):
                continue
            clase = self.determinar_color(nombre_archivo)
            if clase is None:
                continue

            ruta = os.path.join(self.carpeta, nombre_archivo)
            imagen = cv2.imread(ruta)
            if imagen is None:
                continue

            alto, ancho = imagen.shape[:2]

            for i in range(cantidad_por_imagen):
                transformada = imagen.copy()

                # Rotación aleatoria
                if random.random() < 0.7:
                    angulo = random.choice([-25, -10, -5, 0, 5, 10, 25])
                    M = cv2.getRotationMatrix2D((ancho // 2, alto // 2), angulo, 1)
                    transformada = cv2.warpAffine(transformada, M, (ancho, alto))

                # Ajuste de brillo
                if random.random() < 0.5:
                    valor_brillo = random.randint(-40, 40)
                    transformada = transformada.astype(np.int16) + valor_brillo
                    transformada = np.clip(transformada, 0, 255).astype(np.uint8)

                # Desplazamiento aleatorio
                if random.random() < 0.5:
                    x_offset = random.randint(-10, 10)
                    y_offset = random.randint(-10, 10)
                    M_offset = np.float32([[1, 0, x_offset], [0, 1, y_offset]])
                    transformada = cv2.warpAffine(transformada, M_offset, (ancho, alto))

                # Zoom aleatorio
                if random.random() < 0.4:
                    factor = random.uniform(0.8, 1.0)
                    nuevo_ancho = int(ancho * factor)
                    nuevo_alto = int(alto * factor)
                    x_inicio = random.randint(0, ancho - nuevo_ancho)
                    y_inicio = random.randint(0, alto - nuevo_alto)
                    recorte = transformada[y_inicio:y_inicio+nuevo_alto, x_inicio:x_inicio+nuevo_ancho]
                    transformada = cv2.resize(recorte, (ancho, alto))

                # Espejado horizontal
                if random.random() < 0.5:
                    transformada = cv2.flip(transformada, 1)

                # Contraste aleatorio
                if random.random() < 0.4:
                    alpha = random.uniform(0.8, 1.2)  # contraste
                    transformada = cv2.convertScaleAbs(transformada, alpha=alpha, beta=0)

                # Ruido gaussiano
                if random.random() < 0.3:
                    ruido = np.random.normal(0, 10, transformada.shape).astype(np.int16)
                    transformada = transformada.astype(np.int16) + ruido
                    transformada = np.clip(transformada, 0, 255).astype(np.uint8)

                # Guardar imagen
                nombre_base = os.path.splitext(nombre_archivo)[0]
                nombre_nuevo = f"{codigo[clase]}_{nombre_base}_{i+1}.png"
                transformada = cv2.resize(transformada, self.tamano)
                cv2.imwrite(os.path.join(carpeta_destino, nombre_nuevo), transformada)

                print(f"Imagen generada: {nombre_nuevo}") #DEBUG
            
    def construir_modelo(self):
        self.modelo = tf.keras.Sequential([
            tf.keras.layers.Flatten(input_shape=(self.tamano[1], self.tamano[0], 3)), #alto, ancho
            tf.keras.layers.Dense(254, activation = 'relu'),
            tf.keras.layers.Dense(64, activation = 'relu'),
            tf.keras.layers.Dense(len(self.clases), activation='softmax')
        ])
        self.modelo.compile(optimizer='adam',
                            loss = 'sparse_categorical_crossentropy',
                            metrics=['accuracy'])

    def entrenar_modelo(self, carpeta_datos=None, epochs=20, batch_size=4):
        if carpeta_datos:
            self.carpeta = carpeta_datos
            
        x, y = self.cargar_datos()
        x_train, x_val, y_train, y_val = train_test_split(x, y, test_size=0.3)
        historial = self.modelo.fit(x_train, y_train, validation_data=(x_val, y_val),
                                    epochs=epochs, batch_size=batch_size)
        self.mostrar_perdida(historial)

    def mostrar_perdida(self, historial):
        plt.plot(historial.history['loss'])
        plt.title('Pérdida durante el entrenamiento')
        plt.xlabel('Epocas')
        plt.ylabel('Loss')
        plt.grid(True)
        plt.show()

    def guardar_modelo(self, ruta):
        if self.modelo is not None:
            self.modelo.save(ruta)
    
    
class EvaluadorSemaforo:
    def __init__(self, ruta_modelo, tamano=(60, 100)): #ancho, alto
        self.modelo = tf.keras.models.load_model(ruta_modelo)
        self.tamano = tamano
        self.clases = {0:"rojo", 1:"amarillo", 2:"verde"}
    
    def predecir_color(self, ruta_imagen):
        imagen = cv2.imread(ruta_imagen)
        if imagen is None:
            print("No se pudo cargar la imagen")
            return None
        imagen = cv2.resize(imagen, self.tamano) #ancho, alto
        imagen_normalizada = imagen.astype(np.float32)/255.0
        entrada = imagen_normalizada.reshape((1, *self.tamano, 3))

        prediccion = self.modelo.predict(entrada, verbose=0)
        idx = np.argmax(prediccion)
        probabilidad = prediccion[0][idx]
        return self.clases[idx], probabilidad

    def ejecutar_bucle(self, carpeta_imagenes, repeticiones=5, intervalo=2):
        imagenes = [f for f in os.listdir(carpeta_imagenes) if f.endswith(".png")]
        if not imagenes:
            print("No hay imagenes en la carpeta.")
            return

        for _ in range(repeticiones):
            archivo = random.choice(imagenes)
            ruta = os.path.join(carpeta_imagenes, archivo)
            clase, probabilidad = self.predecir_color(ruta)

            mensaje = {
                "rojo": "Semáforo en rojo! - Detenerse!",
                "amarillo": "Semáforo en amarillo - Atención!",
                "verde": "Semáforo en verde - Avanzar!"
            }.get(clase, "Color no reconocido")
            
            print(f"[{clase.upper()} - {probabilidad*100:1f}%] {mensaje}")

            imagen = cv2.imread(ruta)
            cv2.imshow("Semáforo", imagen)
            cv2.waitKey(intervalo * 1000)
            cv2.destroyAllWindows()

class VisualizadorColor:
    def __init__(self, ruta_modelo, tamano=(60, 100)):
        self.modelo = tf.keras.models.load_model(ruta_modelo)
        self.tamano = tamano
        self.colores = {
            0: ("🟥 Semáforo en ROJO — Detenerse!", "imagenes/semaforo/1.png"),
            1: ("🟨 Semáforo en AMARILLO — Atención!", "imagenes/semaforo/2.png"),
            2: ("🟩 Semáforo en VERDE — Avanzar!", "imagenes/semaforo/3.png")
        }

    def capturar_frame(self):
        camara = obtener_camara_disponible()
        if camara is None:
            return None

        camara.set(cv2.CAP_PROP_FRAME_WIDTH, 640)  # Mejor resolución para recortar
        camara.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

        # Leer varios frames para estabilizar cámara y descartar primeros frames
        for _ in range(5):
            ret, frame = camara.read()
            if not ret:
                print("⚠️ No se pudo leer frame durante estabilización.")
                camara.release()
                return None

        camara.release()

        if not ret or frame is None:
            print("⚠️ No se pudo capturar imagen desde la cámara.")
            return None

        # Recorte central
        alto, ancho = frame.shape[:2]
        tamano_recorte = self.tamano  # ej: (60, 100) ancho x alto esperado

        # Calcular coordenadas para recorte central
        x_inicio = max((ancho - tamano_recorte[0]) // 2, 0)
        y_inicio = max((alto - tamano_recorte[1]) // 2, 0)

        x_fin = x_inicio + tamano_recorte[0]
        y_fin = y_inicio + tamano_recorte[1]

        # Recortar y devolver
        frame_recortado = frame[y_inicio:y_fin, x_inicio:x_fin]

        return frame_recortado
      
    def predecir_desde_frame(self, frame):
        imagen = cv2.resize(frame, self.tamano)
        imagen_normalizada = imagen.astype(np.float32) / 255.0
        entrada = imagen_normalizada.reshape((1, *self.tamano, 3))
        pred = self.modelo.predict(entrada, verbose=0)
        idx = np.argmax(pred)
        prob = pred[0][idx]
        return idx, prob
    
    def mostrar_color(self, clase_idx, probabilidad, frame_original):
        UMBRAL_CONFIANZA = 0.8
        frame_con_texto = frame_original.copy()

        if probabilidad < UMBRAL_CONFIANZA:
            mensaje = "⚠️ Color no reconocido con confianza suficiente"
            color_texto = (255, 255, 255)  # negro
        else:
            mensaje, ruta_imagen = self.colores.get(clase_idx, ("Color desconocido", None))
            color_texto = (0, 0, 0)  # blanco

        # Mostrar la imagen de la cámara (o test) con texto superpuesto
        cv2.putText(frame_con_texto, mensaje, (10, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, color_texto, 2, cv2.LINE_AA)

        cv2.imshow("Captura con resultado", frame_con_texto)
        cv2.waitKey(2000)
        cv2.destroyAllWindows()

        # Si es una predicción confiable, mostrar imagen del semáforo correspondiente
        if probabilidad >= UMBRAL_CONFIANZA and ruta_imagen and os.path.exists(ruta_imagen):
            imagen = cv2.imread(ruta_imagen)
            cv2.imshow("Semáforo detectado", imagen)
            cv2.waitKey(2000)
            cv2.destroyAllWindows()
        elif probabilidad >= UMBRAL_CONFIANZA:
            print(f"⚠️ No se encontró la imagen: {ruta_imagen}")

    def ejecutar(self, ciclos=3, intervalo=10):

        for i in range(ciclos):
            print(f"\n🕐 Captura {i+1}...")
            frame = self.capturar_frame()
            if frame is None:
                continue

            clase_idx, prob = self.predecir_desde_frame(frame)
            print(f"🎯 Confianza: {prob:.2f}")
            self.mostrar_color(clase_idx, prob, frame) 
            time.sleep(intervalo)

    def convertir_y_renombrar_imagenes(self, carpeta_origen="imagenes/semaforo/test_raw", carpeta_destino="imagenes/semaforo/test"):
        print("Iniciando conversión...") #DEBUG
        if not os.path.exists(carpeta_origen):
            print(f"⚠️ Carpeta de origen no encontrada: {carpeta_origen}")
            return
        if not os.path.exists(carpeta_destino):
            os.makedirs(carpeta_destino)
        
        print("Ruta completa de la carpeta de origen:", os.path.abspath(carpeta_origen))

        archivos = [f for f in os.listdir(carpeta_origen) if f.lower().endswith((".jpg", ".jpeg"))]
        #archivos.sort()  # Orden alfabético (opcional)
        print(f"Archivos encontrados en {carpeta_origen}: {archivos}")

        for i, nombre in enumerate(archivos, start=1):
            ruta_origen = os.path.join(carpeta_origen, nombre)
            imagen = cv2.imread(ruta_origen)

            if imagen is None:
                print(f"⚠️ No se pudo leer la imagen: {nombre}")
                continue

            nuevo_nombre = f"test_{i:03d}.png"
            ruta_destino = os.path.join(carpeta_destino, nuevo_nombre)
            cv2.imwrite(ruta_destino, imagen)  # Guarda como PNG sin compresión visible

            print(f"✅ Convertida: {nombre} → {nuevo_nombre}")

    def testear_imagenes(self, carpeta="imagenes/semaforo/test"):
        if not os.path.exists(carpeta):
            print(f"⚠️ La carpeta {carpeta} no existe.")
            return

        archivos = [f for f in os.listdir(carpeta) if f.endswith(".png")]

        for archivo in archivos:
            ruta = os.path.join(carpeta, archivo)
            imagen = cv2.imread(ruta)
            if imagen is None:
                print(f"⚠️ No se pudo cargar la imagen {archivo}")
                continue

            alto, ancho = imagen.shape[:2]
            ancho_obj, alto_obj = self.tamano  # (ancho, alto) que usa el modelo

            # Calcular recorte central
            x_inicio = max((ancho - ancho_obj) // 2, 0)
            y_inicio = max((alto - alto_obj) // 2, 0)
            x_fin = x_inicio + ancho_obj
            y_fin = y_inicio + alto_obj

            imagen_recortada = imagen[y_inicio:y_fin, x_inicio:x_fin]

            # Predecir el color usando el método que tengas para eso:
            clase_idx, prob = self.predecir_desde_frame(imagen_recortada)
            #print(f"Imagen: {archivo} — Confianza: {prob:.2f}")

            # Mostrar resultado (el semáforo o texto)
            self.mostrar_color(clase_idx, prob, imagen_recortada)                                                                           

def obtener_camara_disponible(max_indice=10):
    """
    Busca la primera cámara disponible entre los índices 0 y max_indice-1.
    Retorna un objeto VideoCapture si encuentra una cámara, o None si no encuentra ninguna.
    """
    print("🔎 Buscando cámara disponible...")
    for i in range(max_indice):
        cap = cv2.VideoCapture(i, cv2.CAP_DSHOW)
        if cap.isOpened():
            print(f"✅ Cámara encontrada en el índice {i}")
            return cap  # no se hace release aquí para usarla directamente
        cap.release()

    print("❌ No se encontró ninguna cámara disponible.")
    return None
    
#############################################################################################################            

if __name__ == "__main__":
    # clasificador = ClasificadorColor("imagenes/semaforo")
    # clasificador.aumentar_datos(carpeta_destino="imagenes/semaforo/imagenes_aumentadas", cantidad_por_imagen=40)
    # clasificador.construir_modelo()
    # clasificador.entrenar_modelo(carpeta_datos="imagenes/semaforo/imagenes_aumentadas", epochs=48)
    # clasificador.guardar_modelo("modelo_clasificador_color_semaforo.keras")

    # evaluador = EvaluadorSemaforo("modelo_clasificador_color_semaforo.keras")
    # evaluador.ejecutar_bucle("imagenes/semaforo", repeticiones=10, intervalo=2)
    
    visor = VisualizadorColor("modelo_clasificador_color_semaforo.keras")
    #visor.convertir_y_renombrar_imagenes()
    visor.ejecutar(ciclos=3, intervalo=10)
    #visor.testear_imagenes()

