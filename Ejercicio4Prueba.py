"""
1. Importa el archivo csv como un dataframe
2. Armar los datasets de entradas y salidas con los valores del dataframe
3. Desarrollar un sistema que le permita el asuario predecir la temperatura de la tierra.
4. Que el sistema se ejecute guardando el modelo entrenado.
"""

import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2' #Reduce el ruido en la consola
import tensorflow as tf
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

#Cargar la tabla
clima = pd.read_csv("clima.csv")

#Cargar las capas de entrada
# con NumPy: con np.array(...) convierte el objeto pandas en numpy.ndarray
# Hace una copia (especialmente si el dtype cambia)de objetos panda.Series(clima["year"])
year = np.array(clima["year"]) 
temperatura = np.array(clima["temp"])
# con Pandas: devuelve directamente los datos sin copiar.
#year = clima["year"].values.astype(int)
#temperatura = clima["temp"].values

#Modelo con Keras
capa = tf.keras.layers.Dense(units=1, input_shape=[1])
modelo = tf.keras.Sequential([capa])
modelo.compile(
    optimizer=tf.keras.optimizers.Adam(0.0025), #pasó de 0.1 a 0.0025
    loss='mean_squared_error'
)

#Modelo de 3 capas con Keras (con tasa de aprendizaje más baja)
# oculta1 = tf.keras.layers.Dense(units=3, input_shape=[1])
# oculta2 = tf.keras.layers.Dense(units=3)
# salida = tf.keras.layers.Dense(units=1)
# modelo = tf.keras.Sequential([oculta1, oculta2, salida])
# modelo.compile(
#     optimizer=tf.keras.optimizers.Adam(0.00025), #pasó de 0.1 a 0.00025
#     loss='mean_squared_error'
# )

# #Modelo de 3 capas con Keras con activación ReLU
# oculta1 = tf.keras.layers.Dense(units=3, activation='relu', input_shape=[1])
# oculta2 = tf.keras.layers.Dense(units=3, activation='relu',)
# salida = tf.keras.layers.Dense(units=1)
# modelo = tf.keras.Sequential([oculta1, oculta2, salida])
# modelo.compile(
#     optimizer=tf.keras.optimizers.Adam(0.0025),
#     loss='mean_squared_error'
# )

# #Entrenamiento
print("Comenzando entrenamiento...")
historial = modelo.fit(year, temperatura, epochs=500, verbose=False)
print("Modelo entrenado!")

#Mostrar los pesos resultantes
# print("Variables internas del modelo")
# print(capa.get_weights())

# # Guardar el modelo entrenado (Conjunto de archivos-arq, pesos y config)
modelo.save("modelo_year_temperatura.keras")
print("Modelo guardado como 'modelo_year_temperatura.keras'")

# #Gráfico de pérdida
plt.xlabel("# ronda")
plt.ylabel("Grado de Pérdida")
plt.plot(historial.history["loss"])
plt.show()

# # Predicción
#Una única predicción
resultado = modelo.predict(np.array([[2025]]))
print(f"Predicción de Temperatura para 2025: {resultado[0][0]:.2f}°C")
#Una lista de predicciones:
anios_futuros = np.array(list(range(2021, 2032))).astype(float)
#También: anios_futuros = np.arange(2021, 2032, dtype=float)
predicciones = modelo.predict(anios_futuros)
for anio, temp in zip(anios_futuros, predicciones):
    print(f"Predicción para {anio}: {temp[0]:.2f}°C")
#Gráfica de las temperaturas
plt.plot(year, temperatura, label= "Temperaturas registradas", color="blue", marker='o')
plt.plot(anios_futuros, predicciones, label="Predicción de temperaturas (2021-2032)", color="red", marker='*')
plt.title("Evolución de la temperatura global media (1920-2032)")
plt.xlabel("Año")
plt.ylabel("Temperatura (°C)")
plt.legend()
plt.grid(True)
plt.show()

