import tensorflow as tf
import keras
import numpy as np


#Esto lo puedo hacer desde otro ódulo para traer el modelo entrenado
model=keras.models.load_model("modelo.keras")
valor=int(input("Ingrese el valor bucado: "))
valor=[valor]
valor=np.asarray(valor)
print(model.predict(valor))