import brickpi
import time
import Motor

interface=brickpi.Interface()
interface.initialize()

motors = [0,1] #motor 0 = A; motor 1 = B;

interface.motorEnable(motors[0])
interface.motorEnable(motors[1])

motorParams = interface.MotorAngleControllerParameters()
motorParams.maxRotationAcceleration = 6.0
motorParams.maxRotationSpeed = 12.0
motorParams.feedForwardGain = 255/20.0
motorParams.minPWM = 18.0
motorParams.pidParameters.minOutput = -255
motorParams.pidParameters.maxOutput = 255
motorParams.pidParameters.k_p = 150.0
motorParams.pidParameters.k_i = 0.0
motorParams.pidParameters.k_d = 0.0
distance_per_angle = []
rotation_per_angle = []


interface.setMotorAngleControllerParameters(motors[0],motorParams)
interface.setMotorAngleControllerParameters(motors[1],motorParams)

def move(distance):
    desired_angle = distance/distance_per_angle #desired angle = 40cm
    interface.increaseMotorAngleReferences(motors,[desired_angle,desired_angle])

    while not interface.motorAngleReferencesReached(motors) :
    	motorAngles = interface.getMotorAngles(motors)
    	if motorAngles :
    		print "Motor angles: ", motorAngles[0][0], ", ", motorAngles[1][0]
    		time.sleep(0.1)

def turn(rotation):
    desired_angle = rotation/rotation_per_angle
    interface.increaseMotorAngleReferences(motors,[+desired_angle,-desired_angle])

    while not interface.motorAngleReferencesReached(motors) :
    	motorAngles = interface.getMotorAngles(motors)
    	if motorAngles :
    		print "Motor angles: ", motorAngles[0][0], ", ", motorAngles[1][0]
    		time.sleep(0.1)

def Left90deg():
    turn(-90)

def Right90deg():
    turn(90)
