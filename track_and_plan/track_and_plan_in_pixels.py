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
from geometry_alexedit import geometry


class GlobalPlanner():
    def __init__(self):
        self.all_paths = []

    def collision_detect(self,path1,path2):
        replan_indices = []
        replan_obstacles = []
        len1 = len(path1)
        len2 = len(path2)
        if len1 < len2:
            checks = len1
        else:
            checks = len2
        for i in range(checks):
            if path1[i]== path2[i]:
                print("bad: ",i)
                replan_indices.append(i)
                replan_obstacles.append(path1[i])


    def main(self,tracker,goals):
        # While camera is detected
        start = 0
        loop_counter = 0
        while tracker._isCamera:
            colored_frame = tracker.track_frame()

            if start == 0:
                for i in range(3):
                    colored_frame = tracker.track_frame()
                    cv2.imshow('frame', colored_frame)
                    if cv2.waitKey(tracker.WAIT_TIME) & 0xFF == ord('q'):
                        self._cap.release()
                        cv2.destroyAllWindows()
                        sys.exit()
                    print(i)
                    time.sleep(1)
                start = 1
            else:
                time.sleep(1)

            # if loop_counter%1 == 0:
                if tracker._first_obstacle == 1:
                    path_init = 0
                    cnt = 0
                    for robot in tracker.ROBOT_IDS:
                        robot_pose = (int(tracker._robots[robot][0]),int(tracker._robots[robot][1]))

                        start = (robot_pose)
                        goal = (int(goals[cnt]),int(goals[cnt+1]))
                        for obstacle in tracker._obstacle_array:
                            if goal == obstacle:
                                print("Invalid goal")
                            else:
                                path = astar(tracker.maze,start,goal)
                                self.all_paths.append(path)
                                # print("Path: ",path)
                                # if path_init == 0:
                                #     path_init == 1
                                #     prior_path = path
                                # else:
                                #     self.collision_detect(path,prior_path)

                                image = colored_frame

                                for entry in path:
                                    cv2.circle(image, (int(entry[0]),int(entry[1])), 2, (155, int(robot*4), 255), 2)
                                cv2.circle(image, (int(goal[0]), int(goal[1])), 4, (0, 0, 0), 4)

                        cnt += 2



            # loop_counter += 1
                cv2.imshow('frame', colored_frame)
                if cv2.waitKey(tracker.WAIT_TIME) & 0xFF == ord('q'):
                    self._cap.release()
                    cv2.destroyAllWindows()
                    sys.exit()


if __name__ == '__main__':
    # Init global planner
    planner = GlobalPlanner()
    # Init tracking markers
    tracker = Tracker()
    print("Number of robot markers: ",tracker.NUM_ROBOTS)
    # Init geometry
    geom = geometry()
    # Get robot goals
    goals = geom.main()
    print(goals)
    planner.main(tracker,goals)


