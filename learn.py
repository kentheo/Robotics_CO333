# This function characterizes the current location, and stores the obtained
# signature into the next available file.

from Signature import *
from Robot import *

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

signatures = SignatureContainer(5)

def learn_location():
    ls = LocationSignature()
    Robot.characterize_location(ls)
    idx = signatures.get_free_index()
    if idx == -1:  # run out of signature files
        print "\nWARNING:"
        print "No signature file is available. NOTHING NEW will be learned and stored."
        print "Please remove some loc_%%.dat files.\n"
        return
    signatures.save(ls, idx)
    print "STATUS:  Location " + str(idx) + " learned and saved."

learn_location()

Robot.terminate_interface()
