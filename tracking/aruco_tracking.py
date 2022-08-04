#!/usr/bin/env python

# Module to track fiducial markers


import numpy as np
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


class Tracker():
    def __init__(self):
        print("hi init cap")
        self._cap = cv2.VideoCapture(VIDEO_SOURCE_ID,cv2.CAP_DSHOW)
        print("hi init dict")
        self._dictionary = aruco.getPredefinedDictionary(aruco.DICT_4X4_50)
        print("hi init font")
        self._font = cv2.FONT_HERSHEY_SIMPLEX
        self._isCamera = True
        self._start_time = time.time()

    def track_every_frame(self):
        while self._isCamera:
            ret, frame = self._cap.read()
            if not ret:
                print("No camera source")
                self._isCamera = False
                break

            cv2.namedWindow('frame', cv2.WINDOW_NORMAL)
            cv2.resizeWindow('frame', 1280, 720)
            colored_frame = frame
            cv2.imshow('frame', colored_frame)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            parameters = aruco.DetectorParameters_create()
            font = cv2.FONT_HERSHEY_SIMPLEX

            self._detected_markers_in_this_frame = aruco.detectMarkers(colored_frame, self._dictionary,
                                                                       parameters=parameters)
            corners, ids, rejectedImgPoints = self._detected_markers_in_this_frame
            print(ids)

            if len(self._detected_markers_in_this_frame[0]) > 0:
                for (fids, index) in zip(self._detected_markers_in_this_frame[0], self._detected_markers_in_this_frame[1]):
                    for pt in fids:
                        try:
                            index_number = int(index[0])
                            points_list = []
                            for point in pt:
                                points_list.extend(list(point))

                            if time.time() - self._start_time > 2:
                                # if index_number == 1:
                                cv2.putText(frame, "Aruco: " + str(1) + " ", (0, 64), font, 1,
                                            (100, 0, 200), 2, cv2.LINE_AA)
                        except IndexError:
                            pass

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