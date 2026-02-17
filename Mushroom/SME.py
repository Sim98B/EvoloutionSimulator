import numpy as np
import matplotlib.pyplot as plt
from Mushroom import Mush
from Wood import Wood

#np.random.seed(42)
plt.ion()
fig, ax = plt.subplots()

wood = Wood(size = 1, resolution = 200)
mushrooms = 10
generations = 20

wood.mush=[Mush(x=np.random.uniform(0,wood.size), y=np.random.uniform(0,wood.size)) for i in range(10)]
#wood.display(ax)
#plt.pause(1)


survival_threshold = 0.1  # soglia minima per sopravvivere

for gen in range(generations):
    # Calcola fitness
    for m in wood.mush:
        m.compute_fitness(wood)

    # Selezione
    wood.mush = [m for m in wood.mush if m.fitness > survival_threshold]

    # Riproduzione
    new_mushrooms = []
    for m in wood.mush:
        offspring = m.reproduce()
        if np.random.rand() < 0.05:
            offspring.mycelium_density *= np.random.uniform(0.8, 1.2)
            offspring.cap_size *= np.random.uniform(0.8, 1.2)
        new_mushrooms.append(offspring)

    wood.mush.extend(new_mushrooms)

    # Visualizza
    wood.display(ax)
    fig.canvas.draw()       # forza il redraw
    fig.canvas.flush_events()  # aggiorna in tempo reale
    plt.pause(1)  # pausa breve, solo per vedere il frame