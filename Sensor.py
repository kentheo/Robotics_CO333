import brickpi
from Motor import *


class Sensor:
    def __init__(self, interface, sensor_id, sensor_name, id_motor_controlled):
        self.sensor_id = sensor_id
        self.sensor_name = sensor_name
        self.id_motor_controlled = id_motor_controlled
        self.interface = interface
        self.interface.sensorEnable(self.sensor_id, getattr(brickpi.SensorType, sensor_name))
        self.instantiated_motor = []

    def get_value(self):
        usReading = self.interface.getSensorValue(self.sensor_id)
        return usReading

    def set_instantiated_motor(self, motor):
        self.instantiated_motor += [motor]

