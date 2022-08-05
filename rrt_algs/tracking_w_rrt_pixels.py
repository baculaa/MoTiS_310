#!/usr/bin/env python
# -*- coding: utf-8 -*-
# https://github.com/Kazuhito00/AprilTag-Detection-Python-Sample

import copy
import time
import argparse
import csv
import numpy as np

import cv2
import sys

sys.path.append("MoTiS_310/tracking")
from aruco_tracking import Tracker
from rrt_star_2d2 import rrt_star_wrap


class Planner():
    def __init__(self):
        self.stop_rrt = 0

    def main(self,tracker):
        # While camera is detected
        while tracker._isCamera:
            colored_frame = tracker.track_frame()

            # if tracker._first_obstacle == 1:
            #     if np.allclose(tracker._obstacle_array, self.prior_obstacle, atol=2):
            #         self.stop_rrt = 0
            #         # print("SAME: ", obstacle_array, self.prior_obstacle)
            #     else:
            #         self.stop_rrt = 0
            #         # print("DIF: ", tracker._obstacle_array, self.prior_obstacle)

                # self.prior_obstacle = obstacle_array

            # if self.stop_rrt == 0:
            #     if tracker._first_obstacle == 1:
            #         path = a_star_wrap(tracker._x_center_origin,tracker._x_center_max,tracker._y_center_origin,tracker._y_center_max,tracker._obstacle_array)
            #     else:
            #         path = []
            #         pass
            # if path:
            #     print("Path: ",path)
            #     tracker.draw_path(path,colored_frame)
            # else:
            #     self.stop_rrt = 0



            cv2.imshow('frame', colored_frame)
            if cv2.waitKey(tracker.WAIT_TIME) & 0xFF == ord('q'):
                self._cap.release()
                cv2.destroyAllWindows()
                sys.exit()


if __name__ == '__main__':
    planner = Planner()
    tracker = Tracker()
    planner.main(tracker)
