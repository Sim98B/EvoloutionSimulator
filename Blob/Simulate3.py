import random
import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import time
from Food import Food
from Blob3 import Blob
from World3 import World

plt.ion()
fig, ax = plt.subplots()
w = World()
epochs_to_evolve = 10
for idx, epoch in enumerate(range(epochs_to_evolve)):
    b = Blob(x=random.randint(0, w.size - 1), y=random.randint(0, w.size - 1))
    w.add_blob(blob = b)
w.display(ax)
plt.pause(3)