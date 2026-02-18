import numpy as np
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from Mushroom import Mush
from Mush import Mush
from Wood import Wood

#np.random.seed(0) # seed 0 e 30 cluster e 50 funghi
plt.ion()
fig, ax = plt.subplots()

mushrooms = 50
generations = 50
survival_threshold = 0.3
pause = 0.01

wood = Wood(size = 50, resolution = 200, hatch=3)#, humidity_clusters=50)
wood.mush=[Mush(x=np.random.uniform(0,wood.size), y=np.random.uniform(0,wood.size)) for i in range(mushrooms)]
wood.display(ax)
plt.pause(pause)
gen = 0
#for gen in range(generations):
while len(wood.mush) > 0:
    if len(wood.mush) == 0:
        print(f"Sim terminated after {gen} generations")
        break
    #wood.humidity_map = wood._generate_humidity()
    #wood.hummus_map = wood._generate_hummus()
    #wood.humidity_map = wood._generate_humidity_clusters(wood.humidity_clusters)
    #wood.hummus_map = wood._generate_hummus_clusters(wood.hummus_clusters)
    for m in wood.mush:
        m.compute_fitness(wood, wood.mush)

    wood.mush = [m for m in wood.mush if m.fitness > survival_threshold]

    new_mushrooms = []
    for m in wood.mush:
        if m.fitness >= survival_threshold + ((survival_threshold / 100) * 10):
            offspring = m.reproduce(wood)
            new_mushrooms.extend(offspring)

    wood.mush.extend(new_mushrooms)

    """new_mushrooms = []
    for m in wood.mush:
        if m.fitness >= survival_threshold + ((survival_threshold/100) * 10):
            offspring = m.reproduce_real(wood)
            #offspring = m.reproduce()
            new_mushrooms.extend(offspring)

    wood.mush.extend(new_mushrooms)"""
    print(f"Gen {gen + 1} | Survivors: {len(wood.mush)} | Fit medio: {np.mean([m.fitness for m in wood.mush]):.4f} | GR: {np.mean([m.mycelial_growth_rate for m in wood.mush]):.4f} | Den: {np.mean([m.branching_density for m in wood.mush]):.4f}")
    #print(
    #    f"Gen {gen + 1} | Survivors: {len(wood.mush)} | Fit medio: {np.mean([m.fitness for m in wood.mush]):.4f} | Cap: {np.mean([m.cap_size for m in wood.mush]):.4f} | Myc: {np.mean([m.mycelium_density for m in wood.mush]):.4f} | Stem: {np.mean([m.stem_length for m in wood.mush]):.4f} | Spore: {np.mean([m.spore_size for m in wood.mush]):.4f} | New: {len(new_mushrooms)}")
    gen += 1
    wood.display(ax)
    plt.pause(pause)