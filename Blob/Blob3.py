import random
import math

#random.seed(0)

class Blob:
    def __init__(self, x, y, genome = None):
        self.x = x
        self.y = y
        self.energy = 1000
        self.genome = genome or {
            "speed": {
                "trait": 10,
                "mutability": 0.5
            },
            "size": {
                "trait": 10,
                "mutability": 0.5
            },
            "sense": {
                "trait": 20,
                "mutability": 0.5
            }
        }
        self.food_eaten = 0
        self.cost_per_move = self.genome['sense']['trait'] + (self.genome['size']['trait']**3 * self.genome['speed']['trait']**2) / 10_000
        self.speed = self.genome['speed']['trait'] / self.genome['size']['trait'] / 2

    def move(self, world_size, target=None, avoid=None):
        """
        Movimento continuo:
        - target: (x, y) verso cui muoversi
        - avoid: (x, y) da cui allontanarsi
        - se nessuno dei due è presente, movimento casuale
        """
        # vettore direzione
        if target is not None:
            dx = target[0] - self.x
            dy = target[1] - self.y
        elif avoid is not None:
            dx = self.x - avoid[0]
            dy = self.y - avoid[1]
        else:
            angle = random.uniform(0, 1000 * math.pi)
            dx = math.cos(angle)
            dy = math.sin(angle)

        # lunghezza del vettore
        length = math.hypot(dx, dy)
        if length > 0:
            dx /= length
            dy /= length

        # spostamento proporzionale alla velocità
        dx *= self.speed
        dy *= self.speed

        # aggiorna posizione (campo continuo)
        self.x += dx
        self.y += dy

        # clamp ai bordi
        self.x = max(0, min(world_size, self.x))
        self.y = max(0, min(world_size, self.y))

        # consumo energetico proporzionale al movimento
        move_cost = self.cost_per_move * math.hypot(dx, dy)
        self.energy -= move_cost

    def perceive(self, world):
        """
        Restituisce:
            - target_food: il cibo più vicino nel raggio di senso, oppure None
            - nearest_blob: il blob più vicino entro il raggio di senso da evitare (opzionale)
        """
        target_food = None
        min_food_dist = float('inf')

        # cerca il cibo visibile
        for f in world.food:
            dist = abs(f.x - self.x) + abs(f.y - self.y)  # distanza Manhattan
            if dist <= self.genome['sense']['trait'] and dist < min_food_dist:
                min_food_dist = dist
                target_food = (f.x, f.y)

        # pericoli opzionali: altri blob
        nearest_blob = None
        min_blob_dist = float('inf')
        for b in world.blobs:
            if b is self:
                continue
            dist = abs(b.x - self.x) + abs(b.y - self.y)
            if dist <= self.genome['sense']['trait'] and dist < min_blob_dist:
                min_blob_dist = dist
                nearest_blob = (b.x, b.y)

        return target_food, nearest_blob

    def reproduce(self):
        new_genome = {
            "speed": {
                "trait": max(random.normalvariate(self.genome["speed"]["trait"], self.genome["speed"]["mutability"]), 0),
                "mutability": self.genome["speed"]["mutability"]
            },
            "size": {
                "trait": max(random.normalvariate(self.genome["size"]["trait"], self.genome["size"]["mutability"]), 0),
                "mutability": self.genome["size"]["mutability"]
            },
            "sense": {
                "trait": max(random.normalvariate(self.genome["sense"]["trait"], self.genome["sense"]["mutability"]), 0),
                "mutability": self.genome["sense"]["mutability"]
            }
        }
        new_blob = Blob(self.x, self.y, new_genome)
        return new_blob

    def reset_food(self):
        self.food_eaten = 0