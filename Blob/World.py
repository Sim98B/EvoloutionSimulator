import random
import matplotlib.patches as patches
from Food import Food
from Blob import Blob
import matplotlib.pyplot as plt
import numpy as np
import math

def distance(a, b):
    return math.hypot(a.x - b.x, a.y - b.y)
def reproduce(blob):
    child_genome = {}
    for k, v in blob.genome.items():
        mutation = random.gauss(v, 0.2)
        child_genome[k] = max(0.1, v + mutation)
    return Blob(blob.x, blob.y, genome=child_genome)

class World:
    def __init__(self, size=50, food_per_gen=100):
        self.size = size
        self.food_per_gen = food_per_gen
        self.blobs = []
        self.food = []

    def spawn_food(self):
        self.food = [
            Food(
                random.randint(0, self.size - 1),
                random.randint(0, self.size - 1)
            )
            for _ in range(self.food_per_gen)
        ]

    def add_blob(self, blob):
        self.blobs.append(blob)

    def display(self, ax):
        ax.clear()

        grid = np.zeros((self.size, self.size, 3))

        for f in self.food:
            grid[f.y, f.x] = [0, 1, 0]

        for b in self.blobs:
            grid[b.y, b.x] = [1, 0, 0]

        ax.imshow(grid, interpolation="nearest")
        ax.set_title(f"Popolazione: {len(self.blobs)}")
        ax.axis("off")

        # cerchi sense radius
        for b in self.blobs:
            circle = patches.Circle(
                (b.x, b.y),
                radius=b.genome["sense_radius"],
                fill=True,
                color="blue",
#                linewidth=0.5,
                alpha = 0.15
            )
            ax.add_patch(circle)

    def step(self):
        for blob in self.blobs:
            # cerca cibo nel raggio sensoriale
            visible_food = [
                f for f in self.food
                if distance(blob, f) <= blob.genome["sense_radius"]
            ]

            if visible_food:
                target = min(visible_food, key=lambda f: distance(blob, f))
                dx = target.x - blob.x
                dy = target.y - blob.y
            else:
                dx = random.choice([-1, 0, 1])
                dy = random.choice([-1, 0, 1])

            steps = max(1, int(blob.genome["speed"]))

            for _ in range(steps):
                blob.move(
                    max(-1, min(1, dx)),
                    max(-1, min(1, dy)),
                    self.size
                )

            # mangia il cibo
            for f in self.food:
                if blob.x == f.x and blob.y == f.y:
                    blob.food_eaten += 1
                    self.food.remove(f)
                    break

    def reproduce(self):
        new_blobs = []
        survivors = []
        deaths = 0

        for blob in self.blobs:
            if blob.food_eaten == 0:
                deaths += 1
                continue  # muore
            survivors.append(blob)
            if blob.food_eaten >= 2:
                new_blobs.append(reproduce(blob))
            blob.reset_food()

        self.blobs = survivors + new_blobs

        # ritorna statistiche della generazione
        return len(new_blobs), len(survivors), deaths


"""world = World(size=30, food_per_gen=30)
world.spawn_food()
for i in range(20):
    world.add_blob(Blob(x = random.randint(1, 29),y = random.randint(1, 29)))

world.display()"""