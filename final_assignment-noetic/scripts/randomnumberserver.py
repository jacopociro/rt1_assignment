#! /usr/bin/env

from __future__ import print_function

from final_assignment.srv import randomnumber,randomnumberResponse
import random
import rospy

def random_number(request): 
    return randomnumberResponse(random.randint(0,5))


def random_number_server():
    rospy.init_node('random_number_server')
    srv = rospy.Service('random_number', randomnumber, random_number)
    print("ready to generate random numbers")
    rospy.spin()


if __name__ == "__main__":
    random_number_server()
