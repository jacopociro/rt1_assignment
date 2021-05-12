#include "ros/ros.h"
#include "geometry_msgs/Twist.h"
#include "nav_msgs/Odometry.h"
#include "first_assignment/randtarget.h"
#include <sstream>
#include <iostream>


ros::Publisher pub;
ros::ServiceClient client1;
int count = 10;
float x,y;
float distx = 0.0;
float disty = 0.0;
void positionCallback (const nav_msgs::Odometry::ConstPtr &odom)
{
    
    first_assignment::randtarget target;
    geometry_msgs::Twist msg_sent;
    
    int targetmetx = (distx < 0.1 && distx > -0.1);
    int targetmety = (disty < 0.1 && disty > -0.1);
    if (targetmetx & targetmety)
    {
        target.request.min=-6.0;
        target.request.max=6.0;
        client1.call(target);
        x = target.response.x;
        y = target.response.y;
        printf("getting a new target!\n");
        distx = x - odom->pose.pose.position.x;
        disty = y - odom->pose.pose.position.y;
    } 
    
    else if ((distx >= 0.1)||(distx <= -0.1))
    {
        msg_sent.linear.x = distx/*k->(xt-x)*/;
        distx = x - odom->pose.pose.position.x;
        printf("moving!\n");
    }
    
    else if ((disty >= 0.1)||(disty <= -0.1))   
    {
        msg_sent.linear.y = disty/* k*(yt-y)*/;
        disty = y - odom->pose.pose.position.y;
        printf("moving!\n");
    }

   
    ROS_INFO("Robot position [%f, %f]", odom->pose.pose.position.x, odom->pose.pose.position.y);
    ROS_INFO("Target position [%f, %f]", x, y);
    ROS_INFO("Robot speed [%f, %f]", distx, disty);
    pub.publish(msg_sent);
}

int main(int argc, char **argv)
{
    ros::init(argc, argv, "reach_target");
    ros::NodeHandle n;
    client1 = n.serviceClient<first_assignment::randtarget>("/random");
    pub = n.advertise<geometry_msgs::Twist>("/cmd_vel",1000);
    ros::Subscriber sub = n.subscribe("/odom", 1000, positionCallback);
    
    ros::spin();
    return 0;
}