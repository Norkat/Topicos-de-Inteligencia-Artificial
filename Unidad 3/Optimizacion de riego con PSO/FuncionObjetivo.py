import numpy as np
import math
from itertools import combinations

# Metodo para calcular la distancia en metros entre dos coordenadas
# Parmetros de entrada:
# punto_1: Coordenadas del punto 1
# punto_2: Coordenadas del punto 2
# Retorna:
# La distancia en metros entre las dos coordenadas.
def distancia_haversine(punto_1, punto_2):
    RADIO_TIERRA = 6371000.0

    # 1. Convertir grados a radianes
    phi1 = math.radians(punto_1[0])
    lambda1 = math.radians(punto_1[1])
    phi2 = math.radians(punto_2[0])
    lambda2 = math.radians(punto_2[1])

    # 2. Diferencias
    dlon = lambda2 - lambda1
    dlat = phi2 - phi1

    # 3. Aplicar Fórmula de Haversine
    # a = sin²(Δφ/2) + cos(φ1) * cos(φ2) * sin²(Δλ/2)
    a = math.sin(dlat / 2)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlon / 2)**2
    
    # c = 2 * atan2(√a, √(1−a))
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    # 4. Distancia = R * c
    distancia_m = RADIO_TIERRA * c
    
    return distancia_m

# Metodo para calcular la humedad representativa que podria detecar un sensor
# Parametros de entrada:
# sensor: El sensor al cual se le esta calculando su humedad representativa
# puntos: Los puntos de cultivo (unicamente las coordenadas)
# humedades: Las humedades de cada uno de los puntos de cultivo
# p: Parametro de IDW (2 por defecto)
# Retorna:
# h: la humedad representativa de la funcion en porcentaje (valores de 0 a 1)
# Funcionamiento de la funcion
# Calculamos la distancia entre todos los puntos y el sensor y lo guardamos
#   en dist
# Se tomara como la humedad del sensor la humeda del punto mas ceranco.
def humedad_sensor(sensor, puntos, humedades, p=2):
    dist = []
    for punto in puntos:
        dist.append(distancia_haversine(punto, sensor))
    
    dist = np.array(dist)

    idx = np.argmin(dist)
    h = humedades[idx]
    return h

# Metodo para calcular la humedad estimada de los puntos de cultivo, por cada
#   punto de cultivo
# Parametros de Entrada:
# puntos: Coordenadas de todos los puntos de cultivo
# sensores: Coordenadas de todos los sensores
# h_sensores: Humedad representativa de cada sensor
# p: Parametro de IDW (2 por defecto)
# Retorna:
# h_estim: La humedad estimada de cada punto que los sensores
# obtendrian
# Funcionameiento de la funcion:
# 
# Por cada punto de cultivo se calcula su humedad estimada con la siguiente
#   formula:
#   h_j: (∑ w_i * hS_i) / (∑ w_i)
#   Donde el peso (w_i) es: w_i = 1 / d_i^p
#   d_i: distancia entre el sensor i y el punto j
#   hS_i: humedad del sesnor i
def humedad_estimada(puntos, sensores, h_sensores, p=2):
    N = len(puntos)
    h_estim = np.zeros(N)
    for i in range(N):
        dist = []
        for sensor in sensores:
            dist.append(distancia_haversine(puntos[i], sensor))
        
        dist = np.array(dist)
        dist = np.maximum(dist, 1e-6)  # evitar división por 0
        pesos = 1 / (dist ** p)
        h_estim[i] = np.sum(h_sensores * pesos) / np.sum(pesos)
    return h_estim

