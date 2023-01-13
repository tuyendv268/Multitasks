import random
from individual import individual

class CrossOver():
    def __init__(self) -> None:
        pass
    
    @classmethod
    def check_steiner_vertexs(cls, individual_1, individual_2):
        assert len(individual_1.steiner_vertexs) == len(individual_2.steiner_vertexs)
        length = len(individual_1.steiner_vertexs)
        
        for i in range(length):
            assert individual_1.steiner_vertexs[i] == individual_2.steiner_vertexs[i]
        
    @classmethod
    def crossover(cls, parent_1, parent_2):
        cls.check_steiner_vertexs(parent_1, parent_2)
        length = len(parent_1.gene)
        
        crossover_index_start, crossover_index_end = None, None
        while crossover_index_end == crossover_index_start:
            crossover_index_start = random.randint(1, length-1)
            crossover_index_end = random.randint(1, length-1)
            
        if crossover_index_start > crossover_index_end:
            tmp = crossover_index_start
            crossover_index_start = crossover_index_end
            crossover_index_end = tmp
        
        gene_1 = parent_1.gene[0:crossover_index_start] + parent_2.gene[crossover_index_start:crossover_index_end] + parent_1.gene[crossover_index_end:]
        cluster_index_1 = parent_1.cluster_index[0:crossover_index_start] + parent_2.cluster_index[crossover_index_start:crossover_index_end] + parent_1.cluster_index[crossover_index_end:]
        steiner_vertexs_1 = parent_1.steiner_vertexs
        
        child_1 = individual(
            steiner_vertexs=steiner_vertexs_1,
            gene=gene_1,
            cluster_index=cluster_index_1
        )
        
        gene_2 = parent_2.gene[0:crossover_index_start] + parent_1.gene[crossover_index_start:crossover_index_end] + parent_2.gene[crossover_index_end:]
        cluster_index_2 = parent_2.cluster_index[0:crossover_index_start] + parent_1.cluster_index[crossover_index_start:crossover_index_end] + parent_2.cluster_index[crossover_index_end:]
        steiner_vertexs_2 = parent_1.steiner_vertexs
        
        child_2 = individual(
            steiner_vertexs=steiner_vertexs_2,
            gene=gene_2,
            cluster_index=cluster_index_2
        )
        
        return child_1, child_2
    
    @classmethod
    def mutate_gene(cls, indi):
        new_gen = list(indi.gene)
        length = len(indi.gene)
        
        index = random.randint(0, length-1)
        new_gen[index] = 1 - new_gen[index]
        indi.gene = tuple(new_gen)
        return indi