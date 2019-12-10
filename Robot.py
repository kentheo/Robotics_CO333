import brickpi
import time
from Motor import *
from Sensor import *
from Signature import *
import math
import numpy as np

# MAC Address: 80:1f:02:ab:a6:0d

# Robot constants. These depend on the architecture of the robot, and have been determined after calibration
distance_per_angle = 54.2/20.2
rotation_per_angle = 360/21.7

interface = brickpi.Interface()


class Robot:
    # motors_list is in the format [[Motor 1 ID, Motor Side],[Motor 2 ID, Motor Side]]
    def __init__(self, motors_list, sensors_list):
        self.available_motors_id = [motors_list[i][0] for i in range(len(motors_list))]
        self.available_motors_names = [motors_list[i][1] for i in range(len(motors_list))]
        self.available_sensors_id = [sensors_list[i][0] for i in range(len(sensors_list))]
        self.available_sensors_names = [sensors_list[i][1] for i in range(len(sensors_list))]
        self.available_sensors_controlled_motors = [sensors_list[i][2] for i in range(len(sensors_list))]
        self.instantiated_motors = []
        self.instantiated_sensors = []
        self.instantiated_sensors_motors = []
        self.distance_per_angle = distance_per_angle
        self.rotation_per_angle = rotation_per_angle
        self.interface = interface
        self.interface.initialize()
        self.x = 0
        self.y = 0
        self.theta = 0

    # <------------------- Sets and gets, used for robot map coordinates ------------------>

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def get_theta(self):
        return self.theta

    def set_x(self, new_x):
        self.x = new_x
        return self.x

    def set_y(self, new_y):
        self.y = new_y
        return self.y

    def set_theta(self, new_theta):
        self.theta = new_theta
        return self.theta

    # <------------------------------- Initialisation methods ----------------------------->

    # Method to be called at the end of every script
    def terminate_interface(self):
        self.interface.terminate()

    # Instantiate every motor with the class Motor. The constructor applies default parameters to motors
    # After this instantiation, all motors can be used.
    def motor_init(self):
        self.instantiated_motors = [Motor(self.available_motors_id[i], self.available_motors_names[i], self.interface) for i in
                                    range(len(self.available_motors_id))]

    # Instantiate every sensor with the sensor class, as well as all the potential motors driving these sensors.
    def sensor_init(self):
        self.instantiated_sensors = [Sensor(self.interface, self.available_sensors_id[i], self.available_sensors_names[i],
                                            self.available_sensors_controlled_motors[i]) for i in range(len(self.available_sensors_id))]
        self.instantiated_sensors_motors += [Motor(self.instantiated_sensors[i].id_motor_controlled, "none", self.interface)
                                     for i in range(len(self.instantiated_sensors))]
        for i, sensor in enumerate(self.instantiated_sensors):
            sensor.set_instantiated_motor(self.instantiated_sensors_motors[i])

    # <----------------------------------- Robot move methods ------------------------------------>

    def linear_move(self, distance):
        if self.instantiated_motors == []:
            print("Motors have not been initialized, Robot cannot move. Use Robot.motor_init() first")
            return 0
        corresponding_angle = distance / self.distance_per_angle
        for motor in self.instantiated_motors:
            motor.increase_angle(corresponding_angle)
        while not self.instantiated_motors[0].motor_angle_reached():
            while not self.instantiated_motors[1].motor_angle_reached():
                time.sleep(0.5)

    def rotation_move(self, rotation):
        if self.instantiated_motors == []:
            print("Motors have not been initialized, Robot cannot move. Use Robot.motor_init() first")
            return 0
        # corresponding_angle = rotation / self.rotation_per_angle
        # we put the result in the [-pi;pi] range
        def put_in_range(angle):
            in_range_angle = 0.0
            if (-360. < angle) and (angle < - 180.):
                in_range_angle = angle + 360.
            elif (- 180. < angle) and (angle <= 180.):
                in_range_angle = angle
            elif (180. < angle) and (angle < 360.):
                in_range_angle = angle - 360.
            else:
                in_range_angle = put_in_range(float(angle % (360.)))
            return in_range_angle

        # in_range_corresponding_angle = put_in_range(corresponding_angle)
        in_range_corresponding_angle = put_in_range(rotation) / self.rotation_per_angle
        #print("put in range in degrees: ", in_range_corresponding_angle * self.rotation_per_angle)
        for motor in self.instantiated_motors:
                if motor.motor_side == "Left":
                    motor.increase_angle(-in_range_corresponding_angle)
                elif motor.motor_side == "Right":
                    motor.increase_angle(in_range_corresponding_angle)
        while not self.instantiated_motors[0].motor_angle_reached():
            while not self.instantiated_motors[1].motor_angle_reached():
                time.sleep(0.5)

    # Command the robot to move at specified motor speeds during a certain amount of time
    def move_at_speed(self, speed_motor_1, speed_motor_2, duration):
        if self.instantiated_motors == []:
            print("Motors have not been initialized, Robot cannot move. Use Robot.motor_init() first")
            return 0
        self.instantiated_motors[0].set_speed(speed_motor_1)
        self.instantiated_motors[1].set_speed(speed_motor_2)
        time.sleep(duration)

    def left_90_deg(self):
        self.rotation_move(90)

    def right_90_deg(self):
        self.rotation_move(-90)

    # If all instantiated motors of the robot reached the angle command, the robot is not moving, otherwise it is moving
    def is_moving(self):
        for motor in self.instantiated_motors:
            if not motor.motor_angle_reached():
                return True
            else:
                pass
        return False

    def navigateToWaypoint(self, x, y):
        destination_coordinates = np.array([x, y])
        vector = [destination_coordinates[0] - self.x, destination_coordinates[1] - self.y]
        orientation_to_turn = math.atan2(vector[1], vector[0])  # Gives the correct result
        alpha = orientation_to_turn - self.theta
        #print('alpha =',alpha)
        self.rotation_move(alpha * 180 / np.pi)
        distance_to_move = np.sqrt(vector[0] ** 2 + vector[1] ** 2)
        self.linear_move(distance_to_move)
        return distance_to_move, alpha

    # <----------------------------- Mapping and localisation methods ------------------------------>

    def characterize_location(self, ls):
        ultrasonic_sensor = []
        motor_to_activate = []
        # First we get the motor driving the ultrasonic sensor
        for sensor in self.instantiated_sensors:
            if sensor.sensor_name == "SENSOR_ULTRASONIC":
                ultrasonic_sensor += [sensor]
                motor_to_activate += sensor.instantiated_motor       # sensor.instantiated_motor is already a list
        if motor_to_activate is []:
            print(" !! Could not find any motor driving the ultrasonic sensor !!")
            return 0
        # place sensor looking backwards to begin with
        # If we start with the sensor looking backwards, comment the following 3 lines
        # motor_to_activate[0].increase_angle(- np.pi)
        # while not motor_to_activate[0].motor_angle_reached():
        #    pass
        scan_distances = []
        # If number of measures is changed, be careful to change it in the location signature instance as well
        number_of_measures = 360
        #elementary_angle = 2 * np.pi / number_of_measures
        # lower the motor speed
        motor_to_activate[0].set_speed(np.pi/2, 3)
        starting_motor_angle = motor_to_activate[0].get_motor_angle()
        motor_to_activate[0].increase_angle(2 * np.pi)
        # Array that will be passed to the location signature instance at the end of the procedure

        for i in range(number_of_measures):
            distance_measured = ultrasonic_sensor[0].get_value()[0]   # get the distance measured by the sonar
            scan_distances += [distance_measured]                   # append this measure to the list of all measures
            time.sleep(4.4/number_of_measures)                       # Time interval between each measure, corresponds to
        #difference_start_end = starting_motor_angle[0] - motor_to_activate[0].get_motor_angle()[0]
        #print("Motor angle difference during sonar measures is :", difference_start_end)
        time1 = time.time()
        # the motor speed (2pi radians in 4 seconds)
        # Make sure the sonar has finished moving before going forward
        while not motor_to_activate[0].motor_angle_reached():
            pass
        time2 = time.time()
        differencetime = time2 - time1
        print('We have {0:.6f} second of no measurement by the sonar'.format(differencetime))
        # put back the sensor looking forward, running at normal speed
        motor_to_activate[0].set_speed(6, 6)
        motor_to_activate[0].increase_angle(- np.pi)
        while not motor_to_activate[0].motor_angle_reached():
            pass
        # We now have to update the location signature instance with the new measures
        ls.set_sig(scan_distances)
        return ls.sig

    # FILL IN: compare two signatures
    def compare_signatures(self, ls1, ls2):
        histo_ls1 = ls1.histogram()
        histo_ls2 = ls2.histogram()
        dist = 0
        for i in range(len(histo_ls1)):
            dist += (histo_ls2[i] - histo_ls1[i]) ** 2
        return dist

    def compare_signatures_histo(self, ls1, histo_ls2):
        histo_ls1 = ls1.histogram()
        dist = 0
        for i in range(len(histo_ls1)):
            dist += (histo_ls2[i] - histo_ls1[i]) ** 2
        return dist

    def get_angle_from_signature(self, ls_obs, ls2):
        # Initialise best distance with highest possible value
        best_dist = 360 ** 2 * 360
        best_match_idx = - 1
        # We will loop over all the 360 possible shifts of the signature, from -180 to +180 to have easier computation
        # later for the translation to radians.
        for shift in range(- int(len(ls_obs.sig)/2), int(len(ls_obs.sig)/2)):
            dist = 0
            # For every shift, we compute the distance to the observed signature, and keep track of the shift which
            # leads to the smallest distance
            for angle_idx in range(len(ls_obs.sig)):
                dist += (ls_obs.sig[(angle_idx + shift) % len(ls_obs.sig)] - ls2.sig[angle_idx]) ** 2
            # If the distance computed with this shift is the smallest ever seen at this point, we store this shift
            if dist < best_dist:
                best_dist = dist
		best_match_idx = shift
        # We translate the shift which is in degrees to radians.
        theta = float(best_match_idx * np.pi / 180.)
        return theta
