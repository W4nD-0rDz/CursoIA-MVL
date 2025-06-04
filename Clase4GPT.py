#Imágenes
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import os
from PIL import Image, ImageFilter
import numpy as np

# #Tratar imagen como variable
# img = mpimg.imread("imagenes/fotos/angel di maria.jpg")
# plt.imshow(img)
# # plt.show()
# #Mostrar sus dimensiones
# print(img.shape)


# #Mostrar varias imágenes juntas
# carpeta = "imagenes/fotos/"
# archivos = [f for f in os.listdir(carpeta) if f.endswith(('.jpg', '.png', '.jpeg')) ]
# archivo = "leonel messi.jpg"
# # filas = 3
# # columnas = 4
# filas,  columnas = 3, 4

# Versión base
# fig0, axes0 = plt.subplots(nrows=filas, ncols=columnas, figsize =(12,8))
# axes0 = axes0.flatten()
# for i, archivo in enumerate(archivos):
#     if i>= filas * columnas:
#         break
#     img = mpimg.imread(os.path.join(carpeta, archivo))
#     axes0[i]. imshow(img)
#     axes0[i].set_title(archivo, fontsize=8)
#     axes0[i].axis('off')
#     #Mostrar sus dimensiones
#     print(img.shape)
# # Ocultar subplots vacíos
# for j in range(i + 1, filas * columnas):
#     axes0[j].axis('off')
# plt.suptitle("Versión 0: sin configuraciones", fontsize=12)

# Versión primera corrección
# fig1, axes1 = plt.subplots(nrows=filas, ncols=columnas, figsize =(12,8))
# axes1 = axes1.flatten()
# for i, archivo in enumerate(archivos):
#     if i>= filas * columnas:
#         break
#     img = mpimg.imread(os.path.join(carpeta, archivo))
#     axes1[i]. imshow(img)
#     axes1[i].imshow(img, aspect='auto') #estira/comprime para evitar tamaños desparejos (deforma)
#     axes1[i].set_title(archivo, fontsize=8)
#     axes1[i].axis('off')
# # Ocultar subplots vacíos
# for j in range(i + 1, filas * columnas):
#     axes1[j].axis('off')
# plt.suptitle("Versión 1: imágenes deformadas, grilla equilibrada", fontsize=12)


# Versión 2: mejora con resize (mantiene proporciones)
# fig2, axes2 = plt.subplots(nrows=filas, ncols=columnas, figsize =(12,8))
# axes2 = axes2.flatten()

# for i, archivo in enumerate(archivos):
#     if i >= filas * columnas:
#         break
#     # Abrir imagen con PIL y redimensionar
#     im_pil = Image.open(os.path.join(carpeta, archivo))
#     im_pil = im_pil.resize((100, 90))  # (ancho, alto)Cambiar por tamaño deseado
#     img = np.array(im_pil)
#     # Quitar la extensión del nombre del archivo
#     nombreSinExtension = os.path.splitext(archivo)[0]
#     # Mostrar imagenes
#     axes2[i].imshow(img)
#     axes2[i].text(0.5, -0.1, nombreSinExtension, 
#                  transform = axes2[i].transAxes,
#                  fontsize = 8, ha = 'center')
#     axes2[i].axis('off')

# # Ocultar subplots vacíos
# for j in range(i + 1, filas * columnas):
#     axes2[j].axis('off')
# plt.suptitle("Versión 2: imágenes equilibradas, sin deformación. subtítulos personalizados", fontsize=12)

# plt.tight_layout()
# plt.show()

###################################################################################################################################################

#Los archivos están en formatos diferentes en tamaño y en cant de canales RGB (una de las fotos no tiene)
#Conviene tratar las imágenes con PIL para usar estos métodos:
#Fuerza la imagen a tener 3 canales (R, G, B), aunque sea blanco y negro.
# img2 = Image.open(os.path.join(carpeta, archivo)).convert("RGB")
# #Redimensiona
# img2 = img2.resize((300, 300))
# #Gira
# img2.rotate(45)
# #Filtros
# img2.filter(ImageFilter.SHARPEN) #también BLUR, GaussianBlur(radius=X), EDGE_ENHANCE_MORE, EMBOSS, FIND_EDGES, SMOOTH, SMOOTH_MORE, UnsharpMask(...)
# img2.show()

#Cortar la imagen, Usando PIL.image
#Se cuenta en pixels desde la esquina sup izq (0,0)
#por ejemplo si tenemos una imagen de 1039 x 600 (Leandro Paredes)
# img3 = Image.open("imagenes/fotos/leandro paredes.jpg")
# width, height = img3.size
# left = 100
# top = 0
# right = 500
# bottom = 300
# recortada = img3.crop((left, top, right, bottom))
# recortada.show()

################################################################################################################################







