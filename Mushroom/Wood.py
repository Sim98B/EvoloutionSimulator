import numpy as np
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from scipy.ndimage import gaussian_filter
from Mushroom import Mush
from Mush import Mush

#np.random.seed(0)
plt.ion()
fig, ax = plt.subplots()

class Wood:
    def __init__(self, size: int = 1, resolution: int = 2000, hatch:int = 10, humidity_clusters: int = None):
        self.size = size
        self.mush = []
        self.resolution = resolution
        self.hatch = hatch
        self.humidity_map = self._generate_humidity_clusters(n_clusters=humidity_clusters) if humidity_clusters  else self._generate_humidity()

    def _generate_humidity(self):
        field = np.random.rand(self.resolution, self.resolution)
        field = gaussian_filter(field, sigma=self.hatch)
        field = (field - field.min()) / (field.max() - field.min())
        #field = field**1.5
        return field

    def _generate_humidity_clusters(self, n_clusters):
        res = self.resolution
        x = np.linspace(0, 1, res)
        y = np.linspace(0, 1, res)
        X, Y = np.meshgrid(x, y)

        field = np.zeros((res, res))

        for _ in range(n_clusters):  # numero macro zone
            cx, cy = np.random.rand(2)
            field += np.exp(-((X - cx) ** 2 + (Y - cy) ** 2) / 0.02)

        field = field / field.max()
        return field

    def get_humidity(self, x, y, radius):
        res = self.resolution

        # coordinate centro in indice
        cx = int(x / self.size * (res - 1))
        cy = int(y / self.size * (res - 1))

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
            cmap='Blues', # RdYlBu
            alpha=1,
           )
        if self.mush:
            ax.scatter([m.x for m in self.mush],
                           [m.y for m in self.mush],
                           c="brown",
                           #s=35,
                           s=[m.stem * 5 for m in self.mush],
                           edgecolor="black")
            for m in self.mush:
                cap = patches.Circle(
                    (m.x, m.y),
                    m.cap,#*(self.size/5),
                    color='red',
                    alpha=0.2
                )
                myc = patches.Circle(
                    (m.x, m.y),
                    m.mycelium,#*(self.size/5),
                    color='green',
                    alpha=0.2
                )
                ax.add_patch(cap)
                ax.add_patch(myc)

        ax.set_xlim(0, self.size)
        ax.set_ylim(0, self.size)
        ax.set_aspect('equal')
        ax.set_title(f"Popolazione: {len(self.mush)}")
        #plt.show()
        plt.tight_layout()

wood = Wood(size = 50, resolution=200)
for _ in range(10):
    wood.mush=[Mush(x=np.random.uniform(0,wood.size), y=np.random.uniform(0,wood.size)) for i in range(10)]
    wood.display(ax)

    plt.pause(0.5)

