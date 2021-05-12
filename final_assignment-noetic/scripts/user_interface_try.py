#! /usr/bin/env 

import rospy
import time

from geometry_msgs.msg import Point
from sensor_msgs.msg import LaserScan
from nav_msgs.msg import Odometry
from tf import transformations

from std_srvs.srv import *
from geometry_msgs.msg import Twist

import math


srv_client_wall_follower_ = None
srv_client_bug0_ = None




regions_ = None
state_desc_ = ['wall follow', 'bug0']
state_ = 0


def clbk_laser(msg):
    global regions_
    regions_ = {
        'right':  min(min(msg.ranges[0:143]), 10),
        'fright': min(min(msg.ranges[144:287]), 10),
        'front':  min(min(msg.ranges[288:431]), 10),
        'fleft':  min(min(msg.ranges[432:575]), 10),
        'left':   min(min(msg.ranges[576:719]), 10),
    }

def change_state(state):
    global state_, state_desc_
    global srv_client_bug0_, srv_client_wall_follower_
    state_ = state
    log = "state changed: %s" %state_desc_[state]
    rospy.loginfo(log)
    if state_ == 0: 
        resp = srv_client_wall_follower_(True)
        resp = srv_client_bug0_(False)
    if state_ == 1:
        resp = srv_client_bug0_(True)
        resp = srv_client_wall_follower_(False)

def main():
    time.sleep(2)
    global regions_, state_
    global srv_client_wall_follower_, srv_client_bug0_

    rospy.init_node('try')

    sub_laser = rospy.Subscriber('/scan', LaserScan, clbk_laser)

    srv_client_bug0_ = rospy.ServiceProxy('/bug0_switch', SetBool)
    srv_client_wall_follower_ = rospy.Subscriber('/wall_follower_switch', SetBool)

    while not rospy.is_shutdown():
        print('choose cacca pupu')
        x = input()
        change_state(int(x))
        if regions_ == None:
            continue 
        
        if state_ == 0: 
            print('wall following')
        elif state_ == 1: 
            print('algorithm changed')
        
if __name__ == "__main__":
    main()
