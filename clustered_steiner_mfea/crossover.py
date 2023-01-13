import random
from individual import individual
import numpy as np
import copy
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
        # cls.check_steiner_vertexs(parent_1, parent_2)
        length = len(parent_1.gene)
        
        crossover_index_start, crossover_index_end = None, None
        while crossover_index_end == crossover_index_start:
            crossover_index_start = random.randint(1, length-1)
            crossover_index_end = random.randint(1, length-1)
            
        if crossover_index_start > crossover_index_end:
            tmp = crossover_index_start
            crossover_index_start = crossover_index_end
            crossover_index_end = tmp
        
        parent_1_gene = list(parent_1.gene)
        parent_2_gene = list(parent_2.gene)
        
        parent_1_cluster_index = list(parent_1.cluster_index)
        parent_2_cluster_index = list(parent_2.cluster_index)
        
        gene_1 = parent_1_gene[0:crossover_index_start] + parent_2_gene[crossover_index_start:crossover_index_end] + parent_1_gene[crossover_index_end:]
        cluster_index_1 = parent_1_cluster_index[0:crossover_index_start] + parent_2_cluster_index[crossover_index_start:crossover_index_end] + parent_1_cluster_index[crossover_index_end:]
        steiner_vertexs_1 = parent_1.steiner_vertexs
        
        child_1 = individual(
            steiner_vertexs=steiner_vertexs_1,
            gene=np.array(gene_1),
            cluster_index=np.array(cluster_index_1)
        )
        
        gene_2 = parent_2_gene[0:crossover_index_start] + parent_1_gene[crossover_index_start:crossover_index_end] + parent_2_gene[crossover_index_end:]
        cluster_index_2 = parent_2_cluster_index[0:crossover_index_start] + parent_1_cluster_index[crossover_index_start:crossover_index_end] + parent_2_cluster_index[crossover_index_end:]
        steiner_vertexs_2 = parent_1.steiner_vertexs
        
        child_2 = individual(
            steiner_vertexs=steiner_vertexs_2,
            gene=np.array(gene_2),
            cluster_index=np.array(cluster_index_2)
        )
        
        return child_1, child_2
    
    @classmethod
    def mutate(cls, indi, num_cluster):
        length = len(indi.gene)
        new_indi = copy.deepcopy(indi)
        index = random.randint(0, length-1)
        if new_indi.gene[index] == 0:
            new_indi.gene[index] = 1
            new_indi.cluster_index[index] = random.randint(0, num_cluster-1)
        else:
            new_indi.gene[index] = 0
            new_indi.cluster_index[index] = -1
        return new_indi