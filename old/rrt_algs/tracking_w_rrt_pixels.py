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
from a_star import astar


class Planner():
    def __init__(self):
        pass

    def main(self,tracker):
        # While camera is detected
        start = 0
        while tracker._isCamera:
            colored_frame = tracker.track_frame()

            cv2.imshow('frame', colored_frame)
            if cv2.waitKey(tracker.WAIT_TIME) & 0xFF == ord('q'):
                self._cap.release()
                cv2.destroyAllWindows()
                sys.exit()

            if start == 0:
                time.sleep(5)
                start = 1
            else:
                pass

            if tracker._first_obstacle == 1:
                start = (150,150)
                goal = (500,500)
                path = astar(tracker.maze,start,goal)
                print(path)
                tracker.draw_path(path,colored_frame)

                # cv2.imshow('frame', colored_frame)


if __name__ == '__main__':
    planner = Planner()
    tracker = Tracker()
    planner.main(tracker)
