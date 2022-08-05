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


# Maximum number of robots in the scene
MAX_BOTS = 2
# 0 -> in-built camera, 1 -> external USB webcam
VIDEO_SOURCE_ID = 0  ##TODO: This should be parameterized
WAIT_TIME = 1
ORIGIN_ID = 2
MAX_ID = 3


class Tracker():
    def __init__(self):
        print("init cap")
        self._cap = cv2.VideoCapture(VIDEO_SOURCE_ID, cv2.CAP_DSHOW)
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
        self._centers = []

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

    def define_coordinates(self,origin_corners,max_corners):
        self._x_center_origin = abs(origin_corners[0] - origin_corners[4])
        self._y_center_origin = abs(origin_corners[1] - origin_corners[5])

        self._x_center_max = abs(max_corners[0] - max_corners[4])
        self._y_center_max = abs(max_corners[1] - max_corners[5])


    def get_vectors_and_angle(self,corner_points,frame):
        x,y = self.get_center_from_corners(corner_points,frame)

        vector = [x,y,self._x_center_origin,y]
        cv2.line(frame, (int(vector[0]), int(vector[1])),
                        (int(vector[2]), int(vector[3])), (255, 0, 255), 2)

        vector2 = [x,y,corner_points[0],corner_points[1]]
        cv2.line(frame, (int(vector2[0]), int(vector2[1])),
                 (int(vector2[2]), int(vector2[3])), (0, 0, 255), 2)

        angle = (np.degrees(self.angle_between(vector,vector2)) + 360) % 360
        print(angle)
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

    def track_every_frame(self):
        # Get camera FOV dimensions
        args = self.get_args()
        cap_width = args.width
        cap_height = args.height

        # While camera is detected
        while self._isCamera:
            ret, frame = self._cap.read()
            if not ret:
                print("No camera source")
                self._isCamera = False
                break

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

            if len(self._detected_markers_in_this_frame[0]) > 0:
                self._centers = []
                for (fids, index) in zip(self._detected_markers_in_this_frame[0], self._detected_markers_in_this_frame[1]):
                    for pt in fids:
                        try:
                            index_number = int(index[0])
                            points_list = []

                            for point in pt:
                                points_list.extend(list(point))
                            if index_number == ORIGIN_ID:
                                self._origin_corners = points_list
                            elif index_number == MAX_ID:
                                self._max_corners = points_list
                            else:
                                self.define_coordinates(self._origin_corners, self._max_corners)
                                x_center,y_center = self.get_center_from_corners(points_list,colored_frame)
                                self._centers.append([x_center,y_center])
                                angle = self.get_vectors_and_angle(points_list,colored_frame)
                                print(self._origin_corners,self._max_corners)

                        except IndexError:
                            pass
                print(self._centers)
            if len(self._detected_markers_in_this_frame[0]) > 0:
                aruco.drawDetectedMarkers(colored_frame, self._detected_markers_in_this_frame[0],
                                          self._detected_markers_in_this_frame[1])

            cv2.imshow('frame', colored_frame)
            if cv2.waitKey(WAIT_TIME) & 0xFF == ord('q'):
                self._cap.release()
                cv2.destroyAllWindows()
                sys.exit()



if __name__ == "__main__":
    watch_dogs = Tracker()
    watch_dogs.track_every_frame()



##### OLD FUNCTIONS ####
    # def define_coordinates(self,origin_corners,max_corners):
    #     x_center_origin = abs(origin_corners[0] - origin_corners[4])
    #     y_center_origin = abs(origin_corners[1] - origin_corners[5])
    #
    #     x_center_max = abs(max_corners[0] - max_corners[4])
    #     y_center_max = abs(max_corners[1] - max_corners[5])