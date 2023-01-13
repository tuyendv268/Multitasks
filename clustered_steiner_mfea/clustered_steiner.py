import utils
import numpy as np

class Clustered_Steiner():
    def __init__(self, path, idx) -> None:
        self.map = map
        self.idx = idx
        self.graph, self.require_vertexs = utils.load_data(
            path=path
        )
        self.num_dim = self.graph.shape[0]
        self.num_cluster = len(self.require_vertexs)
        
        self.init_ignore_vertexs()
        self.steiner_vertexs = np.array([i for i in range(self.num_dim) if i not in self.clusters])
    
    def init_ignore_vertexs(self):
        tmps = []
        for ele in self.require_vertexs:
            tmps += list(ele)
        self.clusters = set(tmps)
        
    def get_fitness(self, individual):
        return individual.get_fitness(self.idx)
        
    def init_factorial_rank(self, population):
        tmp_population = sorted(population, key=self.get_fitness)
        
        for idx, ele in enumerate(tmp_population):
            ele.set_factorial_rank(self.idx, idx)
        
        return population
        
    def parse_individual(self, individual):
        _gene = individual.gene[self.steiner_vertexs]
        _steiner_vertexs= self.steiner_vertexs
        _cluster_index = individual.cluster_index[self.steiner_vertexs]
        
        for index in range(len(_cluster_index)):
            if _cluster_index[index] >= self.num_cluster:
                _cluster_index[index] = _cluster_index[index] - self.num_cluster
        
        return _gene, _steiner_vertexs, _cluster_index
        
    def calculate_fitness(self, individual):
        _gene, _steiner_vertexs, _cluster_index = self.parse_individual(
                individual=individual
        )
        fitness = utils.calculate_fitness(
            _steiner_vertexs= _steiner_vertexs, 
            _cluster_index= _cluster_index, 
            _gene= _gene, 
            clusters=self.require_vertexs, 
            graph=self.graph)
        
        return fitness
    
    def update_fitness(self, population):
        for individual in population:
            _gene, _steiner_vertexs, _cluster_index = self.parse_individual(
                individual=individual
            )
            fitness = utils.calculate_fitness(
                _steiner_vertexs= _steiner_vertexs, 
                _cluster_index= _cluster_index, 
                _gene= _gene, 
                clusters=self.require_vertexs, 
                graph=self.graph)
            individual.set_fitness(fitness)
            
    def update_factorial_rank(self, population):
        tmp_population =  sorted(population,key=self.get_fitness)
        
        for idx, ele in enumerate(tmp_population):
            ele.set_factorial_rank(self.idx, idx)
        
        return population
    