#!/usr/bin/env python

from __future__ import print_function

import rospy
import actionlib
import random
from final_assignment.srv import randomnumber, randomnumberRequest
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from numpy import *

a = array([[-4,-3],[-4,-2],[-4,7],[5,-7],[5,-3],[5,1]])

def random_number_client():
    rospy.wait_for_service('random_number')
    srv = rospy.ServiceProxy('random_number', randomnumber)
    #request = randomnumberRequest()
    response = srv()
    return response.resp

def movebase_client():
    num = random_number_client()
    x = a[num][0]
    y = a[num][1]
    client = actionlib.SimpleActionClient('move_base', MoveBaseAction)
    client.wait_for_server()

    goal = MoveBaseGoal()
    goal.target_pose.header.frame_id = "map"
    goal.target_pose.pose.position.x = x
    goal.target_pose.pose.position.y = y
    goal.target_pose.pose.orientation.w = 1
    print("reaching point [%d %d]"%(x, y))
    client.send_goal(goal)
    wait = client.wait_for_result()
    rospy.spin()

    if not wait:
        rospy.logerr("action server not available")
        rospy.signal_shutdown("action server not available")
    else:
        return client.get_result()

if __name__ == "__main__":
    try:
        rospy.init_node('move_client_py')
        result = movebase_client()
        if result:
            rospy.loginfo("goal execution done!")
    except rospy.ROSInterruptException:
        rospy.loginfo("navigation test finished")