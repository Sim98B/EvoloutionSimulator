import numpy as np                      ######################## AGGIUGERE ALTRO NUTRIENTE (ROBA MORTA) ###########################

class Mush:
    def __init__(self, x, y, traits=None):
        self.x = x
        self.y = y
        if traits is None:
            traits = np.random.dirichlet([1,1,1,1])
        self.cap_size, self.stem_length, self.mycelium_density, self.spore_size = traits
        self.fitness = 0.0

    def compute_fitness(self, wood_env):
        radius = self.mycelium_density * 0.25  # scala ecologica del micelio
        local_humidity = wood_env.get_local_humidity(self.x, self.y, radius)
        soil_energy = self.mycelium_density * local_humidity
        sun_energy = self.cap_size * self.stem_length  # puoi moltiplicare per un coefficiente esterno se vuoi luce
        cost = 0.5 * self.cap_size + 0.3 * self.stem_length + 0.4 * self.mycelium_density + 0.2 * self.spore_size
        self.fitness = sun_energy + soil_energy - cost
        return self.fitness

    def reproduce(self):
        mutation = np.random.normal(0, 0.05, 4)
        new_traits = np.array([self.cap_size, self.stem_length, self.mycelium_density, self.spore_size]) + mutation
        new_traits = np.clip(new_traits, 0, None)
        new_traits /= new_traits.sum()
        return Mush(new_traits)
