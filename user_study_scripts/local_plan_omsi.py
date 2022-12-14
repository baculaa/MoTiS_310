#!/usr/bin/env python

import rospy
import math
import actionlib
import socket


from std_msgs.msg import String
from nav_msgs.msg import Odometry
from move_base_msgs.msg import MoveBaseGoal, MoveBaseAction
from actionlib_msgs.msg import GoalStatus
from geometry_msgs.msg import Pose, Point, Quaternion, Twist
from tf.transformations import quaternion_from_euler, euler_from_quaternion
from sensor_msgs.msg import LaserScan

from math import atan2



#msg_pub = rospy.Publisher('msgTest', String, queue_size=10)
#move_pub = rospy.Publisher('moveTest', MoveBaseGoal, queue_size=10)

# rospy.init_node('move_bot', anonymous=True)
# vel_pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
# rate = rospy.Rate(10)
# move = Twist()


class Movement:
    def __init__(self):
        # self.goal = Point()
        # self.goal.x = 0
        # self.goal_y = 0

        self.cur_x = 0.0
        self.cur_y = 0.0
        self.theta = 0.0

        self.obs_tol = 0.7

        self.delta = 0.2

        self.rot_speed = 0.25
        self.forward_speed = 0.6
        # rospy.init_node("speed_controller")

        # create publisher and subscriber
        self.sub = rospy.Subscriber("/odom", Odometry,
                                    self.newOdom)  # our odometry node is called /odom and not /odometry/filtered
        self.pub = rospy.Publisher("/cmd_vel", Twist, queue_size=1)
        self.sub_laser = rospy.Subscriber("/base_scan", LaserScan, self.newLaserScan)

        # create a move variable
        self.move = Twist()

        # set the rate
        self.r = rospy.Rate(4)

        self.moveScan = {}

        # def set_goal_point(self, goal_x, goal_y):
        #     self.goal.x = goal_x
        #     self.goal.y = goal_y

    def newOdom(self, msg):
        # get the current x and y position values for the robot
        self.cur_x = msg.pose.pose.position.x
        self.cur_y = msg.pose.pose.position.y

        rot_q = msg.pose.pose.orientation
        (roll, pitch, self.theta) = euler_from_quaternion([rot_q.x, rot_q.y, rot_q.z, rot_q.w])
        # rospy.loginfo("Current x-coordinate: " + str(self.cur_x))
        # rospy.loginfo("Current y-coordinate: " + str(self.cur_y))
        # rospy.loginfo("Current theta value: " + str(self.theta))

    def newLaserScan(self, msg):
        self.moveScan = {
            'fleft': min(min(msg.ranges[300:]), self.obs_tol),
            'fright': min(min(msg.ranges[:45]), self.obs_tol)
        }

        # curGoal is of type Point()



    def move_to_goal_avoidance(self, curGoal,l_speed,r_speed):
        reached = False
        x = curGoal.x
        y = curGoal.y
        rospy.loginfo("Inside move_to_goal_point()")
        while not rospy.is_shutdown() and not reached:
            inc_x = x - self.cur_x
            inc_y = y - self.cur_y

            rospy.loginfo("Incrementation of x: " + str(inc_x))
            rospy.loginfo("Incrementation of y: " + str(inc_y))
            rospy.loginfo("Current goal: " + str(curGoal))

            angle_to_goal = atan2(inc_y, inc_x)
            dist = math.sqrt(((x - self.cur_x) ** 2) + ((y - self.cur_y) ** 2))
            # rospy.loginfo("Current distance to goal: " + str(dist))

            # IS NOT UPDATING TO THE NEW ANGLE SEEN, SO IT IS STUCK AT 0.78
            if dist <= self.delta:  # and abs(self.theta) <= self.delta * 0.5:
                rospy.loginfo("Theta: " + str(self.theta))
                rospy.loginfo("Robot is close enough to the participants. Stopping now!")
                self.move.linear.x = 0.0
                self.move.angular.z = 0.0
                reached = True


            elif abs(angle_to_goal - self.theta) > 0.1:  # self.delta:
                if self.cur_y < y:
                    self.move.linear.x=0.0
                    self.move.angular.z = r_speed
                else:
                    self.move.linear.x = 0.0
                    self.move.angular.z = -r_speed


            else:
                if self.moveScan['fleft'] < self.obs_tol or self.moveScan['fright'] < self.obs_tol:
                    rospy.loginfo("Fleft range is: " + str(self.moveScan['fleft']))
                    rospy.loginfo("Fright range is: " + str(self.moveScan['fleft']))
                    self.move.linear.x = 0.0
                    self.move.angular.z = 0.0
                else:
                    self.move.linear.x = l_speed  # 0.5
                    self.move.angular.z = 0.0

            self.pub.publish(self.move)
            self.r.sleep()

    def return_to_starting_pos(self,curGoal):
        reached = False
        x = curGoal.x
        y = curGoal.y
        rospy.loginfo("Inside move_to_goal_point()")
        while not rospy.is_shutdown() and not reached:
            inc_x = x - self.cur_x
            inc_y = y - self.cur_y

            rospy.loginfo("Incrementation of x: " + str(inc_x))
            rospy.loginfo("Incrementation of y: " + str(inc_y))
            rospy.loginfo("Current goal: " + str(curGoal))

            angle_to_goal = atan2(inc_y, inc_x)
            dist = math.sqrt(((x - self.cur_x) ** 2) + ((y - self.cur_y) ** 2))
            # rospy.loginfo("Current distance to goal: " + str(dist))

            # IS NOT UPDATING TO THE NEW ANGLE SEEN, SO IT IS STUCK AT 0.78
            if dist <= self.delta*0.5:  # and abs(self.theta) <= self.delta * 0.5:
                rospy.loginfo("Theta: " + str(self.theta))
                rospy.loginfo("Robot is close enough to the participants. Stopping now!")
                self.move.linear.x = 0.0
                self.move.angular.z = 0.0
                reached = True


            elif abs(angle_to_goal - self.theta) > self.delta:
                if self.cur_y < y:
                    self.move.linear.x = 0.0
                    self.move.angular.z = self.rot_speed*0.9  # 0.25
                    # do something
                else:

                    self.move.linear.x = 0.0
                    self.move.angular.z = -1 * self.rot_speed*0.9  # -0.25

            else:
                if self.moveScan['fleft'] < self.obs_tol or self.moveScan['fright'] < self.obs_tol:
                    rospy.loginfo("Fleft range is: " + str(self.moveScan['fleft']))
                    rospy.loginfo("Fright range is: " + str(self.moveScan['fleft']))
                    self.move.linear.x = 0.0
                    self.move.angular.z = 0.0
                else:
                    self.move.linear.x = self.forward_speed  # 0.5
                    self.move.angular.z = 0.0

            self.pub.publish(self.move)
            self.r.sleep()


    # PASS GOAL POINT TO MOVEMENT FUNCTION
    def stop(self):
        self.move.linear.x = 0.0
        self.move.angular.z = 0.0
        self.pub.publish(self.move)

    def dance(self,num_wiggle):
        self.move.linear.x = 0.0
        self.move.angular.z = 0.35
        self.pub.publish(self.move)
        rospy.sleep(0.5)
        for _ in range(num_wiggle):
            self.move.angular.z = -0.35
            self.pub.publish(self.move)
            rospy.sleep(1.0)
            self.move.angular.z = 0.35
            self.pub.publish(self.move)
            rospy.sleep(1.0)

    def dance_villain(self,num_wiggle):
        self.move.linear.x = 0.5
        self.move.angular.z = 0.0
        self.pub.publish(self.move)
        rospy.sleep(0.5)
        for _ in range(num_wiggle):
            self.move.linear.x = -0.65
            self.pub.publish(self.move)
            rospy.sleep(1.5)
            self.move.linear.x = 0.5
            self.pub.publish(self.move)
            rospy.sleep(1.0)


    def final_formation_orientation(self,orientation):
        #rospy.loginfo("Rotating to: "+str(orientation))
        while abs(self.theta - orientation) > self.delta*0.5:
            #rospy.loginfo("Need to rotate: "+str(abs(self.theta - orientation)))
            if self.theta < orientation:
                self.move.linear.x = 0.0
                self.move.angular.z = self.rot_speed  # 0.25
            else:
                self.move.linear.x = 0.0
                self.move.angular.z = -self.rot_speed
            self.pub.publish(self.move)
