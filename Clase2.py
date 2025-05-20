#Gráficos
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

#para graficar dos variables (x e y)
nba = pd.read_csv("nba.csv")
nba.rename(columns={"nombre":"jugador"})
x = nba.jugador
y = nba.puntos

#Plotea el gráfico
plt.bar(x,y) 
plt.show()

rnb = pd.read_csv("renabap.csv", encoding="ISO-8859-1")
#print(rnb.columns.tolist())
serv=rnb[['id_renabap', 'Barrio', 'Familias', 'Electricid', 'Agua', 'Cloaca']]
x = serv.Barrio
y = serv.Familias
plt.bar(x,y, color="yellow")
plt.title("Cantidad de Familias por Barrio (ReNaBaP)")
plt.xlabel("Barrio")
plt.ylabel("Cantidad de Familias")
# Rótulos del eje X en diagonal y con tamaño legible
plt.xticks(rotation=45, ha='right', fontsize=9)
plt.yticks(fontsize=10)
# Agregar cuadrícula horizontal suave
plt.grid(axis='y', linestyle='--', alpha=0.6)
# Ajuste automático de espacio
plt.tight_layout()
plt.show(block=True)

#Identificar duplicados
nba = pd.read_csv("nba.csv")
nba.rename(columns={"nombre":"jugador"}, inplace=True)
nba["jugador"] = np.where((nba.pos == 10), nba["jugador"].astype(str) + "1", nba["jugador"]) #<-- casi manual

# Versión chatGPT
df = pd.read_csv("nba.csv")
df["Etiqueta"] = df["Jugador"]
duplicados = df["Etiqueta"].duplicated(keep=False)
df.loc[duplicados, "Etiqueta"] = df.loc[duplicados].groupby("Etiqueta").cumcount().astype(str) + " - " + df.loc[duplicados, "Etiqueta"] 

x = nba.jugador
y = nba.puntos
plt.bar(x,y, color="green")
plt.title("Jugadores NBA - Puntaje")
plt.xlabel("Jugador")
plt.ylabel("Puntaje")
plt.xticks(rotation=0, fontsize=10, fontweight='bold', color='darkgreen')
plt.yticks(rotation=45, fontsize=12, color='darkgreen')

plt.tick_params(axis='x', pad=15)
plt.tick_params(axis='y', pad=20)

plt.tight_layout()
plt.show(block=True)