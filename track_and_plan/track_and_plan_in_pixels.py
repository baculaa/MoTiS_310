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

    def collision_detect(self,path1,path2):
        for entry1 in path1:
            for entry2 in path2:
                if entry1 == entry2:
                    print("bad")

    def main(self,tracker):
        # While camera is detected
        start = 0
        loop_counter = 0
        while tracker._isCamera:
            colored_frame = tracker.track_frame()

            # cv2.imshow('frame', colored_frame)


            if start == 0:
                for i in range(300):
                    # cv2.imshow('frame', colored_frame)
                    # if cv2.waitKey(tracker.WAIT_TIME) & 0xFF == ord('q'):
                    #     self._cap.release()
                    #     cv2.destroyAllWindows()
                    #     sys.exit()
                    print(i)
                start = 1
            else:
                time.sleep(1)

            if loop_counter%10 == 0:
                if tracker._first_obstacle == 1:
                    path_init = 0
                    for robot in tracker.ROBOT_IDS:
                        robot_pose = (int(tracker._robots[robot][0]),int(tracker._robots[robot][1]))

                        start = (robot_pose)
                        goal = (int(tracker._x_center_origin),int(tracker._y_center_origin))
                        path = astar(tracker.maze,start,goal)
                        print("Path: ",path)
                        # if path_init == 0:
                        #     path_init == 1
                        #     prior_path = path
                        # else:
                        #     self.collision_detect(path,prior_path)


                        # tracker.draw_path(path,colored_frame)


                        # image = colored_frame
                        # for entry in path:
                        #     cv2.circle(image, (int(entry[0]),int(entry[1])), 2, (155, 0, 255), 2)


            loop_counter += 1
            # cv2.imshow('frame', colored_frame)
            # if cv2.waitKey(tracker.WAIT_TIME) & 0xFF == ord('q'):
            #     self._cap.release()
            #     cv2.destroyAllWindows()
            #     sys.exit()


if __name__ == '__main__':
    planner = Planner()
    tracker = Tracker()
    planner.main(tracker)
