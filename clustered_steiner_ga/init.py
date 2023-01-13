import random
import numpy as np
from individual import individual

def init_tree_from_vertexs_set(vertexs, graph):
    selected_vertexs = set([])
    init_tree = []

    u = random.choice(list(vertexs))
    vertexs.remove(u)
    selected_vertexs.add(u)

    while len(vertexs) != 0:
        u = random.choice(list(selected_vertexs))
        v = random.choice(list(vertexs))
        while graph[u][v] == 0:
            v = random.choice(list(vertexs))
            
        init_tree.append([u, v])
        
        vertexs.remove(v)
        selected_vertexs.add(v)
    
    return np.array(init_tree)

def init_individual(steiner_vertexs, num_clusters):
    steiner_vertexs = list(steiner_vertexs)
    gene = [random.randint(0,1) for i in steiner_vertexs]
    cluster_index = [random.randint(-1, num_clusters-1) for i in steiner_vertexs]
    
    indi = individual(
        steiner_vertexs=tuple(steiner_vertexs),
        gene=tuple(gene),
        cluster_index=tuple(cluster_index)
    )
    
    return indi

def init_population(vertexs, population_size, clusters):
    clustered_vertexs = []
    num_clusters = len(clusters)
        
    for cluster in clusters:
        clustered_vertexs += list(cluster)
    required_vertexs = set(clustered_vertexs)

    steiner_vertexs = vertexs - required_vertexs
    populations = []
    
    for _ in range(population_size):
        indi = init_individual(
            steiner_vertexs=steiner_vertexs,
            num_clusters=num_clusters
        )
        
        populations.append(indi)
        
    return populations
    