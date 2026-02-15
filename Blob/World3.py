import random
import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import time
from Food import Food
from Blob3 import Blob

#plt.ion()
fig, ax = plt.subplots()

class World:
    def __init__(self, size: int = 350, food_per_gen: int = 50):
        self.size = size
        self.food_per_gen = food_per_gen
        self.blobs = []
        self.food = []

    def add_blob(self, blob):
        self.blobs.append(blob)

    def display(self, ax):
        """Visualizza il mondo con cibi (verde) e blob (rosso) su campo continuo"""
        ax.clear()

        # Scatter plot cibo
        if self.food:
            ax.scatter([f.x for f in self.food], [f.y for f in self.food],
                       c='green', s=50, label='Food')

        # Scatter plot blob
        if self.blobs:
            ax.scatter([b.x for b in self.blobs], [b.y for b in self.blobs],
                       c='red', s=50, label='Blob')

            # Sense radius
            for b in self.blobs:
                circle = patches.Circle(
                    (b.x, b.y),
                    radius=b.genome["sense"]['trait'],
                    fill=True,
                    color='blue',
                    alpha=0.2
                )
                ax.add_patch(circle)

        ax.set_xlim(0, self.size)
        ax.set_ylim(0, self.size)
        ax.set_aspect('equal')
        ax.set_title(f"Popolazione: {len(self.blobs)} | Cibo: {len(self.food)}")
        plt.tight_layout()
        ax.legend(loc='upper right')

    def spawn_food_normal(self):
        """Genera cibo con distribuzione normale attorno al centro"""
        self.food = [
            Food(
                max(0, min(random.gauss(self.size / 2, self.size / 5), self.size)),
                max(0, min(random.gauss(self.size / 2, self.size / 5), self.size))
            )
            for _ in range(self.food_per_gen)
        ]

    def spawn_blob_at_border(self, genome=None):
        """Spawn di un blob casuale ai bordi (coordinate float)"""
        side = random.choice(["top", "bottom", "left", "right"])
        if side == "top":
            x = random.uniform(0, self.size)
            y = 0.0
        elif side == "bottom":
            x = random.uniform(0, self.size)
            y = float(self.size)
        elif side == "left":
            x = 0.0
            y = random.uniform(0, self.size)
        else:  # right
            x = float(self.size)
            y = random.uniform(0, self.size)
        self.blobs.append(Blob(x, y, genome=genome))

"""for i in range(100):
    w = World()
    w.spawn_food_normal()
    for i in range(50):
        #w.add_blob(blob = Blob(x=random.randint(0, w.size - 1), y=random.randint(0, w.size - 1)))
        w.spawn_blob_at_border()
    w.display(ax)
    plt.pause(0.5)"""

w = World(size = 100, food_per_gen = 100)
w.spawn_food_normal()
for i in range(10):
    w.spawn_blob_at_border()
w.display(ax)
plt.pause(0.01)

"""while w.blobs[0].energy > 0:
    for blob in w.blobs:
        target_food, danger = blob.perceive(w)

        if target_food:
            blob.move(world_size=w.size, target=target_food)
            print("Food found")
        elif danger:
            blob.move(world_size=w.size, avoid=danger)
        else:
            blob.move(world_size=w.size)

        w.display(ax)
        plt.pause(0.1)"""

max_ticks = 200

for tick in range(max_ticks):
    all_dead = True

    for blob in w.blobs:
        if blob.energy <= 0:
            continue

        all_dead = False
        target_food, danger = blob.perceive(w)

        if target_food:
            blob.move(world_size=w.size, target=target_food)
        elif danger:
            blob.move(world_size=w.size, avoid=danger)
        else:
            blob.move(world_size=w.size)

        # se ha raggiunto del cibo, lo “mangia”
        for f in w.food:
            if abs(blob.x - f.x) < 1 and abs(blob.y - f.y) < 1:
                blob.food_eaten += 1
                w.food.remove(f)
                break

    # visualizza tutti i blob e cibo ad ogni tick
    w.display(ax)
    plt.pause(0.05)

    if all_dead:
        print("Tutti i blob sono morti")
        break