# Librerías necesarias:
import random
import numpy as np
import pandas as pd
import operator
import matplotlib.pyplot as plt 

# -------------------------------------------------------------------
#               Definición de Clases Principales
# -------------------------------------------------------------------

class municipio:
    """
    Representa una entidad 'municipio' (o ciudad) con coordenadas 2D.
    Almacena las coordenadas 'x' e 'y' y calcula distancias.
    """
    def __init__(self, x, y):
        """
        Inicializa un nuevo municipio.
        
        @param x: Coordenada X del municipio.
        @param y: Coordenada Y del municipio.
        """
        self.x = x
        self.y = y
    
    def distancia(self, municipio):
        """
        Calcula la distancia Euclidiana (Teorema de Pitágoras) entre
        este municipio y otro.
        
        @param municipio: El objeto municipio al cual se calculará la distancia.
        @return: La distancia (float) entre los dos municipios.
        """
        xDis = abs(self.x - municipio.x)
        yDis = abs(self.y - municipio.y)
        distancia = np.sqrt((xDis ** 2) + (yDis ** 2))
        return distancia

    def __repr__(self):
        """
        Define la representación oficial en string del objeto.
        
        @return: Un string formateado con las coordenadas "(x,y)".
        """
        return "(" + str(self.x) + "," + str(self.y) + ")"


class Aptitud:
    """
    Calcula la aptitud (fitness) de una ruta (individuo).
    La aptitud es inversamente proporcional a la distancia total de la ruta.
    """
    def __init__(self, ruta):
        """
        Inicializa el objeto de aptitud para una ruta específica.
        
        @param ruta: Una lista de objetos 'municipio' que define una ruta.
        """
        self.ruta = ruta
        self.distancia = 0
        self.f_aptitud = 0.0
    
    def distanciaRuta(self):
        """
        Calcula la distancia total de la ruta, incluyendo el regreso
        al punto de partida. Utiliza memoización simple para evitar
        recálculos.
        
        @return: La distancia total (float) de la ruta.
        """
        if self.distancia == 0:
            distanciaRelativa = 0
            for i in range(0, len(self.ruta)):
                puntoInicial = self.ruta[i]
                puntoFinal = None
                
                # Comprueba si es el último punto para volver al inicio
                if i + 1 < len(self.ruta):
                    puntoFinal = self.ruta[i + 1]
                else:
                    puntoFinal = self.ruta[0] 
                
                distanciaRelativa += puntoInicial.distancia(puntoFinal)
            self.distancia = distanciaRelativa
        return self.distancia
    
    def rutaApta(self):
        """
        Calcula la puntuación de aptitud (fitness score) de la ruta.
        La aptitud es el inverso de la distancia (1 / distancia).
        
        @return: El valor de aptitud (float).
        """
        if self.f_aptitud == 0:
            # La aptitud es el inverso de la distancia.
            # Rutas más cortas tienen mayor aptitud.
            self.f_aptitud = 1 / float(self.distanciaRuta())
        return self.f_aptitud

# -------------------------------------------------------------------
#                Funciones del Algoritmo Genético
# -------------------------------------------------------------------

def crearRuta(listaMunicipios):
    """
    Crea una ruta aleatoria (una permutación) a partir de la lista
    de municipios.
    
    @param listaMunicipios: La lista de todos los municipios a visitar.
    @return: Una lista (ruta) con un orden aleatorio de municipios.
    """
    ruta = random.sample(listaMunicipios, len(listaMunicipios))
    return ruta

def poblacionInicial(tamanoPob, listaMunicipios):
    """
    Crea la población inicial de rutas aleatorias.
    
    @param tamanoPob: El número de individuos (rutas) en la población.
    @param listaMunicipios: La lista base de municipios.
    @return: Una lista de rutas (población).
    """
    poblacion = []
    for i in range(0, tamanoPob):
        poblacion.append(crearRuta(listaMunicipios))
    return poblacion

def clasificacionRutas(poblacion):
    """
    Evalúa y clasifica todas las rutas en la población según su aptitud.
    
    @param poblacion: La lista de rutas (individuos).
    @return: Una lista ordenada (descendente) de tuplas (índice, aptitud).
    """
    fitnessResults = {}
    for i in range(0, len(poblacion)):
        fitnessResults[i] = Aptitud(poblacion[i]).rutaApta()
        
    # Ordena por valor de aptitud de mayor a menor
    return sorted(fitnessResults.items(), key = operator.itemgetter(1), reverse = True)

