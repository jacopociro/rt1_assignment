#!/usr/bin/env python

from __future__ import print_function

import rospy
from final_assignment.srv import *

def random_number_client():
    rospy.init_node('client')
    rospy.wait_for_service('random_number')
    srv = rospy.ServiceProxy('random_number', randomnumber)
    request = randomnumberRequest()
    response = randomnumberResponse
    return int(response.resp)
    
    rospy.spin()

if __name__ == "__main__":
  random_number_client()
  print ("%d"%(random_number_client()))
