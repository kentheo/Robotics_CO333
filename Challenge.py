from Robot import *
from recognize_location import *
from ParticleFilter import *
from map import *
import time

List_plugged_motors = [[0, "Right"], [3, "Left"]]

# Information displayed, to be sure software motor configuration matches reality
print("The configuration states that plugged motors are :\n")
for i in List_plugged_motors:
    print("Port ", i[0], " for ", i[1], " side motor\n")

# Necessary for the instantiation of the Robot, empty for the moment
List_plugged_sensors = [[2, "SENSOR_ULTRASONIC", 2]]

# Create the instance of the robot, initialize the interface
Robot = Robot(List_plugged_motors, List_plugged_sensors)
# Enable its motors and sensors
Robot.motor_init()
Robot.sensor_init()

# Coordinates possibilities
waypoints = [(84., 30.), (180., 30.), (180., 54.), (138., 54.), (138., 168.), (138., 54.)]

# Create a ParticleFilter
PF = ParticleFilter(100)

# Create a Map
mymap = Map()

'''
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
'''
def MonteCarlo(robot, particles, distance, angle):
    particles.update_after_rotation_full(angle, 0, 0.03)
    particles.update_after_straight_line_full(distance, 0, 0.03, 0.01)
    z = robot.instantiated_sensors[0].get_value()[0]
    likelihood = particles.calculate_likelihood_full(mymap, z)
    particles.update_weights(np.array(likelihood))
    particles.resampling()
    new_estimated_coordinates = particles.estimate_position_from_particles()
    robot.set_x(new_estimated_coordinates[0])
    robot.set_y(new_estimated_coordinates[1])
    robot.set_theta(new_estimated_coordinates[2])

# Stuck the program here before going further
user_start = raw_input("Are you ready to start?! ")
# Start the time
start_time = time.time()
# ---------- Comment while tuning MC parameters ---------
# Run the recognize location script to get the starting coordinates
initial_parameters = recognize_location_model(Robot)
print("The initial parameters are: ", initial_parameters)

# Check if the angle is good:

def check_angle():
    Robot.instantiated_sensors_motors[0].increase_angle(-np.pi)
    check_parameters = recognize_location_model(Robot)
    if (check_parameters[0] != initial_parameters[0]) or ( -0.09 > check_parameters[1]) or (check_parameters[1] > 0.09):
        return check_angle()
    else:
        return check_parameters

check_parameters = check_angle()
# get back the coordinates from the initial parameters and waypoints coordinates
starting_point = waypoints[check_parameters[0]]
starting_angle = check_parameters[1]
'''
# ------ For MC tuning only, remove for challenge ------ #
starting_point = [84., 30.]
starting_angle = 0
# -------------------------------------------------------#
'''
# Pass these starting parameters to the robot and the particules filter
Robot.set_x(starting_point[0])
Robot.set_y(starting_point[1])
Robot.set_theta(starting_angle)
PF.particles = np.array([[starting_point[0], starting_point[1], starting_angle]] * PF.num_particles)

# -------- Comment while tuning MC parameters ------------
# MC on the beginning to correct first angle
PF.update_after_rotation_full(starting_angle, 0, 0.05)
z = Robot.instantiated_sensors[0].get_value()[0]
likelihood = PF.calculate_likelihood_full(mymap, z)
PF.update_weights(np.array(likelihood))
PF.resampling()
new_estimated_coordinates = PF.estimate_position_from_particles()
Robot.set_x(new_estimated_coordinates[0])
Robot.set_y(new_estimated_coordinates[1])
Robot.set_theta(new_estimated_coordinates[2])
#--------------------------------------------------------------
# create the list of points to go to, according to the starting point (shift of waypoints)
destinations = waypoints[initial_parameters[0]:] + waypoints[:initial_parameters[0] + 1]
'''
# ------ For MC tuning only, remove for challenge ------ #
destinations = waypoints + [(84., 30.)]
# -------------------------------------------------------#
'''

# Go through all the waypoints, applying MonteCarlo algorithm

for point in destinations[1:]:
    print("---------------------------")
    print("-> Current location before next move is: ", Robot.x, Robot.y)
    print("---------------------------")
    print("-> Heading towards: ", point)
    move = Robot.navigateToWaypoint(point[0], point[1])
    print("---------------------------")
    start_update = time.time()

    MonteCarlo(Robot, PF, move[0], move[1])
    print(" ---||||| I am on the waypoint, I must sleep for 1 second before going further |||||---")

    #particles = [(conversion(PF.particles[i][0]), conversiony(PF.particles[i][1]), PF.particles[i][2]) for i in
    #             range(PF.num_particles)]
    #print "drawParticles:" + str(particles)


duration = start_time - time.time()
print('It takes {0:.6f} seconds to complete the challenge.'.format(duration))
