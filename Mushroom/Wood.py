import numpy as np
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from scipy.ndimage import gaussian_filter

class Wood:
    def __init__(self, size: int = 1, resolution: int = 2000, hatch:int = 10, humidity_clusters: int = None, organic_clusters: int = None):
        self.size = size
        self.mush = []
        self.resolution = resolution
        self.hatch = hatch
        self.humidity_map = self._generate_clusters(n_clusters=humidity_clusters) if humidity_clusters  else self._generate_field()
        self.organic_map = self._generate_clusters(n_clusters=organic_clusters) if organic_clusters else self._generate_field()
        self.nutrients_map = (self.humidity_map + self.organic_map).astype(np.float32)

    def _generate_field(self):
        field = np.random.rand(self.resolution, self.resolution)
        field = gaussian_filter(field, sigma=self.hatch)
        field = (field - field.min()) / (field.max() - field.min())
        #field = field**0.9
        return field

    def _generate_clusters(self, n_clusters):
        res = self.resolution
        x = np.linspace(0, 1, res)
        y = np.linspace(0, 1, res)
        x_map, y_map = np.meshgrid(x, y)
        field = np.zeros((res, res))
        for _ in range(n_clusters):
            cx, cy = np.random.rand(2)
            field += np.exp(-((x_map - cx) ** 2 + (y_map - cy) ** 2) / 0.02)
        field = field / field.max()
        return field

    def get_nutrients(self, x, y, radius, grid):
        res = grid.shape[0]
        cx, cy = int(x / self.size * (res - 1)), int(y / self.size * (res - 1))
        r_pix = int(radius * res)

        x_idx = np.arange(cx - r_pix, cx + r_pix + 1)
        y_idx = np.arange(cy - r_pix, cy + r_pix + 1)
        x_idx = x_idx[(x_idx >= 0) & (x_idx < res)]
        y_idx = y_idx[(y_idx >= 0) & (y_idx < res)]

        X, Y = np.meshgrid(x_idx, y_idx)
        mask = (X - cx) ** 2 + (Y - cy) ** 2 <= r_pix ** 2

        return grid[Y, X][mask].mean()

    def display(self, ax):
        ax.clear()
        """ax.imshow(
            self.humidity_map,
            extent=[0, self.size, 0, self.size],
            origin='lower',
            cmap='Blues', # RdYlBu
            alpha=1,
           )
        ax.imshow(
            self.organic_map,
            extent=[0, self.size, 0, self.size],
            origin='lower',
            cmap='Greens',
            alpha=1,
        )"""
        ax.imshow(
            self.nutrients_map,
            extent=[0, self.size, 0, self.size],
            origin='lower',
            cmap='Blues',
            alpha=1,
        )
        if self.mush:
            ax.scatter([m.x for m in self.mush],
                           [m.y for m in self.mush],
                           c="brown",
                           s=[m.stem * 5 for m in self.mush],
                           edgecolor="black")
            for m in self.mush:
                cap = patches.Circle(
                    (m.x, m.y),
                    m.cap,
                    color='red',
                    alpha=0.2
                )
                myc = patches.Circle(
                    (m.x, m.y),
                    m.mycelium,
                    color='green',
                    alpha=0.2
                )
                ax.add_patch(cap)
                ax.add_patch(myc)

        ax.set_xlim(0, self.size)
        ax.set_ylim(0, self.size)
        ax.set_xticklabels([])
        ax.set_yticklabels([])
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_aspect('equal')
        ax.set_title(f"Popolazione: {len(self.mush)}")
        plt.tight_layout()