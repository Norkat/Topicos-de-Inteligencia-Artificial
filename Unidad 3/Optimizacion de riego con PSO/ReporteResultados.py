import matplotlib.pyplot as plt
import numpy as np
import PSO

# Metodo que obtiene los datos resultantes de correr el algoritmo PSO
# Parametros de entrada:
# n_particulas: Numero de particulas que tendra el enjambre
# n_sensores: Numero de sensores que obtendra la solucion
# limites: limites minimos y maximos de coordenadas donde podran estar 
#   posicionados los sensores. Tiene el formato: [[min_lat, min_lon], [max_lat, max_lon]]
# f_objetivo: funcion objetivo con lo que se evaluara las soluciones
# max_iter: Numero maximo de iteraciones que correra el PSO
# datos: Datos extra necesarios para ejecutar la funcion objetivo
# Retorna:
# gbest: La mejor solucion encontrada, la mejor manera de posicionar
#   los sensores
# gbest_value: Valor que representa la mejor solucion
# valor_iteracion: Arreglo donde se guarda el mejor valor global
#   por cada iteracion
def reporte(n_particulas, n_sensores, limites, f_objetivo, max_iter, datos):
    pso = PSO.PSO(n_particulas, n_sensores, limites, f_objetivo)

    gbest, gbest_value, valor_iteracion = pso.optimizar(max_iter, datos)

    return gbest, gbest_value, valor_iteracion

# Metodo que muestra los resultados obtenidos al correr el algoritmo PSO
#   por consola
# Parametros de entrada:
# n_particulas: Numero de particulas que tendra el enjambre
# n_sensores: Numero de sensores que obtendra la solucion
# limites: limites minimos y maximos de coordenadas donde podran estar 
#   posicionados los sensores. Tiene el formato: [[min_lat, min_lon], [max_lat, max_lon]]
# f_objetivo: funcion objetivo con lo que se evaluara las soluciones
# max_iter: Numero maximo de iteraciones que correra el PSO
# datos: Datos extra necesarios para ejecutar la funcion objetivo
def reporte_consola(n_particulas, n_sensores, limites, f_objetivo, max_iter, datos):

    gbest, gbest_value, valor_iteracion = reporte(n_particulas, n_sensores, limites, f_objetivo, max_iter, datos)

    # Parámetros iniciales
    print("### Valores INICIALES ###")
    print(f"Número de partículas (soluciones): {n_particulas}")
    print(f"Número de sensores a optimizar:   {n_sensores}")
    print(f"Número máximo de iteraciones:    {max_iter}")
    print("-" * 50)
    
    # Resultados finales
    print("### RESULTADOS FINALES ###")
    print(f"Mejor valor encontrado (gbest_value): {gbest_value}")
    print(f"Mejor posición encontrada (gbest):\n{gbest}")
    print("-" * 50)

    print("### HISTORIAL DE CONVERGENCIA ###")
    print(f"{valor_iteracion}")

# Metodo que muestra los resultados obtenidos al correr el algoritmo PSO
#   de forma grafica / visual.
# Parametros de entrada:
# n_particulas: Numero de particulas que tendra el enjambre
# n_sensores: Numero de sensores que obtendra la solucion
# limites: limites minimos y maximos de coordenadas donde podran estar 
#   posicionados los sensores. Tiene el formato: [[min_lat, min_lon], [max_lat, max_lon]]
# f_objetivo: funcion objetivo con lo que se evaluara las soluciones
# max_iter: Numero maximo de iteraciones que correra el PSO
# datos: Datos extra necesarios para ejecutar la funcion objetivo
def reporte_visual(n_particulas, n_sensores, limites, f_objetivo, max_iter, datos):

    (puntos, cultivos, _, _, _, _) = datos

    gbest, gbest_value, valor_iteracion = reporte(n_particulas, n_sensores, limites, f_objetivo, max_iter, datos)

    # --- GRÁFICA 1: CONVERGENCIA DEL ALGORITMO (valor_iteracion) ---
    plt.figure(figsize=(10, 6))
    if valor_iteracion is not None and len(valor_iteracion) > 0:
        plt.plot(range(1, len(valor_iteracion) + 1), valor_iteracion, marker='o', linestyle='-', color='blue')
        plt.title('Convergencia del Mejor Valor Global por Iteración')
        plt.xlabel('Número de Iteración')
        plt.ylabel('Mejor Valor Global (gbest_value)')
        plt.grid(True)
        plt.minorticks_on()
        plt.grid(which='major', linestyle='-', linewidth='0.5', color='gray')
        plt.grid(which='minor', linestyle=':', linewidth='0.5', color='gray')
    else:
        plt.text(0.5, 0.5, "No hay datos de historial de iteración disponibles.", horizontalalignment='center', verticalalignment='center', transform=plt.gca().transAxes)
        plt.title('Convergencia del Mejor Valor Global')
    plt.show()

    # --- GRÁFICA 2: PUNTOS DE MUESTREO Y SENSORES ÓPTIMOS ---
    plt.figure(figsize=(12, 8))

    # Graficar los sensores óptimos (gbest)
    # gbest contendrá las coordenadas [lat, lon] de los sensores
    plt.scatter(gbest[:, 1], gbest[:, 0], # Longitud en X, Latitud en Y
                marker='X', 
                color='red', 
                s=200,
                edgecolors='black', 
                label='Sensores Óptimos')

    # Definir colores para los cultivos
    colores_cultivos = {}
    cultivos_unicos = np.unique(cultivos)
    cmap = plt.cm.get_cmap('tab10', len(cultivos_unicos))
    for i, c_name in enumerate(cultivos_unicos):
        colores_cultivos[c_name] = cmap(i)

    # Graficar los puntos de muestreo por tipo de cultivo
    for c_name in cultivos_unicos:
        idx = (cultivos == c_name)
        plt.scatter(puntos[idx, 1], puntos[idx, 0], 
                    color=colores_cultivos[c_name], 
                    label=f'Cultivo: {c_name}', 
                    alpha=0.6, s=50)
        
    # Creamos la cadena de texto a mostrar
    texto_solucion = f"Mejor Valor (Fitness): {gbest_value:.4f}"

    # Configuración del gráfico
    plt.title('Distribución de Puntos de Muestreo y Posición Óptima de Sensores. ' + texto_solucion)
    plt.xlabel('Longitud')
    plt.ylabel('Latitud')
    plt.grid(True)
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.minorticks_on()
    plt.grid(which='major', linestyle='-', linewidth='0.5', color='gray')
    plt.grid(which='minor', linestyle=':', linewidth='0.5', color='gray')
    plt.tight_layout()
    plt.show()