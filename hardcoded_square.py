import brickpi
import time

print("************ START ***********************")
interface = brickpi.Interface()
interface.initialize()
print("************ Successful initialize ***********************")
motors = [0,3]	# A, D ports

interface.motorEnable(motors[0])
interface.motorEnable(motors[1])

print("************ After motor enabling ***********************")
# PID parameters - Ziegler-Nichols method
p_u = 0.28				# Period
k_u = 950				# Based on our first try with a good k_p = 550
k_p = 0.6 * k_u
ki_correction = -400
k_i = 2 * k_p / p_u + ki_correction
k_d = k_p * p_u / 8

# Ratios
distance_per_angle_right = 54.2/20.2	 # Two variables for each motor, in case the battery is a pain
distance_per_angle_left = 54.2/20.2
rotation_per_angle = 360/22.1

motorParams = interface.MotorAngleControllerParameters()
motorParams.maxRotationAcceleration = 4.0
motorParams.maxRotationSpeed = 8.0
motorParams.feedForwardGain = 290/20.0 # 255/20.0
motorParams.minPWM = 18.0
motorParams.pidParameters.minOutput = -255
motorParams.pidParameters.maxOutput = 255
motorParams.pidParameters.k_p = k_p
motorParams.pidParameters.k_i = k_i
motorParams.pidParameters.K_d = k_d

print("************ Before setting of motor angles ***********************")

interface.setMotorAngleControllerParameters(motors[0],motorParams)
interface.setMotorAngleControllerParameters(motors[1],motorParams)

print("************ About to startLogging ***********************")

# Logging
interface.startLogging("/home/pi/prac-files/logfile.txt")
square_size = float(input("Enter a square size (in centimeters): "))

corresponding_angle_forward_right = square_size / distance_per_angle_right
corresponding_angle_forward_left = square_size / distance_per_angle_left
corresponding_angle_rotation = (90+360) / rotation_per_angle

print("************ About to start moving ***********************")

for i in range(4):
    print("Moving forward")
    interface.increaseMotorAngleReferences(motors, [corresponding_angle_forward_right, corresponding_angle_forward_left])

    while not interface.motorAngleReferencesReached(motors):
        motorAngles = interface.getMotorAngles(motors)
    print("Rotating Left")
    interface.increaseMotorAngleReferences(motors, [corresponding_angle_rotation, - corresponding_angle_rotation])
    while not interface.motorAngleReferencesReached(motors):
        motorAngles = interface.getMotorAngles(motors)


print("Destination reached!")

interface.stopLogging()
interface.terminate()
