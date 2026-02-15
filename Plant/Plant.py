import numpy as np
#np.random.seed(0)

class Plant:
    def __init__(self,total_energy=1):
        self.total_energy = total_energy

        props = np.random.dirichlet([1, 1, 1])
        self.alpha, self.beta, self.gamma = props

        self.height = self.alpha * self.total_energy
        self.leaf   = self.beta * self.total_energy
        self.roots  = self.gamma * self.total_energy

    def daily_adaptation(self, sun, water):
        # --- Parametri modello ---
        c = 0.5  # vantaggio altezza sulla luce
        d = 0.3  # saturazione effetto altezza
        k = 0.05  # intensità plasticità
        eps = 1e-8  # stabilità numerica

        # 1️⃣ Sole effettivo (altezza aumenta accesso ma satura)
        effective_sun = sun * (1 + c * self.height) / (1 + d * self.height)

        # 2️⃣ Guadagni separati
        sun_gain = effective_sun * (self.leaf / (1 + self.leaf))
        water_gain = water * (self.roots / (1 + self.roots)) - 0.05 * self.leaf * sun
        water_gain = max(0, water_gain)

        # 3️⃣ Crescita limitata dal fattore più scarso (Liebig)
        growth = min(sun_gain, water_gain)

        # 4️⃣ Costo strutturale (cresce più che linearmente)
        total_mass = self.height + self.leaf + self.roots
        maintenance = 0.02 * total_mass
        growth = max(0, growth - maintenance)

        # 5️⃣ Plasticità armonica (proporzionale allo squilibrio relativo)
        imbalance = (sun_gain - water_gain) / (sun_gain + water_gain + eps)
        imbalance = np.tanh(3 * imbalance)

        plastic_shift = k * imbalance * growth

        self.beta -= plastic_shift
        self.gamma += plastic_shift

        water_stress = max(0, sun_gain - water_gain)
        self.height -= 0.05 * water_stress
        self.height = max(0.01, self.height)

        # 6️⃣ Mantieni simplex
        props = np.clip([self.alpha, self.beta, self.gamma], 0.01, None)
        props = props / np.sum(props)
        self.alpha, self.beta, self.gamma = props

        # 7️⃣ Crescita reale distribuita secondo strategia aggiornata
        self.height += self.alpha * growth
        self.leaf += self.beta * growth
        self.roots += self.gamma * growth

        print(f"Height: {self.height:.3f}, leaf: {self.leaf:.3f}, roots: {self.roots:.3f}")

#p = Plant()
#print(f"Height: {p.height:.3f}, leaf: {p.leaf:.3f}, roots: {p.roots:.3f}")

"""for day in range(10):
    rain_factor = np.random.uniform(0, 1)

    water = rain_factor
    sun = 1 - rain_factor + np.random.normal(0, 0.1)

    sun = np.clip(sun, 0, 1)

    #print(sun, water)

    p.daily_adaptation(sun, water)"""

"""for day in range(20):
    #print(f"{day + 1}")
    if day < 10:
        water = 0.9
        sun = 0.1
    else:
        water = 0.2
        sun = 0.9

    p.daily_adaptation(sun, water)"""