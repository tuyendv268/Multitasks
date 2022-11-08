import numpy as np
import random
from individual import individual

class TSP:
    def __init__(self, config, idx_probl) -> None:
        self.config = config
        self.map = self.load_map()
        self.idx_probl = idx_probl

    def load_map(self):
        # print("-------------load map------------")
        with open(self.config["path"], "r", encoding="utf-8") as tmp:
            lines  = tmp.readlines()
            lines = [[float(i) for i in line.replace("\n", "").split()] for line in lines]
            map = -1 * np.ones((len(lines) + 1, len(lines) + 1))
            
        for i in range(len(lines)-1):
            x = lines[i][0]
            x_coordinate = np.array(lines[i][1:])
            for j in range(i+1, len(lines)):  
                y = lines[j][0] 
                y_coordinate = np.array(lines[j][1:]) 
                distance = np.linalg.norm(x_coordinate - y_coordinate)
                
                map[int(x), int(y)] = map[int(y), int(x)] = round(distance,2)
        # print("map: ", map)
        return map
    
    def calculate_fitness(self, gene):
        length = int(self.config["gen_length"])
        total = 0
        if len(gene)-1 == length:
            for i in range(length):
                total += self.map[gene[i]][gene[i+1]]
                
            return round(total,3)
        else:
            solution = gene.copy()
            for i in range(length+1, len(gene)):
                solution.remove(i)
                
            for i in range(length):
                total += self.map[solution[i]][solution[i+1]]
                
            return round(total,3)
    
    # def calculate_fitness(self, gene):
    #     length = len(gene)
    #     total = 0
    #     for i in range(length-1):
    #         total += self.map[gene[i]][gene[i+1]]
        
    #     return round(total,3)
    
    def get_fitness(self, individual):
        return individual.get_fitness(self.idx_probl)

    def evaluate(self, population):
        tmp_population =  sorted(population,key=self.get_fitness)
        
        for idx, ele in enumerate(tmp_population):
            ele.set_factorial_rank(self.idx_probl, idx)
        
        return population

        
        