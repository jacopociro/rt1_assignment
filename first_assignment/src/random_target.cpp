#include "ros/ros.h"
#include "first_assignment/randtarget.h"

double randomnumber(double M, double N)
{

return M + (rand() / (RAND_MAX/(N-M)));
}

bool random (first_assignment::randtarget::Request &req, first_assignment::randtarget::Response &res)
{
    res.x = randomnumber(req.min, req.max);
    res.y = randomnumber(req.min, req.max);
    return true;
}

int main( int argc, char **argv)
{
    ros::init(argc, argv, "random_target");
    ros::NodeHandle n;
    ros::ServiceServer service = n.advertiseService("/random", random);
    
    ros::spin();
    return 0;
}