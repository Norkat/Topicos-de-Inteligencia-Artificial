import pandas as pd
import random
import time
from collections import deque

# Leer las matrices de distancias
def read_distances():
    distances_df = pd.read_csv("distance_matrix.csv")

    # Separacion de titulos a valores (quiza se usa luego)
    nombres_nodos = distances_df.columns.tolist()

    distances = distances_df.values.tolist()

    return distances

# Leer el Data sobre las tiendas y centros de distribucion
def read_store_data():
    df = pd.read_csv("store_distribution_data.csv")

    centers = df[df["Tipo"] == "Centro de Distribución"]
    stores = df[df["Tipo"] == "Tienda"]

    centers = centers[["Nombre", "Latitud_WGS84", "Longitud_WGS84"]].to_dict(orient="records")
    stores = stores[["Nombre", "Latitud_WGS84", "Longitud_WGS84"]].to_dict(orient="records")

    return centers, stores

# Generamos una solucion inicial
def generate_initial_solve(centers, stores, distance):
    routes = []
    for i in range(centers):
        routes.append([i])
    
    random_stores = random.sample(range(centers, centers + stores), stores)
    
    for i in range(len(random_stores)):
        id_store = random_stores[i]
        best_route = 0
        for j in range(centers):
            last_loc = routes[j][-1]
            best_loc = routes[best_route][-1]
            if distance[last_loc][id_store] < distance[best_loc][id_store]:
                best_route = j
        routes[best_route].append(id_store)
    
    return routes

# Calculamos el costo de una solucion
def calculate_cost(routes, centers, distance):
    cost = 0
    for i in range(centers):
        stores = len(routes[i])
        for j in range(stores):
            cost += distance[j][(j + 1) % stores]
    return cost

# Encontramos cual es la mejor relocalizacion para una tienda dada con una
# solucion anterior, la relocalizacion puede ser en la misma ruta o en una
# diferente
def best_relocation(routes, cost, centers, distances, pos_store):
    (route, pos) = pos_store
    store = routes[route][pos]
    a = routes[route][pos - 1]
    c = routes[route][(pos + 1) % len(routes[route])]
    cost1 = distances[a][c] - (distances[a][store] + distances[store][c])

    best_relocation = float('inf')
    movs = ()
    for i in range(centers):
        lenRoute = len(routes[i])
        for j in range(lenRoute):
            if route == i and (pos == j or pos - 1 == j):
                continue
            d = routes[i][j]
            e = routes[i][(j + 1) % lenRoute]
            cost_act = cost + cost1 + (distances[d][store] + distances[store][e]) - distances[d][e]
            if cost_act < best_relocation:
                best_relocation = cost_act
                movs = (route, pos, i, j)
    
    return (best_relocation, movs)

# Generamos el vecino dado una solucion anterior y los movimientos que se deben de hacer
def generate_neighbor(routes, movs):
    (route_or, pos_or, route_tg, pos_tg) = movs
    store = routes[route_or][pos_or]

    new_routes = [row[:] for row in routes]

    if route_or != route_tg or pos_or > pos_tg:
        pos_tg += 1

    new_routes[route_or].pop(pos_or)
    new_routes[route_tg].insert(pos_tg, store)

    return new_routes

# Generamos el mejor vecino posible dado una solucion anterior
def generate_best_neighbor(routes, cost, centers, distances, tabu_stores):
    best_cost = float('inf')
    movs = ()
    for i in range(centers):
        for j in range(1, len(routes[i])):
            if(routes[i][j] in tabu_stores):
                continue

            (cost_act, movs_act) = best_relocation(routes, cost, centers, distances, (i, j))
            if cost_act < best_cost:
                best_cost = cost_act
                movs = movs_act

    best_neighbor = generate_neighbor(routes, movs)

    (route_or, pos_or, _, _) = movs
    tabu_stores.append(routes[route_or][pos_or])

    return (best_neighbor, best_cost)   

# Busqueda de solucion pro tabu
def solve(centers, stores, distances):
    N = centers + stores
    # Generar solucion inicial y su costo
    act_routes = generate_initial_solve(centers, stores, distances)
    act_cost = calculate_cost(act_routes, centers, distances)

    # Tomar la solucion inicial como la mejor
    best_routes = act_routes
    best_cost = act_cost

    # Registrar el costo (se hara por cada iteracion)
    steps = [act_cost]

    # Crearemos la cola tabu, donde guardaremos las tiendas que no se usen
    max_tabu = N // 10
    tabu_stores = deque()

    # Definimos un maximo de iteraciones permitidos 
    # sin mejora
    start_time = time.time()
    max_time=10.0

    while time.time() - start_time < max_time:
        (best_neighbor, neighbor_cost) = generate_best_neighbor(act_routes, act_cost, centers, distances, tabu_stores)

        if neighbor_cost < best_cost:
            best_cost = neighbor_cost
            best_routes = best_neighbor

        if len(tabu_stores) > max_tabu:
            tabu_stores.popleft()

        act_routes = best_neighbor
        act_cost = neighbor_cost
        steps.append(act_cost)

    return (best_routes, best_cost, steps)

def main():
    distances = read_distances()
    centers, stores = read_store_data()
    
    (routes, cost, steps) = solve(len(centers), len(stores), distances)

    # Imprimir resultados
    print("Mejor ruta encontrada: ")
    print(routes)
    print("Costo de la ruta: " + str(cost))

    # Imprimir resultados de primeras 10 iteraciones
    # y de ultimas 10 iteraciones
    print(steps[:10])
    print(steps[-10:])


main()
