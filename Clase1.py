import statistics as st
import pandas as pd
import tabulate
import chardet

"""
#Listas = dataset
numeros=[2,20,4,18,6,16,8,14,10,12]
nombres=["juan", "alberto","pedro","josé", "mario", "alberto"]

#Media: valor promedio
total=0

for numero in numeros:
    total += numero

cantidad = len(numeros)
print("total",  total)
print("cantidad", cantidad)
print("la media es de" , total/cantidad)
media = st.mean(numeros)
print("la media según statistics es", media)

#valor del dato ubicado en la posición central de un conjunto de datos
posmedia=round(len(numeros)/2)
print("la posición media es ", posmedia)
print("el valor en el medio no ordenado es", numeros[posmedia])
mediana = st.median(numeros)
print("la mediana según statistics es", mediana)

#Moda: valor más repetido en el dataset
moda = st.mode(nombres)
print("la moda de los nombres es", moda)
"""
#Archivos csv contiene los datos en filas (con salto de línea) y 
#cada columna separada por (, ; . o lo que se defina)
"""df=pd.read_csv("nba.csv")
#imprime todo el archivo
print("Con la impresión directa del archivo")
print(df)"""
#muestra todos los campos por columna, una a continuación de otra
"""print("Con bucle FOR básico, muestra cada columna con su contenido,\n nombre de columna y tipo de datos")
for i in df:
    print(df[i])"""
"""
print("Con ciclo FOR con iterrows")
for index, row in df.iterrows():
    print("Nombre:", row["nombre"], "Puntos:", row["puntos"])

print("Muestra solo la posición y el nombre del jugador")
for i, row in df.iterrows():
    print(row["pos"], (row["nombre"].upper()))
"""
#imprime las primeras 5 filas del archivo
"""print("Muestra las primeras 5 filas")
print(df.head())"""
#imprime la cantidad de registros
"""print("Muestra una cantidad determinada de filas (en este caso 2)")
print(df.head(2))"""
# Modifica los nombres de vista de las columnas (no el archivo)
"""df=df.rename(columns={"pos":"N°", "nombre":"Jugador", "puntos":"Puntaje"})
print(df)"""
# Ver datos del archivo:
"""df.info()
print(df.dtypes)"""
#Muestra partes del archivo

# Abrimos una parte del archivo en modo binario
"""with open("renabap.csv", "rb") as file:
    resultado = chardet.detect(file.read(5000))  # lee los primeros 5000 bytes
print("Codificación detectada:", resultado["encoding"])
"""
renabap = pd.read_csv("renabap.csv", encoding="ISO-8859-1")

"""print("Barrios del RENABAP en la Ciudad de Buenos Aires")
print(renabap.Barrio)
print("")
cantidadFamilias=0
for i in renabap.Familias:
    cantidadFamilias += i
print("Cantidad de Familias en Barrios Populares CABA: ", cantidadFamilias, ".")
print("")

print("Barrios de la CABA, que contiene barrios registrados en el ReNaBaP")
print(renabap.Localidad.unique())"""

#imprime según cumple una condición
"""mediaFamilias = st.mean(renabap.Familias)
print("Barrios (por ID) que superan la media de familias")
print(renabap[renabap.Familias > mediaFamilias][["id_renabap", "Barrio", "Familias"]].to_markdown(index=False))"""

"""filtro = renabap["Familias"] > mediaFamilias
resultado = renabap[filtro][["id_renabap", "Barrio", "Familias"]]
print("Barrios que superan la media de familias")
print(resultado)"""

#Eliminar un campo
renabapSinIndex = renabap.drop("fid", axis=1)
print(renabapSinIndex)
#Eliminar un campo según condición
renabapCabaSinComuna1 = renabap[renabap.Departamen != "Comuna 1"]
renabapCabaComuna1 = renabap[renabap.Departamen == "Comuna 1"]
print(renabapCabaComuna1[["id_renabap", "Barrio", "Familias"]].to_markdown(index=False))
#Seleccionar ciertos campos
"""renabapSoloServicios = renabap[["id_renabap", "Barrio", "Familias", "Electricidad", "Agua", "Cloacas"]]
for row in renabapSoloServicios.iterrows():
    print(renabap[row])"""
#Renombrar un campo
"""renabap = renabap.rename(columns={"A�o de Cr": "Fecha de Cr"})
renabap.to_csv("renabap.csv", index=False)"""

