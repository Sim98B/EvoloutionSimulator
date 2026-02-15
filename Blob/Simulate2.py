import random
import matplotlib.pyplot as plt
from Blob2 import Blob
from World2 import World

# ----------------------------
# Impostazioni iniziali
# ----------------------------
world_size = 30
initial_food = 30
initial_blobs = 100
generations = 50
ticks_per_gen = 50
mutation_var = 0.5

# Creazione mondo
world = World(size=world_size, food_per_gen=initial_food)

# Spawn iniziale dei blob ai bordi
for _ in range(initial_blobs):
    world.spawn_blob_at_border(genome={
        "speed": 10.0,
        "size": 10.0,
        "sense_radius": 20.0
    })

# Attiva matplotlib interattivo
plt.ion()
fig, ax = plt.subplots()

# ----------------------------
# Stampa iniziale
# ----------------------------
print(
    f"Gen 0 | Popolazione: {len(world.blobs)} | "
    f"Speed medio: {sum(b.genome['speed'] for b in world.blobs)/len(world.blobs):.2f} | "
    f"Sense medio: {sum(b.genome['sense_radius'] for b in world.blobs)/len(world.blobs):.2f}"
)

# ----------------------------
# Ciclo generazioni
# ----------------------------
for gen in range(1, generations + 1):
    # Genera cibo
    world.spawn_food()

    # Tick della generazione
    for _ in range(ticks_per_gen):
        world.step()

    # Riproduzione e statistica
    nati, sopravvissuti, morti = world.reproduce(mutation_var=mutation_var)

    if len(world.blobs) == 0:
        print(f"Simulazione finita alla generazione {gen}")
        break

    # Statistiche
    speed_medio = sum(b.genome['speed'] for b in world.blobs)/len(world.blobs)
    sense_medio = sum(b.genome['sense_radius'] for b in world.blobs)/len(world.blobs)

    print(
        f"Gen {gen} | Popolazione: {len(world.blobs)} | "
        f"Speed medio: {speed_medio:.2f} | "
        f"Sense medio: {sense_medio:.2f} | "
        f"Nati: {nati} | Sopravvissuti: {sopravvissuti} | Morti: {morti}"
    )

    # Visualizzazione
    world.display(ax)
    plt.pause(0.1)

# ----------------------------
# Mostra grafico finale
# ----------------------------
plt.ioff()
plt.show()
plt.tight_layout()
