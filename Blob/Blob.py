import random
#import numpy as np
import math

class Blob:
    def __init__(self, x, y, genome=None):
        self.x = x
        self.y = y
        self.genome = genome or {
            "speed": random.uniform(0.5, 1.5),
            "sense_radius": random.randint(1, 5)
        }
        self.food_eaten = 0  # conteggio cibi

    def reset_food(self):
        self.food_eaten = 0

    def move(self, dx, dy, world_size):
        self.x = max(0, min(world_size - 1, self.x + dx))
        self.y = max(0, min(world_size - 1, self.y + dy))

    def is_alive(self):
        # nel modello semplificato, tutti i blob sono “alive” fino alla fine della generazione
        return True