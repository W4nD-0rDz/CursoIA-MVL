#REDES NEURONALES CONVOLUCIONALES: identificación y clasificación de imágenes
#Objetivo del ejercicio: descubrir aplicaciones para CNN
#Se usan arquitecturas predefinidas que se parametrizan
#La semana que viene es la reunión en el fablab

import os
import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
import cv2

categorias = ["imagenes/africanos", "imagenes/anglosajones", "imagenes/latinos", "imagenes/orientales"]
# imagenes = []
# etiquetas = []

# #carga de los datos
# x = 0
# for i in categorias:
#     archivos = os.listdir(i)
#     for archivo in archivos:
#         ruta = os.path.join(i, archivo)
#         img = cv2.imread(ruta, 0)
#         if img is not None:
#             img = cv2.resize(img, (200, 200))
#             imagenes.append(img)
#             etiquetas.append(x)
#     x+=1

# #convertir arrays a numpy
# imagenes=np.asarray(imagenes).astype('float32') / 255.0
# imagenes = imagenes.reshape(-1, 200, 200, 1)
# etiquetas=np.asarray(etiquetas)

# #red neuronal
# entrada=tf.keras.layers.Conv2D(128, (3,3), input_shape=(200,200,1), activation="relu")
# agrupamiento1=tf.keras.layers.MaxPooling2D(2,2)
# convolucion1=tf.keras.layers.Conv2D(64, (3,3), activation="relu")
# agrupamiento2=tf.keras.layers.MaxPooling2D(2,2)
# eliminacion=tf.keras.layers.Dropout(0.5)
# aplastamiento= tf.keras.layers.Flatten()
# oculta1=tf.keras.layers.Dense(32, activation="relu")
# salida=tf.keras.layers.Dense(len(categorias), activation="softmax")
# modelo= tf.keras.Sequential([
#     entrada, agrupamiento1, convolucion1, agrupamiento2, eliminacion, aplastamiento, oculta1, salida
# ])

# #compilar el modelo
# modelo.compile(optimizer="adam", 
#                loss="sparse_categorical_crossentropy",
#                metrics=["accuracy"])

# #aumentar las imágenes de entrenamiento
# def aumentar(img, etiqueta):
#     img = tf.image.random_flip_left_right(img)
#     img = tf.image.random_brightness(img, max_delta=0.1)
#     img = tf.image.random_contrast(img, 0.9, 1.1)
#     return img, etiqueta

# # crear dataset para entrenamiento
# dataset_original = tf.data.Dataset.from_tensor_slices((imagenes, etiquetas))
# dataset_aumentado1 = dataset_original.map(aumentar)
# dataset_aumentado2 = dataset_original.map(aumentar)
# dataset = dataset_original.concatenate(dataset_aumentado1).concatenate(dataset_aumentado2)
# dataset = dataset.shuffle(100).batch(32)

# #función para graficar la pérdida
# def mostrar_perdida(historial):
#     plt.plot(historial.history['loss'])
#     plt.title('Pérdida durante el entrenamiento')
#     plt.xlabel('Epocas')
#     plt.ylabel('Loss')
#     plt.grid(True)
#     plt.show()

# #entrenamiento del modelo
# historial = modelo.fit(dataset, epochs=100, verbose=False)
# mostrar_perdida(historial)

# #guardar modelo
# modelo.save("modelo_conv_personas.keras")

# #Para ver la arquitectura del modelo
# modelo.summary()

#prueba
modelo = tf.keras.models.load_model("modelo_conv_personas.keras")
ruta_imagenes_prueba = "imagenes/imagenes_prueba"
imagenes_prueba = os.listdir("imagenes/imagenes_prueba")

for archivo in imagenes_prueba:
    ruta = os.path.join(ruta_imagenes_prueba,archivo)
    imagen=cv2.imread(ruta)
    img = cv2.imread(ruta, 0)  # leer en escala de grises
    img = cv2.resize(img, (200, 200))  # normalizar tamaño
    img = np.asarray(img).astype('float32') / 255.0  # convertir y normalizar valores

    img = np.expand_dims(img, axis=(0, -1))  # forma (1, 200, 200, 1) si es modelo convolucional

    prediccion = modelo.predict(img)  # devuelve algo como [[0.1, 0.7, 0.2]]
    clase = np.argmax(prediccion)  # obtiene el valor más alto (por ejemplo, 0.7)
    nombre = os.path.splitext(archivo)[0]

    titulo = f"{nombre} => clase: {categorias[clase].split('/')[-1]}"

    cv2.imshow(titulo, imagen)
    print(titulo)
    cv2.waitKey(0)
    cv2.destroyAllWindows()