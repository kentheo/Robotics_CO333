from Robot import *
List_plugged_motors = [[0, "Left"], [3, "Right"]]

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

speed_mean = 4.0
distance_to_wall = 30.
correction_factor = 0.05

for i in range(20):
    print(Simple_robot.instantiated_sensors[0].get_value())
    correction = correction_factor * (Simple_robot.instantiated_sensors[0].get_value()[0]-distance_to_wall)
    print(correction)
    Simple_robot.move_at_speed(speed_mean + correction, speed_mean - correction, 0.5)

Simple_robot.terminate_interface()
