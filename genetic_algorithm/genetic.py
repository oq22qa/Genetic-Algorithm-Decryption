import random
from evaluation import fitness
from evaluation import decrypt

class GA:
    def __init__(self, pop_size, key_length, cipher):
        self.pop_size = pop_size #how many members/chromosomes in the population
        self.key_length = key_length #number of characters/keys in a chromosome
        self.cipher = cipher #cipher text to be operated on
        self.pop = self.create_initial_pop() #start with an initial generated population

    def create_initial_pop(self):
        gene_values = "abcdefghijklmnopqrstuvwxyz-" #all the possible values that can be a key/character within a chromosome combination
        pop = []
        for i in range(self.pop_size): #create chromosome combinations equal to population size by selecting a random gene value and appending to chromosome string according to key size
            chromosome = ''.join(random.choice(gene_values) for j in range(self.key_length)) 
            pop.append(chromosome)
        return pop
    
    def evaluate_pop_fitness(self):
        evaluated_pop = [] #using the provided fitness function in evaluation.py to give fitness scores to population members
        for chromosome in self.pop: #loop through each member of the population
            score = fitness(chromosome, self.cipher) #check fitness
            evaluated_pop.append((chromosome, score)) #add member and its fitness to new array
        return evaluated_pop
    
    def tournament_selection(self, evaluated_pop, k):
        #select a random k members of the population that has already been evaluated for their fitness scores
        competitors = random.sample(evaluated_pop, k)
        #sort them by which has the best fitness (lower is better)
        competitors.sort(key=lambda x: x[1])
        #return the best one
        return competitors[0][0]

    def uniform_crossover(self, p1, p2):
        c1 = []
        c2 = []

        for i in range(self.key_length):
            if random.random() < 0.5:
                c1.append(p1[i])
                c2.append(p2[i])
            else:
                c1.append(p2[i])
                c2.append(p1[i])

        return ''.join(c1), ''.join(c2)
    
    def onepoint_crossover(self, p1, p2):
        random_point = random.randint(1, self.key_length - 1)
        c1 = p1[:random_point] + p2[random_point:]
        c2 = p2[:random_point] + p1[random_point:]
        return c1, c2
    
    #BONUS CROSSOVER: SHUFFLE CROSSOVER, works by initially shuffling the indices/genes of parent chromosomes before applying uniform crossover 
    def shuffle_crossover(self, p1, p2):
        #take the parents and shuffle their genes
        indices = list(range(self.key_length))
        random.shuffle(indices)  

        # apply uniform crossover on shuffled indices
        c1 = [''] * self.key_length
        c2 = [''] * self.key_length

        for i in range(self.key_length):
            idx = indices[i]
            if random.random() < 0.5:
                c1[idx] = p1[idx]
                c2[idx] = p2[idx]
            else:
                c1[idx] = p2[idx]
                c2[idx] = p1[idx]

        return ''.join(c1), ''.join(c2)


    def mutate(self, chromosome, mutation_rate):
        gene_values = "abcdefghijklmnopqrstuvwxyz-"
        new_chromosome = []

        for gene in chromosome:
            if random.random() < mutation_rate:
                new_gene = random.choice(gene_values)
                new_chromosome.append(new_gene)
            else:
                new_chromosome.append(gene)
        return ''.join(new_chromosome)

    def generate(self, generations=100, mutation_rate=0.1, crossover_method="uniform", k=3, elite_count=1, crossover_rate=1.0):
        fitness_over_time = []
        for gen in range(generations):
        
            #first step is evaluating the current pop
            evaluated = self.evaluate_pop_fitness()
            evaluated.sort(key=lambda x: x[1])
            #keep elites
            new_pop=[chromosome for chromosome, i in evaluated[:elite_count]]
            
            while len(new_pop) < self.pop_size:

                p1 = self.tournament_selection(evaluated, k)
                p2 = self.tournament_selection(evaluated, k)

                if random.random() < crossover_rate:
                    if crossover_method == "uniform":
                        c1, c2 = self.uniform_crossover(p1, p2)
                    elif crossover_method == "shuffle":
                        c1, c2 = self.shuffle_crossover(p1, p2)
                    else:
                        c1, c2 = self.onepoint_crossover(p1, p2)
                else:
                    # No crossover, children are clones of parents
                    c1, c2 = p1, p2
                
                c1 = self.mutate(c1,mutation_rate)
                c2 = self.mutate(c2, mutation_rate)

                new_pop.extend([c1, c2])
            
            self.pop = new_pop[:self.pop_size]

            best_chromosome, best_score = evaluated[0]
            fitness_over_time.append(best_score)
            if (gen + 1) % 100 == 0:
                print(f"[Gen {gen+1}] Key: {best_chromosome} | Preview: {decrypt(best_chromosome, self.cipher)[:100]}")
            print(f"Gen {gen+1}: Best score = {best_score:.4f} | Key = {best_chromosome}")

        final_best = min(self.evaluate_pop_fitness(), key=lambda x: x[1])
        self.fitness_over_time = fitness_over_time
        return final_best
        




