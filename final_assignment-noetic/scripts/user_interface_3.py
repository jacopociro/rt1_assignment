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
srv_client_wall_follower_ = None
srv_client_bug0_ = None
desired_position_ = Point()
#desired_position_.x = rospy.get_param('des_pos_x')
#desired_position_.y = rospy.get_param('des_pos_y')
desired_position_.z = 0

position_ = Point()
yaw_ = 0
yaw_error_allowed_ = 5 * (math.pi / 180 )


state_desc_ = ['choose point', 'go to random point', 'stop', 'interfaccia', 'wall following', 'bug0']
state_ = 0
regions_ = None
a = array([[-4,-3],[-4,-2],[-4,7],[5,-7],[5,-3],[5,1]])

def clbk_odom(msg): 
    global position_, yaw_
    position_ = msg.pose.pose.position

    quaternion = (
        msg.pose.pose.orientation.x,
        msg.pose.pose.orientation.y,
        msg.pose.pose.orientation.z,
        msg.pose.pose.orientation.w)
    euler = transformations.euler_from_quaternion(quaternion)
    yaw_ = euler[2]


def clbk_laser(msg):
    global regions_
    regions_ = {
        'right':  min(min(msg.ranges[0:143]), 10),
        'fright': min(min(msg.ranges[144:287]), 10),
        'front':  min(min(msg.ranges[288:431]), 10),
        'fleft':  min(min(msg.ranges[432:575]), 10),
        'left':   min(min(msg.ranges[576:719]), 10),
    }

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
    global srv_client_bug0_, srv_client_wall_follower_
    state_ = state
    log = "state changed: %s" %state_desc_[state]
    rospy.loginfo(log)
    if state_ == 0:
        resp = srv_client_bug0_(False)
        resp = srv_client_wall_follower_(False)
        
        twist_msg = Twist()
        twist_msg.linear.x = 0
        twist_msg.angular.z = 0
        pub.publish(twist_msg)

        movebase_client()
    if state_ == 1:
        resp = srv_client_bug0_(False)
        resp = srv_client_wall_follower_(False)
        
        twist_msg = Twist()
        twist_msg.linear.x = 0
        twist_msg.angular.z = 0
        pub.publish(twist_msg)

        movebaserandom_client()
    if state_ == 2:
        resp = srv_client_bug0_(False)
        resp = srv_client_wall_follower_(False)
        
        twist_msg = Twist()
        twist_msg.linear.x = 0
        twist_msg.angular.z = 0
        pub.publish(twist_msg)

        cancel_goal()

    if state_ == 3:
        resp = srv_client_bug0_(False)
        resp = srv_client_wall_follower_(False)
        twist_msg = Twist()
        twist_msg.linear.x = 0
        twist_msg.angular.z = 0
        pub.publish(twist_msg)
        cancel_goal()

    if state_ == 4: 
        resp = srv_client_wall_follower_(True)
        resp = srv_client_bug0_(False)
        
    if state_ == 5:
        resp = srv_client_bug0_(True)
        resp = srv_client_wall_follower_(False)
        
#da sistemare list is out of index
def callback(data):
    
    return data.status_list[0].status
    


def main():
    time.sleep(2)
    global pub, my_data, desired_position_, position_, yaw_, yaw_error_allowed_
    global srv_client_bug0_, srv_client_wall_follower_
    rospy.init_node('assignment')
    my_data = rospy.Subscriber("/move_base/status", GoalStatusArray, callback)
    rospy.Subscriber('/scan', LaserScan, clbk_laser)

    srv_client_bug0_ = rospy.ServiceProxy('/bug0_switch', SetBool)
    srv_client_wall_follower_ = rospy.ServiceProxy('/wall_follower_switch', SetBool)
    
    pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
    
    change_state(3)
    
    rate = rospy.Rate(20)
    while not rospy.is_shutdown():
        
        if regions_ == None:
            continue 


        if state_ == 0:
            
            if my_data == 3:
                change_state(3)
        elif state_ == 1:
            
            if my_data == 3:
                change_state(3)
        elif state_ == 2:
            print('shutting down')
            rospy.signal_shutdown("user chose to shutdown")
        elif state_ == 3:
            print("choose another function")
            x = input()
            change_state(int(x))
        elif state_ == 4: 
            print('wall following')
            change_state(3)
        
        elif state_ == 5: 
            print("please insert position")
            x = int(input('x :'))
            y = int(input('y :'))
            rospy.set_param("des_pos_x", x)
            rospy.set_param("des_pos_y", y)
            desired_position_.x = rospy.get_param('des_pos_x')
            desired_position_.y = rospy.get_param('des_pos_y')
            print("thanks! reaching position")
            err_pos = math.sqrt(pow(desired_position_.y - position_.y,
                                    2) + pow(desired_position_.x - position_.x, 2))
            if(err_pos < 0.3):
                change_state(3)
   
        rate.sleep()
   

if __name__ == '__main__':
    main()