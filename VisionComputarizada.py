
import tensorflow as tf
import keras
import numpy as np
import cv2


cat=["latinos","anglosajones","orientales","africanos" ]
imgs=[]  
labels=[] 
x=0
for i in cat: 
    c=1
    for k in range (5): 
        img=cv2.imread(i+"/"+str(c)+".jpg",0)
        img=cv2.resize(img,(64,64)) 
        img=np.asarray(img)
        imgs.append(img)
        c=c+1
        labels.append(x) 
    x=x+1 


model=tf.keras.Sequential([
    tf.keras.layers.Conv2D(32, (3,3), input_shape=(64,64,1), activation="relu"), 
    tf.keras.layers.MaxPooling2D(2,2),
    tf.keras.layers.Conv2D(64, (3,3), input_shape=(64,64,1), activation="relu"),
    tf.keras.layers.MaxPooling2D(2,2),
    tf.keras.layers.Dropout(0.5), 
    tf.keras.layers.Flatten(), 
    tf.keras.layers.Dense(units=100, activation="relu"),
    tf.keras.layers.Dense(4, activation="softmax") 
])

model.compile(optimizer="adam",
loss="sparse_categorical_crossentropy", 
metrics=["accuracy"])


imgs=np.array(imgs)
labels=np.array(labels)
model.fit(imgs , labels , epochs=20)

test=cv2.imread("test.jpg",0) 
test=cv2.resize(test,(64,64)) 
test=np.asarray(test)
test=np.array([test]) 


result=model.predict(test)
print(result) 


print("latino:" , result[0][0]*100, "%" ) 
print("anglosajon:" , result[0][1]*100, "%" ) 
print("oriental:" , result[0][2]*100, "%" )
print("africano:" , result[0][2]*100, "%" ) 
 

