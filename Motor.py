import brickpi

# Global Constants of Motors, obtained after calibration (lab 1)
max_rotation_acceleration = 6.0  #To be customized
max_rotation_speed = 12.0  #To be customized
feed_forward_gain = 290/20.0  #To be customized
min_pwm = 18.0  #To be customized
min_output = -255  #To be customized
max_output = 255  #To be customized

# PID parameters - Ziegler-Nichols method
p_u = 0.28 				# Period
k_u = 950				# Based on our first try with a good corresponding at k_p = 550
k_p = 0.6 * k_u
ki_correction = -400      # Ziegler-Nichols method gives a too high k_i. We apply a correction to it.
k_i = 2 * k_p / p_u + ki_correction
k_d = k_p * p_u / 8


class Motor:
    def __init__(self, motor_id, motor_side, interface):
        self.motor_id = motor_id
        self.motor_side = motor_side
        self.interface = interface
        self.interface.motorEnable(motor_id)
        self.motorParams = self.interface.MotorAngleControllerParameters()
        self.motorParams.maxRotationAcceleration = max_rotation_acceleration
        self.motorParams.maxRotationSpeed = max_rotation_speed
        self.motorParams.feedForwardGain = feed_forward_gain
        self.motorParams.minPWM = min_pwm
        self.motorParams.pidParameters.minOutput = min_output
        self.motorParams.pidParameters.maxOutput = max_output
        self.motorParams.pidParameters.k_p = k_p
        self.motorParams.pidParameters.k_i = k_i
        self.motorParams.pidParameters.K_d = k_d                       # Not a typo!! Based on piazza note by instructor
        self.interface.setMotorAngleControllerParameters(motor_id, self.motorParams)

    def increase_angle(self, angle):
        self.interface.increaseMotorAngleReferences([self.motor_id], [angle])

    def set_speed(self, speed, acceleration):
        self.motorParams.maxRotationSpeed = speed
        self.motorParams.maxRotationAcceleration = acceleration
        self.interface.setMotorAngleControllerParameters(self.motor_id, self.motorParams)

    ''' Abstraction of Interface methods giving motors information '''
    # return the current angle of a list of motors
    def get_motor_angle(self):
        return self.interface.getMotorAngles([self.motor_id])

    # return boolean value true if the command in angle is reached, and false if not. Can be called in a loop
    # to check whether the movement is done or not.
    def motor_angle_reached(self):
        return self.interface.motorAngleReferencesReached([self.motor_id])

