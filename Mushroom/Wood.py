import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from scipy.ndimage import gaussian_filter

np.random.seed(0)
plt.ion()
fig, ax = plt.subplots()

class Wood:
    def __init__(self, size: int = 10, resolution: int = 200, humidity_clusters: int = None, hummus_clusters: int = None):
        self.size = size
        self.mush = []
        self.resolution = resolution
        self.humidity_map = self._generate_humidity_clusters(n_clusters=humidity_clusters) if humidity_clusters  else self._generate_humidity()
        self.hummus_map = self._generate_humidity_clusters(n_clusters=hummus_clusters) if hummus_clusters else self._generate_hummus()

    def _generate_humidity(self):
        field = np.random.rand(self.resolution, self.resolution)
        field = gaussian_filter(field, sigma=10)
        field = (field - field.min()) / (field.max() - field.min())
        #field = field**1.5
        return field

    def _generate_hummus(self):
        field = np.random.rand(self.resolution, self.resolution)
        field = gaussian_filter(field, sigma=10)
        field = (field - field.min()) / (field.max() - field.min())
        #field = field**1.5
        return field

    def _generate_humidity_clusters(self, n_clusters: int):
        res = self.resolution
        x = np.linspace(0, 1, res)
        y = np.linspace(0, 1, res)
        X, Y = np.meshgrid(x, y)

        field = np.zeros((res, res))

        for _ in range(30):  # numero macro zone
            cx, cy = np.random.rand(2)
            field += np.exp(-((X - cx) ** 2 + (Y - cy) ** 2) / 0.02)

        field = field / field.max()
        return field

    def _generate_hummus_clusters(self, n_clusters: int):
        res = self.resolution
        x = np.linspace(0, 1, res)
        y = np.linspace(0, 1, res)
        X, Y = np.meshgrid(x, y)

        field = np.zeros((res, res))

        for _ in range(30):  # numero macro zone
            cx, cy = np.random.rand(2)
            field += np.exp(-((X - cx) ** 2 + (Y - cy) ** 2) / 0.02)

        field = field / field.max()
        return field

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

    def get_local_hummus(self, x, y, radius):
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
        ax.imshow(
            self.humidity_map,
            extent=[0, self.size, 0, self.size],
            origin='lower',
            cmap='Blues',
            #alpha=0.9,
           )
        ax.imshow(
            self.hummus_map,
            extent=[0, self.size, 0, self.size],
            origin='lower',
            cmap='Greens',   # YlOrRd
            alpha=0.5,
        )

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

