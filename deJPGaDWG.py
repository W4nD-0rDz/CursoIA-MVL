import cv2 #Librería para imágenes
import ezdxf #Librería para imágenes vectoriales

# 1. Cargar imagen (usa la que elijas)
img = cv2.imread("imagenes/transporte/barrio.jpg")
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
edges = cv2.Canny(gray, 100, 200)

# 2. Detectar contornos
contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
print(f"Contornos encontrados: {len(contours)}")

# 3. Crear un archivo DXF
doc = ezdxf.new()
msp = doc.modelspace()

# 4. Convertir contornos a polilíneas en el DXF
scale_factor = 0.1  # escala píxel → unidad CAD
for cnt in contours:
    pts = [(p[0][0] * scale_factor, p[0][1] * scale_factor) for p in cnt]
    if len(pts) > 2:
        msp.add_lwpolyline(pts, close=True)

# 5. Guardar DXF
doc.saveas("barrio_contornos.dxf")
print("Archivo DXF guardado: contornos.dxf")

