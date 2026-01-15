import matplotlib.pyplot as plt
from evaluation import read_encrypted_data
from evaluation import decrypt
from genetic import GA
import random

random.seed(101)
key_len, cipher_text = read_encrypted_data("data/Data1.txt")
ga=GA(pop_size=500, key_length=key_len, cipher=cipher_text)

best_key, best_fitness = ga.generate(generations=50, mutation_rate=0.0, crossover_method="uniform", k=3, elite_count=2, crossover_rate=0.9)

print(f"\nBest key: {best_key}")
print(f"Best fitness: {best_fitness:.4f}")
print(f"Decrypted preview:\n{decrypt(best_key, cipher_text)[:200]}")


plt.plot(ga.fitness_over_time)
plt.title("Fitness Over Generations")
plt.xlabel("Generation")
plt.ylabel("Fitness Score (lower is better)")
plt.grid(True)
plt.tight_layout()
plt.show()
