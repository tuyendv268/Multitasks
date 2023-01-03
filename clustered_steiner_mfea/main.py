import configparser
from tqdm import tqdm
import random
import utils
from crossover import CrossOver
from clustered_steiner import Clustered_Steiner
import pickle as pkl
import numpy as np
import os

random.seed(1)
config_path = "config/config.ini"
config = configparser.ConfigParser()
config.read(config_path)

population_size = int(config["general"]["population_size"])
num_generation = int(config["general"]["num_generation"])
rmp = float(config["general"]["rmp"])
gene_length = None
num_cluster = None

input_path = config["general"]["input_path"]
problems = []
for index, inp in enumerate(os.listdir(input_path)):
    abs_path = os.path.join(input_path, inp)
    probl = Clustered_Steiner(
        path=abs_path,
        idx=index
    )
    # print(probl.clusters)
    problems.append(probl)
    if gene_length is None or probl.num_dim > gene_length:
        gene_length = probl.num_dim
    if num_cluster is None or probl.num_cluster > num_cluster:
        num_cluster = probl.num_cluster
print(f"gene_length: {gene_length}")
print(f"num_cluster: {num_cluster}")

population = utils.init_population(
    vertexs=set(range(gene_length)),
    population_size=population_size,
    num_clusters=num_cluster
)

# for probl in tqdm(problems, desc="update fitness"):
#     probl.update_fitness(population)
for indi in tqdm(population, desc="init fitness"):
    fitness = np.array([1, 1])
    fitness[0] = problems[0].calculate_fitness(indi)
    fitness[1] = problems[1].calculate_fitness(indi)
    
    indi.set_fitness(fitness)
    
print(population[0].fitness)

for probl in problems:
    probl.init_factorial_rank(population)

# print(population[0].factorial_ranks)

for ele in population:
    ele.update_skill_factor()
    
print(population[99].skill_factors)

min_glob_1 = 9999999
min_glob_2 = 9999999
_tqdm = tqdm(range(num_generation))
for _ in _tqdm:
    new_population = []
    tmp_population = set(population.copy())
    
    while(len(tmp_population) >= 2):
        parent = random.sample(list(tmp_population), 2)
        rand = random.randint(0, 100) / 100
        if parent[0].skill_factors == parent[1].skill_factors or rand < rmp:
            child_1, child_2 = CrossOver.crossover(*parent)
        else:
            child_1 = CrossOver.mutate(parent[0])
            child_2 = CrossOver.mutate(parent[1])
        new_population.append(child_1)
        new_population.append(child_2)
        tmp_population -= set(parent)
    
    for ele in new_population:
        if ele.skill_factors == 0:
            fitness_1 = problems[0].calculate_fitness(ele)
            ele.fitness = [fitness_1, 999999]
        else:
            fitness_2 = problems[1].calculate_fitness(ele)
            ele.fitness = [999999, fitness_2]
    
    population = population + new_population
    problems[0].update_factorial_rank(population)
    problems[1].update_factorial_rank(population)
    
    for ele in population:
        ele.update_skill_factor()
            
    population.sort(key=lambda individual:individual.scalar_fitness, reverse=True)
    population = population[0:population_size]
    
    # _tqdm.set_postfix({
    #     "fitness":population[0].fitness
    # })
    
    min_1 = 9999999
    min_2 = 9999999
    for indi in population:
        # print(indi.to_string())
        min_1 = min(min_1, indi.fitness[0])
        min_2 = min(min_2, indi.fitness[1])
        min_glob_1 = min(min_1, min_glob_1)
        min_glob_2 = min(min_2, min_glob_2)
    
    _tqdm.set_postfix({"task_1":min_glob_1, "task_2":min_glob_2})

# for i in population:
#     print(i.fitness)
