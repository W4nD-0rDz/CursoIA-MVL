import tensorflow as tf
import numpy as np
import keras
import pandas as pd


oculta1=keras.layers.Dense(units=3,input_shape=[1])
oculta2=keras.layers.Dense(units=3)
capasalida=keras.layers.Dense(units=1)



model=keras.Sequential([oculta1,oculta2,capasalida])
model.compile(optimizer="Nadam" , loss="mean_squared_error")





pesos=[1,2,3,4,5]
dolares=[100,200,300,400,500]


pesos=np.asarray(pesos)
dolares=np.asarray(dolares)


model.fit(pesos,dolares,epochs=10) 

valor=int(input("Ingrese el valor: "))
valor=[valor]
valor=np.asarray(valor)
print(model.predict(valor)) 
