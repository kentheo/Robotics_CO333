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

size_step = 10
turn_side = 'L'

PF = ParticleFilter(100)

#Conversion from cm to pixels
def conversion(x):
    u = 60 + 16*x
    return u

def draw_square(distance, left_or_right):
    line1 = (conversion(0),conversion(0), conversion(0), conversion(distance*4))
    line2 = (conversion(0),conversion(distance*4), conversion(distance*4), conversion(distance*4))
    line3 = (conversion(distance*4), conversion(distance*4), conversion(distance*4), conversion(0))
    line4 = (conversion(distance*4),conversion(0), conversion(0), conversion(0))
    print "drawLine:" + str(line1)
    print "drawLine:" + str(line2)
    print "drawLine:" + str(line3)
    print "drawLine:" + str(line4)
    for i in range(4):
        for j in range(4):
            Simple_robot.linear_move(distance)
            print("Robot moving forward")
            # Temporary Time sleep: we have to determined if method increase_angle is blocking or not. I set this value so
            # that if increase angle is not blocking, we at least wait 0.5 seconds between each moving command.
            time.sleep(0.5)
            PF.update_after_straight_line_full(distance, 0, 0.02 / 100)
            particles = [(conversion(PF.particles[i][0]), conversion(PF.particles[i][1]), PF.particles[i][2]) for i in range(PF.num_particles)]
            print "drawParticles:" + str(particles)
        #print(particles)
        if left_or_right == "L":
            Simple_robot.left_90_deg()
            time.sleep(0.5)
            PF.update_after_rotation_full(90*(np.pi/180), 0, 0.01 )
        elif left_or_right == "R":
            Simple_robot.right_90_deg()
            time.sleep(0.5)
        else:
            print("Issues with specified side turn, can't turn left or right. Check if you entered 'L' or 'R' correctly")
    return PF.particles

particles = draw_square(size_step, turn_side)
x_mean = PF.estimate_position(particles)
print(x_mean)

#newParticles_WP = ParticleFilter(100)

'''
def navigateToWaypoint(X, Y):
    location_new = np.array([X,Y])
    x_mean = newParticles_WP.estimate_position(newParticles_WP.particles)
    vector = [location_new[0] - x_mean[0], location_new[1] - x_mean[1]]
    orientation_new = math.atan2(vector[1], vector[0]) # Gives the correct result
    print("New orientation angle:", orientation_new)
    alpha = orientation_new - x_mean[2]
    Simple_robot.rotation_move(alpha * 180 / (np.pi))
    time.sleep(0.5)
    newParticles_WP.update_after_rotation_full(alpha, 0, 0.01)
    distance_to_move = np.sqrt(vector[0]**2 + vector[1]**2)
    print("Distance:", distance_to_move)
    Simple_robot.linear_move(distance_to_move)
    time.sleep(0.5)
    newParticles_WP.update_after_straight_line_full(distance_to_move, 0, 0.02)
    print("Position", np.mean(newParticles_WP.particles, axis = 0))

#navigateToWaypoint(- 10, 10)

def interactive_navigation() :
    newParticles_WP = ParticleFilter(100)
    destination = (input("Enter (Wx, Wy) coordinates (in metres): "))
    print(destination)
    while destination != "stop" :
        #destination = [float(n) for n in destination.split(',')]
        print("destination", destination)
        navigateToWaypoint(destination[0], destination[1])
        destination_raw = (input("Enter (Wx, Wy) coordinates (in metres): "))

interactive_navigation()
'''

Simple_robot.terminate_interface()
