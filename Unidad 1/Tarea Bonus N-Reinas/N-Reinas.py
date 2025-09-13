import random
from collections import deque

# Crear un arreglo con los numeros de 1 a N
# y luego revolverlo aleatorimente. Representara
# la primera solución de las N reinas
def generateRandomSolution(N):
    chess = list(range(1, N + 1))
    random.shuffle(chess)
    return chess

# Dado una solucion inicial y las posciones para 
# hacer el swap, se regresa una solucion vecina
def getNeighbor(chess, i, j):
    chess[i], chess[j] = chess[j], chess[i]
    return chess

# Regresa el numero de colisiones de una solucion
def targetFunction(chess, N):
    diags = [0] * (2 * N + 1)
    diags2 = [0] * (2 * N)
    colissions = 0

    for i in range(N):
        # Obtener las coordenadas en el tablero
        # para saber en que diagonales esta la reina
        x = i + 1
        y = chess[i]
        diag = x + y
        diag2 = (x - y) + N

        # Contar el numero de colisiones por el numero
        # de reinas que hay en las diagonales
        colissions += diags[diag] + diags2[diag2]

        # Actualizar las diagonales para la consulta de
        # futuras reinas
        diags[diag] += 1
        diags2[diag2] += 1

    return colissions

def tabu(N):
    # Generamos una primera solucion aleatoria
    chess = generateRandomSolution(N)

    # bestChess guardara la mejor solucion global encontrada
    # bestSolve guardara el numero de colisiones de bestChess
    bestSolve = targetFunction(chess, N)
    bestChess = chess

    # steps llevara el registro de colisiones de los mejores vecinos
    # por default agregamos el numero de colisiones del estado inicial
    steps = [bestSolve]

    # Si da la casualidad de que la solucion inicial es la mejor
    # la retornamos
    if bestSolve == 0:
        return (chess, steps)

    # Creamos una lista donde estaran los movimientos
    # tabu y establecemos el maximo
    maxTabu = (N // 2) + 1
    tabuMovs = deque()

    # Definimos un maximo de iteraciones permitidos 
    # sin mejora
    maxTries = 100
    tries = 0

    while tries < maxTries:

        # bestNeighbor es donde guardaremos el mejor vecino
        # bestMov es el movimiento hecho para llegar al mejor vecino
        # bestColission el numero de colisiones de bestNeighbor
        bestNeighbor = []
        bestMov = ()
        bestColission = N * N

        # Crear y revisar vecindario
        for i in range(N):
            j = (i + 1) % N

            # Si el movimiento esta dentro del tabu, entonces
            # ignoramos este vecino
            mov = (chess[i], chess[j])
            if mov[0] > mov[1]:
                mov = (mov[1], mov[0])

            if mov in tabuMovs:
                continue
            
            # Obtenemos el vecino y sus colisiones
            neighbor = getNeighbor(chess, i, j)
            neighborColission = targetFunction(neighbor, N)

            # Si el vecino tiene 0 colisiones se encontro la mejor solución
            if(neighborColission == 0):
                steps.append(0)
                return (neighbor, steps)
            # Si resulta ser un mejor vecino que los antes procesados
            # lo tomamos
            elif neighborColission < bestColission:
                bestNeighbor = neighbor
                bestColission = neighborColission
                bestMov = mov

        #Checamos si es la mejor solucion global
        if bestColission < bestSolve:
            bestSolve = bestColission
            bestChess = bestNeighbor
            tries = 0
        else:
            tries += 1
        
        # Guardamos el movimiento usado en los tabus
        # Si la cola excedio el maximo, sacamos el primero
        tabuMovs.append(bestMov)
        if len(tabuMovs) > maxTabu:
            tabuMovs.popleft()
        
        # Actualizamos chess para que sea el mejor vecino
        # y agregamos este nuevo paso al registro
        chess = bestNeighbor
        steps.append(bestColission)
        
    # Si excedemos el maximo de iteraciones
    # Retornamos la mejor que encontramos
    return (bestChess, steps) 


# Imprimir el estado en formato tablero
def printChessBoard(chess, N):
    for i in range(N):
        row = "*" * N
        row = row[:chess[i] - 1] + "R" + row[chess[i]:]
        print(row)


def main():
    # Preguntar por el tamaño del tablero
    N = int(input("Inserte el tamaño del tablero: "))
    
    # Obtenemos la mejor solución encontrada y los pasos dados
    # para llegar a ella
    (chessSolve, steps) = tabu(N)
    colissions = targetFunction(chessSolve, N)

    if colissions == 0:
        print(f"Se encontro la solución: {chessSolve}")
    else:
        print(f"La mejor solucion encontrada fue de {colissions} colisiones: {chessSolve}")

    print("Tablero")
    printChessBoard(chessSolve, N)

    print(f"Numero de pasos para llegar a la solucion: {len(steps)}")
    print(f"Pasos: {steps}")

main()
