import numpy as np
import matplotlib

matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from Mush import Mush
from Wood import Wood

np.random.seed(1)

plt.ion()
fig, ax = plt.subplots()

mushrooms = 150
generations = 150
survival_threshold = 0.3
pause = 0.01

# Inizializza il mondo e i funghi
wood = Wood(size=100, resolution=200, hatch=3)#, humidity_clusters=15, organic_clusters=15)
wood.mush = [Mush(x=np.random.uniform(0, wood.size), y=np.random.uniform(0, wood.size))
             for _ in range(mushrooms)]
wood.display(ax)
plt.pause(1)

# DataFrame-like structure per salvare statistiche fenotipi
stats = {
    'gen': [],
    'cap_mean': [], 'cap_std': [], 'cap_min': [], 'cap_max': [],
    'stem_mean': [], 'stem_std': [], 'stem_min': [], 'stem_max': [],
    'mycelium_mean': [], 'mycelium_std': [], 'mycelium_min': [], 'mycelium_max': [],
    'spore_mean': [], 'spore_std': [], 'spore_min': [], 'spore_max': [],
    'population': []
}

for gen in range(generations):
    if len(wood.mush) == 0:
        print(f"Sim terminated after {gen} generations")
        break
    for m in wood.mush:
        m.compute_fitness(wood, wood.mush)
    wood.mush = [m for m in wood.mush if m.fitness > survival_threshold]
    new_mushrooms = []
    for m in wood.mush:
        if m.fitness >= survival_threshold + ((survival_threshold / 100) * 5):
            offspring = m.reproduce(wood)
            new_mushrooms.extend(offspring)
    wood.mush.extend(new_mushrooms)
    wood.display(ax)
    plt.pause(pause)
    caps = np.array([m.cap for m in wood.mush])
    stems = np.array([m.stem for m in wood.mush])
    myc = np.array([m.mycelium for m in wood.mush])
    spores = np.array([m.spore for m in wood.mush])
    stats['gen'].append(gen)
    stats['population'].append(len(wood.mush))
    for arr, key in zip([caps, stems, myc, spores], ['cap', 'stem', 'mycelium', 'spore']):
        stats[f'{key}_mean'].append(arr.mean() if len(arr) > 0 else 0)
        stats[f'{key}_std'].append(arr.std() if len(arr) > 0 else 0)
        stats[f'{key}_min'].append(arr.min() if len(arr) > 0 else 0)
        stats[f'{key}_max'].append(arr.max() if len(arr) > 0 else 0)
    print(gen + 1)
plt.ioff()

fig2, axes = plt.subplots(2, 2, figsize=(14, 10), sharex=True)
axes = axes.flatten()
phenotypes = ['cap', 'stem', 'mycelium', 'spore']
colors = ['orange', 'saddlebrown', 'green', 'purple']
for i, (pheno, color) in enumerate(zip(phenotypes, colors)):
    ax = axes[i]
    mean = np.array(stats[f'{pheno}_mean'])
    std = np.array(stats[f'{pheno}_std'])
    min_ = np.array(stats[f'{pheno}_min'])
    max_ = np.array(stats[f'{pheno}_max'])
    ax.plot(stats['gen'], mean, color=color, lw=2, label=f'{pheno} mean')
    ax.fill_between(stats['gen'], mean - std, mean + std, color=color, alpha=0.2, label='±1 std')
    ax.plot(stats['gen'], max_, color=color, lw=1, linestyle='--', label='max')
    ax.plot(stats['gen'], min_, color=color, lw=1, linestyle='--', label='min')
    ax.set_title(pheno.capitalize())
    ax.set_ylabel(pheno.capitalize())
    ax.legend(fontsize=8)

# ---- Popolazione ----
"""ax_pop = axes[3]
ax_pop.plot(stats['gen'], stats['population'], color='black', lw=2)
ax_pop.set_title("Population")
ax_pop.set_ylabel("Number of mushrooms")"""

for ax in axes:
    ax.set_xlabel("Generation")
plt.suptitle('Mushroom Phenotypes + Population over Generations', fontsize=16)
plt.tight_layout(rect=[0, 0, 1, 0.95])
plt.show()