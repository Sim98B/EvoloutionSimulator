import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

class Mush:
    SPECIES_INFO = {
        "Amanita Muscaria": {
            "color": "red",
            "tree_weights": [1.0, 0.9, 0.9, 0.3, 0.0, 0.0],
            "humidity_opt": (0.65, 0.9),
            "temp_opt": (10, 20),
            "ph_opt": (5.0, 6.5)
        },
        "Boletus Edulis": {
            "color": "brown",
            "tree_weights": [0.8, 0.5, 0.3, 0.9, 1.0, 1.0],
            "humidity_opt": (0.35, 0.55),
            "temp_opt": (15, 24),
            "ph_opt": (5.0, 6.5)
        },
        "Cantharellus Cibarius": {
            "color": "yellow",
            "tree_weights": [0.3, 0.5, 0.5, 1.0, 1.0, 1.0],
            "humidity_opt": (0.3, 0.5),
            "temp_opt": (10, 18),
            "ph_opt": (4.5, 6.5)
        }
    }
    def __init__(self, specie: str, x: float | int, y: float):
        self.x = x
        self.y = y
        if specie not in Mush.SPECIES_INFO:
            raise ValueError(f"Specie non valida: {specie}")
        self.specie = specie
        info = Mush.SPECIES_INFO[specie]
        self.color = info["color"]
        self.mycelium = np.random.normal(loc=3, scale=1)
        self.preferred_trees = info["preferred_trees"]
        self.humidity_opt = info["humidity_opt"]
        self.temp_opt = info["temp_opt"]
        self.ph_opt = info["ph_opt"]

"""for _ in range(10):
    specie = np.random.choice(["Amanita Muscaria", "Boletus Edulis", "Cantharellus Cibarius"])
    m = Mush(x=0,y=0,specie=specie)
    print(f"{specie} | Mycelium: {m.mycelium}")"""