def seleccionRutas(popRanked, indivSelecionados):
    """
    Selecciona los individuos para la siguiente generación usando una
    combinación de elitismo y selección por ruleta.
    
    @param popRanked: La lista clasificada de (índice, aptitud).
    @param indivSelecionados: El número de individuos a pasar
                               directamente (elitismo).
    @return: Una lista de índices de los individuos seleccionados.
    """
    resultadosSeleccion = []
    
    # Selección por Elitismo
    # Se seleccionan directamente los indivSelecionados mejores.
    for i in range(0, indivSelecionados):
        resultadosSeleccion.append(popRanked[i][0])
        
    # Selección por Ruleta
    # Se prepara el DataFrame para el cálculo de la ruleta.
    df = pd.DataFrame(np.array(popRanked), columns=["Indice", "Aptitud"])
    df['cum_sum'] = df.Aptitud.cumsum()
    df['cum_perc'] = 100 * df.cum_sum / df.Aptitud.sum()
    
    # Se eligen los individuos restantes usando la ruleta.
    for i in range(0, len(popRanked) - indivSelecionados):
        seleccion = 100 * random.random()
        for i in range(0, len(popRanked)):
            # Se selecciona el primer individuo cuya suma acumulada de porcentaje es mayor que el número aleatorio seleccion.
            if seleccion <= df.iat[i, 3]: # iat[i, 3] accede a 'cum_perc'
                resultadosSeleccion.append(popRanked[i][0])
                break
    return resultadosSeleccion

def grupoApareamiento(poblacion, resultadosSeleccion):
    """
    Crea el "grupo de apareamiento" (mating pool) a partir de la
    población y los índices seleccionados.
    
    @param poblacion: La población actual.
    @param resultadosSeleccion: Los índices de los individuos seleccionados.
    @return: Una lista con los individuos (rutas) seleccionados.
    """
    grupoApareamiento = []
    for i in range(0, len(resultadosSeleccion)):
        index = resultadosSeleccion[i]
        grupoApareamiento.append(poblacion[index])
    return grupoApareamiento

def reproduccion(progenitor1, progenitor2):
    """
    Realiza el cruce (crossover) entre dos progenitores para crear un hijo.
    Utiliza una variante de "Ordered Crossover (OX)":
    1. Se toma un segmento aleatorio del progenitor1.
    2. Se rellena el resto del hijo con los genes del progenitor2,
       en el orden en que aparecen, omitiendo los ya presentes.
       
    @param progenitor1: La primera ruta progenitora.
    @param progenitor2: La segunda ruta progenitora.
    @return: Una nueva ruta (hijo).
    """
    hijo = []
    hijoP1 = []
    hijoP2 = []
    
    # Selecciona dos puntos aleatorios para el cruce
    generacionX = int(random.random() * len(progenitor1))
    generacionY = int(random.random() * len(progenitor1))
    
    generacionInicial = min(generacionX, generacionY)
    generacionFinal = max(generacionX, generacionY)

    # Copia el segmento del progenitor 1 al hijo
    for i in range(generacionInicial, generacionFinal):
        hijoP1.append(progenitor1[i])
        
    # Rellena el resto con genes del progenitor 2 (evitando duplicados)
    hijoP2 = [item for item in progenitor2 if item not in hijoP1]

    # Concatena las dos partes para formar el hijo completo
    hijo = hijoP1 + hijoP2
    return hijo

def reproduccionPoblacion(grupoApareamiento, indivSelecionados):
    """
    Crea la nueva población mediante la reproducción (cruce).
    Conserva a los individuos élite y cruza al resto.
    
    @param grupoApareamiento: El pool de individuos seleccionados.
    @param indivSelecionados: El número de individuos élite (sin cruzar).
    @return: La nueva generación (lista de hijos).
    """
    hijos = []
    tamano = len(grupoApareamiento) - indivSelecionados
    espacio = random.sample(grupoApareamiento, len(grupoApareamiento))

    # Preserva el elitismo, los mejores pasan sin cambios
    for i in range(0, indivSelecionados):
        hijos.append(grupoApareamiento[i])
    
    # Cruza el resto de la población
    for i in range(0, tamano):
        hijo = reproduccion(espacio[i], espacio[len(grupoApareamiento) - i - 1])
        hijos.append(hijo)
    return hijos

