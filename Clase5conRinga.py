import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2' #Reduce el ruido en la consola
import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt

#El ejemplo consiste en un conversor de °C a °F
#Machine Learning con TensorFlow y NumPy (librerías de Py) y Keras
#capa entrada = °C
celsius = np.array([-40, -10, 0, 8, 15, 22, 38],dtype=float)
#capa salida = °F
fahrenheit = np.array([-40, 14, 32, 46, 59, 72, 100], dtype=float)

#Modelo con Keras
#API de redes neuronales escrita en Python. Se ejecuta sobre framework TensorFlow
#Diseñada por Google. 
#Permite entrenamiento de modelos de aprendizaje profundo 
#Utiliza cluster de unidades de procesamiento gráfico (GPU) o tensorial (TPU)

#####MODELO CON UNA SOLA CAPA#######
#Modelo
# capa = tf.keras.layers.Dense(units=1, input_shape=[1])
# modelo = tf.keras.Sequential([capa])
# modelo.compile(
#     optimizer=tf.keras.optimizers.Adam(0.1),
#     loss='mean_squared_error'
# )
# #Entrenamiento
# print("Comenzando entrenamiento...")
# historial = modelo.fit(celsius, fahrenheit, epochs=1000, verbose=False)
# print("Modelo entrenado!")
# print("Variables internas del modelo")
# print(capa.get_weights())
# # Guardar el modelo entrenado (Conjunto de archivos-arq, pesos y config)
# modelo.save("modelo_celsius_fahrenheit.keras")
# print("Modelo guardado como 'modelo_celsius_fahrenheit.keras'")
# # Predicción
# resultado = modelo.predict(np.array([[100.0]]))
# print(f"Predicción de 100°C: {resultado[0][0]:.2f}°F")
# #Gráfico de pérdida
# plt.xlabel("# ronda")
# plt.ylabel("Grado de Pérdida")
# plt.plot(historial.history["loss"])
# plt.show()
# #Para ver el modelo guardado
# modelo_cargado = tf.keras.models.load_model("modelo_celsius_fahrenheit.keras")
# modelo_cargado.summary()
# #Para ver solo los pesos
# pesos = modelo_cargado.get_weights()
# print(pesos)

#########MODELO CON 3 CAPAS INTERNAS############
#Modelo
oculta1 = tf.keras.layers.Dense(units=3, input_shape=[1])
oculta2 = tf.keras.layers.Dense(units=3)
salida = tf.keras.layers.Dense(units=1)
modelo = tf.keras.Sequential([oculta1, oculta2, salida])
modelo.compile(
    optimizer=tf.keras.optimizers.Adam(0.1),
    loss='mean_squared_error'
)
#Entrenamiento
print("Comenzando entrenamiento...")
historial = modelo.fit(celsius, fahrenheit, epochs=100, verbose=False)
print("Modelo entrenado!")
#Muestra las variables (pesos resultantes), el primero es multiplicación, el segundo suma
#y = mx + b
print("Variables internas del modelo")
print(oculta1.get_weights())
print(oculta2.get_weights())
print(salida.get_weights())
# Predicción
resultado = modelo.predict(np.array([[100.0]]))
print(f"Predicción de 100°C: {resultado[0][0]:.2f}°F")
#Gráfico de pérdida
plt.xlabel("# ronda")
plt.ylabel("Grado de Pérdida")
plt.plot(historial.history["loss"])
plt.show()