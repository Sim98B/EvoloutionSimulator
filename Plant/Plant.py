import numpy as np
import random
#np.random.seed(0)

class Plant:
    def __init__(self,total_energy=1):
        self.total_energy = total_energy

        props = np.random.dirichlet([1, 1, 1])
        self.alpha, self.beta, self.gamma = props
        self.height = self.alpha * self.total_energy
        self.leaf   = self.beta * self.total_energy
        self.roots  = self.gamma * self.total_energy
        self. stress_days = 0
        self.age = 0
        self.alive = True

    def daily_adaptation(self, sun, water):
        if not self.alive:
            return

        eps = 1e-8
        c, d, k = 0.5, 0.3, 0.05

        effective_sun = sun * (1 + c * self.height) / (1 + d * self.height)
        sun_gain = effective_sun * (self.leaf / (1 + self.leaf))
        water_gain = max(0, water * (self.roots / (1 + self.roots)) - 0.05 * self.leaf * sun)

        growth = min(sun_gain, water_gain)
        total_mass = self.height + self.leaf + self.roots
        maintenance = 0.02 * total_mass
        growth = max(0, growth - maintenance)

        # plasticità
        imbalance = np.tanh(3 * (sun_gain - water_gain) / (sun_gain + water_gain + eps))
        plastic_shift = k * imbalance * growth
        self.beta -= plastic_shift
        self.gamma += plastic_shift
        water_stress = max(0, sun_gain - water_gain)
        self.height -= 0.05 * water_stress
        self.height = max(0.01, self.height)

        props = np.clip([self.alpha, self.beta, self.gamma], 0.01, None)
        props /= np.sum(props)
        self.alpha, self.beta, self.gamma = props

        self.height += self.alpha * growth
        self.leaf += self.beta * growth
        self.roots += self.gamma * growth

        threshold = 0.05
        if self.height < threshold or self.leaf < threshold or self.roots < threshold:
            self.alive = False

        # DECAY e MORTALITÀ
        total_mass = self.height + self.leaf + self.roots
        decay_factor = 0.03  # perde 5% se stress
        if sun_gain < 0.01 or water_gain < 0.01:
            self.height *= (1 - decay_factor)
            self.leaf *= (1 - decay_factor)
            self.roots *= (1 - decay_factor)

        if total_mass < 0.05:
            self.alive = False

        if self.alive:
            self.age += 1

    def generate_offspring(self, trait_std=0.05, mutation_prob=0.05, mutation_std=0.1):
        """
        Genera un figlio della pianta con tratti derivati dai genitori
        """
        # campioniamo i tratti
        alpha = np.random.normal(self.alpha, trait_std)
        beta  = np.random.normal(self.beta, trait_std)
        gamma = np.random.normal(self.gamma, trait_std)

        # mutazione rara
        if random.random() < mutation_prob:
            alpha += np.random.normal(0, mutation_std)
            beta  += np.random.normal(0, mutation_std)
            gamma += np.random.normal(0, mutation_std)

        traits = np.clip([alpha, beta, gamma], 0.01, None)
        traits /= np.sum(traits)

        child = Plant(total_energy=self.total_energy)
        child.alpha, child.beta, child.gamma = traits
        child.height = child.alpha * child.total_energy
        child.leaf   = child.beta  * child.total_energy
        child.roots  = child.gamma * child.total_energy

        return child