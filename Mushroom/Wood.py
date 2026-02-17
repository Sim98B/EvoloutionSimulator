import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from scipy.ndimage import gaussian_filter
from noise import pnoise2
from Mushroom import Mush

np.random.seed(42)
plt.ion()
fig, ax = plt.subplots()

import numpy as np
from noise import pnoise2

class Wood:
    def __init__(self, size: int = 10, resolution: int = 200):
        self.size = size
        self.mush = []
        self.resolution = resolution
        self.humidity_map = None
        self._generate_humidity()

    def _generate_humidity(self):
        field = np.random.rand(self.resolution, self.resolution)
        field = gaussian_filter(field, sigma=5)
        field = (field - field.min()) / (field.max() - field.min())
        #field = field**1.5
        self.humidity_map = field

    def get_local_humidity(self, x, y, radius):
        res = self.resolution

        # coordinate centro in indice
        cx = int(x * (res - 1))
        cy = int(y * (res - 1))

        # raggio in pixel
        r_pix = int(radius * res)

        values = []

        for i in range(cx - r_pix, cx + r_pix + 1):
            for j in range(cy - r_pix, cy + r_pix + 1):

                if 0 <= i < res and 0 <= j < res:
                    if (i - cx) ** 2 + (j - cy) ** 2 <= r_pix ** 2:
                        values.append(self.humidity_map[j, i])

        if values:
            return np.mean(values)
        else:
            return 0

    def display(self, ax):
        ax.clear()

        # ---- Sfondo umidità ----
        ax.imshow(
            self.humidity_map,
            extent=[0, self.size, 0, self.size],
            origin='lower',
            cmap='Blues',
            #alpha=0.8,
           )

        # ---- Tuo codice originale intatto ----
        if self.mush:
            w = ax.scatter([m.x for m in self.mush],
                           [m.y for m in self.mush],
                           c="brown",
                           s=35,
                           edgecolor="black")
            for m in self.mush:
                cap = patches.Circle(
                    (m.x, m.y),
                    m.cap_size*(self.size/5),
                    color='red',
                    alpha=0.2
                )
                myc = patches.Circle(
                    (m.x, m.y),
                    m.mycelium_density*(self.size/5),
                    color='green',
                    alpha=0.2
                )
                ax.add_patch(cap)
                ax.add_patch(myc)

        ax.set_xlim(0, self.size)
        ax.set_ylim(0, self.size)
        ax.set_aspect('equal')
        ax.set_title(f"Popolazione: {len(self.mush)}")
        plt.tight_layout()

wood = Wood(size=1)
wood.mush.extend([Mush(x=np.random.uniform(0,wood.size), y=np.random.uniform(0,wood.size)) for i in range(10)])
wood.display(ax)

for m in wood.mush:
    print("mycelium_density:", m.mycelium_density)
    print("r_pix:", int(m.mycelium_density * wood.resolution))
    humidity = wood.get_local_humidity(m.x, m.y, m.mycelium_density)
    soil_energy = m.mycelium_density * humidity
    print(soil_energy)
    ax.text(m.x, m.y + 0.02, f"{humidity:.2f}", color='black', fontsize=8, ha='center')

plt.pause(1)

