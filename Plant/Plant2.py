import numpy as np
import random

class Plant:
    def __init__(self, total_energy=1, traits=None):
        self.total_energy = total_energy

        if traits is None:
            props = np.random.dirichlet([1, 1, 1])
        else:
            props = traits

        self.alpha, self.beta, self.gamma = props

        # tratti strutturali fissi
        self.height = self.alpha * self.total_energy
        self.leaf   = self.beta  * self.total_energy
        self.roots  = self.gamma * self.total_energy

        self.alive = True

    def survive(self, sun_hits, water_hits, min_energy=1):
        """
        Sopravvive solo se intercetta almeno min_energy unità totali.
        """
        if sun_hits + water_hits < min_energy:
            self.alive = False

    def generate_offspring(self,
                           trait_std=0.05,
                           mutation_prob=0.05,
                           mutation_std=0.1):

        alpha = np.random.normal(self.alpha, trait_std)
        beta  = np.random.normal(self.beta, trait_std)
        gamma = np.random.normal(self.gamma, trait_std)

        if random.random() < mutation_prob:
            alpha += np.random.normal(0, mutation_std)
            beta  += np.random.normal(0, mutation_std)
            gamma += np.random.normal(0, mutation_std)

        traits = np.clip([alpha, beta, gamma], 0.01, None)
        traits /= np.sum(traits)

        return Plant(total_energy=self.total_energy, traits=traits)