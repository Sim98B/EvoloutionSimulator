import numpy as np

class Mush():
    def __init__(self, x:float | int, y: float):
        self.x = x
        self.y = y
        total_size = np.random.normal(7,2)
        allocation = np.random.dirichlet(alpha=np.ones(4))
        self.cap, self.stem, self.mycelium, self.spore = total_size * allocation
        self.cap_genes = {
            "a": np.random.rand(),
            "b": np.random.rand(),
            "c": np.random.rand()
        }
        self.mycelium_genes = {
            "d": np.random.rand(),
            "e": np.random.rand(),
            "f": np.random.rand()
        }
        self.stem_genes = {
            "g": np.random.rand(),
            "h": np.random.rand(),
            "i": np.random.rand()
        }
        self.spore_genes = {
            "j": np.random.rand(),
            "k": np.random.rand(),
            "m": np.random.rand(),
            "n": np.random.rand()
        }
        # Cap
        self.spore_output = 1 + self.cap_genes["a"] * np.sqrt(self.cap)
        self.cap_energy_cost = self.cap_genes["b"] * self.cap
        self.cap_risk = 1 + self.cap_genes["c"] * self.cap
        # Mycelium
        self.energy_absorbed = self.mycelium * (1 + self.mycelium_genes["d"])
        self.maintenance_cost = self.mycelium_genes["e"] * self.mycelium
        self.expansion_speed = self.mycelium / (1 + self.mycelium_genes["f"])
        # Stem
        # Stem
        self.stem_dispersion_radius = self.stem * (1 + self.stem_genes["g"])
        self.stem_fail_prob = 1 + self.stem_genes["h"] * self.stem
        self.stem_structural_cost = self.stem_genes["i"] * self.stem
        # Spore Size/Resistance
        self.spore_germ_prob = 1 + self.spore_genes["j"] * self.spore
        self.spore_survival = 1 + self.spore_genes["k"] * self.spore
        self.spore_number = self.spore / (1 + self.spore_genes["m"] * self.spore)
        self.spore_dispersion_radius = self.spore * (1 - self.spore_genes["n"])

        self.fitness = 0.0

    def compute_fitness(self, wood_env):
        radius = self.mycelium * 0.25
        local_humidity = wood_env.get_humidity(self.x, self.y, radius)
        energy_gain = self.energy_absorbed * local_humidity
        cost = self.cap_energy_cost + self.stem_structural_cost + self.maintenance_cost
        risk_factor = 1 / (self.cap_risk + self.stem_fail_prob)
        self.fitness = (energy_gain - cost) * risk_factor
        return self.fitness

    def reproduce(self, wood_env):
        offspring_list = []

        base_spores = self.cap + self.spore + self.stem
        expected_spores = max(1, int(np.random.poisson(lam=base_spores * 0.2 * self.spore_output)))

        for _ in range(expected_spores):
            new_cap_genes = {k: np.clip(v + np.random.normal(0, 0.01), 0, 1) for k, v in self.cap_genes.items()}
            new_mycelium_genes = {k: np.clip(v + np.random.normal(0, 0.01), 0, 1) for k, v in self.mycelium_genes.items()}
            new_stem_genes = {k: np.clip(v + np.random.normal(0, 0.01), 0, 1) for k, v in self.stem_genes.items()}
            new_spore_genes = {k: np.clip(v + np.random.normal(0, 0.01), 0, 1) for k, v in self.spore_genes.items()}

            new_cap = max(0.1, self.cap + np.random.normal(0, 0.5))
            new_stem = max(0.1, self.stem + np.random.normal(0, 0.5))
            new_mycelium = max(0.1, self.mycelium + np.random.normal(0, 0.5))
            new_spore = max(0.1, self.spore + np.random.normal(0, 0.5))

            max_dispersion = self.stem_dispersion_radius + self.spore_dispersion_radius * 10
            angle = np.random.uniform(0, 2 * np.pi)
            radius = np.random.uniform(0, max_dispersion)
            dx = radius * np.cos(angle)
            dy = radius * np.sin(angle)
            new_x = np.clip(self.x + dx, 0, 1)
            new_y = np.clip(self.y + dy, 0, 1)

            local_hum = wood_env.get_humidity(new_x, new_y, new_mycelium * 0.25)
            local_quality = local_hum
            germ_prob = np.clip(new_spore_genes["j"] * local_quality, 0, 1)  # usa gene 'j' per germinabilità

            if np.random.rand() < germ_prob:
                child = Mush(new_x, new_y)  # scale_factor=1, poi aggiorniamo i fenotipi e geni
                child.cap, child.stem, child.mycelium, child.spore = new_cap, new_stem, new_mycelium, new_spore
                child.cap_genes = new_cap_genes
                child.mycelium_genes = new_mycelium_genes
                child.stem_genes = new_stem_genes
                child.spore_genes = new_spore_genes
                offspring_list.append(child)

        return offspring_list
