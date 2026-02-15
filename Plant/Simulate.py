import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
#import plotly.graph_objects as go
from Plant import Plant
from World import World
#np.random.seed(0)
# --- setup mondo ---
world = World(width=10, height=10)
starting_plants = 50
plants = [Plant(total_energy = 1) for _ in range(starting_plants)]
positions = np.random.uniform(0, 10, (starting_plants, 2))
stats_df = pd.DataFrame(columns=[
    'day',
    'height_mean', 'height_std', 'height_min', 'height_max',
    'leaf_mean',   'leaf_std',   'leaf_min',   'leaf_max',
    'roots_mean',  'roots_std',  'roots_min',  'roots_max'
])

for pos, plant in zip(positions, plants):
    world.place_plant(pos[0], pos[1], plant)

# --- simulazione per 10 giorni ---
for day in range(100):
    print(f"\n=== Day {day + 1} ===")
    print(len(world.plants))

    # energia totale giornaliera dall'ambiente
    water, sun = world.energy()
    print(f"Total water received: {water:.3f}")
    print(f"Total sun received: {sun:.3f}")

    # ordiniamo le piante per altezza decrescente per gestire luce
    plants_sorted = sorted(world.plants, key=lambda x: x[2].height, reverse=True)

    # calcolo luce (sun) considerando sovrapposizione e ombreggiamento
    for i, (x, y, plant) in enumerate(plants_sorted):
        sun_received = sun
        for j in range(i):  # piante più alte già processate
            xj, yj, other = plants_sorted[j]
            dist = np.hypot(x - xj, y - yj)
            if dist < (plant.leaf + other.leaf):
                # riduzione luce proporzionale a sovrapposizione e altezza
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

    world.plants = [(x, y, p) for (x, y, p) in world.plants if p.alive]

    if world.plants:  # se ci sono piante vive
        heights = np.array([p.height for _, _, p in world.plants])
        leaves = np.array([p.leaf for _, _, p in world.plants])
        roots = np.array([p.roots for _, _, p in world.plants])

        stats_df.loc[len(stats_df)] = [
            day + 1,
            heights.mean(), heights.std(), heights.min(), heights.max(),
            leaves.mean(), leaves.std(), leaves.min(), leaves.max(),
            roots.mean(), roots.std(), roots.min(), roots.max()
        ]
    else:
        # nessuna pianta viva, riempi NaN
        stats_df.loc[len(stats_df)] = [day + 1] + [np.nan] * 12

    # mostra stato del mondo come testo
    """for i, (x, y, plant) in enumerate(world.plants):
        print(f"Plant {i}: Height={plant.height:.3f}, Leaf={plant.leaf:.3f}, Roots={plant.roots:.3f}")"""
    if day % 10 == 0 or day == 10:
        world.show_world()
fig, axes = plt.subplots(1, 3, figsize=(18, 5), sharex=True)

attributes = ['height', 'leaf', 'roots']
colors = ['green', 'lime', 'saddlebrown']

#print(stats_df.iloc[-1])

for ax, attr, color in zip(axes, attributes, colors):
    mean = stats_df[f'{attr}_mean']
    std  = stats_df[f'{attr}_std']
    min_ = stats_df[f'{attr}_min']
    max_ = stats_df[f'{attr}_max']

    # linea media
    ax.plot(stats_df['day'], mean, color=color, lw=2, label=f'{attr} mean')

    # alone ± std
    ax.fill_between(stats_df['day'], mean - std, mean + std, color=color, alpha=0.2, label='±1 std')

    # linee max e min
    ax.plot(stats_df['day'], max_, color=color, lw=1, linestyle='--', label='max')
    ax.plot(stats_df['day'], min_, color=color, lw=1, linestyle='--', label='min')

    ax.set_title(attr.capitalize())
    ax.set_xlabel('Day')
    ax.set_ylabel(attr.capitalize())
    ax.legend(fontsize=8)

plt.suptitle('Daily Plant Statistics with Mean ± Std and Min/Max', fontsize=16)
plt.tight_layout(rect=[0, 0, 1, 0.95])
plt.show()

"""attributes = ['height', 'leaf', 'roots']
colors = ['green', 'lime', 'saddlebrown']

fig = go.Figure()

for attr, color in zip(attributes, colors):
    fig.add_trace(go.Scatter(
        x=stats_df['day'],
        y=stats_df[f'{attr}_mean'],
        mode='lines+markers',
        name=f'{attr} mean',
        line=dict(color=color, width=2),
        hovertemplate=
        f"{attr} mean: %{y:.3f}<br>Day: %{x}<extra></extra>"
    ))

    # ± std come area
    fig.add_trace(go.Scatter(
        x=list(stats_df['day']) + list(stats_df['day'])[::-1],
        y=list(stats_df[f'{attr}_mean'] + stats_df[f'{attr}_std']) +
          list((stats_df[f'{attr}_mean'] - stats_df[f'{attr}_std'])[::-1]),
        fill='toself',
        fillcolor=color.replace('green','rgba(0,128,0,0.2)').replace('lime','rgba(50,205,50,0.2)').replace('saddlebrown','rgba(139,69,19,0.2)'),
        line=dict(color='rgba(255,255,255,0)'),
        hoverinfo='skip',
        showlegend=False
    ))

    # max
    fig.add_trace(go.Scatter(
        x=stats_df['day'],
        y=stats_df[f'{attr}_max'],
        mode='lines',
        line=dict(color=color, width=1, dash='dash'),
        name=f'{attr} max',
        hovertemplate=f"{attr} max: %{y:.3f}<br>Day: %{x}<extra></extra>"
    ))

    # min
    fig.add_trace(go.Scatter(
        x=stats_df['day'],
        y=stats_df[f'{attr}_min'],
        mode='lines',
        line=dict(color=color, width=1, dash='dot'),
        name=f'{attr} min',
        hovertemplate=f"{attr} min: %{y:.3f}<br>Day: %{x}<extra></extra>"
    ))

fig.update_layout(
    title="Daily Plant Statistics (Interactive)",
    xaxis_title="Day",
    yaxis_title="Value",
    hovermode="x unified",
    template="plotly_white"
)

fig.show()"""