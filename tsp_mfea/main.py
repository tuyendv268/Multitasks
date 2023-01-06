import configparser
from TSP import TSP
from init import Init
import random
from crossover import Crossover
import json
from tqdm import tqdm
import numpy as np
import pickle as pkl

best_founds = [[], []]
num_seed = 30

path = "config/config.cfg"
config = configparser.ConfigParser()
config.read(path)

population_size = int(config["general"]["population_size"])
gene_length = int(config["general"]["gen_length"])
num_generation = int(config["general"]["num_generation"])
rmp = float(config["general"]["rmp"])

results = np.zeros((num_seed, num_generation))

seed_tqdm = tqdm(range(0, num_seed))
for seed in seed_tqdm:
    min_glob_1 = 9999999
    min_glob_2 = 9999999
    random.seed(seed)

    # print("-------------init population--------------")
    population = Init.init_population(population_size=population_size, gene_length=gene_length)

    TSP_1 = TSP(config["TSP_1"], 0)
    TSP_2 = TSP(config["TSP_2"], 1)

    for ele in population:
        fitness_1 = TSP_1.calculate_fitness(ele.gene)
        fitness_2 = TSP_2.calculate_fitness(ele.gene)
        ele.fitness = [fitness_1, fitness_2]

    TSP_1.init_factorial_rank(population)
    TSP_2.init_factorial_rank(population)

    for ele in population:
        ele.update_skill_factor()

    # for ele in population:
    #     print(ele.to_string())
        
    # print()

    for _ in range(num_generation):
        new_population = []
        tmp_population = set(population.copy())
        # for i in range(int(population_size)):
        while len(tmp_population) >= 2:
            parent = random.sample(list(tmp_population), 2)
            rand = random.randint(0, 100) / 100
            if parent[0].skill_factors == parent[1].skill_factors or rand < rmp:
                child_1, child_2 = Crossover.crossover_PMX(*parent)
            else:
                child_1 = Crossover.mutita_gen(parent[0])
                child_2 = Crossover.mutita_gen(parent[1])
            new_population.append(child_1)
            new_population.append(child_2)
            tmp_population -= set(parent)
            
        for ele in new_population:
            if ele.skill_factors == 0:
                fitness_1 = TSP_1.calculate_fitness(ele.gene)
                ele.fitness = [fitness_1, 999999]
            else:
                fitness_2 = TSP_2.calculate_fitness(ele.gene)
                ele.fitness = [999999, fitness_2]
                
        population = population + new_population
        TSP_1.update_factorial_rank(population)
        TSP_2.update_factorial_rank(population)

        for ele in population:
            ele.update_skill_factor()
            
        population.sort(key=lambda individual:individual.scalar_fitnesss, reverse=True)
        population = population[0:population_size]

        min_1 = 9999999
        min_2 = 9999999
        for indi in population:
            # print(indi.to_string())
            min_1 = min(min_1, indi.fitness[0])
            min_2 = min(min_2, indi.fitness[1])
            min_glob_1 = min(min_1, min_glob_1)
            min_glob_2 = min(min_2, min_glob_2)
        results[seed][_] = min_1
        
        seed_tqdm.set_postfix({"task_1":min_glob_1, "task_2":min_glob_2})
        seed_tqdm.set_description(f'seed={seed}')
                
        # print(f'min_1: {min_1}')
        # print(f'min_2: {min_2}')

with open("results.pkl", "wb") as tmp:
    pkl.dump(results, tmp)