#Calculadora de interés compuesto
import math
print("Bienvenido a calculadora de interés")
capital_inicial = float(input("Indica el monto a invertir: $"))
tna = tna = float(input("Indica la TNA informada por el banco (en porcentaje): ").replace(",", "."))

dias = int(input("Indica la cantidad de días que deseas invertir: "))
if capital_inicial <= 0 or tna <= 0 or dias <= 0:
    print("Por favor, ingresa valores positivos y mayores a cero.")
else:
    tasa_diaria = (tna / 100) / 365
    monto_final = capital_inicial * math.pow(1 + tasa_diaria, dias)
    interes = monto_final - capital_inicial

print(f"Monto final: ${monto_final:.2f}")
print(f"Interés ganado: ${interes:.2f}")