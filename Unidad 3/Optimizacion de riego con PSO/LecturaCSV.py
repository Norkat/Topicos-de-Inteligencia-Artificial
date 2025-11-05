import pandas as pd
import numpy as np

# Metodo que lee un csv para obtener toda la informacion inicial requerida
# Parametros de entrada:
# nombre_archivo: nombre del archivo csv a leer
# normalizar: Valor booleano que nos indica si se van a normalizar
# alguno de los datos proporciondos
# Retorna:
# puntos: Coordenadas de los puntos de cultivo
# cultivos: Tipo de cultivo presente en cada punto
# humedades: Humedad en porcentaje (0 - 100) de cada punto
# salinidades: Salinidad normalizada de cada punto (0 - 1)
#   En caso de no estar normalizada se devuelve con la unidad dS/m
# temperaturas: Temperatura normalizada de cada punto (0 - 1)
#   En caso de no estar normalizada se devuelve con la unidad C°
# elevaciones: Elevacion noramlizadad de cada punto (0 - 1)
#   En caso de no estar normalizada se devuelve con la unidad metros (m)
def leer_archivo(nombre_archivo, normalizar = True):
    puntos_cultivo = pd.read_csv(nombre_archivo)
    humedades = puntos_cultivo.iloc[:, 0].values.astype(float)
    cultivos = puntos_cultivo.iloc[:, 1].values.astype(str)
    elevaciones = puntos_cultivo.iloc[:, 2].values.astype(float)
    salinidades = puntos_cultivo.iloc[:, 3].values.astype(float)
    temperaturas = puntos_cultivo.iloc[:, 4].values.astype(float)
    puntos = puntos_cultivo.iloc[:, 5:7].values.astype(float)

    if normalizar:
        elevaciones = normalizar_arreglo(elevaciones)
        salinidades = normalizar_arreglo(salinidades)
        temperaturas = normalizar_arreglo(temperaturas)

    return humedades, cultivos, elevaciones, salinidades, temperaturas, puntos

# Metodo que normaliza un arreglo
# Parametros de entrada:
# arr: El arreglo a normalizar
# Retorna:
# arr_normalizado: El arreglo normalizado
# Funcionamiento del metodo
# Del arreglo proporcionado toma el menor y el mayor elemento
# Con ello se aplica la formula de normalización Min-Max:
#   (x - x_min) / (x_max - x_min)
# En caso de que el menor y mayor elemento sean iguales, significa
#   que todos los elementos son iguales, por lo que en ese caso
#   retornamos como arreglo normalizado un arreglo lleno de ceros.
def normalizar_arreglo(arr):
    lo, hi = arr.min(), arr.max()

    if hi - lo == 0:
        return np.zeros_like(arr)

    arr_normalizado = (arr - lo) / (hi - lo)
    
    return arr_normalizado