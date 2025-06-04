import tensorflow as tf
import keras
import numpy as np


model=keras.Sequential([keras.layers.Dense(units=1,input_shape=[1])])
model.compile(optimizer="Nadam" , loss="mean_squared_error")



x=[1,2,3,4,5,6,7,8,9,10]
y=[10,200,300,400,500,600,700,800,900,1000]
x=np.asarray(x)
y=np.asarray(y)
model.fit(x,y,epochs=100) 



model.save("modelo.keras") #guarda el modelo entrenado en la ruta del archivo

