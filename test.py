import brickpi
import time

print("************ START ***********************")
interface = brickpi.Interface()
interface.initialize()
print("************ Successful initialize ***********************")
motors = [1,3]	# A, D ports

interface.motorEnable(motors[0])
interface.motorEnable(motors[1])

print("************ After motor enabling ***********************")
# PID parameters - Ziegler-Nichols method
p_u = 0.28				# Period
k_u = 950				# Based on our first try with a good k_p = 550
k_p = 0.6 * k_u
k_i = 2 * k_p / p_u
k_d = k_p * p_u / 8

distance_per_angle = 54.2/20
rotation_per_angle = 360/15.2
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

corresponding_angle_forward = square_size / distance_per_angle
corresponding_angle_rotation = 90 / rotation_per_angle

def Left90deg(corresponding_angle, motors):
    interface.increaseMotorAngleReferences(motors, [-corresponding_angle, corresponding_angle])
    while not interface.motorAngleReferencesReached(motors):
        motorAngles = interface.getMotorAngles(motors)

def Right90deg(corresponding_angle, motors):
    interface.increaseMotorAngleReferences(motors, [corresponding_angle, -corresponding_angle])
    while not interface.motorAngleReferencesReached(motors):
        motorAngles = interface.getMotorAngles(motors)

#distance
print("Moving forward")
interface.increaseMotorAngleReferences(motors, [corresponding_angle_forward, corresponding_angle_forward])
while not interface.motorAngleReferencesReached(motors):
        motorAngles = interface.getMotorAngles(motors)

time.sleep(3)

print("Moving backward")
interface.increaseMotorAngleReferences(motors, [-corresponding_angle_forward, -corresponding_angle_forward])
while not interface.motorAngleReferencesReached(motors):
        motorAngles = interface.getMotorAngles(motors)

time.sleep(3)

#rotation
print("Rotating Left 90")
Left90deg(corresponding_angle_rotation, motors)

time.sleep(3)

print("Rotating Right 90")
Right90deg(corresponding_angle_rotation, motors)

time.sleep(3)
