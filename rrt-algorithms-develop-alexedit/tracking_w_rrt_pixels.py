#!/usr/bin/env python
# -*- coding: utf-8 -*-
# https://github.com/Kazuhito00/AprilTag-Detection-Python-Sample

import copy
import time
import argparse
import csv
import numpy as np

import cv2 as cv
import sys

sys.path.append("C:/Users/Alexandra/PycharmProjects/MoTiS/apriltags/src/pupil_apriltags")
from bindings import Detector
from rrt_star_2d2 import rrt_star_wrap

class tracking():
    def __init__(self):
        self.centers = []
        # top right corner
        self.id_origin = [0,0]
        # bottom left corner
        self.id_max = [10,10]
        self.init_update = 0

        self.zero_zero_tag = 4
        self.max_max_tag = 3
        self.stop_rrt = 0
        self.prior_obstacle = []
        self.robot_tags = [7,8]

    def get_args(self):
        parser = argparse.ArgumentParser()

        parser.add_argument("--device", type=int, default=0)
        parser.add_argument("--width", help='cap width', type=int, default=960)
        parser.add_argument("--height", help='cap height', type=int, default=540)

        parser.add_argument("--families", type=str, default='tag36h11')
        parser.add_argument("--nthreads", type=int, default=1)
        parser.add_argument("--quad_decimate", type=float, default=2.0)
        parser.add_argument("--quad_sigma", type=float, default=0.0)
        parser.add_argument("--refine_edges", type=int, default=1)
        parser.add_argument("--decode_sharpening", type=float, default=0.25)
        parser.add_argument("--debug", type=int, default=0)

        args = parser.parse_args()

        return args


    def main(self):
        args = self.get_args()

        ##################################
        ######### CAMERA SETUP ###########
        ##################################
        cap_device = 1 #args.device 1 for southtown cam
        cap_width = args.width
        cap_height = args.height
        # print(cap_height,cap_width)
        # print("hi this file")

        families = args.families
        nthreads = args.nthreads
        quad_decimate = args.quad_decimate
        quad_sigma = args.quad_sigma
        refine_edges = args.refine_edges
        decode_sharpening = args.decode_sharpening
        debug = args.debug

        cap = cv.VideoCapture(cap_device,cv.CAP_DSHOW)
        print(cap.isOpened())
        cap.set(cv.CAP_PROP_FRAME_WIDTH, cap_width)
        cap.set(cv.CAP_PROP_FRAME_HEIGHT, cap_height)


        at_detector = Detector(
            # searchpath=["C:/Users/Alexandra/PycharmProjects/MoTiS/apriltags/src/pupil_apriltags/lib"],
            families=families,
            nthreads=nthreads,
            quad_decimate=quad_decimate,
            quad_sigma=quad_sigma,
            refine_edges=refine_edges,
            decode_sharpening=decode_sharpening,
            debug=debug,
        )
        elapsed_time = 0

        # Does the image exist?
        while True:
            start_time = time.time()

            ret, image = cap.read()
            if not ret:
                break
            debug_image = copy.deepcopy(image)
            image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)

            ##################################
            ### TAG DETECTION AND SORTING  ###
            ##################################
            tags = at_detector.detect(
                image,
                estimate_tag_pose=False,
                camera_params=None,
                tag_size=None,
            )

            # Init obstacle flag
            first_obstacle = 0
            # Go through all the tags
            for tag in tags:
                # If the tag is the origin, set it as the global origin
                if tag.tag_id == self.zero_zero_tag:
                    self.id_origin = tag.center
                # If the tag is the max, set it as the global max
                elif tag.tag_id == self.max_max_tag:
                    self.id_max = tag.center
                # If the tag is a robot, save robot positions
                elif tag.tag_id == any(self.robot_tags):
                    pass
                    # fix this function later
                # Otherwise assume the tag is an obstacle
                else: #tag.tag_id != self.zero_zero_tag and tag.tag_id != self.max_max_tag:
                    obstacle_padding = 25
                    ob1,ob2 = self.pixel_to_coords(tag.corners[1][0],tag.corners[1][1])
                    ob3,ob4 = self.pixel_to_coords(tag.corners[3][0],tag.corners[3][1])
                    if np.linalg.norm([ob1,ob2]) < np.linalg.norm([ob3,ob4]):
                        obstacle = (ob1-obstacle_padding,ob2-obstacle_padding,ob3+obstacle_padding,ob4+obstacle_padding)
                    else:
                        obstacle = (ob3-obstacle_padding, ob4-obstacle_padding, ob1+obstacle_padding, ob2+obstacle_padding)


                    if first_obstacle == 0:
                        obstacle_array = np.array([(obstacle)])
                        first_obstacle = 1
                        self.prior_obstacle = obstacle_array
                    else:
                        obstacle_array = np.append(obstacle_array,(obstacle))
                    # print("obstacle:", obstacle_array)



            x_min,y_min = self.pixel_to_coords(self.id_origin[0],self.id_origin[1])
            x_max,y_max = self.pixel_to_coords(self.id_max[0],self.id_max[1])
            # print("Is Obstacles? ",  first_obstacle)
            if self.stop_rrt == 0:
                if first_obstacle == 1:
                    path = rrt_star_wrap(x_min,x_max,y_min,y_max,obstacle_array)

                else:
                    # path = rrt_star_wrap(x_min, x_max, y_min, y_max, np.array([(4,1,5,2)]))
                    path = []
                    pass
            if path:
                self.draw_path(path,debug_image)
                print("Path: ",path)
            else:
                self.stop_rrt = 0


            if first_obstacle == 1:
                if np.allclose(obstacle_array, self.prior_obstacle, atol=2):
                    self.stop_rrt = 0
                    # print("SAME: ", obstacle_array, self.prior_obstacle)
                else:
                    self.stop_rrt = 0
                    print("DIF: ", obstacle_array, self.prior_obstacle)

                self.prior_obstacle = obstacle_array

            elapsed_time = time.time() - start_time
            debug_image = self.draw_tags(debug_image, tags, elapsed_time)


            key = cv.waitKey(1)
            if key == 27:  # ESC
                break


            cv.imshow('AprilTag Detect Demo', debug_image)

        cap.release()
        cv.destroyAllWindows()

    def draw_path(self,path,image):
        initial_entry = 1
        for entry in path:
            if initial_entry == 1:
                cv.circle(image, (int(entry[0]), int(entry[1])), 5, (255, 0, 255), 3)
                initial_entry = 0
                prior_entry = entry
            else:
                cv.circle(image, (int(entry[0]), int(entry[1])), 5, (255, 0, 255), 3)
                cv.line(image, (int(prior_entry[0]), int(prior_entry[1])),
                        (int(entry[0]), int(entry[1])), (255, 0, 255), 2)
                prior_entry = entry


    def pixel_to_coords(self,current_x,current_y):
        # min_x = self.id_origin[0]
        # min_y = self.id_origin[1]
        # max_x = self.id_max[0]
        # max_y = self.id_max[1]
        #
        # x_dif = max_x-min_x
        # y_dif = max_y-min_y
        #
        # if y_dif >= x_dif:
        #     dif = x_dif
        # else:
        #     dif = y_dif
        #
        # x_coord = (10 * (current_x - min_x) / dif)
        # y_coord = (10 * (current_y - min_y) / dif)
        # # x_coord = '%.1f'%(10*(current_x - min_x) / dif)
        # # y_coord = '%.1f'%(10*(current_y-min_y)/ dif)

        return int(current_x),int(current_y)


    def draw_axes(self,image):
        x_origin = int(self.id_origin[0])
        y_origin = int(self.id_origin[1])
        cv.putText(image, "+X ----> ", (x_origin + 20, y_origin),cv.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2, cv.LINE_AA)

        cv.putText(image, "+Y ", (x_origin - 10, y_origin + 30),cv.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2, cv.LINE_AA)
        cv.putText(image, " | ", (x_origin - 6, y_origin + 60),cv.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2, cv.LINE_AA)
        cv.putText(image, " | ", (x_origin - 6, y_origin + 80),cv.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2, cv.LINE_AA)
        cv.putText(image, " V ", (x_origin -9, y_origin + 100),cv.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2, cv.LINE_AA)


    def draw_tags(self,image,tags,elapsed_time,):

        self.centers = []
        for tag in tags:
            tag_family = tag.tag_family
            tag_id = tag.tag_id
            center = tag.center
            corners = tag.corners

            center = (int(center[0]), int(center[1]))
            corner_01 = (int(corners[0][0]), int(corners[0][1]))
            corner_02 = (int(corners[1][0]), int(corners[1][1]))
            corner_03 = (int(corners[2][0]), int(corners[2][1]))
            corner_04 = (int(corners[3][0]), int(corners[3][1]))


            x_coord,y_coord = self.pixel_to_coords(center[0],center[1])

            self.centers.append("tag_id")
            self.centers.append(tag_id)
            self.centers.append(x_coord)
            self.centers.append(y_coord)

            cv.circle(image, (center[0], center[1]), 5, (0, 0, 255), 2)
            cv.circle(image, (int(corners[1][0]), int(corners[1][1])), 5, (255, 255, 0), 2)
            cv.circle(image, (int(corners[3][0]), int(corners[3][1])), 5, (255, 0, 0), 2)


            cv.line(image, (corner_01[0], corner_01[1]),
                    (corner_02[0], corner_02[1]), (255, 0, 0), 2)
            cv.line(image, (corner_02[0], corner_02[1]),
                    (corner_03[0], corner_03[1]), (255, 0, 0), 2)
            cv.line(image, (corner_03[0], corner_03[1]),
                    (corner_04[0], corner_04[1]), (0, 255, 0), 2)
            cv.line(image, (corner_04[0], corner_04[1]),
                    (corner_01[0], corner_01[1]), (0, 255, 0), 2)


            # cv.putText(image,
            #            str(tag_family) + ':' + str(tag_id),
            #            (corner_01[0], corner_01[1] - 10), cv.FONT_HERSHEY_SIMPLEX,
            #            0.6, (0, 255, 0), 1, cv.LINE_AA)
            cv.putText(image, str(tag_id), (center[0] - 10, center[1] - 10),
                       cv.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2, cv.LINE_AA)

        # cv.putText(image,
        #            "Elapsed Time:" + '{:.1f}'.format(elapsed_time * 1000) + "ms",
        #            (10, 30), cv.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2,
        #            cv.LINE_AA)

        self.draw_axes(image)

        if self.centers != []:
            with open('output_track.csv', 'w', newline='') as csvfile:
                outputWriter = csv.writer(csvfile, delimiter=',')
                outputWriter.writerow(self.centers)
                # print(self.centers)

        return image


if __name__ == '__main__':
    track = tracking()
    track.main()
