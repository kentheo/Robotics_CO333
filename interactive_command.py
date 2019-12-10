import math
import numpy as np
from Robot import *
from ParticleFilter import *
List_plugged_motors = [[0, "Right"], [3, "Left"]]

# Information displayed, to be sure software motor configuration matches reality
print("The configuration states that plugged motors are :\n")
for i in List_plugged_motors:
    print("Port ", i[0], " for ", i[1], " side motor\n")

# Necessary for the instantiation of the Robot, empty for the moment
List_plugged_sensors = [[2, "SENSOR_ULTRASONIC", 2]]

# Create the instance of the robot, initialize the interface
Simple_robot = Robot(List_plugged_motors, List_plugged_sensors)
# Enable its motors and sensors
Simple_robot.motor_init()
Simple_robot.sensor_init()

PF = ParticleFilter(100)

while True:
    destination = (input("Enter (Wx, Wy) coordinates (in meters): "))
    move = Simple_robot.navigateToWaypoint(destination[0], destination[1])
    print("alpha angle value is :", move[1])
    PF.update_after_rotation_full(move[1], 0, 0.01)
    PF.update_after_straight_line_full(move[0], 0, 0.01)
    new_estimated_coordinates = PF.estimate_position_from_particles()
    print("Particles angle estimation is :", new_estimated_coordinates[2])
    Simple_robot.set_x(new_estimated_coordinates[0][0])
    Simple_robot.set_y(new_estimated_coordinates[1][0])
    Simple_robot.set_theta(new_estimated_coordinates[2][0])



