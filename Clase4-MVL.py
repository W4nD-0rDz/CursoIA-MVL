import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from PIL import Image, ImageDraw
from os import unlink
import numpy as np
import pandas as pd

####################################NORMALIZACION DE IMAGENES##########################################################################
#img almacena la matriz del contenido de cada pixel en RBG [0.0.0.] hasta [255.255.255]
#(en el caso de circulo_azul son 100 filas x 100 columnas) con
# img = mpimg.imread("imagenes/simples/circulo_azul.png")
# #Devuelve una matriz que contiene listas de RGB [1.1.1.] = color blanco
# # print(img)
# # plt.imshow(img)
# # plt.show()
# #Para obtener el tamaño de la imagen
# size = img.shape #Tupla: (100, 100, 3) (ancho, alto, canales)
# print("Tamaño de la imagen: ", size)

# img1 = mpimg.imread("imagenes/simples/circulo_gris128.png")
# img2 = mpimg.imread("imagenes/simples/circulo_gris64.png")
# sizeRGB = img1.shape #El len(tupla) es 3, está en RGB 
# sizeL = img2.shape #El len(tupla) es 2, está en escala de grises
# print("Tamaño de la imagen (alto, ancho, canales): ", sizeRGB)
# print("Tamaño de la imagen (alto, ancho, canales): ", sizeL)
########################################################################################################################################

#Para abrir varias imágenes en la misma figure = SUBPLOT
# filas = 2
# columnas = 3
# posicion = ""
# plt.subplot(filas, columnas, 1) #(filas, columnas, posicion)
# imgGrid1 = mpimg.imread("imagenes/simples/circulo_rojo.png")
# plt.imshow(imgGrid1)
# plt.axis('off') #borra los ejes de borde
# plt.subplot(filas, columnas, 2)
# imgGrid2 = mpimg.imread("imagenes/simples/circulo_azul.png")
# plt.imshow(imgGrid2)
# plt.axis('off')
# plt.subplot(filas, columnas, 3)
# imgGrid3 = mpimg.imread("imagenes/simples/circulo_amarillo.png")
# plt.imshow(imgGrid3)
# plt.axis('off')
# plt.subplot(filas, columnas, 4)
# imgGrid4 = mpimg.imread("imagenes/simples/circulo_violeta.png")
# plt.imshow(imgGrid4)
# plt.axis('off')
# plt.subplot(filas, columnas, 5)
# imgGrid5 = mpimg.imread("imagenes/simples/circulo_naranja.png")
# plt.imshow(imgGrid5)
# plt.axis('off')
# plt.subplot(filas, columnas, 6)
# imgGrid6 = mpimg.imread("imagenes/simples/circulo_verde.png")
# plt.imshow(imgGrid6)
# plt.axis('off')

# plt.tight_layout()
# plt.show()

##################################################################################################################
#Unlink borra rutas realmente de la PC (OJO!!!)
# color = str(input("Indique el color a borrar: ")).lower()

# #Con una excepción, por si el archivo no se encuentra:
# try:
#     unlink("imagenes/simples/"+color+".jpg")
#     print("Se ha eliminado ", color, "de la lista.")
# except FileNotFoundError:
#     print("Color no encontrado.")

####################################################################################################################
#Dataframe a matriz:
df = pd.read_csv("imagenes/argentina.csv")
print(df)
matriz= df.to_numpy().tolist()
print(matriz)


# def mostrarJugadores():
#     carpeta = "imagenes/fotos/"
#     filas,  columnas = 3, 4
#     archivos = [f for f in os.listdir(carpeta) if f.endswith(('.jpg', '.png', '.jpeg')) ]

#     fig, axes = plt.subplots(nrows=filas, ncols=columnas, figsize =(12,8))
#     axes = axes.flatten()

#     for i, archivo in enumerate(archivos):
#         if i >= filas * columnas:
#             break
#         # Abrir imagen con PIL y redimensionar
#         im_pil = Image.open(os.path.join(carpeta, archivo))
#         im_pil = im_pil.resize((100, 90))  # (ancho, alto)Cambiar por tamaño deseado
#         img = np.array(im_pil)
#         # Quitar la extensión del nombre del archivo
#         nombreSinExtension = os.path.splitext(archivo)[0]
#         # Mostrar imagenes
#         axes[i].imshow(img)
#         axes[i].text(0.5, -0.1, nombreSinExtension, 
#                     transform = axes[i].transAxes,
#                     fontsize = 8, ha = 'center')
#         axes[i].axis('off')

#         # Ocultar subplots vacíos
#         for j in range(i + 1, filas * columnas):
#             axes[j].axis('off')
#         plt.suptitle("Versión 2: imágenes equilibradas, sin deformación. subtítulos personalizados", fontsize=12)

#         plt.tight_layout()
#         plt.show()


########################################################################################################################################
#Python también puede crear el dibujo (en este caso muy simple)
# # 1. Crear imagen blanca de 100x100 píxeles
# img1 = Image.new("RGB", (100, 100), "white")
# # 2. Crear objeto para dibujar
# draw = ImageDraw.Draw(img1)
# # 3. Centro y radio del círculo
# cx, cy = 50, 50  # centro
# radio = 35
# # 4. Dibujar círculo azul lleno
# draw.ellipse((cx - radio, cy - radio, cx + radio, cy + radio), fill=(128, 128, 128))
# # 5. Guardar la imagen o mostrarla
# img1.save("imagenes/simples/circulo_gris.png")  # Guarda en disco
# #img1.show()  # Muestra en una ventana (opcional)
# plt.imshow(img1)
# plt.show()
#Ahora un circulo negro sobre fondo blanco y otro a la inversa
# img2 = Image.new("RGB", (100, 100), "white")
# draw = ImageDraw.Draw(img2)
# draw.ellipse((cx - radio, cy - radio, cx + radio, cy + radio), fill=(0, 0, 0))
# img2.save("imagenes/simples/circulo_negro.png")
# plt.imshow(img2)
# plt.show()
# # # # # # # # # # # # # # # # # # # # # # # #
# img3 = Image.new("RGB", (100, 100), "black")
# draw = ImageDraw.Draw(img3)
# draw.ellipse((cx - radio, cy - radio, cx + radio, cy + radio), fill=(255, 255, 255))
# img3.save("imagenes/simples/circulo_blanco.png")
# plt.imshow(img3)
# plt.show()
# # # # # # # # # # # # # # # # # # # # # # # #
# Ahora una en modo L (escala de grises, no RGB)
# img = Image.new("L", (100, 100), 255)  # Fondo blanco
# draw = ImageDraw.Draw(img)
# draw.ellipse((cx - radio, cy - radio, cx + radio, cy + radio), fill=64)
# img.save("imagenes/simples/circulo_gris64.png")
########################################################################################################################################

#Bucle ver_todos()
# def ver_todos()
#     posicion=1
#     for i in lista:
#         plt.subplot(2,6,posicion)
#         img=npimg.read("fotos/"+i[2]+ " " + i[1]+ ".jpg")
#         plt.imshow(img)
#         plt.axis("off")
#         posicion =+1
#         if i[0]==11:
#             break
#     plt.show()
#     menu()

