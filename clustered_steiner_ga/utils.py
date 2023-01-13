import numpy as np
import random
import pandas as pd
from collections import Counter

def load_data(path):
    with open(path, "r") as tmp:
        lines = tmp.readlines()

    graph = parse_graph(lines)
    clusters = parse_clusters(lines)
    
    return graph, clusters

def parse_graph(lines):
    num_vertexs = int(lines[0].replace("\n", "").split(" ")[0])
    
    weights = [line.replace("\n", "").split("\t") for line in lines[6:6+num_vertexs]]
    weights = [[int(col.strip()) for col in line if len(col.strip()) != 0] for line in weights]
    weights = np.array(weights)
     
    return weights

def parse_clusters(lines):
    num_clusters = int(lines[0].replace("\n", "").split(" ")[1])
    
    clusters = lines[-num_clusters:]
    clusters = [line.replace("\n", "") for line in clusters]
    clusters = [line.split()[1:-1] for line in clusters]
    clusters = [[int(col)-1 for col in line] for line in clusters]
    clusters = tuple([tuple(line) for line in clusters])
    
    return clusters

def find_MST(graph, vertexs):
    N = graph.shape[0]
    
    marks = [0]*N
    marks[0] = True
    
    MST = []
    INF = 999999
    index = 0

    while (index < N - 1):
        minimum = INF
        a,b = 0, 0
        for m in range(N):
            if not marks[m]:
                continue
            for n in range(N):
                if not ((not marks[n]) and graph[m][n]):  
                    continue
                if minimum > graph[m][n]:
                    minimum = graph[m][n]
                    a = m; b = n
        marks[b] = True
        index += 1
        
        MST.append([vertexs[a], vertexs[b], graph[a][b]])
    
    return np.array(MST)
def convert2set(clusters):
    new_clusters = [set(cluster) for cluster in clusters]
    
    return new_clusters

def remove_non_required_vertex_with_degree(clusteres, graphs, represent_local_vertexs):
    #  remove non-require vextex in clusters
    new_graph = []
    for index in range(len(clusteres)):
        cluster = set(clusteres[index])
        graph = graphs[index]
        
        # count degree
        degrees = Counter([v for e in graphs[index] for v in e])
        remove_vertexs = set(
                [key for key, value in degrees.items() 
                if (value==1 and key not in cluster and key != represent_local_vertexs[index])]
            )
        # print(remove_vertexs)
        
        for edge in graph:
            if edge[0] in remove_vertexs or edge[1] in remove_vertexs:
                continue
            new_graph.append(edge)
    return new_graph

def calculate_fitness(individual, clusters, graph):
    tmp_clusters = convert2set(clusters)
    steiner_vertexs = list(individual.steiner_vertexs)
    cluster_indexs = list(individual.cluster_index)
    represent_local_vertexs = [-1]*len(clusters)
    
    # print("gene: ", individual.gene)
    # print("cluster_indexs: ", cluster_indexs)
    # print("steiner_vertexs: ", steiner_vertexs)
    # print("clusters: ", tmp_clusters)

    for index, is_select in enumerate(individual.gene):
        if is_select == 0 or cluster_indexs[index] == -1:
            continue
        cluster_index = cluster_indexs[index]

        if represent_local_vertexs[cluster_index] == -1:
            represent_local_vertexs[cluster_index] = steiner_vertexs[index]
            # tmp_clusters[cluster_index].add(steiner_vertexs[index])
        else:
            if random.randint(0, 100) / 100.0 > 0.9:
                represent_local_vertexs[cluster_index] = steiner_vertexs[index]
    
    # print("represent_local_vertexs: ", represent_local_vertexs)
    for index, vertex in enumerate(represent_local_vertexs):
        if vertex == -1:
            continue
        tmp_clusters[index].add(vertex)
    # print("news tmp_clusters: ", tmp_clusters)

    clustered_steiners = []

    # find MST on local clustered
    for cluster in tmp_clusters:
        cluster = list(cluster)
        clustered_steiners.append(find_MST(graph[cluster, :][:, cluster], cluster).tolist())
        
    clustered_steiners = remove_non_required_vertex_with_degree(
        clusteres=clusters,
        graphs=clustered_steiners,
        represent_local_vertexs=represent_local_vertexs
    )

    # print(f"1 represent_local_vertexs: {represent_local_vertexs}")
    tmp_clusters = convert2set(clusters)
    for index, represent in enumerate(represent_local_vertexs):
        if represent != -1:
            continue
        represent_local_vertexs[index] = random.choice(list(tmp_clusters[index]))
    # print(f"2 represent_local_vertexs: {represent_local_vertexs}")
    
    # sample 1 dinh dai dien trong cac dinh steiner co chung 1 cluster index
    tmp = pd.DataFrame({
        "steiner_vertex":steiner_vertexs,
        "cluster_index":cluster_indexs
    })
    
    # print("steiner_vertexs: ", steiner_vertexs)
    # print("cluster_index: ", cluster_indexs)
    
    represent_steiner_vertexs = []

    for name, group in tmp.groupby("cluster_index"):
        if name == -1:
            represent_steiner_vertexs += group["steiner_vertex"].tolist()
            continue
        # represent_steiner_vertexs += group.sample(1)["steiner_vertex"].tolist()
    
    # print("represent_steiner_vertexs: ", represent_steiner_vertexs)
    # print("represent_local_vertexs: ", represent_local_vertexs)
    # print()

    news_vertexs = list(set(represent_steiner_vertexs + represent_local_vertexs))
    clustered_steiners += find_MST(graph[news_vertexs, :][:, news_vertexs], news_vertexs).tolist()
    
    total = 0
    for i in clustered_steiners:
        total += graph[i[0], i[1]]
    
    return total

def update_fitness(population, clusters, graph):
    for individual in population:
        fitness = calculate_fitness(
            clusters=clusters,
            graph=graph,
            individual=individual
        )
        
        individual.set_fitness(fitness)