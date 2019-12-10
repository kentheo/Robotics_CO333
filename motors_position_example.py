import brickpi
import time

print("************ START ***********************")
interface = brickpi.Interface()
interface.initialize()
print("************ Successful initialize ***********************")
motors = [0,3]	# B, D ports

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

motorParams = interface.MotorAngleControllerParameters()
motorParams.maxRotationAcceleration = 2.0
motorParams.maxRotationSpeed = 6.0
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
angle = float(input("Enter a angle to rotate (in radians): "))

interface.increaseMotorAngleReferences(motors,[-angle,angle])
# time.sleep(2)

# interface.increaseMotorAngleReferences(motors,[-2*angle,angle])

# motorAngles = interface.getMotorAngles(motors)

# interface.increaseMotorAngleReferences(motors,[0,0])

#while(1>0):
#    print("After stop exec")
#    time.sleep(0.5)

while not interface.motorAngleReferencesReached(motors) :
	motorAngles = interface.getMotorAngles(motors)
	if motorAngles :
		print "Motor angles: ", motorAngles[0][0], ", ", motorAngles[1][0]
		time.sleep(0.1)

print "Destination reached!"

interface.stopLogging()
interface.terminate()
