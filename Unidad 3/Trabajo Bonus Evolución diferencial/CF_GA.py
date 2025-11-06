# Algoritmo genético para decifrar una contraseña "HELLO WORLD"
import random

# Definimos las variables importantes

objetive = 1
poblation_size = 50
mutation_rate = 1 / poblation_size * 3
max_generations = 100

def fitness(a, b, c, x):
    
    return round(1 / (1 + (a * (x**2)) + (b * x) + c), 2)


def initial_poblation(x, poblation_size):
    poblation = [(
        coef := [round(random.uniform(-100, 100),2) for _ in range(3)],
        fitness(coef[0], coef[1], coef[2], x)
    ) for _ in range(poblation_size)]
    return poblation

def mutation(son):

    son = list(son)

    for i in range(3):
        if(random.uniform(0,1) <= mutation_rate):
            delta = round(random.uniform(-0.5, 0.5),2)
            son[i] += delta

    return tuple(son)

def crossover(father1, father2):
   
    alpha = round(random.uniform(0,1),2)

    as1 = round((alpha * father1[0]) + ((1 - alpha) * father2[0]), 2)
    bs1 = round((alpha * father1[1]) + ((1 - alpha) * father2[1]), 2)
    cs1 = round((alpha * father1[2]) + ((1 - alpha) * father2[2]), 2)

    as2 = round(((1 - alpha) * father1[0]) + (alpha * father2[0]), 2)
    bs2 = round(((1 - alpha) * father1[1]) + (alpha * father2[1]), 2)
    cs2 = round(((1 - alpha) * father1[2]) + (alpha * father2[2]), 2)

    son1 = (as1, bs1, cs1)
    son2 = (as2, bs2, cs2)

    son1 = mutation(son1)
    son2 = mutation(son2)

    return son1, son2
    
def selection(poblation):
    best = min(poblation, key=lambda x: abs(x[1] - 1))
    
    participants = random.sample(poblation, 5)
    tournament_winner = max(participants, key=lambda x: x[1])

    best_coefficients = tuple(best[0])
    winner_coefficients = tuple(tournament_winner[0])


    return best_coefficients, winner_coefficients

   
x_value = int(input("Ingresa el valor de X: "))
poblation = sorted(initial_poblation(x_value, poblation_size),key=lambda x:x[1], reverse=True)

for individuo in poblation:
    print(individuo)

for i in range(max_generations):
    generation_best_coefs, generation_winner_coefs = selection(poblation)
    
    son1_coefs, son2_coefs = crossover(generation_best_coefs, generation_winner_coefs)
    
    son1 = (son1_coefs, fitness(son1_coefs[0], son1_coefs[1], son1_coefs[2], x_value))
    son2 = (son2_coefs, fitness(son2_coefs[0], son2_coefs[1], son2_coefs[2], x_value))

    
    poblation[0] = son1
    poblation[-1] = son2

    best = max(poblation, key=lambda x: x[1])
    print(f"Generación {i}: Mejor fitness = {best[1]}, Coefs = {best[0]}")
    
for individuo in poblation:
    print(individuo)
