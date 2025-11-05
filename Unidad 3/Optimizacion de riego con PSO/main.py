import numpy as np
import LecturaCSV
import ReporteResultados
import FuncionObjetivo

# Metodo que genera un reporte del PSO con datos extraidos de una archivo csv
# Parametros de entrada:
# nombre_csv: nombre del archivo csv
# n_sensores: Numero de sensores que contendra la solucion
def caso_csv(nombre_csv, n_sensores = 10):
    # Extraer los datos
    humedades, cultivos, elevaciones, salinidades, temperaturas, puntos = LecturaCSV.leer_archivo(nombre_csv)

    # Imprimir los primeros 5 de cada uno (verificar que se leyeron bien)
    print(humedades[:5])
    print(cultivos[:5])
    print(elevaciones[:5])
    print(salinidades[:5])
    print(temperaturas[:5])
    print(puntos[:5])

    datos = (puntos, cultivos, humedades, salinidades, temperaturas, elevaciones)

    # Encontrar los Mínimos de puntos
    minimos = np.min(puntos, axis=0)
    latitud_min = minimos[0]
    longitud_min = minimos[1]

    # Encontrar los Máximos de puntos
    maximos = np.max(puntos, axis=0)
    latitud_max = maximos[0]
    longitud_max = maximos[1]

    # Generar reporte
    ReporteResultados.reporte_visual(100, 
                                     n_sensores, 
                                     [[latitud_min, longitud_min], [latitud_max, longitud_max]], 
                                     FuncionObjetivo.funcion_objetivo, 
                                     250,
                                     datos)

# Metodo que genera un reporte del PSO con datos generados de forma aleatoria
# Parametros de entrada:
# n_puntos: Cantidad de puntos de cultivos a generar de forma aleatoria
# n_particulas: Cantidad de particulas a usar en el algoritmo PSO
# n_sensores: Numero de sensores que contendra la solucion
# max_iter: Cantidad maxima de iteraciones que hara el algoritmo PSO
def caso_random(n_puntos, n_particulas, n_sensores, max_iter):

    # Rango de Latitud
    lat_min, lat_max = 25.40, 25.80
    # Rango de Longitud
    lon_min, lon_max = -108.70, -108.30

    # Generar latitudes y longitudes por separado y luego combinarlas
    latitudes = np.random.uniform(lat_min, lat_max, n_puntos)
    longitudes = np.random.uniform(lon_min, lon_max, n_puntos)
    
    # Combinar en la forma [[lat, lon], ...]
    puntos = np.stack((latitudes, longitudes), axis=1)
    
    # Humedades: Porcentajes de 0 a 100
    humedades = np.random.uniform(0.0, 100.0, n_puntos)

    # Salinidades, Temperaturas, Elevaciones: Valores de 0 a 1 (normalizados)
    salinidades = np.random.rand(n_puntos)
    temperaturas = np.random.rand(n_puntos)
    elevaciones = np.random.rand(n_puntos)
    
    # Generación de Cultivos
    opciones_cultivos = np.array(['Tomate', 'Chile', 'Maíz'])
    
    cultivos = np.random.choice(opciones_cultivos, size=n_puntos)

    datos = (puntos, cultivos, humedades, salinidades, temperaturas, elevaciones)

    # Generar reporte
    ReporteResultados.reporte_visual(n_particulas, 
                                     n_sensores, 
                                     [[lat_min, lon_min], [lat_max, lon_max]], 
                                     FuncionObjetivo.funcion_objetivo, 
                                     max_iter,
                                     datos)

# Ejecutador del programa
# Caso principal con datos cultivos.csv
# En caso de querer probar otro descomentarlo y comentar el anterior
if __name__ == "__main__":
    # Primer caso, datos cultivos.csv
    caso_csv("data/cultivos.csv")

    # Segundo caso, datos cultivos2.csv
    #caso_csv("data/cultivos2.csv")

    # Tercer caso, problema reducido con datos random
    # caso_random(50, 100, 5, 120)