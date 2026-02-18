import numpy as np

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
        local_hummus = wood_env.get_local_hummus(self.x, self.y, radius)
        soil_energy = self.mycelium_density * local_humidity
        hummus_energy = self.mycelium_density * local_hummus
        survival_fitness = hummus_energy + soil_energy
        dispersion_ability = (self.cap_size + self.stem_length + self.spore_size) / 3
        cost = 0.1 * self.cap_size + 0.4 * self.stem_length + 0.4 * self.mycelium_density + 0.1 * self.spore_size
        self.fitness = survival_fitness + dispersion_ability - cost
        return self.fitness

    def compute_fitness_local(self, wood_env):
        # raggio di influenza locale proporzionale al micelio
        radius = self.mycelium_density * 0.25

        # trova tutti i funghi vicini (competizione)
        local_mushrooms = [m for m in wood_env.mush
                           if np.hypot(m.x - self.x, m.y - self.y) <= radius]

        # calcola risorse locali divise per numero di funghi
        local_humidity = wood_env.get_local_humidity(self.x, self.y, radius)
        local_hummus = wood_env.get_local_hummus(self.x, self.y, radius)
        n_neighbors = len(local_mushrooms)
        if n_neighbors > 0:
            local_humidity /= n_neighbors
            local_hummus /= n_neighbors

        soil_energy = self.mycelium_density * local_humidity
        hummus_energy = self.mycelium_density * local_hummus

        survival_fitness = soil_energy + hummus_energy

        # dispersione → migliora la capacità di far sopravvivere i discendenti
        dispersion_ability = (self.cap_size + self.stem_length + self.spore_size) / 3

        # costo di mantenimento dei tratti
        cost = 0.1 * self.cap_size + 0.4 * self.stem_length + 0.4 * self.mycelium_density + 0.1 * self.spore_size

        # fitness finale
        self.fitness = survival_fitness + dispersion_ability - cost
        return self.fitness

    def reproduce(self):
        mutation = np.random.normal(0, 0.1, 4)
        new_traits = np.array([self.cap_size, self.stem_length, self.mycelium_density, self.spore_size]) + mutation
        new_traits = np.clip(new_traits, 0, None)
        new_traits /= new_traits.sum()
        # dispersione spore proporzionale alla cappella
        max_dispersion = (self.cap_size + self.spore_size + self.stem_length) * 0.5 # scala della distanza massima
        angle = np.random.uniform(0, 2 * np.pi)
        radius = np.random.uniform(0, max_dispersion)  # distanza casuale fino al massimo
        dx = radius * np.cos(angle)
        dy = radius * np.sin(angle)

        # posizione figlio
        new_x = np.clip(self.x + dx, 0, 1)
        new_y = np.clip(self.y + dy, 0, 1)

        return Mush(new_x, new_y, new_traits)

    def reproduce_real(self, wood_env):
        """
        Genera un numero variabile di nuovi funghi (spore che diventano funghi)
        in modo casuale, modulato dai tratti del fungo e dalle condizioni locali del terreno.
        """
        # Numero di spore casuale, proporzionale ai tratti (cap, spore e gambo)
        expected_spores = np.random.poisson(lam=(self.cap_size + self.spore_size + self.stem_length) * 3)
        offspring_list = []

        for _ in range(expected_spores):
            # Mutazione genetica casuale
            if np.random.rand() < 0.05:
                new_traits = np.random.uniform(0.8, 1.2, 4)
            else:
                mutation = np.random.normal(0, 0.1, 4)
                new_traits = np.array([self.cap_size, self.stem_length, self.mycelium_density, self.spore_size]) + mutation
                new_traits = np.clip(new_traits, 0, None)
                new_traits /= new_traits.sum()

            # Dispersione casuale proporzionale ai tratti
            max_dispersion = (self.cap_size + self.spore_size + self.stem_length)# * 0.5
            angle = np.random.uniform(0, 2 * np.pi)
            radius = np.random.uniform(0, max_dispersion)
            dx = radius * np.cos(angle)
            dy = radius * np.sin(angle)

            new_x = np.clip(self.x + dx, 0, 1)
            new_y = np.clip(self.y + dy, 0, 1)

            # Fitness locale naturale: maggiore umidità/hummus → più probabilità che la spora cresca
            local_hum = wood_env.get_local_humidity(new_x, new_y, radius)
            local_hummus = wood_env.get_local_hummus(new_x, new_y, radius)
            local_quality = (local_hum + local_hummus) / 2  # combinazione naturale delle risorse

            # probabilità casuale, più terreno buono → più chance di sopravvivere
            if np.random.rand() < local_quality:
                offspring_list.append(Mush(new_x, new_y, new_traits))

        return offspring_list