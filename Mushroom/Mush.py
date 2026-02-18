import numpy as np

class Mush:
    def __init__(self, x:float | int, y: float):
        self.x = x
        self.y = y
        total_size = np.random.normal(10,2)
        allocation = np.random.dirichlet(alpha=np.ones(4))
        self.cap, self.stem, self.mycelium, self.spore = total_size * allocation
        self.cap_genes = {
            "a": np.random.rand(),
            "b": np.random.rand(),
            "c": np.random.rand()
        }
        self.mycelium_genes = {
            "d": np.random.rand(),  # efficienza assorbimento
            "e": np.random.rand(),  # costo manutenzione
            "f": np.random.rand(),  # dispersion/espansione
            "g": np.random.rand(),  # growth rate
            "h": np.random.rand()  # branching density
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
        self.expansion_speed = self.mycelium / (1 + self.mycelium_genes["f"])
        self.mycelial_growth_rate = (self.mycelium * (0.2 + self.mycelium_genes["g"]))
        self.branching_density = 0.5 + self.mycelium_genes["h"]
        self.energy_absorbed = (self.mycelium * (1 + self.mycelium_genes["d"]) * np.log1p(self.branching_density))
        self.maintenance_cost = (self.mycelium * self.mycelium_genes["e"] * (1 + self.branching_density))
        self.growth_cost = self.mycelial_growth_rate * 0.5
        self.total_mycelium_cost = self.maintenance_cost + self.growth_cost
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

    def compute_competitors(self, population):
        positions = np.array([[m.x, m.y] for m in population])
        my_pos = np.array([self.x, self.y])
        distances = np.linalg.norm(positions - my_pos, axis=1)
        mask_self = distances > 0
        competitors = np.sum(distances[mask_self] < self.mycelium * 0.25)
        return competitors

    def compute_fitness(self, wood_env, population):
        radius = self.mycelium * 0.25
        local_food = wood_env.get_nutrients(self.x, self.y, radius, wood_env.nutrients_map)
        population_sorted = sorted(population, key=lambda m: m.mycelial_growth_rate * m.branching_density, reverse=True)
        competitors = self.compute_competitors(population_sorted)
        #share_factor = 1 / np.sqrt(competitors + 1)
        share_factor = 1 / (competitors + 1.5)
        energy_gain = self.energy_absorbed * local_food * share_factor
        cost = self.cap_energy_cost + self.stem_structural_cost + self.maintenance_cost
        risk_factor = 1 / (self.cap_risk + self.stem_fail_prob)
        self.fitness = (energy_gain - cost) * risk_factor
        return self.fitness

    def reproduce(self, wood_env):
        base_spores = self.cap + self.spore + self.stem
        expected_spores = max(1, np.random.poisson(lam=base_spores * 0.2 * self.spore_output))

        if expected_spores == 0:
            return []

        # ---- Genera mutazioni vettorialmente ----
        # Fenotipi
        new_traits = np.random.normal(
            loc=[self.cap, self.stem, self.mycelium, self.spore],
            scale=0.5,
            size=(expected_spores, 4)
        )
        new_traits = np.clip(new_traits, 0.1, None)  # valori minimi 0.1

        # Geni
        def mutate_genes(genes):
            arr = np.array(list(genes.values()))
            mutated = np.clip(arr + np.random.normal(0, 0.01, size=(expected_spores, len(arr))), 0, 1)
            return [dict(zip(genes.keys(), row)) for row in mutated]

        cap_genes_list = mutate_genes(self.cap_genes)
        mycelium_genes_list = mutate_genes(self.mycelium_genes)
        stem_genes_list = mutate_genes(self.stem_genes)
        spore_genes_list = mutate_genes(self.spore_genes)

        # ---- Dispersione e posizione ----
        max_dispersion = self.stem_dispersion_radius + self.spore_dispersion_radius + (wood_env.size / 10)
        min_radius = self.cap
        mean_dispersion = max_dispersion * 0.4

        angles = np.random.uniform(0, 2 * np.pi, expected_spores)
        radii = min_radius + np.random.exponential(scale=mean_dispersion, size=expected_spores)
        radii = np.clip(radii, min_radius, max_dispersion)

        dx = radii * np.cos(angles)
        dy = radii * np.sin(angles)
        new_xs = np.clip(self.x + dx, 0, wood_env.size)
        new_ys = np.clip(self.y + dy, 0, wood_env.size)

        # ---- Germinazione vettoriale ----
        # Nutrienti
        qualities = np.array([
            wood_env.get_nutrients(x, y, myc * 0.25, wood_env.nutrients_map)
            for x, y, myc in zip(new_xs, new_ys, new_traits[:, 2])
        ])
        germ_probs = np.clip([g["j"] for g in spore_genes_list] * qualities, 0, 1)
        germ_mask = np.random.rand(expected_spores) < germ_probs

        # ---- Crea oggetti Mush per quelli che germinano ----
        offspring_list = []
        for i in np.where(germ_mask)[0]:
            child = Mush(new_xs[i], new_ys[i])
            child.cap, child.stem, child.mycelium, child.spore = new_traits[i]
            child.cap_genes = cap_genes_list[i]
            child.mycelium_genes = mycelium_genes_list[i]
            child.stem_genes = stem_genes_list[i]
            child.spore_genes = spore_genes_list[i]
            offspring_list.append(child)

        return offspring_list

        return offspring_list
