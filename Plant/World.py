import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from Plant import Plant

class World:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.plants = []  # lista di tuple (x, y, Plant)

    def place_plant(self, x, y, plant):
        self.plants.append((x, y, plant))

    def show_world(self):
        fig, ax = plt.subplots(figsize=(8, 8))
        ax.set_xlim(0, self.width)
        ax.set_ylim(0, self.height)
        ax.set_aspect('equal')
        ax.set_title("Plant visualization")

        for x, y, p in self.plants:
            # cerchio radici (marrone)
            root_circle = Circle((x, y), radius=p.roots, color='saddlebrown', alpha=0.5)
            ax.add_patch(root_circle)
            # cerchio foglie (verde) sopra radici
            leaf_circle = Circle((x, y), radius=p.leaf, color='green', alpha=0.5)
            ax.add_patch(leaf_circle)

            # facoltativo: piccola linea per l'altezza
            ax.plot([x, x], [y, y + p.height], color='darkgreen', lw=2)

        plt.show()

    def energy(self):
        rain_factor = np.random.uniform(0, 1)
        water = rain_factor
        sun = 1 - rain_factor + np.random.normal(0, 0.1)
        sun = np.clip(sun, 0, 1)
        return water, sun