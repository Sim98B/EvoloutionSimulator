import numpy as np
np.set_printoptions(precision=3, suppress=True)
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from matplotlib.patches import Circle
from scipy.ndimage import gaussian_filter
from Mush import Mush

class Wood:
    def __init__(self, size: int = 10, resolution: int = 2000,
                 temp_mean: float = 10.0, temp_std: float = 5.0):
        self.size = size
        self.resolution = resolution

        self.mush = []
        self.forest = {1:"Betulla", 2:"Abete", 3:"Pino", 4:"Faggio", 5:"Quercia", 6:"Castagno"}

        self.hum_map = self._generate_humidity_map()
        self.org_map = self._generate_organic_map()
        self.ph_map = self._generate_ph_map()
        self.temp_map = self._generate_temperature_map(temp_mean, temp_std)
        self.tree_map = self._generate_tree_map()

    def _generate_humidity_map(self, smooth_sigma: float = 20):
        hum_field = np.random.randn(self.resolution, self.resolution)
        hum_field = gaussian_filter(hum_field, sigma=smooth_sigma)
        hum_min = np.min(hum_field)
        hum_max = np.max(hum_field)
        hum_field = (hum_field - hum_min) / (hum_max - hum_min)
        return hum_field
    def _generate_organic_map(self, smooth_sigma: float = 20):
        org_field = np.random.randn(self.resolution, self.resolution)
        org_field = gaussian_filter(org_field, sigma=smooth_sigma)
        org_max = np.max(org_field)
        org_min = np.min(org_field)
        org_field = (org_field - org_min) / (org_max- org_min)
        return org_field
    def _generate_ph_map(self, smooth_sigma: float = 20):
        ph_field = np.random.randn(self.resolution, self.resolution)
        ph_field = gaussian_filter(ph_field, sigma=smooth_sigma)
        ph_min = np.min(ph_field)
        ph_max = np.max(ph_field)
        ph_field = (ph_field - ph_min) / (ph_max - ph_min) * 14
        return ph_field
    def _generate_temperature_map(self, mean: float, std: float, smooth_sigma: float = 20):
        temp_field = np.random.randn(self.resolution, self.resolution)
        temp_field = gaussian_filter(temp_field, sigma=smooth_sigma)
        temp_field = mean + temp_field / np.std(temp_field) * std
        return temp_field
    def _generate_tree_map(self, smooth_sigma: float = 7, n_types: int = 6):
        tree_field = np.random.randn(self.resolution, self.resolution)
        tree_field = gaussian_filter(tree_field, sigma=smooth_sigma)
        thresholds = np.quantile(tree_field, np.linspace(0, 1, n_types + 1)[1:-1])
        tree_discrete = np.digitize(tree_field, thresholds)
        return tree_discrete

    def sample_env(self, x: float, y: float, radius):
        res = self.resolution
        cx = int(x / self.size * (res - 1))
        cy = int(y / self.size * (res - 1))
        r_pix = int(radius / self.size * res)
        x_idx = np.arange(cx - r_pix, cx + r_pix + 1)
        y_idx = np.arange(cy - r_pix, cy + r_pix + 1)
        x_idx = x_idx[(x_idx >= 0) & (x_idx < res)]
        y_idx = y_idx[(y_idx >= 0) & (y_idx < res)]
        X, Y = np.meshgrid(x_idx, y_idx)
        mask = (X - cx) ** 2 + (Y - cy) ** 2 <= r_pix ** 2
        hum_local = self.hum_map[Y, X][mask].mean()
        org_local = self.org_map[Y, X][mask].mean()
        ph_local = self.ph_map[Y, X][mask].mean()
        temp_local = self.temp_map[Y, X][mask].mean()
        tree_vals = self.tree_map[Y, X][mask]
        count_array = np.zeros(6, dtype=int)
        if len(tree_vals) > 0:
            types, counts = np.unique(tree_vals, return_counts=True)
            count_array[types.astype(int)] = counts
        return np.concatenate(([hum_local, org_local, ph_local, temp_local], count_array))

    def display(self, ax):
        tree_colors = ["lightgreen","yellowgreen","forestgreen","darkgreen","olive","saddlebrown"]
        cmap = ListedColormap(tree_colors)
        ax[0].imshow(self.hum_map, cmap="Blues", vmin=0, vmax=1)
        ax[1].imshow(self.org_map, cmap="terrain_r", vmin=self.org_map.min(), vmax=self.org_map.max())
        ax[2].imshow(self.ph_map, cmap="RdBu_r", vmin=0, vmax=14)
        ax[3].imshow(self.temp_map, cmap="plasma", vmin=self.temp_map.min(), vmax=self.temp_map.max())
        ax[4].imshow(self.tree_map, cmap=cmap, vmin=0, vmax=len(tree_colors) - 1)
        titles = ["Humidity", "Organic matter", "Ph", "Temperature", "Tree"]

        for i in range(5):
            ax[i].set_xticks([])
            ax[i].set_yticks([])
            ax[i].axis("off")
            ax[i].set_title(titles[i], y=-0.15)
        plt.tight_layout()

"""plt.ion()
fig, ax = plt.subplots(1, 5, figsize=(15,3))
for _ in range(5):
    wood = Wood(size=50, resolution=200, temp_mean=10, temp_std=3)
    wood.display(ax)
    print(wood.sample_env(3,3,3.4))
    plt.pause(20)"""

wood = Wood(size=50, resolution=200, temp_mean=10, temp_std=3)
for _ in range(10):
    specie = np.random.choice(["Amanita Muscaria", "Boletus Edulis", "Cantharellus Cibarius"])
    x_m = np.random.uniform(0, wood.size)
    y_m = np.random.uniform(0, wood.size)
    m = Mush(x=x_m, y=y_m, specie=specie)
    sample = wood.sample_env(x_m, y_m, radius=m.mycelium)
    print(f"Myc: {m.mycelium:.3f} | Hum: {sample[0]:.3f} | Org: {sample[1]:.3f} | Ph: {sample[2]:.3f} | Temp: {sample[3]:.3f} | Betulle: {sample[4]:.0f} | Abeti: {sample[5]:.0f} | Pini: {sample[6]:.0f} |  Faggi: {sample[7]:.0f} |  Querce: {sample[8]:.0f} |  Castagni: {sample[9]:.0f} | {specie}")
#print(wood.sample_env(25,25, 10))