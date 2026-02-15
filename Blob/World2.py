import random
import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from Blob2 import Blob
from Food import Food

def distance(a, b):
    return math.hypot(a.x - b.x, a.y - b.y)

def reproduce(blob, var=0.5):
    """Crea un clone con mutazioni gaussiane sui geni"""
    child_genome = {}
    for trait, value in blob.genome.items():
        child_genome[trait] = max(0.1, random.gauss(value, var))
    return Blob(blob.x, blob.y, genome=child_genome)

class World:
    def __init__(self, size=50, food_per_gen=50):
        self.size = size
        self.food_per_gen = food_per_gen
        self.blobs = []
        self.food = []

    def spawn_food(self):
        """Genera cibo in posizioni casuali della griglia"""
        self.food = [
            Food(random.randint(0, self.size - 1),
                 random.randint(0, self.size - 1))
            for _ in range(self.food_per_gen)
        ]

    def add_blob(self, blob):
        self.blobs.append(blob)

    def spawn_blob_at_border(self, genome=None):
        """Spawn di un blob casuale ai bordi"""
        side = random.choice(["top", "bottom", "left", "right"])
        if side == "top":
            x = random.randint(0, self.size - 1)
            y = 0
        elif side == "bottom":
            x = random.randint(0, self.size - 1)
            y = self.size - 1
        elif side == "left":
            x = 0
            y = random.randint(0, self.size - 1)
        else:  # right
            x = self.size - 1
            y = random.randint(0, self.size - 1)
        self.blobs.append(Blob(x, y, genome=genome))

    def step(self):
        """Muove tutti i blob verso il cibo in modo realistico"""
        for blob in self.blobs:
            for _ in range(max(1, int(blob.genome["speed"] / blob.genome["size"] * 10))):
                # Lista di cibi visibili ad ogni passo
                visible_food = [
                    f for f in self.food
                    if distance(blob, f) <= blob.genome["sense_radius"]
                ]

                if visible_food:
                    # Trova il cibo più vicino
                    target = min(visible_food, key=lambda f: distance(blob, f))
                    dx = target.x - blob.x
                    dy = target.y - blob.y

                    # Movimento unitario verso il cibo
                    move_x = 0
                    move_y = 0
                    if dx > 0:
                        move_x = 1
                    elif dx < 0:
                        move_x = -1
                    if dy > 0:
                        move_y = 1
                    elif dy < 0:
                        move_y = -1

                else:
                    # Movimento casuale se non vede cibo
                    move_x = random.choice([-1, 0, 1])
                    move_y = random.choice([-1, 0, 1])

                # Muove il blob
                blob.move(move_x, move_y, self.size)

                # Controlla se c'è cibo sulla cella dopo il movimento
                for f in self.food:
                    if blob.x == f.x and blob.y == f.y:
                        blob.food_eaten += 1
                        self.food.remove(f)
                        break

    def reproduce(self, mutation_var=0.5):
        """Applica la logica di sopravvivenza e riproduzione"""
        new_blobs = []
        survivors = []
        deaths = 0

        for blob in self.blobs:
            if blob.food_eaten == 0:
                deaths += 1
                continue  # muore
            survivors.append(blob)

            if blob.food_eaten >= 2:
                # genera un figlio con mutazioni
                new_blobs.append(reproduce(blob, var=mutation_var))

            # Reset e ritorno al bordo
            blob.reset_food()
            self.return_to_border(blob)

        self.blobs = survivors + new_blobs
        return len(new_blobs), len(survivors), deaths

    def return_to_border(self, blob):
        """Riporta il blob al bordo dopo una generazione"""
        side = random.choice(["top", "bottom", "left", "right"])
        if side == "top":
            blob.y = 0
            blob.x = random.randint(0, self.size - 1)
        elif side == "bottom":
            blob.y = self.size - 1
            blob.x = random.randint(0, self.size - 1)
        elif side == "left":
            blob.x = 0
            blob.y = random.randint(0, self.size - 1)
        else:  # right
            blob.x = self.size - 1
            blob.y = random.randint(0, self.size - 1)

    def display(self, ax):
        """Visualizza il mondo con cibi (verde) e blob (rosso)"""
        ax.clear()
        grid = np.zeros((self.size, self.size, 3))

        for f in self.food:
            grid[f.y, f.x] = [0, 1, 0]  # verde

        for b in self.blobs:
            grid[b.y, b.x] = [1, 0, 0]  # rosso

        ax.imshow(grid, interpolation="nearest")
        ax.set_title(f"Popolazione: {len(self.blobs)}")
        ax.axis("off")

        # cerchi sense_radius
        for b in self.blobs:
            circle = patches.Circle(
                (b.x, b.y),
                radius=b.genome["sense_radius"],
                fill=True,
                color="blue",
                alpha=0.15
            )
            ax.add_patch(circle)