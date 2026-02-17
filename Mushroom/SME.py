import numpy as np
import matplotlib.pyplot as plt
from Mushroom import Mush
from Wood import Wood

#np.random.seed(42)
plt.ion()
fig, ax = plt.subplots()

wood = Wood(size = 1, resolution = 200)
mushrooms = 10
generations = 20

wood.mush=[Mush(x=np.random.uniform(0,wood.size), y=np.random.uniform(0,wood.size)) for i in range(10)]
wood.display(ax)
plt.pause(1)
