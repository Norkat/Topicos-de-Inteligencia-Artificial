
## Tabú
# Entradas
Como único valor a ingresar está el tamaño del tablero (N), que va definir la cantidad de reinas que habrá en el tablero.
# Salida
La salida mostrará la mejor solución, en caso de no encontrar una solución que satisfaga al problema, mostrará también el número de colisiones, la cantidad de pasos para llegar a la solución y los propios pasos.

# Solución
Lo primero es generar un arreglo con los números de 1 a N permutados de manera aleatoria.
Una vez teniendo este "tablero" inicial, se declaran las siguientes variables:
- bestChess: guarda la mejor solución global encontrada.
- bestSolve: guarda el número de colisiones de bestChest.
- steps: lleva el registro de colisiones de los mejores vecinos (el valor por defecto es la cantidad del estado inicial)

Como primer paso, es importante añadir una validación en caso de que el estado inicial generado sea una solución (0 colisiones), se retorna como "bestSolve" y "steps" como 0.
En nuestro caso, definimos "maxTabu" como la máxima cantidad de tabus como (N / 2) + 1
Se define la variable "maxTries" para el máximo de iteraciones permitido (en nuestro caso: 100) y "tries" para la cantidad de iteraciones actuales.

Se definen las variables:
- bestNeighbor: guarda el mejor vecino.
- bestMov: es el movimiento hecho para llegar al mejor vecino.
- bestColission: la cantidad de colisiones de bestNeighbor.

Mientras "tries" sea menor que "maxTries" se estará creando y revisando un nuevo vecindario, realizando swaps, los vecinos generados se comparan con los movimientos que sean tabus, para descartarlos.
Una vez obtenido un vecino, se obtiene con él el numero de colisiones. 
Si el vecino tiene 0 colisiones, se ha encontrado la mejor solución, si no, pero si resulta ser un vecino mejor que los anteriomente procesados, se toma como "bestNeighbor".
En caso de que se encuentre una mejor solución, "tries" se reinicia para seguir buscando.
Para guardar los tabus, se agregan a un arreglo definido como "tabuMovs" de tamaño "maxTabu", donde se van guardando los tabus y en caso de que se exceda el limite, se expulsa el primero guardado (sigue la lógica de FIFO).
Una vez que "tries" deja de ser menor que "maxTries", la función termina y retorna "bestChess".

Por último, la función objetivo (que retorna el número de colisiones de un estado): las colisiones únicamente se pueden dar en diagonal, por lo que se definen las dos tipos de diagonales, las que van de izquieda a derecha y las que van de derecha a izquierda.
- De Izquieda a derecha: para definir este tipo de diagonal, se restan las coordenadas de las casillas. Una casilla pertenece a una misma diagonal que otra si la resta de sus cordenadas da el mismo resultado.
- De Derecha a izquierda: para definir este tipo de diagonal, se suman las coordenadas de las casillas. Una casilla pertenece a una misma diagonal que otra si la suma de sus coordenadas da el mismo resultado.





 
