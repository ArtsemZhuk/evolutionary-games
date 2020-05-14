from graph import *
import numpy as np
import matplotlib.pyplot as plt
import time
from utils import Timer

if __name__ == '__main__':
    timer = Timer()
    graph = ScaleFree(1000, 2)
    print(f'Elapsed for generation {timer.measure()}')
    print(f'Average degree = {graph.average_degree()}')
    degs = graph.degrees()
    x = [np.log(d) for d in degs.keys()]
    y = [np.log(c) for c in degs.values()]
    plt.scatter(x, y)
    plt.show()