def mutacion(individuo, razonMutacion):
    """
    Aplica una mutación de "intercambio" (Swap Mutation) a un individuo.
    Recorre cada gen y, si se cumple la 'razonMutacion', intercambia
    su posición con otro gen aleatorio.
    
    @param individuo: La ruta (lista) a mutar.
    @param razonMutacion: La probabilidad (0.0 a 1.0) de que ocurra
                          una mutación en un gen.
    @return: El individuo (posiblemente) mutado.
    """
    for swapped in range(len(individuo)):
        if(random.random() < razonMutacion):
            swapWith = int(random.random() * len(individuo))
            
            lugar1 = individuo[swapped]
            lugar2 = individuo[swapWith]
            
            individuo[swapped] = lugar2
            individuo[swapWith] = lugar1
    return individuo

def mutacionPoblacion(poblacion, razonMutacion):
    """
    Aplica el proceso de mutación a toda la población.
    
    @param poblacion: La lista de individuos.
    @param razonMutacion: La probabilidad de mutación.
    @return: La población mutada.
    """
    pobMutada = []
    
    for ind in range(0, len(poblacion)):
        individuoMutar = mutacion(poblacion[ind], razonMutacion)
        pobMutada.append(individuoMutar)
    return pobMutada

def nuevaGeneracion(generacionActual, indivSelecionados, razonMutacion):
    """
    Orquesta la creación de una nueva generación completa, ejecutando
    los pasos de clasificación, selección, reproducción y mutación.
    
    @param generacionActual: La población de la generación actual.
    @param indivSelecionados: El tamaño del elitismo.
    @param razonMutacion: La probabilidad de mutación.
    @return: La nueva generación de individuos.
    """
    # Clasificar rutas por aptitud
    popRanked = clasificacionRutas(generacionActual)
    
    # Seleccionar los mejores candidatos con elitismo + ruleta
    selectionResults = seleccionRutas(popRanked, indivSelecionados)
    
    # Generar el grupo de apareamiento
    grupoApa = grupoApareamiento(generacionActual, selectionResults)
    
    # Generar la nueva población mediante cruce con elitismo
    hijos = reproduccionPoblacion(grupoApa, indivSelecionados)
    
    # Aplicar mutaciones a la nueva generación
    nuevaGeneracion = mutacionPoblacion(hijos, razonMutacion)
    
    return nuevaGeneracion

def algoritmoGenetico(poblacion, tamanoPoblacion, indivSelecionados, razonMutacion, generaciones):
    """
    Función principal que ejecuta el Algoritmo Genético para resolver el TSP.
    
    @param poblacion: Lista de objetos 'municipio'.
    @param tamanoPoblacion: Número de individuos por generación.
    @param indivSelecionados: Número de individuos élite.
    @param razonMutacion: Probabilidad de mutación.
    @param generaciones: Número total de generaciones a ejecutar.
    @return: Una tupla (mejorRuta, progreso), donde 'mejorRuta' es la
             mejor ruta encontrada y 'progreso' es una lista con la
             mejor distancia de cada generación.
    """
    # Inicializa la población
    pop = poblacionInicial(tamanoPoblacion, poblacion)
    
    # Calcula la distancia inicial para referencia
    distanciaInicial = 1 / clasificacionRutas(pop)[0][1]
    print("Distancia Inicial: " + str(distanciaInicial))
    
    progreso = []
    progreso.append(distanciaInicial)
    

    # Itera a través de las generaciones
    for i in range(0, generaciones):
        pop = nuevaGeneracion(pop, indivSelecionados, razonMutacion)
        # Registra la mejor distancia de esta generación
        progreso.append(1 / clasificacionRutas(pop)[0][1])
    
    print("Distancia Final: " + str(1 / clasificacionRutas(pop)[0][1]))
    bestRouteIndex = clasificacionRutas(pop)[0][0]
    mejorRuta = pop[bestRouteIndex]
    
    return mejorRuta, progreso

# -------------------------------------------------------------------
#                   Ejecución del Algoritmo
# -------------------------------------------------------------------

