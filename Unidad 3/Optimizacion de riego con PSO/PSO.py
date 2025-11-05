import numpy as np
import Particula

# Clase que representa un enjambre de particulpas para aplicar
#   el algoritmo de PSO
class PSO:

    # Consutructor de la clase PSO
    # Parametros de entrada
    # n_particulas: numero de particulas que contendra el enjambre
    # n_sensores: numero de sensores que contendra cada particula
    # f_objetivo: Funcion objetivo con lo que se evaluara cada solucion
    # w: Inercia
    # c1: Coeficiente de localidad
    # c2: Coeficiente global
    # Atributos:
    # particulas: Arreglo que contendra todas las particulas del enjambre
    # gbest: Mejor posicion de una particula que representa la mejor solucion
    #   encontrada
    # gbest_value: Valor que corresponde a gbest
    def __init__(self, n_particulas, n_sensores, limites, f_objetivo, w = 0.8, c1 = 2, c2 = 2):
        self.particulas = [Particula.Particula(n_sensores, limites) for _ in range(n_particulas)]
        self.f_objetivo = f_objetivo
        self.w = w
        self.c1 = c1
        self.c2 = c2
        self.gbest = None
        self.gbest_value = np.inf

    # Metodo que corre la logica del PSO
    # Parametros de entrada:
    # max_iters: Maxima cantidad de iteraciones
    # datos: Datos extra que necesita la funcion objetivo para funcionar
    # Retorna:
    # gbest: La mejor solucion encontrada, la mejor manera de posicionar
    #   los sensores
    # gbest_value: Valor que representa la mejor solucion
    # valor_iteracion: Arreglo donde se guarda el mejor valor global
    #   por cada iteracion
    # Funcionamiento del metodo:
    # Por cada iteracion suceden tres pasos:
    # 1.- Se actualizan los valores de las particulas, dada su posicion
    #   se calculan su valores, a su vez que se ve si alguno de esos nuevos
    #   valores es el nuevo optimo global
    # 2.- Actualizar la velocidad de todas las particulas
    # 3.- Con la velocidad actualizada, mover la posicion de todas las particulas
    def optimizar(self, max_iters, datos):
        valor_iteracion = []
        for it in range(max_iters):
            print(f"Itercaion {it}/{max_iters}")
            for p in self.particulas:
                p.actualizar_valor(self.f_objetivo, datos)
                if p.valor < self.gbest_value:
                    self.gbest_value = p.valor
                    self.gbest = p.posicion.copy()

            for p in self.particulas:
                p.actualizar_velocidad(self.gbest,
                                       self.w,
                                       self.c1,
                                       self.c2)
                p.mover()

            valor_iteracion.append(self.gbest_value)

        return self.gbest, self.gbest_value, valor_iteracion