import random

class Blob:
    def __init__(self, x, y, genome=None):
        self.x = x
        self.y = y
        # Geni: speed, size e sense_radius
        self.genome = genome or {
            "speed": 10.0,
            "size": 10.0,
            "sense_radius": 20.0
        }
        self.food_eaten = 0  # contatore di cibo mangiato in questa generazione

    def reset_food(self):
        self.food_eaten = 0

    def move(self, dx, dy, world_size):
        # Muove il blob limitando la posizione alla griglia
        self.x = max(0, min(world_size - 1, self.x + dx))
        self.y = max(0, min(world_size - 1, self.y + dy))

    def is_alive(self):
        # Tutti i blob sono “alive” fino a fine generazione
        return True
