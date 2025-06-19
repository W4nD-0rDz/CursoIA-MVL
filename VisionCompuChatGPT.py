import cv2 #Librería para imágenes
import ezdxf #Librería para imágenes vectoriales

# 1. Cargar la imagen
img = cv2.imread("imagenes/transporte/calle.jpg")
assert img is not None, "No se pudo cargar calle.jpg"

# 2. Mostrar la imagen original
cv2.imshow("Original", img)

# 3. Pasar a escala de grises
gris = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
cv2.imshow("Gris", gris)

# 4. Aplicar detección de bordes (Canny)
edges = cv2.Canny(gris, threshold1=100, threshold2=200)
cv2.imshow("Bordes (Canny)", edges)

# 5. Encontrar contornos
contornos, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
print(f"Encontrados {len(contornos)} contornos")
contorno_img = img.copy()
cv2.drawContours(contorno_img, contornos, -1, (0, 255, 0), 2)
cv2.imshow("Contornos", contorno_img)

# 6. Redimensionar
resize = cv2.resize(img, (img.shape[1]//2, img.shape[0]//2))
cv2.imshow("Redimensionada", resize)

# 7. Guardar resultado
cv2.imwrite("urban_gray.jpg", gris)
cv2.waitKey(0)
cv2.destroyAllWindows()

############################################Dibujar vectores SVG
# 8 Dimensiones de la imagen
height, width = img.shape[:2]

# 11.a Crear archivo SVG
with open("contornos.svg", "w") as f:
    f.write(f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}">\n')
    
    # Dibujar cada contorno como una "polyline"
    for cnt in contornos:
        puntos = " ".join(f"{pt[0][0]},{pt[0][1]}" for pt in cnt)
        f.write(f'  <polyline points="{puntos}" stroke="black" fill="none" stroke-width="1"/>\n')
    
    f.write('</svg>\n')
print("SVG generado: contornos.svg")


############################################Dibujar vectores DXF
# 9 Detectar contornos
contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
print(f"Contornos encontrados: {len(contours)}")

# 10 Crear un archivo DXF
doc = ezdxf.new()
msp = doc.modelspace()

# 11 Dibujar contornos en el modelo
for cnt in contours:
    points = [(int(p[0][0]), int(p[0][1])) for p in cnt]
    if len(points) > 2:
        msp.add_lwpolyline(points, close=True)

# 12 Guardar como DXF
doc.saveas("contornos.dxf")
print("Archivo DXF guardado: contornos.dxf")