# Asegura que este código solo se ejecute cuando el script es ejecutado directamente, no cuando es importado como un módulo.
if __name__ == "__main__":
    
    # Definición de Municipios
    listaMunicipios1 = [
      municipio(x=40.4168, y=-32.7038),
      municipio(x=41.3851, y=21.1734),
      municipio(x=9.4699, y=-8.3763), 
      municipio(x=20.3891, y=-6.9845),
      municipio(x=41.6488, y=-7.8891),
      municipio(x=33.7213, y=-42.4214),
      municipio(x=15.0000, y=5.0000),
      municipio(x=55.0000, y=10.0000),
      municipio(x=10.0000, y=-40.0000),
      municipio(x=50.0000, y=-25.0000),
      municipio(x=25.0000, y=15.0000),
      municipio(x=30.0000, y=-15.0000),
      municipio(x=45.0000, y=30.0000),
      municipio(x=5.0000, y=0.0000),
      municipio(x=35.0000, y=18.0000)
    ]

    listaMunicipios2 = [
      municipio(x=50.1234, y=-110.5678),
      municipio(x=-75.9876, y=15.4321),
      municipio(x=12.3456, y=170.8901),
      municipio(x=68.0123, y=-45.6789),
      municipio(x=-22.7890, y=99.0123),
      municipio(x=39.4567, y=-8.7890),
      municipio(x=-1.2345, y=130.6789),
      municipio(x=80.5678, y=-175.9012),
      municipio(x=5.9012, y=25.3456),
      municipio(x=45.6789, y=-140.0123),
      municipio(x=-15.3456, y=60.7890),
      municipio(x=77.0123, y=10.4567)
    ]

    listaMunicipios3 = [
      municipio(x=50.1020, y=15.3040),
      municipio(x=-10.5060, y=-150.7080),
      municipio(x=33.7799, y=88.5511),
      municipio(x=-66.2244, y=-122.8866),
      municipio(x=7.0102, y=177.3456),
      municipio(x=80.9876, y=-5.4321),
      municipio(x=-40.1122, y=-140.3344),
      municipio(x=25.5566, y=70.7788),
      municipio(x=-5.9900, y=110.0011),
      municipio(x=1.2233, y=-179.4455),
      municipio(x=9.0000, y=9.0000),
      municipio(x=-55.1234, y=13.5678),
      municipio(x=38.7654, y=-100.9876)
    ]

    listaMunicipios4 = [
      municipio(x=44.1100, y=-10.2200),
      municipio(x=-18.3300, y=150.4400),
      municipio(x=67.5500, y=20.6600),
      municipio(x=1.7700, y=-170.8800),
      municipio(x=-35.9900, y=55.0000),
      municipio(x=22.1122, y=-120.3344),
      municipio(x=85.5566, y=95.7788),
      municipio(x=-9.9900, y=-9.0011)
    ]

    listaMunicipios5 = [
      municipio(x=40.0000, y=-10.0000),
      municipio(x=-25.5000, y=175.7500),
      municipio(x=85.2500, y=-70.1250),
      municipio(x=-15.9999, y=10.0001),
      municipio(x=5.6789, y=145.2345),
      municipio(x=-50.4321, y=-20.0123),
      municipio(x=30.1020, y=160.3040),
      municipio(x=-10.5060, y=-15.7080),
      municipio(x=33.7799, y=10.5511),
      municipio(x=-66.2244, y=-100.8866),
      municipio(x=7.0102, y=100.3456),
      municipio(x=80.9876, y=-125.4321),
      municipio(x=-40.1122, y=-40.3344),
      municipio(x=25.5566, y=170.7788)
    ] 



    # Configuración y Ejecución del AG
    mejorRuta, progreso = algoritmoGenetico(poblacion=listaMunicipios5, 
                                            tamanoPoblacion=100, 
                                            indivSelecionados=20, 
                                            razonMutacion=0.01, 
                                            generaciones=500)

    # Impresión de Resultados
    print("\nMejor ruta encontrada:")
    print(mejorRuta)

    # ---------------------------------------------------------------
    #                 Visualización de Resultados
    # ---------------------------------------------------------------

    # Gráfico 1 para el Progreso de la Optimización
    # Muestra cómo la distancia total de la mejor ruta disminuye a lo largo de las generaciones.
    plt.figure(1)
    plt.plot(progreso)
    plt.title("Progreso de la Distancia de la Ruta")
    plt.xlabel("Generación")
    plt.ylabel("Distancia")
    plt.show(block=False)

    # Gráfico 2 para mostrar l Ruta Óptima
    # Dibuja la ruta óptima encontrada en un plano 2D.
    plt.figure(2)
    x_coords = []
    y_coords = []
    
    # Extrae las coordenadas de la mejor ruta
    for ciudad in mejorRuta:
        x_coords.append(ciudad.x)
        y_coords.append(ciudad.y)
        
    # Añade el punto de inicio al final para cerrar el ciclo
    x_coords.append(mejorRuta[0].x)
    y_coords.append(mejorRuta[0].y)

    # Dibuja los puntos y las líneas
    plt.plot(x_coords, y_coords, 'o-')
    plt.title("Ruta Óptima del Vendedor")
    plt.xlabel("Coordenada X")
    plt.ylabel("Coordenada Y")

    # Añade etiquetas numericas a cada ciudad
    for i, ciudad in enumerate(listaMunicipios5):
        plt.text(ciudad.x, ciudad.y, f" {i+1}")

    # Muestra el grafico
    plt.show()