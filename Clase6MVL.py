#Visión Computarizada: no es IA, sino análisis de datos gráficos, imágenes.
#Se usa la librería: openCV
import cv2

# img=cv2.imread("imagenes\simples\circulo_amarillo_sobre_rojo.png") #(path,0)para normalizar: almacenada en escala de grises
# print(img) #muestra los arrays que componen la imagen
# cv2.imshow("circulo amarillo",img) #muestra la imagen
# cv2.waitKey(2000) #click/press key to close
# cv2.destroyAllWindows() #cierra todas las ventanas
# img_inversa = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
# cv2.imshow("inversa", img_inversa)
# cv2.waitKey(2000) #click/press key to close

# cv2.imwrite("imagenes/concv2.png", img_inversa) #guarda la inversa en la carpeta imagenes

##############################################
# #usar la pc(la cámara de la pc) para capturar imagenes
# img_video = cv2.VideoCapture(0) #puerto del dispositivo (0, en windows es la webcam)
# img_video.set(cv2.CAP_PROP_FRAME_WIDTH,400)
# img_video.set(cv2.CAP_PROP_FRAME_HEIGHT,200)

# ret, frame = img_video.read()
# cv2.imshow("captura", frame)
# cv2.imwrite("micaptura.jpg", frame)
# cv2.waitKey(2000)
# cv2.destroyAllWindows()

# #La captura se puede poner en un bucle
# for i in range(5):
#     img_video = cv2.VideoCapture(0) #puerto del dispositivo (0, en windows es la webcam)
#     img_video.set(cv2.CAP_PROP_FRAME_WIDTH,400)
#     img_video.set(cv2.CAP_PROP_FRAME_HEIGHT,200)
#     ret, frame = img_video.read()
#     cv2.imshow("captura", frame)
#     cv2.imwrite(f"micaptura{i+1}.jpg", frame)
#     cv2.waitKey(5000) #cada 5 segundos toma una imagen
#     cv2.destroyAllWindows()

#normalizacion de imágenes
imagen = cv2.imread("imagenes/semaforo/1.png")
imagen_resized = cv2.resize(imagen, (200,600))
valor_GBR = print(imagen_resized[50,100])
imagen_rezised_splited_arriba = imagen_resized[0:200, 0:200] #altura, ancho
imagen_rezised_splited_medio = imagen_resized[200:400, 0:200]
imagen_rezised_splited_abajo = imagen_resized[400:600, 0:200]
cv2.imshow("original",imagen) #muestra la imagen
cv2.waitKey(3000) #click/press key to close
cv2.destroyAllWindows() #cierra todas las ventanas
cv2.imshow("reducida",imagen_resized) #muestra la imagen
cv2.waitKey(3000) #click/press key to close
cv2.destroyAllWindows() #cierra todas las ventanas
cv2.imshow("recorte arriba",imagen_rezised_splited_arriba) #muestra la imagen
cv2.waitKey(3000) #click/press key to close
cv2.destroyAllWindows() #cierra todas las ventanas
cv2.imshow("recorte medio",imagen_rezised_splited_medio) #muestra la imagen
cv2.waitKey(3000) #click/press key to close
cv2.destroyAllWindows() #cierra todas las ventanas
cv2.imshow("recorte abajo",imagen_rezised_splited_abajo) #muestra la imagen
cv2.waitKey(3000) #click/press key to close
cv2.destroyAllWindows() #cierra todas las ventanas

(b,g,r)=cv2.split(imagen_rezised_splited_arriba)
imagen_rezised_splited_arriba[(b==255)&(g==255)&(r==255)]=0,0,0 #vuelve lo blanco a negro
cv2.imshow("recorte arriba_sobre_negro",imagen_rezised_splited_arriba) #muestra la imagen
cv2.waitKey(2000) #click/press key to close
cv2.destroyAllWindows() #cierra todas las ventanas