import numpy as np

# Clase que representa una particula del enjambpre
# para el algoritmo PSO
class Particula:
    # Constructor de la clase particula
    # Parametros de entrada:
    # n_sensore: numero de sensores que tendra la solucion
    # limites: limites minimos y maximos de coordenadas donde podran estar 
    #   posicionados los sensores. Tiene el formato: [[min_lat, min_lon], [max_lat, max_lon]]
    # Atributos:
    # posicion: lista de pares de coordenadas, donde cada par representa un sensor diferente
    #   La lista es de tamaño n_sensor
    # velocidad: velocidad que dicta la siguiente posicion de la particula, en un inicio se
    #   inicaliza en ceros.
    # mejor_posicion: La mejor posicion que la particula ha encontrado
    # mejor_valor: El mejor valor que la particula ha encontrado
    # valor: El valor actual que tiene la particula  

    def __init__(self, n_sensores, limites):
        self.limites = limites
        self.n_sensores = n_sensores

        self.posicion = np.random.uniform(limites[0], limites[1], size=(n_sensores, 2))
        self.velocidad = np.zeros((n_sensores, 2))
        self.mejor_posicion = self.posicion.copy()
        self.mejor_valor = np.inf
        self.valor = np.inf

    # Metodo que actualiza el valor de la particula con la posicion actual
    # En caso de que el valor calculado supere a best_position entonces
    #   actualiza este de igual forma
    # Parametros de Entrada:
    # f_objetivo: funcion objetivo con la que se calcula el valor
    # datos: Resto de parametros necesarios que se necesitan para que la 
    # funcion objetivo calcule correctamente el valor

    def actualizar_valor(self, f_objetivo, datos):
        self.valor = f_objetivo(self.posicion, datos)
        if self.valor < self.mejor_valor:
            self.mejor_valor = self.valor
            self.mejor_posicion = self.posicion.copy()

    # Metodo que actualiza el valor de la velocidad de la particula
    # Parametros de entrada:
    # gbest: La mejor posicion global del enjambre
    # w: Inercia
    # c1: Coeficiente de localidad
    # c2: Coeficiente global
    def actualizar_velocidad(self, gbest, w, c1, c2):
        r1, r2 = np.random.rand(), np.random.rand()
        self.velocidad = (w*self.velocidad
                         + c1*r1*(self.mejor_posicion - self.posicion)
                         + c2*r2*(gbest - self.posicion))

    # Metodo para mover la posicion actual de la particula con la velocidad
    # Parametros de entrada:
    # bounds: Limites de los cuales los valores de las posiciones no se 
    #   pueden salir
    def mover(self):
        self.posicion += self.velocidad
        self.posicion = np.clip(self.posicion, self.limites[0], self.limites[1])