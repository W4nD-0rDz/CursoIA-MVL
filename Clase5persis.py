import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2' #Reduce el ruido en la consola
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf #librería para ia de py
import keras #crear redes neuronales

#Ejemplo 2

#Configuración de la red
#Arquitectura
entrada = np.array([1,2,3,4,5,6], dtype=float)
salida = np.array([123, 456, 789, 1011, 1213, 1415], dtype=float)

# Normalizamos a valores entre 0 y 1
entrada_norm = entrada / np.max(entrada)
salida_norm = salida / np.max(salida)

# Capas
oculta1 = tf.keras.layers.Dense(units=3, activation='relu', input_shape=[1])
oculta2 = tf.keras.layers.Dense(units=3, activation='relu')
final = tf.keras.layers.Dense(units=1) #debe ser uno, xq quiero un unico valor
modelo = keras.Sequential([oculta1, oculta2, final])
#Criterios
modelo.compile(keras.optimizers.Adam(learning_rate=0.001), loss="mean_squared_error")

#Entrenamiento
print("Comenzando entrenamiento...")
historial = modelo.fit(entrada_norm, salida_norm, epochs=2000, verbose=False)
print("Modelo entrenado!")

#Gráfico de pérdida (cerrar para que continue)
plt.xlabel("# ronda")
plt.ylabel("Grado de Pérdida")
plt.plot(historial.history["loss"])
plt.show()

#Guarda el modelo entrenado
modelo.save("entrenamiento_adam_relu_3.keras")