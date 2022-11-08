import configparser
from TSP import TSP
from init import Init
import random
from crossover import Crossover
from tqdm import tqdm

for seed in range(0, 2):
    random.seed(seed)

    path = "config/config.cfg"
    config = configparser.ConfigParser()
    config.read(path)

    population_size = int(config["general"]["population_size"])
    gene_length = int(config["general"]["gen_length"])
    num_generation = int(config["general"]["num_generation"])
    rmp = float(config["general"]["rmp"])

    # print("-------------init population--------------")
    population = Init.init_population(population_size=population_size, gene_length=gene_length)


    TSP_1 = TSP(config["TSP_1"], 0)
    TSP_2 = TSP(config["TSP_2"], 1)

    for ele in population:
        fitness_1 = TSP_1.calculate_fitness(ele.gene)
        fitness_2 = TSP_2.calculate_fitness(ele.gene)
        ele.fitness = [fitness_1, fitness_2]

    TSP_2.evaluate(population)
    TSP_1.evaluate(population)

    for ele in population:
        ele.update_skill_factor()

    # for ele in population:
    #     print(ele.to_string())
        
    # print()

    for _ in tqdm(range(num_generation)):
        new_population = []
        for i in range(int(population_size/2)):
            parent = random.sample(population, 2)
            rand = random.randint(0, 100) / 100
            if parent[0].skill_factors == parent[1].skill_factors or rand < rmp:
                child_1, child_2 = Crossover.crossover_PMX(*parent)
            else:
                child_1 = Crossover.mutita_gen(parent[0])
                child_2 = Crossover.mutita_gen(parent[1])
            new_population.append(child_1)
            new_population.append(child_2)
            
        for ele in new_population:
            if ele.skill_factors == 0:
                fitness_1 = TSP_1.calculate_fitness(ele.gene)
                ele.fitness = [fitness_1, 999999]
            else:
                fitness_2 = TSP_2.calculate_fitness(ele.gene)
                ele.fitness = [999999, fitness_2]
                
        population = population + new_population
        TSP_2.evaluate(population)
        TSP_1.evaluate(population)

        for ele in population:
            ele.update_skill_factor()
            
        population.sort(key=lambda individual:individual.scalar_fitnesss, reverse=True)
        population = population[0:population_size]

    min_1 = 9999999
    min_2 = 9999999
    for indi in population:
        print(indi.to_string())
        if min_1 > indi.fitness[0]:
            min_1 = indi.fitness[0]
        if min_2 > indi.fitness[1]:
            min_2 = indi.fitness[1]
            
    print(f'min_1: {min_1}')
    print(f'min_2: {min_2}')