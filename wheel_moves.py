from Motor import *
import brickpi
from Robot import *

interface=brickpi.Interface()
interface.initialize()

List_motors_id = [0,3]      # A, D ports
List_motors_name = ["Left","Right"]

Left_motor = Motor(List_motors_id[0],List_motors_name[0])
Right_motor = Motor(List_motors_id[1],List_motors_name[1])

# def linear_move(motors_list,distance):
#     corresponding_angle = distance/(motors_list[0].distance_per_angle)
#     interface.increaseMotorAngleReferences(motors_list[i].id for i in range(len(motors_list)),[corresponding_angle]*len(motors_list))
# def rotation_move(motors_list,rotation):
#     List_left_motors = [motors_list[i].id for i in range(len(motors_list)) if motors_list[i].name == "Left"]
#     List_right_motors = [motors_list[i].id for i in range(len(motors_list)) if motors_list[i].name == "Right"]
#     corresponding_angle = rotation/(motors_list[0].rotation_per_angle)
#     interface.increaseMotorAngleReferences(List_left_motors, corresponding_angle)
#     interface.increaseMotorAngleReferences(List_right_motors, - corresponding_angle)

def linear_move(motors_list,distance):
    corresponding_angle = distance/(motors_list[0].distance_per_angle)
    interface.increaseMotorAngleReferences(motors_list,[corresponding_angle, corresponding_angle])

def rotation_move(motors_list, rotation):
    corresponding_angle = rotation / (motors_list[0].rotation_per_angle)
    interface.increaseMotorAngleReferences(motors_list, [corresponding_angle, -corresponding_angle])

def Left90deg(motors_list):
    rotation_move(motors_list,-90)

def Right90deg(motors_list):
    rotation_move(motors_list,90)

def U_turn_left(motors_list):
    rotation_move(motors_list,-180)

def U_turn_right(motors_list):
    rotation_move(motors_list,180)

def Complete_rotation_left(motors_list):
    rotation_move(motors_list,-360)

def Complete_rotation_right(motors_list):
    rotation_move(motors_list,360)
