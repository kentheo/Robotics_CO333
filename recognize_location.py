# This function tries to recognize the current location.
# 1.   Characterize current location
# 2.   For every learned locations
# 2.1. Read signature of learned location from file
# 2.2. Compare signature to signature coming from actual characterization
# 3.   Retain the learned location whose minimum distance with
#      actual characterization is the smallest.
# 4.   Display the index of the recognized location on the screen
from Signature import *
from Robot import *
import os
'''
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
'''
signatures = SignatureContainer(5);


def save_in_memory(ls_obs):
    filename = "loc_obs.dat"
    if os.path.isfile(filename):
        os.remove(filename)

    f = open(filename, 'w')

    for i in range(len(ls_obs)):
        s = str(ls_obs[i]) + "\n"
        f.write(s)
    f.close()

def recognize_location(Robot):
    ls_obs = LocationSignature(360)
    Robot.characterize_location(ls_obs)
    save_in_memory(ls_obs)
    ls_obs.histogram()
    # FILL IN: COMPARE ls_read with ls_obs and find the best match
    smallest_dist_idx = -1
    smallest_dist = 360 **2 * 256
    penultimate_dist_idx = -1
    penultimate_dist = 360 ** 2 * 256
    for idx in range(signatures.size):
        print "STATUS:  Comparing signature " + str(idx) + " with the observed signature."
        ls_read = signatures.read(idx)
        ls_read.histogram()
        dist = Robot.compare_signatures(ls_obs, ls_read)
        if dist < smallest_dist:
            if idx > 0:
                penultimate_dist = smallest_dist
                penultimate_dist_idx = smallest_dist_idx
            smallest_dist = dist
            smallest_dist_idx = idx
    ls_nearest = signatures.read(smallest_dist_idx)
    theta = - Robot.get_angle_from_signature_optim(ls_obs, ls_nearest)
    confidence = 1. - float(smallest_dist)/float(penultimate_dist)  
    return [smallest_dist_idx, theta, smallest_dist, confidence, penultimate_dist_idx, penultimate_dist]


# Prior to starting learning the locations, it should delete files from previous
# learning either manually or by calling signatures.delete_loc_files().
# Then, either learn a location, until all the locations are learned, or try to
# recognize one of them, if locations have already been learned.

# signatures.delete_loc_files()

#print(recognize_location())
