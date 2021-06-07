
# rt1_assignement
both the first and second assignment for research track 1 course.

for the first assignment, inside the folder first_assignment:
  -to run the code:

    catkin_make in root folder

    rosrun stage_ros stageros $(rospack find assignment1)/world/exercise.world 

    rosrun first_assignment random_target

    rosrun first_assignment reach_target

  in the package i'm using the following nodes:
  random_target- this is the node i created to handle the service

  reach_target- this is the node i created to handle the subscriber, the publisher and the client 
  for the service

  stageros- this node is used by the simulation

  rosout- this node is used for the output to screen

  computational graph of the system: 
  we can see that the node reach_target has both a subscriber and a publisher in the node stageros. 
  The random_target server is broadcasting a message and the reach_target can read it with is client.
  
for the final assignment, inside the folder final_assignment:
  the final assignment has many scripts, most of them are outdated. In the scripts folder the ones i use are:
    
    wall_follow_service_m.py: this is a service we use to make the robot follow the walls
    
    go_to_point_service_m.py: this is a service used by the robot to reach a point using the bug0 algorithm
    
    randomnumberserver.py: this node generates a random number
    
    user_interface.py which is in a folder called robot_description
    
    user_interface_4.py: this is the node that is used to reach points using the move_base algorithm and to change the states of the robot.
   in the launch folder we will use the launch files called:
    
    move_base.launch: launch the move_base algorithm
    
    simulation_gmapping.launch: launches the simulation
    
    user2.launch: launches the program to run the robot.
   -to run the code:

    catkin_make in root folder
    
    in a terminal write: roslaunch final_assignment simulation_gmapping.launch
    
    in another terminal write: roslaunch final_assignment move_base.launch
    
    lastly in a third terminal write: roslaunch final_assignment user2.launch
   this should start the robot, and the robot should move to a set position (-3, -3). Once this is done it should ask for further instructions in the terminal. 
   When using the move_base algorithm it displays an error message but this does not stop the program and the callback helps with making the robot work continuosly.
