import tensorflow as tf
import os
import numpy as np
import cv2
from sklearn.model_selection import train_test_split
import random
import time

class EvaluadorForma:
    def __init__(self, ruta_modelo, tamano=(50, 50)):
        self.modelo = tf.keras.models.load_model(ruta_modelo)
        self.tamano = tamano
        self.clases = {"triangulo": 0, "cuadrado": 1, "circulo": 2}

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

    def capturar_imagen(self, indice=None, carpeta_destino="imagenes/captura_video"):
        if not os.path.exists(carpeta_destino):
            os.makedirs(carpeta_destino)

        cap = cv2.VideoCapture(0)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 400)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 200)

        ret, frame = cap.read()
        cap.release()

        if not ret:
            print("Error al capturar imagen de la cámara")
            return None
        
        if indice is not None:
            nombre_archivo = f"imagen_{indice}.png"
            ruta_completa = os.path.join(carpeta_destino, nombre_archivo)
            cv2.imwrite(ruta_completa, frame)
            print(f"imagen guardada: {ruta_completa}")
            return ruta_completa
        else:
            return frame
    
    def evaluar_imagen(self, ruta_imagen):
        if isinstance(ruta_imagen, str):
            self.mostrar_prediccion(ruta_imagen)
        else:
            # es imagen numpy array
            # Para usar mostrar_prediccion, hay que guardar imagen temporal o hacer otro método
            # Mejor hacemos aquí el mismo proceso sin mostrar_prediccion, pero similar:
            imagen = ruta_imagen
            # Guardar temporal para usar mostrar_prediccion:
            ruta_temp = "temp_captura.jpg"
            cv2.imwrite(ruta_temp, imagen)
            self.mostrar_prediccion(ruta_temp)
            # Podés borrar el archivo si querés luego

#############################################################################################################
 
#GUARDA UNA CAPTURA Y LA EVALUA
if __name__ == "__main__":
    evaluador = EvaluadorForma("modelo_clasificador_formas.keras")
    # Capturar una imagen de la webcam y guardarla
    ruta = evaluador.capturar_imagen(indice=1, carpeta_destino="imagenes/captura_video")
    # Evaluar la imagen capturada
    if ruta:
        evaluador.evaluar_imagen(ruta)

#GUARDA UN GRUPO DE CAPTURAS Y LAS EVALUA
if __name__ == "__main__":
    evaluador = EvaluadorForma("modelo_clasificador_formas.keras")

    for i in range(5):  # Cambiá el número según cuántas querés
        ruta = evaluador.capturar_imagen(indice=i+1, carpeta_destino="imagenes/captura_video")
        if ruta:
            evaluador.evaluar_imagen(ruta)

#EVALUA SIN GUARDAR LAS IMAGENES
if __name__ == "__main__":
    evaluador = EvaluadorForma("modelo_clasificador_formas.keras")

    imagen = evaluador.capturar_imagen()  # Sin guardar
    if imagen is not None:
        evaluador.evaluar_imagen(imagen)