class individual():
    def __init__(self, gene) -> None:
        self.fitness = None
        self.gene = gene
    
    # def __lt__(self, other):
    #     return self.fitness < other.fitness
    
    # def __gt__(self, other):
    #     return self.fitness > other.finess