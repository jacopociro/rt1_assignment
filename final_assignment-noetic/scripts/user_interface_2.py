#!/usr/bin/env 

import rospy
import time

from geometry_msgs.msg import Point
from sensor_msgs.msg import LaserScan
from nav_msgs.msg import Odometry
from tf import transformations

from std_srvs.srv import *
from geometry_msgs.msg import Twist

import math

import actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from actionlib_msgs.msg import GoalStatus, GoalStatusArray, GoalID
import random
from final_assignment.srv import randomnumber, randomnumberRequest
from numpy import *

pub = None
my_data = None
state_desc_ = ['choose point', 'go to random point', 'stop', 'interfaccia']
state_ = 0
a = array([[-4,-3],[-4,-2],[-4,7],[5,-7],[5,-3],[5,1]])
    
def movebase_client():
    client = actionlib.SimpleActionClient('move_base', MoveBaseAction)
    client.wait_for_server()
    print("choose a room between 0 and 5\n")
    num = input()
    x = a[int(num)][0]
    y = a[int(num)][1]
    goal = MoveBaseGoal()
    goal.target_pose.header.frame_id = "map"
    goal.target_pose.pose.position.x = x
    goal.target_pose.pose.position.y = y
    goal.target_pose.pose.orientation.w = 1
    print("reaching point [%d %d]"%(x, y))
    client.send_goal(goal)
    

def random_number_client():
    rospy.wait_for_service('random_number')
    srv = rospy.ServiceProxy('random_number', randomnumber)
    response = srv()
    return response.resp

def movebaserandom_client():
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
    
def cancel_goal():
    cancel_pub = rospy.Publisher("/move_base/cancel", GoalID, queue_size=1)
    cancel_msg = GoalID()
    cancel_pub.publish(cancel_msg)

def change_state(state):
    global state_, state_desc_
    state_ = state
    log = "state changed: %s" %state_desc_[state]
    rospy.loginfo(log)
    if state_ == 0:
        movebase_client()
    if state_ == 1:
        movebaserandom_client()
    if state_ == 2:
        cancel_goal()
    #if state_ == 3:
   

def callback(data):
    
    return data.status_list[0].status
    

def main():
    time.sleep(2)
    global pub, my_data
    rospy.init_node('assignment')
    my_data = rospy.Subscriber("/move_base/status", GoalStatusArray, callback)
    pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
    change_state(3)
    
    
    rate = rospy.Rate(20)
    while not rospy.is_shutdown():
        

        if state_ == 0:
            
            if my_data == 3:
                change_state(3)
        elif state_ == 1:
            
            if my_data== 3:
                change_state(3)
        elif state_ == 2:
            print('shutting down')
            rospy.signal_shutdown("user chose to shutdown")
        elif state_ == 3:
            print("choose another function")
            x = input()
            change_state(int(x))
   
        #rate.sleep()
   

if __name__ == '__main__':
    main()