import configparser
from tqdm import tqdm
import random
import numpy as np
from init import Init
from TSP import TSP
from crossover import Crossover
import json
import pickle as pkl

path = "C:\\Users\\tuyen\\OneDrive\\Desktop\\TTTH\\TSP\\config\\tsp.cfg"
config = configparser.ConfigParser()
config.read(path)

INT_MAX = 2147483647
NUM_CITY = int(config["general"]["NUM_CITY"])
POPULATION_SIZE = int(config["general"]["POPULATION_SIZE"])
NUM_GENERATION = int(config["general"]["NUM_GENERATION"])
NUM_SEED = 30

results = np.zeros((NUM_SEED, NUM_GENERATION))

for seed in range(NUM_SEED):
    random.seed(seed)
    np.random.seed(seed)
    _TSP = TSP(config)
    population = Init.init_population(population_size=POPULATION_SIZE, gene_length=NUM_CITY)
    min = INT_MAX

    for ele in population:
        fitness_1 = _TSP.calculate_fitness(ele.gene)
        ele.fitness = fitness_1

    # print("\population: \ngene\tfitness")
    # for i in range(POPULATION_SIZE):
    #     print(population[i].gene, population[i].fitness)
    # print()

    for index in tqdm(range(NUM_GENERATION)):
        new_population = []
        crossover_size = int(float(config["general"]["CROSSOVER_RATE"]) * int(config["general"]["POPULATION_SIZE"]))
        crossover_population = set(random.sample(population, crossover_size))
        
        mitate_size = int(float(config["general"]["MITATE_RATE"]) * int(config["general"]["POPULATION_SIZE"]))
        mitate_population = set(population) - crossover_population
        
        while len(crossover_population) >= 2:
            parrent = random.sample(list(crossover_population), 2)
            
            child_1, child_2 = Crossover.crossover_OX(*parrent)
            
            child_1.fitness = _TSP.calculate_fitness(child_1.gene)
            child_2.fitness = _TSP.calculate_fitness(child_2.gene)

            new_population.append(child_1)
            new_population.append(child_2)

            crossover_population = crossover_population - set(parrent)
            
        for indivi in mitate_population:
            indivi.gene = Crossover.mutita_gen(indivi.gene)
            indivi.fitness = _TSP.calculate_fitness(indivi.gene)
            
            new_population.append(indivi)
            
        population = new_population + population

        population.sort(key=lambda indi:indi.fitness)
        for i in population:
            if i.fitness < min:
                min = i.fitness
        population = population[0:POPULATION_SIZE]
        results[seed, index] = min
        
    # print("\population: \ngene\tfitness")
    # for i in range(POPULATION_SIZE):
    #     print(population[i].gene, population[i].fitness)
    # print()
    print(f"min: {min}")

print(results)
with open("results.pkl", "wb") as tmp:
    pkl.dump(results, tmp)