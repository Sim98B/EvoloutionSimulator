import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from scipy.ndimage import gaussian_filter
from noise import pnoise2
from Mushroom import Mush

plt.ion()
fig, ax = plt.subplots()

class Wood:
    def __init__(self, size: int = 10):
        self.size = size
        self.mush = []

    def display(self, ax):
        ax.clear()
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
                    edgecolor="darkred",
                    #hatch="o",
                    alpha=0.2
                )
                myc = patches.Circle(
                    (m.x, m.y),
                    m.mycelium_density*(self.size/5),
                    color='green',
                    edgecolor="darkgreen",
                    #hatch='x',
                    alpha=0.2
                )
                ax.add_patch(cap)
                ax.add_patch(myc)

        ax.set_xlim(0, self.size)
        ax.set_ylim(0, self.size)
        ax.set_aspect('equal')
        ax.set_title(f"Popolazione: {len(self.mush)}")
        plt.tight_layout()

"""wood = Wood(size=1)
wood.mush.extend([Mush(x=np.random.uniform(0,wood.size), y=np.random.uniform(0,wood.size)) for i in range(50)])
wood.display(ax)
plt.pause(1)"""



def perlin_field(size=200, scale=50):
    field = np.zeros((size, size))
    for i in range(size):
        for j in range(size):
            field[i][j] = pnoise2(i/scale, j/scale, octaves=4)
    field = (field - field.min()) / (field.max() - field.min())
    return field

H = perlin_field()

plt.imshow(H, cmap='Blues', origin='lower')
plt.colorbar()
plt.show()

