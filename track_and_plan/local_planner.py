from track_and_plan_in_pixels import GlobalPlanner
from aruco_tracking import Tracker
from geometry_alexedit import geometry


class LocalPlanner:
    def __init__(self):
        pass
    def get_cmd_vel(self,current_pose,goal_pose):
        pass
    def main(self,tracker,GlobalPlanner):
        paths = GlobalPlanner.all_paths

        all_at_goals = [False,False,False]
        i = 0
        goal_increment = 10
        while not all(all_at_goals):
            for robot in len(tracker.ROBOT_IDS):
                robot_id = tracker.ROBOT_IDS[robot]
                robot_path = paths[robot]
                current_pose = [int(tracker._robots[robot_id][0]),int(tracker._robots[robot_id][1])]
                if len(robot_path) < i+goal_increment:
                    goal_pose = robot_path[i+goal_increment]
                    self.get_cmd_vel(current_pose,goal_pose)
                else:
                    all_at_goals[robot] = True

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
    # Get global path
    GlobalPlanner.main(tracker,goals)
