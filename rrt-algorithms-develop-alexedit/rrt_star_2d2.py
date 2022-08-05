# This file is subject to the terms and conditions defined in
# file 'LICENSE', which is part of this source code package.
import numpy as np
import matplotlib.pyplot as plt
# from tracking import tracking

from src.rrt.rrt_star import RRTStar
from src.search_space.search_space import SearchSpace
# from src.utilities.plotting import Plot

# track = tracking()

# This code does positioning with overhead cameras and april tags
## April tags 0 and 1 are set as the corners and used as references to create a coordinate system
# track.main()


def rrt_star_wrap(x_min,x_max,y_min,y_max,obstacle_array):
    X_dimensions = np.array([(x_min, x_max), (y_min, y_max)])  # dimensions of Search Space
    # print("Dimension space: ",X_dimensions)
    # obstacles
    # Obstacles = np.array([(20, 20, 40, 40), (20, 60, 40, 80), (60, 20, 80, 40), (60, 60, 80, 80)])
    Obstacles = obstacle_array
    x_init = (x_min, y_min)  # starting location
    x_goal = (x_max, y_max)  # goal location
    print("x init: ", x_init,"x_goal: ",x_goal)

    Q = np.array([(5, 5)])  # length of tree edges
    r = 1  # length of smallest edge to check for intersection with obstacles
    max_samples = 10048  # max number of samples to take before timing out
    rewire_count = 32  # optional, number of nearby branches to rewire
    prc = 0.1  # probability of checking for a connection to goal

    # create Search Space
    X = SearchSpace(X_dimensions, Obstacles)

    # create rrt_search
    rrt = RRTStar(X, Q, x_init, x_goal, max_samples, r, prc, rewire_count)
    path = rrt.rrt_star()


    # print(path[0][1])
    # if len(path):
    #     x = []
    #     y = []
    #     for i in range(len(path)):
    #         x.append(path[i][0])
    #         y.append(path[i][1])
    #     print(x)
    #     print(y)
    #     plt.plot(x,y)
    #     plt.show()
    return path