import numpy as np
import random
import pandas as pd
from collections import Counter
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

def init_individual(vertexs, num_clusters):
    vertexs = list(vertexs)
    gene = [random.randint(0,1) for i in vertexs]
    cluster_index = [random.randint(-1, num_clusters-1) for i in vertexs]
    
    indi = individual(
        steiner_vertexs=None,
        gene=np.array(gene),
        cluster_index=np.array(cluster_index)
    )
    
    return indi

def init_population(vertexs, population_size, num_clusters):
    populations = []
    
    for _ in range(population_size):
        indi = init_individual(
            vertexs=vertexs,
            num_clusters=num_clusters
        )
        
        populations.append(indi)
        
    return populations
    
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

def remove_non_required_vertex_with_degree(clusteres, graphs):
    clusteres = set([v for clust in clusteres for v in clust])
    
    tmp_graphs = []
    for edge in graphs:
        tmp_graphs.append(edge[0:2])    
    new_graph = []
    
    degrees = Counter([v for e in tmp_graphs for v in e])
    remove_vertexs = set(
            [key for key, value in degrees.items() 
            if (value==1 and key not in clusteres)]
        )
    
    for edge in graphs:
        if edge[0] in remove_vertexs or edge[1] in remove_vertexs:
            continue
        new_graph.append(edge)
    return new_graph

def calculate_fitness(_steiner_vertexs, _cluster_index, _gene, clusters, graph):
    tmp_clusters = convert2set(clusters)
    steiner_vertexs = list(_steiner_vertexs)
    cluster_indexs = list(_cluster_index)
    represent_local_vertexs = [-1]*len(clusters)
    
    for index, is_select in enumerate(_gene):
        if is_select == 0 or cluster_indexs[index] == -1:
            continue
        cluster_index = cluster_indexs[index]

        if represent_local_vertexs[cluster_index] == -1:
            represent_local_vertexs[cluster_index] = steiner_vertexs[index]
        else:
            represent_local_vertexs[cluster_index] = steiner_vertexs[index]
    
    # print("represent_local_vertexs: ", represent_local_vertexs)
    for index, vertex in enumerate(represent_local_vertexs):
        if vertex == -1:
            continue
        tmp_clusters[index].add(vertex)

    clustered_steiners = []

    # find MST on local clustered
    for cluster in tmp_clusters:
        cluster = list(cluster)
        clustered_steiners.append(find_MST(graph[cluster, :][:, cluster], cluster).tolist())

    tmp_clusters = convert2set(clusters)
    for index, represent in enumerate(represent_local_vertexs):
        if represent != -1:
            continue
        # represent_local_vertexs[index] = random.choice(list(tmp_clusters[index]))
        represent_local_vertexs[index] = list(tmp_clusters[index])[0]
    
    # sample 1 dinh dai dien trong cac dinh steiner co chung 1 cluster index
    tmp = pd.DataFrame({
        "steiner_vertex":steiner_vertexs,
        "cluster_index":cluster_indexs
    })
        
    represent_steiner_vertexs = []

    for name, group in tmp.groupby("cluster_index"):
        if name == -1:
            represent_steiner_vertexs += group["steiner_vertex"].tolist()
            continue
        # represent_steiner_vertexs += group.sample(1)["steiner_vertex"].tolist()
    
    news_vertexs = list(set(represent_steiner_vertexs + represent_local_vertexs))
    clustered_steiners = [v for e in clustered_steiners for v in e]
    
    clustered_steiners += find_MST(graph[news_vertexs, :][:, news_vertexs], news_vertexs).tolist()
    
    tmp_clusters = convert2set(clusters)
    clustered_steiners = remove_non_required_vertex_with_degree(
        clusteres=tmp_clusters,
        graphs=clustered_steiners
    )

    total = 0
    for i in clustered_steiners:
        total += graph[i[0], i[1]]
    
    return total