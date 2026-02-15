import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from Plant import Plant

class World:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.plants = []  # lista di tuple (x, y, Plant)
        self.sun_patches = None
        self.water_patches = None

    def place_plant(self, x, y, plant):
        self.plants.append((x, y, plant))

    def show_world(self):
        fig, ax = plt.subplots(figsize=(8, 8))
        ax.set_xlim(0, self.width)
        ax.set_ylim(0, self.height)
        ax.set_aspect('equal')
        ax.set_title("Plant visualization")
        if self.sun_patches is not None:
            ax.scatter(self.sun_patches[:, 0],
                       self.sun_patches[:, 1],
                       color='yellow',
                       s=30,
                       label="Sun patches")

            # --- WATER PATCHES ---
        if self.water_patches is not None:
            ax.scatter(self.water_patches[:, 0],
                       self.water_patches[:, 1],
                       color='blue',
                       s=30,
                       label="Water patches")

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

    def energy(self, world_size, n_sun, n_water):
        self.sun_patches = np.random.uniform(0, world_size, (n_sun, 2))
        self.water_patches = np.random.uniform(0, world_size, (n_water, 2))
        return self.sun_patches, self.water_patches

    def energy_half(self, world_size, n_sun, n_water):

        half = world_size / 2

        # Sole solo nella metà sinistra
        sun_x = np.random.uniform(0, half, n_sun)
        sun_y = np.random.uniform(0, world_size, n_sun)
        self.sun_patches = np.column_stack((sun_x, sun_y))

        # Acqua solo nella metà destra
        water_x = np.random.uniform(half, world_size, n_water)
        water_y = np.random.uniform(0, world_size, n_water)
        self.water_patches = np.column_stack((water_x, water_y))

        return self.sun_patches, self.water_patches