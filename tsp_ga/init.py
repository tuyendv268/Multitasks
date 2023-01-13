import numpy as np
import random
from individual import individual

class Init:
    def __init__(self) -> None:
        pass
    
    @classmethod
    def init_gene(cls, length):
        # num_city = int(self.config["general"]["num_city"])
        gene = [i for i in range(2, length+1)]

        random.shuffle(gene)
        gene = [1] + gene + [1]
        return gene
        
    @classmethod
    def init_population(cls, population_size, gene_length):
        population = []
        
        for index in range(population_size):
            gene = cls.init_gene(gene_length)
            tmp_indi = individual(gene=gene)
            population.append(tmp_indi)
        
        return population