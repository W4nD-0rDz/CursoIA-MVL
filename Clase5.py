import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2' #Reduce el ruido en la consola
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf #librería para ia de py
import keras #crear redes neuronales

# lista=[1,2,3,4,5]
# listanp=np.asarray(lista) #necesario para los métodos de keras
# print(lista)
# print(listanp)

# pesos = float(input("ingrese el monto a cambiar: $"))
# dolares = pesos/1300
# print("el monto ingresado equivale a US$", round(dolares,2))

# #Configuración de la red
# #Arquitectura
# modelo=keras.Sequential([keras.layers.Dense(units=1, activation= None, input_shape=[1])]) activación x default (y= mx+b)
# ambientes = [1,2,3,4,5,6]
# precios = [123, 456, 789, 1011, 1213, 1415]
# x=np.asarray(ambientes)
# y=np.asarray(precios)
# #Criterio
# modelo.compile(optimizer="sgd", loss="mean_squared_error")

# #Entrenamiento
# print("Comenzando entrenamiento...")
# historial = modelo.fit(x, y, epochs=100, verbose=False)
# print("Modelo entrenado!")

# #Gráfico de pérdida (cerrar para que continue)
# plt.xlabel("# ronda")
# plt.ylabel("Grado de Pérdida")
# plt.plot(historial.history["loss"])
# plt.show()

# #Predicción:
# consulta = int(input("Indique la cantidad de ambientes a consultar: "))
# consultaLista = np.asarray([consulta])
# resultado = modelo.predict(consultaLista)
# print(f"Precio estimado para {consulta} ambiente(s): ${resultado[0][0]:.2f}")

# #Pesos y sesgos
# print("Pesos y sesgos del modelo")
# print(modelo.get_weights())

###############################################################################
#Ejemplo 2: más de una capa

#Configuración de la red
#Arquitectura
entrada = np.array([1,2,3,4,5,6], dtype=float)
salida = np.array([123, 456, 789, 1011, 1213, 1415], dtype=float)

# Normalizamos a valores entre 0 y 1
entrada_norm = entrada / np.max(entrada)
salida_norm = salida / np.max(salida)

# # Capas
# oculta1 = tf.keras.layers.Dense(units=3, activation='relu', input_shape=[1])
# oculta2 = tf.keras.layers.Dense(units=3, activation='relu')
# final = tf.keras.layers.Dense(units=1) #debe ser uno, xq quiero un unico valor
# modelo = tf.keras.Sequential([oculta1, oculta2, final])
# #Criterios
# modelo.compile(tf.keras.optimizers.Adam(learning_rate=0.001), loss="mean_squared_error")

# #Entrenamiento
# print("Comenzando entrenamiento...")
# historial = modelo.fit(entrada_norm, salida_norm, epochs=2000, verbose=False)
# print("Modelo entrenado!")

# #Gráfico de pérdida (cerrar para que continue)
# plt.xlabel("# ronda")
# plt.ylabel("Grado de Pérdida")
# plt.plot(historial.history["loss"])
# plt.show()

# #Predicción:
# consulta = int(input("Indique la cantidad de ambientes a consultar: "))
# # consultaLista = np.asarray([consulta])
# # resultado = modelo.predict(consultaLista)
# # print(f"Precio estimado para {consulta} ambiente(s): ${resultado[0][0]:.2f}")
# consulta_norm = consulta / np.max(entrada)
# consulta_array = np.array([[consulta_norm]])  # Forma correcta: matriz 2D
# resultado_norm = modelo.predict(consulta_array)
# resultado_real = resultado_norm[0][0] * np.max(salida)
# print(f"Precio estimado para {consulta} ambiente(s): ${resultado_real}")

# #Pesos y sesgos
# print("Pesos y sesgos del modelo")
# print(modelo.get_weights())
##################################################################################

# #EJEMPLO 3: En caso de modelo ya guardado:
# Importar modelo
modelo = keras.models.load_model("entrenamiento_adam_relu_3.keras")

#Predicción:
consulta = int(input("Indique la cantidad de ambientes a consultar: "))

# Valores máximos del entrenamiento original
ENTRADA_MAX = 6       # porque np.max([1,2,3,4,5,6]) == 6
SALIDA_MAX = 1415     # porque np.max([123,...,1415]) == 1415

# Normalizás como se entrenó el modelo
consulta_norm = consulta / ENTRADA_MAX
consulta_array = np.array([[consulta_norm]])

# Predicción
resultado_norm = modelo.predict(consulta_array)
resultado_real = resultado_norm[0][0] * SALIDA_MAX

print(f"Precio estimado para {consulta} ambiente(s): ${resultado_real:.2f}")
