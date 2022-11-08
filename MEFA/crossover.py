from individual import individual
import random

class Crossover:
    def __init__(self) -> None:
        pass
    
    @classmethod
    def update_mark(cls, mark, arrived):
        for i in arrived:
            mark[i] = -1
        return mark
    
    @classmethod
    def get_cycles(cls, gene_1, gene_2):
        mark = [0 for i in range(len(gene_1))]

        res, tmp_cycle = [], []
        cur_idx = 0
        start = gene_1[cur_idx]
        
        while(True):
            while(mark[cur_idx] == -1):
                cur_idx += 1
                if cur_idx >= len(gene_1)-1:
                    break
                start = gene_1[cur_idx]
            if cur_idx >= len(gene_1) - 1:
                break
            tmp_2 = gene_2[cur_idx]
            tmp_cycle.append(cur_idx)
            if tmp_2 == start:
                mark = cls.update_mark(mark, tmp_cycle)
                res.append(tmp_cycle)
                tmp_cycle = []; cur_idx = 0
            
            cur_idx = gene_1.index(tmp_2)  
        return res
    
    @classmethod
    def crossover_PMX(cls, parent_1, parent_2):
        cycles = cls.get_cycles(parent_1.gene, parent_2.gene)
        # print(f"cycles: {cycles}")
        
        length = len(parent_1.gene)
        child_1, child_2 = individual(gene=[-1]*length), individual(gene=[-1]*length)
        turn = 0
        for cycle in cycles:
            if turn == 0:
                for index in cycle:
                    child_1.gene[index] = parent_1.gene[index]
                    child_2.gene[index] = parent_2.gene[index]
                turn = 1
            else:
                for index in cycle:
                    child_1.gene[index] = parent_2.gene[index]
                    child_2.gene[index] = parent_1.gene[index]
                turn = 0
        child_1.gene[-1] = 1
        child_2.gene[-1] = 1

        return child_1, child_2
    @classmethod
    def mutita_gen(self, individual):
        gene = individual.gene
        while(True):
            r1 = random.randint(2, len(gene)-2)
            r2 = random.randint(2, len(gene)-2)
            if (r1 != r2):
                temp = gene[r1]
                gene[r1] = gene[r2]
                gene[r2] = temp
                break
        individual.gene = gene
        return individual

