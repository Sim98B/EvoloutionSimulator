import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from Plant2 import Plant
from World import World

# =============================
# Setup mondo
# =============================

size = 7.5
world = World(width=size, height=size)

starting_plants = 100
plants = [Plant(total_energy=1) for _ in range(starting_plants)]
positions = np.random.uniform(0, size, (starting_plants, 2))

for pos, plant in zip(positions, plants):
    world.place_plant(pos[0], pos[1], plant)

# =============================
# DataFrame statistiche
# =============================

stats_df = pd.DataFrame(columns=[
    'day',
    'height_mean', 'height_std', 'height_min', 'height_max',
    'leaf_mean',   'leaf_std',   'leaf_min',   'leaf_max',
    'roots_mean',  'roots_std',  'roots_min',  'roots_max'
])

# =============================
# Parametri ambiente
# =============================

n_sun_patches = 100
n_water_patches = 100
min_energy_to_survive = 1
reproduction_threshold = 2

# =============================
# Simulazione
# =============================

for day in range(500):

    print(f"\n=== Day {day + 1} ===")
    print("Plants alive:", len(world.plants))

    sun_patches = np.random.uniform(0, size, (n_sun_patches, 2))
    water_patches = np.random.uniform(0, size, (n_water_patches, 2))

    plants_sorted = sorted(world.plants, key=lambda x: x[2].height, reverse=True)

    sun_hits = {id(p): 0 for _, _, p in plants_sorted}
    water_hits = {id(p): 0 for _, _, p in plants_sorted}

    # -------------------------
    # LUCE (vince il più alto)
    # -------------------------

    for sx, sy in sun_patches:

        candidates = []

        for x, y, plant in plants_sorted:
            if np.hypot(sx - x, sy - y) <= plant.leaf:
                candidates.append((plant.height, plant))

        if candidates:
            winner = max(candidates, key=lambda t: t[0])[1]
            sun_hits[id(winner)] += 1

    # -------------------------
    # ACQUA (condivisa)
    # -------------------------

    for wx, wy in water_patches:

        interceptors = []

        for x, y, plant in plants_sorted:
            if np.hypot(wx - x, wy - y) <= plant.roots:
                interceptors.append(plant)

        if interceptors:
            share = 1 / len(interceptors)
            for plant in interceptors:
                water_hits[id(plant)] += share

    # -------------------------
    # Sopravvivenza
    # -------------------------

    for x, y, plant in plants_sorted:
        plant.survive(
            sun_hits[id(plant)],
            water_hits[id(plant)],
            min_energy=min_energy_to_survive
        )

    world.plants = [(x, y, p) for (x, y, p) in world.plants if p.alive]

    # -------------------------
    # Statistiche
    # -------------------------

    if world.plants:

        heights = np.array([p.height for _, _, p in world.plants])
        leaves  = np.array([p.leaf for _, _, p in world.plants])
        roots   = np.array([p.roots for _, _, p in world.plants])

        stats_df.loc[len(stats_df)] = [
            day + 1,
            heights.mean(), heights.std(), heights.min(), heights.max(),
            leaves.mean(),  leaves.std(),  leaves.min(),  leaves.max(),
            roots.mean(),   roots.std(),   roots.min(),   roots.max()
        ]

    else:
        stats_df.loc[len(stats_df)] = [day + 1] + [np.nan]*12

    # -------------------------
    # Riproduzione
    # -------------------------

    new_plants = []

    for x, y, plant in world.plants:

        energy = sun_hits[id(plant)] + water_hits[id(plant)]

        if energy >= reproduction_threshold:

            child = plant.generate_offspring(
                trait_std=0.05,
                mutation_prob=0.05,
                mutation_std=0.1
            )

            offset = np.random.uniform(-1, 1, 2)
            child_x = np.clip(x + offset[0], 0, size)
            child_y = np.clip(y + offset[1], 0, size)

            new_plants.append((child_x, child_y, child))

    world.plants.extend(new_plants)

    if len(world.plants) == 0:
        print(f"simulation ended after {day + 1} days")
        break

    if day % 5 == 0:
        world.show_world()

# =============================
# Plot finale (IDENTICO AL VECCHIO)
# =============================

fig, axes = plt.subplots(1, 3, figsize=(24, 5), sharex=True)

attributes = ['height', 'leaf', 'roots']
colors = ['green', 'lime', 'saddlebrown']

for ax, attr, color in zip(axes, attributes, colors):

    mean = stats_df[f'{attr}_mean']
    std  = stats_df[f'{attr}_std']
    min_ = stats_df[f'{attr}_min']
    max_ = stats_df[f'{attr}_max']

    ax.plot(stats_df['day'], mean, color=color, lw=2, label=f'{attr} mean')
    ax.fill_between(stats_df['day'], mean - std, mean + std,
                    color=color, alpha=0.2, label='±1 std')
    ax.plot(stats_df['day'], max_, color=color, lw=1, linestyle='--', label='max')
    ax.plot(stats_df['day'], min_, color=color, lw=1, linestyle='--', label='min')

    ax.set_title(attr.capitalize())
    ax.set_xlabel('Day')
    ax.set_ylabel(attr.capitalize())
    ax.legend(fontsize=8)

plt.suptitle('Daily Plant Statistics (Discrete Selection Model)', fontsize=16)
plt.tight_layout(rect=[0, 0, 1, 0.95])
plt.show()