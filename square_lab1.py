import brickpi
from Robot import *
import time
List_plugged_motors = [[0, "Left"], [3, "Right"]]

# Information displayed, to be sure software motor configuration matches reality
print("The configuration states that plugged motors are :\n")
for i in List_plugged_motors:
    print("Port ", i[0], " for ", i[1], " side motor\n")

# Necessary for the instantiation of the Robot, empty for the moment
List_plugged_sensors = [0]

# Create the instance of the robot, initialize the interface
Simple_robot = Robot(List_plugged_motors, List_plugged_sensors)
# Enable its motors
Simple_robot.motor_init()

size_square = float(input("Enter the size of the square (in centimeters): "))
turn_side = raw_input("On which side do you want the robot to turn ('L' or 'R') :")


def draw_square(distance, left_or_right):
    for j in range(4):
        Simple_robot.linear_move(distance)
        print("Robot moving forward")
        # Temporary Time sleep: we have to determined if method increase_angle is blocking or not. I set this value so
        # that if increase angle is not blocking, we at least wait 0.5 seconds between each moving command.
        time.sleep(0.5)
        if left_or_right == "L":
            Simple_robot.left_90_deg()
            time.sleep(0.5)
        elif left_or_right == "R":
            Simple_robot.right_90_deg()
            time.sleep(0.5)
        else:
            print("Issues with specified side turn, can't turn left or right. Check if you entered 'L' or 'R' correctly")


draw_square(size_square,turn_side)

Simple_robot.terminate_interface()
