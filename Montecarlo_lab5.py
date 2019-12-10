import math
import numpy as np
from Robot import *
from ParticleFilter import *
from map import *
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

# Create a ParticleFilter
PF = ParticleFilter(100)

# Start point coordinates in the arena, which are passed to the robot, and to the particle filters
start_point = [84., 30.]

Simple_robot.set_x(start_point[0])
Simple_robot.set_y(start_point[1])

PF.particles = np.array([[start_point[0], start_point[1], 0]] * PF.num_particles)

# Lab spec states it should be 20 cm
step_size = 20

# Create a Map
mymap = Map();

# Create a ParticleFilter
destinations = [[84., 30.], [180., 30.], [180., 54.], [138., 54.], [138., 168.], [114., 168.], [114., 84.], [84., 84.], [84., 30.]]

def conversion(x):
    u = 60 + 3*x
    return u

def conversiony(x):
    u = 700 - 3*x
    return u

line1 = (conversion(0), conversiony(0), conversion(0), conversiony(168))
line2 = (conversion(0), conversiony(168), conversion(84), conversiony(168))
line3 = (conversion(84), conversiony(126), conversion(84), conversiony(210))
line4 = (conversion(84), conversiony(210), conversion(168), conversiony(210))
line5 = (conversion(168), conversiony(210), conversion(168), conversiony(84))
line6 = (conversion(168), conversiony(84), conversion(210), conversiony(84))
line7 = (conversion(210), conversiony(84), conversion(210), conversiony(0))
line8 = (conversion(210), conversiony(0), conversion(0), conversiony(0))
print "drawLine:" + str(line1)
print "drawLine:" + str(line2)
print "drawLine:" + str(line3)
print "drawLine:" + str(line4)
print "drawLine:" + str(line5)
print "drawLine:" + str(line6)
print "drawLine:" + str(line7)
print "drawLine:" + str(line8)

def compute_sub_points(start, end):
    vector = [end[0] - start[0], end[1] - start[1]]
    angle = math.atan2(vector[1], vector[0])
    full_length = np.sqrt(vector[1] ** 2 + vector[0] ** 2)
    if full_length <= step_size:
        return end
    else:
        number_of_step = int(full_length // step_size)
        sub_dest = [start]
        for step in range(1, number_of_step + 1):
            sub_point = [sub_dest[-1][0] + step_size * np.cos(angle), sub_dest[-1][1] + step_size * np.sin(angle)]
            sub_dest += [sub_point]
        sub_dest += [end]
        return sub_dest[1:]    # we don't return de start point


def split_journey(points):
    result = [points[0]]
    for i in range(len(points) - 1):
        sub_part = compute_sub_points(points[i], points[i+1])
        result += sub_part
    return result


# We compute all the sub destinations for the path so that we don't move more than 20cm (step_size) each time
destinations_steps = split_journey(destinations)[1:]
print(destinations_steps)

for point in destinations_steps:
    particles = [(conversion(PF.particles[i][0]), conversiony(PF.particles[i][1]), PF.particles[i][2]) for i in
                 range(PF.num_particles)]
    print "drawParticles:" + str(particles)
    print("---------------------------")
    print("-> Current location before next move is: ", Simple_robot.x, Simple_robot.y)
    print("---------------------------")
    print("Particles status before the next move is: ",PF.particles)
    print("---------------------------")
    print("-> Heading towards: ", point)
    move = Simple_robot.navigateToWaypoint(point[0], point[1])
    print("---------------------------")
    print("Distance for this move is in centimeters: ",move[0])
    print("Angle to rotate for this move is in radians: ",move[1])
    PF.update_after_rotation_full(move[1], 0, 0.01)
    print("After update rotation full, the angle of one particle is: ",PF.particles[0][2])
    PF.update_after_straight_line_full(move[0], 0, 0.01, 0.01)      # Two possible sigma values for particle spreading
    # Get sonar value
    z = Simple_robot.instantiated_sensors[0].get_value()[0]
    likelihood = PF.calculate_likelihood_full(mymap, z)
    PF.update_weights(np.array(likelihood))
    # PF.resampling()
    new_estimated_coordinates = PF.estimate_position_from_particles()
    # new_estimated_coordinates = PF.particles[0]
    print("---------------------------")
    print("Particles mean estimation is:", new_estimated_coordinates)
    print("---------------------------")
    Simple_robot.set_x(new_estimated_coordinates[0])
    Simple_robot.set_y(new_estimated_coordinates[1])
    Simple_robot.set_theta(new_estimated_coordinates[2])
    particles = [(conversion(PF.particles[i][0]), conversiony(PF.particles[i][1]), PF.particles[i][2]) for i in
                 range(PF.num_particles)]
    print "drawParticles:" + str(particles)
