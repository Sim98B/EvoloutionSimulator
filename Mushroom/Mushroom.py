import numpy as np

class Mush:
    def __init__(self, x, y, traits=None):
        self.x = x
        self.y = y
        if traits is None:
            traits = np.random.dirichlet([1,1,1,1])
        self.cap_size, self.stem_length, self.mycelium_density, self.spore_size = traits
        self.fitness = 0.0

    def compute_fitness(self, env):
        sun_energy = self.cap_size * self.stem_length * env['light']
        soil_energy = self.mycelium_density * env['nutrients']
        cost = self.cap_size*0.5 + self.stem_length*0.3 + self.mycelium_density*0.4 + self.spore_size*0.2
        self.fitness = sun_energy + soil_energy - cost
        return self.fitness

    def reproduce(self):
        mutation = np.random.normal(0, 0.05, 4)
        new_traits = np.array([self.cap_size, self.stem_length, self.mycelium_density, self.spore_size]) + mutation
        new_traits = np.clip(new_traits, 0, None)
        new_traits /= new_traits.sum()
        return Mush(new_traits)
