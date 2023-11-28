from random import choice, random
import random
from random import randrange
from collections import Counter


def evolve():
    population = create_pop()
    fitness_population = evaluate_pop(population)
    for gen in range(NUMBER_GENERATION):
        mating_pool = select_pop(population, fitness_population)
        offspring_population = crossover_pop(mating_pool)
        population = mutate_pop(offspring_population)
        fitness_population = evaluate_pop(population)
        best_ind, best_fit = best_pop(population, fitness_population)
        print("#%3d" % gen, "fit:%3d" % best_fit, "".join(best_ind))


# POPULATION-LEVEL OPERATORS


def create_pop():
    return [create_ind() for _ in range(POPULATION_SIZE)]


def evaluate_pop(population):
    return [evaluate_ind(individual) for individual in population]


def select_pop(population, fitness_population):
    sorted_population = sorted(zip(population, fitness_population), key=lambda ind_fit: ind_fit[1])
    return [individual for individual, fitness in sorted_population[:int(POPULATION_SIZE * TRUNCATION_RATE)]]


def crossover_pop(population):
    return [crossover_ind(choice(population), choice(population)) for _ in range(POPULATION_SIZE)]


def mutate_pop(population):
    return [mutate_ind(individual) for individual in population]


def best_pop(population, fitness_population):
    return sorted(zip(population, fitness_population), key=lambda ind_fit: ind_fit[1])[0]


# INDIVIDUAL-LEVEL OPERATORS: REPRESENTATION & PROBLEM SPECIFIC

target = list("HELLO WORLD!")
alphabet = "123456789"
INDIVIDUAL_SIZE = len(target)


def create_ind():
    random_list = []

    for j in range(9):
        row = []
        for d in range(9):
            row.append(randrange(9))
        random_list.append(row)

    return random_list


def evaluate_ind(individual):
    return sum(i != t for i, t in zip(individual, target))


def crossover_ind(individual1, individual2):
    return [choice(ch_pair) for ch_pair in zip(individual1, individual2)]


def mutate_ind(individual):
    return [(choice(alphabet) if random() < MUTATION_RATE else ch) for ch in individual]


def random_board():  # Generates a board and fills its tiles with random numbers
    base = 3
    side = base * base

    # Define a valid base pattern
    def pattern(r, c): return (base * (r % base) + r // base + c) % side

    # Randomise the values of the board
    from random import sample
    def shuffle(s): return sample(s, len(s))

    base_range = range(base)

    row = [g * 3 + r for g in shuffle(base_range) for r in shuffle(base_range)]

    col = [g * 3 + c for g in shuffle(base_range) for c in shuffle(base_range)]
    nums = shuffle(range(1, base * base + 1))

    # Initialise board
    board = [[nums[pattern(i, j)] for j in col] for i in row]

    return board


def fitness(population):
    # loop through all individuals in population
    # find average number of repeats per row for each individual
    # return list of top 2 individuals (who have the lowest number of repeats)

    fitness_dict = {}
    best = []
    repeats = 0

    for individual in population:
        repeats = 0
        average = 0
        for row in individual:
            res = Counter(row)
            for key in res:
                repeats += res[key]
        average = repeats / len(res)
        fitness_dict[population.index(individual)] = average
    best_index = (min(fitness_dict.items(), key=lambda x: x[1])[0])
    best.append(population[best_index])
    fitness_dict.pop(best_index)
    best_index = (min(fitness_dict.items(), key=lambda x: x[1])[0])
    best.append(population[best_index])

    print("The two most fit boards of the generation are:\n")
    for x in best:
        print(x, "\n")

    return best


NUMBER_GENERATION = 100
POPULATION_SIZE = 2
TRUNCATION_RATE = 0.5
MUTATION_RATE = 1.0 / INDIVIDUAL_SIZE

fitness(create_pop())
test = input("test")
