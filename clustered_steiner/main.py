import configparser
from init import init_population
from tqdm import tqdm
import random
import utils
from crossover import CrossOver

# random.seed(1)
config_path = "config/config.ini"
config = configparser.ConfigParser()
config.read(config_path)

POPULATION_SIZE = int(config["general"]["population_size"])
NUM_GENERATION = int(config["general"]["num_generation"])
mutation_rate = float(config["general"]["mutation_rate"])
crossover_rate = float(config["general"]["crossover_rate"])

graph_path = "graph.txt"
graph, clusters = utils.load_data(graph_path)
vertexs = set(range(graph.shape[0]))

population = init_population(
    vertexs=vertexs,
    clusters=clusters,
    population_size=POPULATION_SIZE
)

for ele in population:
    fitness = utils.calculate_fitness(
        individual=ele,
        clusters=clusters,
        graph=graph
    )
    ele.set_fitness(fitness)



_tqdm = tqdm(range(NUM_GENERATION))
for _ in _tqdm:
    news_population = []
    mutation_set = set(random.sample(population, k=int(mutation_rate*POPULATION_SIZE)))
    
    crossover_set = list(set(population) - mutation_set)
    mutation_set = list(mutation_set)
    
    for i in range(int(len(crossover_set)/2)):
        parents = random.sample(crossover_set, k=2)
        
        child_1, child_2 = CrossOver.crossover(
            *parents
        )
        news_population.append(child_1)
        news_population.append(child_2)
    
    for indi in mutation_set:
        CrossOver.mutate_gene(indi)
    utils.update_fitness(news_population, graph=graph, clusters=clusters)
    
    population += news_population
    
    population.sort()
    population = population[0:POPULATION_SIZE]
    
    _tqdm.set_postfix({
        "bestfound":population[0].fitness
    })