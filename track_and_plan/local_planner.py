from track_and_plan_in_pixels import GlobalPlanner
from aruco_tracking import Tracker
from geometry_alexedit import geometry
import numpy as np
import csv
from time import sleep
import socket

class WebSocket:
    def __init__(self):
        pass

    def read_csv(self,filename):
        data_x = " "
        data_y = " "
        ## We start by opening the file
        with open(filename) as file_name:
            ## Then we use the csv.reader() function to allow python to read the data
            file_read = csv.reader(file_name)
            # Next, we go through each row of the data and pull out the x point and the y point
            for row in file_read:
                # We add the x point to a list of the x points
                data_x += str(row[0]) + ","
                # We add the y point to a list of the y points
                data_y += str(row[1]) + ","

        print(data_x)
        goals = data_x + data_y
        print(goals)
        return goals

    def main_send(self,goals):
        interfaces = socket.getaddrinfo(host=socket.gethostname(), port=None, family=socket.AF_INET)
        allips = [ip[-1][0] for ip in interfaces]
        # goals = self.read_csv(filename)
        # msg = b'hello hi world bald'
        i = 0
        while True:
            msg = bytes(goals, 'utf-8-sig')
            for ip in allips:
                print(f'sending on {ip}', flush=True)
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)  # UDP
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
                sock.bind((ip, 0))
                sock.sendto(msg, ("255.255.255.255", 5005))
                sock.close()

            i += 1

            sleep(2)


class LocalPlanner:
    def __init__(self):
        pass
    def get_goal(self,robot_corners,current_pose,current_orientation,goal_pose):
        v1 = [current_pose[0],current_pose[1],robot_corners[0],robot_corners[1]]
        v2 = [goal_pose[0],goal_pose[1]]
        p1 = [v1[0], v1[1]]
        p0 = [v1[2], v1[3]]
        p2 = [v2[0], v2[1]]

        v0 = np.array(p0) - np.array(p1)
        v1 = np.array(p2) - np.array(p1)

        goal_orientation = np.math.atan2(np.linalg.det([v0, v1]), np.dot(v0, v1))

        relative_goal_orientation= goal_orientation - current_orientation
        # print("Current pose: ",current_pose)
        relative_goal_pose = np.linalg.norm(goal_pose-current_pose)
        # print("Goal pose: ",goal_pose)
        return relative_goal_pose,relative_goal_orientation

    def main(self,tracker,GlobalPlanner):
        # Get global paths
        paths = GlobalPlanner.main(tracker, goals)
        # paths = GlobalPlanner.all_paths
        print("Paths: ",paths)

        # Get number of robots
        num_robots = len(tracker.ROBOT_IDS)

        # Set all robots to not be at the local goal
        all_at_goals = []
        for i in range(num_robots):
            all_at_goals.append(False)
        # Get a local
        i = 0
        goal_increment = 50
        while any(all_at_goals) == False:
            to_send = []
            for robot in range(num_robots):
                # print("hi")
                robot_id = tracker.ROBOT_IDS[robot]
                robot_corners = tracker._robot_corners[robot]
                # print("Robot corners: ",robot_corners)
                robot_path = paths[robot]
                # print("Robot path: ",len(robot_path))
                current_pose = [int(tracker._robots[robot_id][0]),int(tracker._robots[robot_id][1])]
                current_orientation = int(tracker._robots[robot_id][2])
                # if len(robot_path) <= (i+goal_increment):
                goal_pose = robot_path[i+goal_increment]
                relative_goal_pose, relative_goal_orientation = self.get_goal(robot_corners,current_pose,current_orientation,goal_pose)
                to_send.append([robot_id,relative_goal_pose,relative_goal_orientation])
                print("To send:",to_send)

                # else:
                #     all_at_goals[robot] = True
            print(to_send)
            # with open('testgoals.csv', 'w', newline='') as csvfile:
            #     outputWriter = csv.writer(csvfile, delimiter=',')
            #     outputWriter.writerow(to_send)
            websocket = WebSocket()
            websocket.main_send(to_send)

if __name__ == '__main__':
    # Init global planner
    GlobalPlanner = GlobalPlanner()
    LocalPlanner = LocalPlanner()
    # Init tracking markers
    tracker = Tracker()
    print("Number of robot markers: ",tracker.NUM_ROBOTS)
    # Init geometry
    geom = geometry()
    # Get robot goals
    goals = geom.main()

    LocalPlanner.main(tracker,GlobalPlanner)

