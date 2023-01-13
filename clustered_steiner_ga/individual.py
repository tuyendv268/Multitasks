
class individual():
    def __init__(self, steiner_vertexs, gene, cluster_index):
        self.steiner_vertexs = steiner_vertexs
        self.gene = gene
        self.cluster_index = cluster_index
    
    def set_fitness(self, fitness):
        self.fitness = fitness
        
    def update_MST(self, MST):
        self.MST = MST
        
    def __lt__(self, other):
        return self.fitness < other.fitness
    
    def __gt__(self, other):
        return self.fitness > other.fitness
    
    def _to_string(self):
        print(f'steiner_vertexs: {self.steiner_vertexs}')
        print(f'gene: {self.gene}')
        print(f'cluster_index: {self.cluster_index}')