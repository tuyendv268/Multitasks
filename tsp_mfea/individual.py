import numpy as np

class individual:
    def __init__(self, gene) -> None:
        self.gene = gene
        self.fitness = None
        
        self.factorial_ranks = [-1, -1]
        self.scalar_fitnesss = None
        self.skill_factors = None    
        
    def set_fitness(self, index, fitness):
        self.fitness[index] = fitness
    
    def set_factorial_rank(self, index, factorial_rank):
        self.factorial_ranks[index] = factorial_rank
    
    def update_skill_factor(self):
        factorial_ranks = np.asarray(self.factorial_ranks)
        self.skill_factors = np.argmin(factorial_ranks)
        self.scalar_fitnesss = 1 / (1 + np.min(factorial_ranks))
        self.factorial_ranks[abs(1-self.skill_factors)] = 999999
    
    def get_fitness(self, index):
        return self.fitness[index]
    
    def get_factorial_rank(self, index):
        return self.factorial_ranks[index]
    
    
    def to_string(self):
        return f"gene: {self.gene} - fitness: {self.fitness} - factorial_rank: {self.factorial_ranks} - scalar_fitness: {self.scalar_fitnesss} - skill_factor: {self.skill_factors}"