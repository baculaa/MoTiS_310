#!/usr/bin/env python

# Module to track fiducial markers

## INSTALL IF NOT ALREADY: opencv-python, opencv-contrib-python

import numpy as np
import argparse
import cv2
import cv2.aruco as aruco
import json
import math
import time
import csv
import sys

# sys.path.insert(0,"MoTiS_310/MoTiS_310/rrt_algs")
# from rrt_star_2d2 import rrt_star_wrap

class Tracker():
    def __init__(self):
        # Generally:
        # 0 -> in-built camera, 1 -> external USB webcam
        self.VIDEO_SOURCE_ID = 0
        self.WAIT_TIME = 1
        self.ORIGIN_ID = 1
        self.MAX_ID = 0
        self.ROBOT_IDS = [2,4]


        print("init cap")
        self._cap = cv2.VideoCapture(self.VIDEO_SOURCE_ID, cv2.CAP_DSHOW)
        print("init dict")
        self._dictionary = aruco.getPredefinedDictionary(aruco.DICT_4X4_50)
        print("init font")
        self._font = cv2.FONT_HERSHEY_SIMPLEX
        print("init camera")
        self._isCamera = True
        print("init time")
        self._start_time = time.time()


        self._origin_corners = [4.0, 48.0, 5.0, 15.0, 33.0, 13.0, 34.0, 46.0]
        self._max_corners = [896.0, 536.0, 899.0, 508.0, 924.0, 506.0, 922.0, 533.0]
        self._x_center_origin = self._origin_corners[0]
        self._y_center_origin = self._origin_corners[1]

        self._x_center_max = 1000
        self._y_center_max = 1000

        self.maze = np.zeros((int(self._x_center_max),int(self._y_center_max)))
        self._robots = np.zeros((10,3))


    def get_args(self):
        ### Get camera field of view dimensions ###
        parser = argparse.ArgumentParser()

        parser.add_argument("--width", help='cap width', type=int, default=960)
        parser.add_argument("--height", help='cap height', type=int, default=540)

        args = parser.parse_args()
        return args

    def angle_between(self,v1, v2):
        p1 = [v1[0],v1[1]]
        p0 = [v1[2],v1[3]]
        p2 = [v2[2],v2[3]]

        v0 = np.array(p0) - np.array(p1)
        v1 = np.array(p2) - np.array(p1)

        angle = np.math.atan2(np.linalg.det([v0, v1]), np.dot(v0, v1))
        return angle

    def define_coordinates(self,origin_corners,max_corners,frame):
        self._x_center_origin,self._y_center_origin = self.get_center_from_corners(origin_corners,frame)

        self._x_center_max,self._y_center_max = self.get_center_from_corners(max_corners,frame)

    def get_vectors_and_angle(self,corner_points,frame):
        x,y = self.get_center_from_corners(corner_points,frame)

        vector = [x,y,self._x_center_origin,y]
        cv2.line(frame, (int(vector[0]), int(vector[1])),
                        (int(vector[2]), int(vector[3])), (255, 0, 255), 2)

        vector2 = [x,y,corner_points[0],corner_points[1]]
        cv2.line(frame, (int(vector2[0]), int(vector2[1])),
                 (int(vector2[2]), int(vector2[3])), (0, 0, 255), 2)

        angle = (np.degrees(self.angle_between(vector,vector2)) + 360) % 360
        # print(angle)
        return angle

    def get_center_from_corners(self,corner_points,frame):
        # Find min dimension in camera x and y
        if corner_points[0] < corner_points[4]:
            x_min = corner_points[0]
        else:
            x_min = corner_points[4]

        if corner_points[1] < corner_points[5]:
            y_min = corner_points[1]
        else:
            y_min = corner_points[5]

        # Find difference between corners in camera x and y
        x_center = abs(corner_points[0]-corner_points[4])/2 + x_min
        y_center = abs(corner_points[1]-corner_points[5])/2 + y_min

        # Draw pink circle in center of each marker
        cv2.circle(frame, (int(x_center), int(y_center)), 2, (255, 0, 255), 2)

        return x_center,y_center

    def obstacle_define(self,obs_x,obs_y):
        # FUNC: Pad the obstacle from its center point so it can be read by the planner
        # Pad constant (unit: pixels)
        obstacle_padding = 35

        # Pad obstacle from center
        ## It's a weird way to do it, but the planner only takes square obstacles
        obstacle = (int(obs_x - obstacle_padding), int(obs_y - obstacle_padding), int(obs_x + obstacle_padding),
                        int(obs_y + obstacle_padding))

        return obstacle

    def draw_path(self, path, image):
        initial_entry = 1
        for entry in path:
            if initial_entry == 1:
                # print("where circle")
                cv2.circle(image, (entry), 5, (155, 0, 255), 3)
                initial_entry = 0
                prior_entry = entry
            else:
                cv2.circle(image, (entry), 5, (155, 0, 255), 3)
                cv2.line(image, (prior_entry),
                        (entry), (155, 0, 255), 2)
                prior_entry = entry



    def create_map(self,height,width):
        # Init map that is the size of the camera view
        self.maze = np.zeros((int(width),int(height)))
        # Add obstacles to map
        for obstacle in self._obstacle_array:
            for x_pixel in range(int(obstacle[0]),int(obstacle[2])):
                for y_pixel in range(int(obstacle[1]),int(obstacle[3])):
                    self.maze[x_pixel,y_pixel] = int(1)
        np.savetxt("foo.csv", self.maze, delimiter=",")

    def track_frame(self):
        # Get camera FOV dimensions
        args = self.get_args()
        cap_width = args.width
        cap_height = args.height


        ret, frame = self._cap.read()
        if not ret:
            print("No camera source")
            self._isCamera = False
        # else:
            # print("Camera ready")


        # Set camera FOV width and height
        self._cap.set(cv2.CAP_PROP_FRAME_WIDTH, cap_width)
        self._cap.set(cv2.CAP_PROP_FRAME_HEIGHT, cap_height)

        # Open window with camera view
        cv2.namedWindow('frame', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('frame', cap_width,cap_height)
        colored_frame = frame
        cv2.imshow('frame', colored_frame)


        # Get aruco tag parameters
        parameters = aruco.DetectorParameters_create()

        # List of detected markers
        self._detected_markers_in_this_frame = aruco.detectMarkers(colored_frame, self._dictionary,
                                                                   parameters=parameters)

        # Corner pixels, aruco id numbers, and rejected tags
        corners, ids, rejectedImgPoints = self._detected_markers_in_this_frame
        # print("here")
        # Init obstacle flag
        self._first_obstacle = 0
        self._obstacle_array = [(100,100,110,110)]

        # If there are markers detected
        if len(self._detected_markers_in_this_frame[0]) > 0:

            # For every detected marker
            for (fids, index) in zip(self._detected_markers_in_this_frame[0], self._detected_markers_in_this_frame[1]):
                for pt in fids:
                    try:
                        # Get the index number of the marker
                        index_number = int(index[0])
                        # print(index_number)
                        # Init the list of corner points
                        points_list = []

                        # For every point in the corners list
                        for point in pt:
                            # Add to the list of corners
                            points_list.extend(list(point))

                        # If the markers is the origin
                        if index_number == self.ORIGIN_ID:
                            # SET ORIGIN
                            self._origin_corners = points_list
                        # If the marker is the max
                        elif index_number == self.MAX_ID:
                            # SET MAX
                            self._max_corners = points_list
                        elif any(index_number == robot for robot in self.ROBOT_IDS):
                            # print("HIHIHIHIHIHIHIHI")
                            # Define the coordinates based on the origin and max
                            self.define_coordinates(self._origin_corners, self._max_corners,colored_frame)
                            # Get the x,y of the center of the marker
                            x_center, y_center = self.get_center_from_corners(points_list, colored_frame)
                            # Add the center to the list of markers
                            # print(index_number)
                            self._robots[index_number,0] = x_center
                            self._robots[index_number,1] = y_center
                            # Get the angle of the marker
                            angle = self.get_vectors_and_angle(points_list, colored_frame)
                            self._robots[index_number,2] = angle
                        # If the marker is not robot
                        else:
                            # FOR NOW ALL OBSTACLES
                            # Define the coordinates based on the origin and max
                            self.define_coordinates(self._origin_corners, self._max_corners,colored_frame)
                            # Get the x,y of the center of the marker
                            x_center,y_center = self.get_center_from_corners(points_list,colored_frame)

                            if self._first_obstacle == 0:
                                self._obstacle_array = [self.obstacle_define(x_center,y_center)]
                                # Set obstacle flag to 1
                                self._first_obstacle = 1
                            else:
                                self._obstacle_array.append(self.obstacle_define(x_center,y_center))

                    except IndexError:
                        pass

            print("Obstacle array: ",self._obstacle_array)
            self.create_map(cap_height,cap_width)

            # print(self.maze)
            aruco.drawDetectedMarkers(colored_frame, self._detected_markers_in_this_frame[0],
                                          self._detected_markers_in_this_frame[1])
        return colored_frame



if __name__ == "__main__":
    watch_dogs = Tracker()
    while watch_dogs._isCamera:
        watch_dogs.track_frame()



##### OLD FUNCTIONS ####
    # def define_coordinates(self,origin_corners,max_corners):
    #     x_center_origin = abs(origin_corners[0] - origin_corners[4])
    #     y_center_origin = abs(origin_corners[1] - origin_corners[5])
    #
    #     x_center_max = abs(max_corners[0] - max_corners[4])
    #     y_center_max = abs(max_corners[1] - max_corners[5])