# Metodo que alcula los pesos de importancia demlos puntos de cultivo.
# Parametros de entrada:
# cultivos: Arreglo que indica el tipo de cultivo por punto.
#   (Puede ser maiz, tomate o chile)
# salinidad: Arreglo que indica la salinidad por punto, ya normalizada.
# temperatura: Arreglo que indica la temperatura de cada punto, ya normalizada.
# elevacion: Arreglo que indica la elevacion de cada punto, ya normalizada.
# peso_cultivo: Mapa donde se le asigna a cada cultivo, un peso para medir
#   su importancia
# alphas: Pesos relativos para la salinidad, temperatura y elevacion
#   respectivamente. Por defecto son (0.3, 0.2, 0.15)
# clip_range: Limite de los pesos finales. Por defecto son (0.5, 4.0)
# Retorna:
#   Un arreglo w, que tiene el peso de cada punto de cultivo
# Funcionamiento del metodo
# Los pesos de cada cultivo se calculan con la siguiente formula:
# w_i = w_cult * (1 + a1 * S_i + a2 * T_i + a3 * E_i)
#   w_i: peso del punto de cultivo i
#   w_cult: peso del tipo de cultivo del punto i
#   (a1, a2, a3): alphas sacadas del arreglo de entrada
#   S_i: salinidad del punto de cultivo i
#   T_i: temperatura del punto de cultivo i
#   E_i: elevacion del punto de cultivo i
# Luego se hace clipping a los pesos
def pesos_puntos_cultivos(cultivos,
                          salinidad,
                          temperatura,
                          elevacion,
                          peso_cultivo=None,
                          alphas=(0.3, 0.2, 0.15),
                          clip_range=(0.5, 4.0)):
    # Default mapping si no se pasa
    if peso_cultivo is None:
        peso_cultivo = {'Tomate': 2.0, 'Chile': 1.5, 'Maíz': 1.0}

    # Peso base por cultivo
    w_cult = np.array([peso_cultivo.get(c, 1.0) for c in cultivos])

    # Aplicar fórmula del peso
    a1, a2, a3 = alphas
    w = w_cult * (1.0 + a1 * salinidad + a2 * temperatura + a3 * elevacion)

    # Clipping
    w = np.clip(w, clip_range[0], clip_range[1])
    return w

# Metodo que calcula el error ponderado de la humedad.
# Parametros de Entrada:
# h_real: Humedad de los puntos de cultivo
# h_estim: Humedad estimada de cada punto por los sensores
# w: Peso de importancia de cada punto de cutivo
# Retorna:
    # En tipo float, el error ponderado de la humedad
# Funcionamiento del metodo:
# Se calcula con la siguiente formula:
#   E = √((∑ w_i * (h_r_i - h_e_i)^2) / (∑ w_i))
#   w_i: Peso del punto de cultivo i
#   h_r_i: Humedad real del punto de cultivo i
#   h_e_i: Humedad estimada del punto de cultivo i
def rmse_ponderado(h_real, h_estim, w):
    num = np.sum(w * (h_real - h_estim)**2)
    den = np.sum(w)
    return np.sqrt(num / den)

# Metodo que calcula la funcion objetivo dado los datos de entrad
#   y la posicion de los sensores
# Parametros de entrada
# sensores: Coordenadas donde estan posicionados los sensores
# datos: Datos sobre los puntos de cultivos, este debe de incluir
#   los siguientes arreglos de datos:
#   puntos: Coordenadas de los puntos de cultivo
#   cultivos: Tipo de cultivo presente en cada punto
#   humedades: Humedad en porcentaje (0 - 100) de cada punto
#   salinidades: Salinidad normalizada de cada punto (0 - 1)
#   temperaturas: Temperatura normalizada de cada punto (0 - 1)
#   elevaciones: Elevacion noramlizadad de cada punto (0 - 1)
# Retorna:
# El valor que representa que tan buena es la funcion: el error
#   interpretado de la humedad, entre menor sea el error mejor
#   es la solución
def funcion_objetivo(sensores, datos):

    (puntos, cultivos, humedades, salinidades, temperaturas, elevaciones) = datos

    h_sensores = np.array([humedad_sensor(s, puntos, humedades)
                           for s in sensores])
    h_estimadas = humedad_estimada(puntos, sensores, h_sensores)
    w = pesos_puntos_cultivos(cultivos, salinidades, temperaturas, elevaciones)

    error_interp = rmse_ponderado(humedades, h_estimadas, w)

    return error_interp

