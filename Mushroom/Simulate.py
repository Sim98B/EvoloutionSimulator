import numpy as np
import matplotlib.pyplot as plt

class Mush:
    def __init__(self, traits=None):
        if traits is None:
            traits = np.random.dirichlet([1,1,1,1])
        self.cap_size, self.stem_length, self.mycelium_density, self.spore_size = traits
        self.fitness = 0.0

    def compute_fitness(self, env):
        # Energia acquisita
        sun_energy = self.cap_size * self.stem_length * env['light']
        soil_energy = self.mycelium_density * env['nutrients']
        # Costo energetico
        cost = self.cap_size*0.5 + self.stem_length*0.3 + self.mycelium_density*0.4 + self.spore_size*0.2
        self.fitness = sun_energy + soil_energy - cost
        return self.fitness

    def reproduce(self):
        # Piccole mutazioni mantenendo somma ≈ 1
        mutation = np.random.normal(0, 0.05, 4)
        new_traits = np.array([self.cap_size, self.stem_length, self.mycelium_density, self.spore_size]) + mutation
        new_traits = np.clip(new_traits, 0, None)
        new_traits /= new_traits.sum()  # Normalizza
        return Mush(new_traits)

# Ambiente
env = {'light': 1.0, 'nutrients': 1.0}

# Popolazione iniziale
population = [Mush() for _ in range(100)]

# Simulazione generazionale
for gen in range(20):
    # Calcola fitness
    for m in population:
        m.compute_fitness(env)
    # Selezione top 50%
    population.sort(key=lambda x: x.fitness, reverse=True)
    survivors = population[:len(population)//2]
    # Riproduzione
    offspring = [s.reproduce() for s in survivors]
    population = survivors + offspring
    print(len(population), len(survivors), len(offspring))

# Visualizza cluster di tratti
traits_matrix = np.array([[m.cap_size, m.stem_length, m.mycelium_density, m.spore_size] for m in population])
plt.scatter(traits_matrix[:,0], traits_matrix[:,1], c=traits_matrix[:,2], s=1000*traits_matrix[:,3], cmap='seismic')
plt.xlabel('Cap Size')
plt.ylabel('Stem Length')
plt.title('Fungi clusters after evolution')
plt.colorbar(label='Mycelium Density (color)')
plt.show()
print(len(population))
