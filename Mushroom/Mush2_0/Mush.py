import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

class Mush:
    def __init__(specie: str, self, x:float | int, y: float):
        self.x = x
        self.y = y
        self.specie = specie if specie in ["Amanita Muscaria", "Boletus Edulis", "Cantharellus Cibarius"] else print("Specie non valida")
        self.mycelium = 0.1



plt.ion()
fig, ax = plt.subplots()
m = Mush(2.5,2.5)
for _ in range(10):
    ax.clear()
    #m = Mush(0.5,0.5)
    plt.scatter(m.x, m.y)
    cap = patches.Circle(
        (m.x, m.y),
        m.mycelium,
        color='red',
        alpha=0.2
    )
    e = np.random.random(0,0.1)
    print(e)
    m.grow_mycelium(energy=e)
    ax.add_patch(cap)
    ax.set_xlim(0, 5)
    ax.set_ylim(0, 5)
    ax.set_aspect('equal')
    #print(m.mycelium)
    plt.pause(1)