import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from Plant import Plant
from World import World
import matplotlib
matplotlib.use("TkAgg")
#np.random.seed(0)

plt.ion()
fig, ax = plt.subplots()
# --- setup mondo ---
size = 5
world = World(width=size, height=size)
starting_plants = 50
plants = [Plant(total_energy=1) for _ in range(starting_plants)]
positions = np.random.uniform(0, size, (starting_plants, 2))

stats_df = pd.DataFrame(columns=[
    'day',
    'height_mean', 'height_std', 'height_min', 'height_max',
    'leaf_mean',   'leaf_std',   'leaf_min',   'leaf_max',
    'roots_mean',  'roots_std',  'roots_min',  'roots_max'
])

for pos, plant in zip(positions, plants):
    world.place_plant(pos[0], pos[1], plant)

# --- simulazione ---
for day in range(500):
    print(f"\n=== Day {day + 1} ===")
    print(len(world.plants))

    # energia totale giornaliera dall'ambiente
    water, sun = world.energy()
    print(f"Total water received: {water:.3f}")
    print(f"Total sun received: {sun:.3f}")

    # ordiniamo le piante per altezza decrescente per gestire luce
    plants_sorted = sorted(world.plants, key=lambda x: x[2].height, reverse=True)

    # calcolo luce considerando sovrapposizione
    for i, (x, y, plant) in enumerate(plants_sorted):
        sun_received = sun
        for j in range(i):
            xj, yj, other = plants_sorted[j]
            dist = np.hypot(x - xj, y - yj)
            if dist < (plant.leaf + other.leaf):
                sun_received *= max(0, 1 - (other.height - plant.height) / (dist + 0.1))
        plant.sun_received = sun_received

    # calcolo acqua condivisa tra radici vicine
    for i, (xi, yi, plant) in enumerate(plants_sorted):
        neighbors = 0
        for xj, yj, other in plants_sorted:
            dist = np.hypot(xi - xj, yi - yj)
            if dist < (plant.roots + other.roots):
                neighbors += 1
        plant.water_received = water / max(neighbors, 1)

    # applica daily_adaptation usando energia calcolata
    for x, y, plant in plants_sorted:
        plant.daily_adaptation(plant.sun_received, plant.water_received)

    # rimuovi piante morte
    world.plants = [(x, y, p) for (x, y, p) in world.plants if p.alive]

    if world.plants:
        heights = np.array([p.height for _, _, p in world.plants])
        leaves = np.array([p.leaf for _, _, p in world.plants])
        roots  = np.array([p.roots for _, _, p in world.plants])
        ages   = np.array([p.age for _, _, p in world.plants])

        stats_df.loc[len(stats_df)] = [
            day + 1,
            heights.mean(), heights.std(), heights.min(), heights.max(),
            leaves.mean(), leaves.std(), leaves.min(), leaves.max(),
            roots.mean(), roots.std(), roots.min(), roots.max()
        ]
    else:
        stats_df.loc[len(stats_df)] = [day + 1] + [np.nan]*16

    if day % 1 == 0 or day == 99:
        world.show_world(ax)
    plt.pause(0.1)

    new_plants = []
    for x, y, p in world.plants:
        energy_available = p.sun_received + p.water_received
        total_mass = p.height + p.leaf + p.roots
        if energy_available >= 1.5 * total_mass:
            child = p.generate_offspring(trait_std=0.05, mutation_prob=0.05, mutation_std=0.1)
            offset = np.random.uniform(-1, 1, size=2)
            child_x = np.clip(x + offset[0], 0, world.width)
            child_y = np.clip(y + offset[1], 0, world.height)
            new_plants.append((child_x, child_y, child))

    world.plants.extend(new_plants)

# --- plot ---
fig, axes = plt.subplots(1, 3, figsize=(24, 5), sharex=True)
attributes = ['height', 'leaf', 'roots']
colors = ['green', 'lime', 'saddlebrown']

for ax, attr, color in zip(axes, attributes, colors):
    mean = stats_df[f'{attr}_mean']
    std  = stats_df[f'{attr}_std']
    min_ = stats_df[f'{attr}_min']
    max_ = stats_df[f'{attr}_max']

    ax.plot(stats_df['day'], mean, color=color, lw=2, label=f'{attr} mean')
    ax.fill_between(stats_df['day'], mean - std, mean + std, color=color, alpha=0.2, label='±1 std')
    ax.plot(stats_df['day'], max_, color=color, lw=1, linestyle='--', label='max')
    ax.plot(stats_df['day'], min_, color=color, lw=1, linestyle='--', label='min')

    ax.set_title(attr.capitalize())
    ax.set_xlabel('Day')
    ax.set_ylabel(attr.capitalize())
    ax.legend(fontsize=8)

plt.suptitle('Daily Plant Statistics with Mean ± Std and Min/Max', fontsize=16)
plt.tight_layout(rect=[0, 0, 1, 0.95])
plt.show()