import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow import keras
import matplotlib.pyplot as plt

class EntrenadorModelo:
    # Carga el CSV.
    def __init__(self, archivo_csv):
        self.df = pd.read_csv(archivo_csv)
        self.modelo = None
        self.entrada_max = None
        self.salida_max = None

    # Normaliza los datos del csv
    # Prepara entradas y salidas
    # Los valores máximos para la normalización (entrada_max.npy, salida_max.npy)
    def preparar_datos(self):
        self.x = self.df['year'].values.astype(float)
        self.y = self.df['temp'].values.astype(float)
        self.entrada_max = np.max(self.x)
        self.salida_max = np.max(self.y)
        self.x_norm = self.x / self.entrada_max
        self.y_norm = self.y / self.salida_max

    # Arma el modelo
    def construir_modelo(self):
        self.modelo = keras.Sequential([
            keras.layers.Dense(units=3, activation='relu', input_shape=[1]),
            keras.layers.Dense(units=3, activation='relu'),
            keras.layers.Dense(units=1)
        ])
        self.modelo.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.001), loss="mean_squared_error")
    
    # Entrena el modelo
    def entrenar(self, epochs=200):
        historial = self.modelo.fit(self.x_norm, self.y_norm, epochs=epochs, verbose=False)
        np.save("entrada_max.npy", self.entrada_max)
        np.save("salida_max.npy", self.salida_max)
        print("Modelo y parámetros guardados correctamente.")
        # Mostrar gráfico de pérdida
        self.mostrar_perdida(historial)

    def mostrar_perdida(self, historial):
        plt.figure(figsize=(8, 4))
        plt.plot(historial.history["loss"])
        plt.xlabel("Época")
        plt.ylabel("Pérdida (loss)")
        plt.title("Evolución del aprendizaje")
        plt.grid(True)
        plt.show()

    # Guarda el modelo como .keras
    def guardar(self, archivo_modelo='modelo_temp.keras'):
        self.modelo.save(archivo_modelo)

##############################################################################################################
if __name__ == "__main__":
    entrenador = EntrenadorModelo("clima.csv")
    entrenador.preparar_datos()
    entrenador.construir_modelo()
    entrenador.entrenar()
    entrenador.guardar()

        
