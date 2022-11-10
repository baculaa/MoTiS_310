#!/usr/bin/env python
#8/2/22

# import pandas as pd
import random
import time
import socket
import sys
import numpy as np

import rospy
import math
import actionlib
import local_plan # imports the Movement class from the movement.py file



# Just here for imports in case the Movement class variables need to see it in this file
from std_msgs.msg import String
from nav_msgs.msg import Odometry
from move_base_msgs.msg import MoveBaseGoal, MoveBaseAction
from actionlib_msgs.msg import GoalStatus
from geometry_msgs.msg import Pose, Point, Quaternion, Twist
from tf.transformations import quaternion_from_euler, euler_from_quaternion

from math import atan2,degrees





#######################################
# CLASS NAME: Initiator

#
#######################################
class Initiator:
    def __init__(self,mover):
        self.mover = mover
        # self.ref_point = (4, 0)
        self.rob_id = 1 # all robots will be 0, 1, 2, 3

    def get_into_formation(self,x_ref,y_ref,direction):
        # Orientation is relative to the reference point so that the
        #### formation is created pointing to the ref point then the robots
        #### all just have to move forward until robot 0 is at the ref point
        orientation = degrees(atan2(y_ref, x_ref))

        if direction == 1:
            # up triangle
            goals = self.away(x_ref,y_ref)
        elif direction == 2:
            # down triangle
            goals = self.towards(x_ref,y_ref)
        else:
            print("Staying Still")


        goal = Point()
        goal.x = goals[0]
        goal.y = goals[1]

        self.mover.move_to_goal_avoidance(goal)



    def reset_to_home(self):
        goal = Point()
        goal.x = 0
        goal.y = 0

        rospy.loginfo("Going home")
        self.mover.return_to_starting_pos(goal)
        self.mover.final_formation_orientation(0)



    def away(self,x_ref, y_ref):
        #        ^
        #        |
        #       +x
        # <- +y
        # ROBOT STARTING POSES
        #        REF
        #
        # 0   1    2   3
        if self.rob_id < 2:
            # move to +y and -x
            goal_x = -x_ref
            goal_y = y_ref
        else:
            #move to -y and -x
            goal_x = -x_ref
            goal_y = y_ref

        awayGoal = [goal_x,goal_y]

        return awayGoal


    def towards(self,x_ref, y_ref):
        #        ^
        #        |
        #       +x
        # <- +y
        # ROBOT STARTING POSES
        #        REF
        #
        # 0   1    2   3
        if self.rob_id < 2:
            # move to -y and +x
            goal_x = x_ref
            goal_y = -y_ref
        else:
            #move to +y and +x
            goal_x = x_ref
            goal_y = y_ref


        towardsGoal = [goal_x,goal_y]

        return towardsGoal




if __name__ == '__main__':
    try:
        rospy.init_node('please_work',anonymous=True)
        mover = local_plan.Movement()

        initiator = Initiator(mover)



        direction = int(input('What direcion would you like? Type Options: 1) away, 2) towards, 3) still: '))

        # THE REFERENCE POINT IS RELATIVE TO ROBOT 0, ROBOT 0 IS CONSIDERED 0,0
        #ref_point_input = input('Where would you like the shape to go? Ex. 3,3: ')
        #ref_point = ref_point_input

        #x_ref = ref_point[0]
        #y_ref = ref_point[1]
        x_ref = 1.25
        y_ref = 0.65
        ready=raw_input('Go? yes/no').lower()

        if ready == 'yes':
            initiator.get_into_formation(x_ref,y_ref,direction)
        else:
            pass



        home = raw_input("return home? yes/no")
        if home == 'yes':
            initiator.reset_to_home()
        else:
            pass


    except rospy.ROSInterruptException:
        rospy.loginfo("Didn't work, so cry")
