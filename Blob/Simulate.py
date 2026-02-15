import math
import random
import time
from Blob import Blob
from Food import Food
from World import World
import matplotlib.pyplot as plt

def distance(a, b):
    return math.hypot(a.x - b.x, a.y - b.y)

def reproduce(blob):
    child_genome = {}
    for k, v in blob.genome.items():
        mutation = random.gauss(-0.1, 0.1)
        child_genome[k] = max(0.1, v + mutation)

    return Blob(blob.x, blob.y, genome=child_genome)

#random.seed(42)
world = World(size=100, food_per_gen=100)

for _ in range(50):
    world.add_blob(Blob(x = random.randint(0, world.size - 1),
                        y = random.randint(0, world.size - 1),
                        genome={
                            "speed": random.gauss(1.5, 0.5),
                            "sense_radius": random.gauss(2, 0.2)
                        }))

plt.ion()
fig, ax = plt.subplots()

print(
    f"Gen 0 | Popolazione: {len(world.blobs)} | "
    f"Speed media: {sum(b.genome['speed'] for b in world.blobs)/len(world.blobs):.2f} | "
    f"Sense medio: {sum(b.genome['sense_radius'] for b in world.blobs)/len(world.blobs):.2f}"
)

for generation in range(50):
    world.spawn_food()

    for _ in range(50):
        world.step()

    # restituisce nati, sopravvissuti, morti
    nati, sopravvissuti, morti = world.reproduce()

    if len(world.blobs) == 0:
        print("Simulazione finita")
        break
    else:
        print(
            f"Gen {generation + 1} | Popolazione: {len(world.blobs)} | "
            f"Speed media: {sum(b.genome['speed'] for b in world.blobs)/len(world.blobs):.2f} | "
            f"Sense medio: {sum(b.genome['sense_radius'] for b in world.blobs)/len(world.blobs):.2f} | "
            f"Nati: {nati} | Sopravvissuti: {sopravvissuti} | Morti: {morti}"
        )

        world.display(ax)
        plt.pause(0.1)

plt.ioff()
plt.show()
plt.tight_layout()