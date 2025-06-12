"""
1. Importa el archivo csv como un dataframe
2. Armar los datasets de entradas y salidas con los valores del dataframe
3. Desarrollar un sistema que le permita el asuario predecir la temperatura de la tierra.
4. Que el sistema se ejecute guardando el modelo entrenado.
"""
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2' #Reduce el "ruido" en la consola
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
import pandas as pd

class PrediccionTemperatura:
    # Carga el modelo ya entrenado.
    def __init__(self, modelo_path, entrada_max_path, salida_max_path):
        self.modelo = tf.keras.models.load_model(modelo_path)
        self.entrada_max = np.load(entrada_max_path)
        self.salida_max = np.load(salida_max_path)

    # Normaliza el dato de entrada del usuario
    def normalizar(self, valor):
        return valor / self.entrada_max
    
    # Desnormaliza el resultado entregado por el modelo
    def desnormalizar(self, valor_norm):
        return valor_norm * self.salida_max
    
    # Usa el modelo para predecir.
    def predecir(self, year):
        year_norm = self.normalizar(year)
        year_array = np.array([[year_norm]])
        temp_norm = self.modelo.predict(year_array, verbose=False)
        temp_real =self.desnormalizar(temp_norm[0][0])
        return temp_real
    
    # Muestra el resultado.
    def ejecutar(self):
        try:
            print("")
            year_consulta = int(input("Ingrese el año que desea consultar: "))
            resultado = self.predecir(year_consulta)
            print(f"Temperatura estimada para {year_consulta}: {resultado:.2f}°C")
        except ValueError:
            print("Por favor, ingrese un año válido")

    def predecir_evolucion(self, desde=2021, hasta=2032):
        # Lista de predicciones
        anios_futuros = np.arange(desde, hasta + 1, dtype=float)
        predicciones = [self.predecir(anio) for anio in anios_futuros]
        print("\nPredicción de temperaturas:")
        for anio, temp in zip(anios_futuros, predicciones):
            print(f"  Año {int(anio)}: {temp:.2f}°C")

        # Intentar leer datos históricos del CSV
        try:
            df = pd.read_csv("clima.csv")
            df_filtrado = df[(df["year"] >= hasta-100) & (df["year"] <= hasta)]
            x = df_filtrado["year"].values.astype(float)
            y = df_filtrado["temp"].values.astype(float)
            # Graficar datos históricos
            plt.plot(x, y, label=f"Temperaturas registradas ({hasta-100}-{hasta})", color="blue", marker='o')
        except Exception as e:
            print(f"No se pudieron cargar datos históricos del CSV: {e}")
        # Graficar predicciones
        plt.plot(anios_futuros, predicciones, label="Predicción futura", marker='*', color='red')
        plt.title("Evolución estimada de la temperatura global")
        plt.xlabel("Año")
        plt.ylabel("Temperatura (°C)")
        plt.legend()
        plt.grid(True)
        plt.show()

#################################################################################################################################
if __name__== "__main__":
    predictor = PrediccionTemperatura(
        "modelo_temp.keras",
        "entrada_max.npy",
        "salida_max.npy"
    )
    predictor.ejecutar()
    predictor.predecir_evolucion()