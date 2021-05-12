#!/usr/bin/env python

import rospy
import actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal

def movebase_client():
    client = actionlib.SimpleActionClient('move_base', MoveBaseAction)
    client.wait_for_server()

    goal = MoveBaseGoal()
    goal.target_pose.header.frame_id = "map"
    goal.target_pose.pose.position.x = 5
    goal.target_pose.pose.position.y = 1
    goal.target_pose.pose.orientation.w = 1

    client.send_goal(goal)
    wait = client.wait_for_result()

    if not wait:
        rospy.logerr("action server not available")
        rospy.signal_shutdown("action server not available")
    else:
        return client.get_result()
    
if __name__ == '__main__':
    try:
        rospy.init_node('move_client_py')
        result = movebase_client()
        if result:
            rospy.loginfo("goal execution done!")
    except rospy.ROSInterruptException:
            rospy.loginfo("navigation test finished")
