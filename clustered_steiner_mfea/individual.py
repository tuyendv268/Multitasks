import numpy as np

class individual():
    def __init__(self, steiner_vertexs, gene, cluster_index):
        self.steiner_vertexs = steiner_vertexs
        self.gene = gene
        self.cluster_index = cluster_index
        
        self.factorial_ranks = [None, None]
        self.scalar_fitness = None
        self.skill_factors = None
    
    def set_factorial_rank(self, index, factorial_rank):
        self.factorial_ranks[index] = factorial_rank
        
    def update_skill_factor(self):
        factorial_ranks = np.asarray(self.factorial_ranks)
        self.skill_factors = np.argmin(factorial_ranks)
        self.scalar_fitness = 1/(1+np.min(factorial_ranks))
        self.factorial_ranks[1-self.skill_factors] = 9999999
    
    def set_fitness(self, fitness):
        self.fitness = fitness
    
    def get_fitness(self, index):
        return self.fitness[index]
    
    def get_factorial_rank(self, index):
        return self.factorial_ranks[index]
    
    def update_MST(self, MST):
        self.MST = MST
            
    def _to_string(self):
        print(f'steiner_vertexs: {self.steiner_vertexs}')
        print(f'gene: {self.gene}')
        print(f'cluster_index: {self.cluster_index}')