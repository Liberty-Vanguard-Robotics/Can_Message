# This file will accept joystick or button values from the main file.
# These will be converted into commands for the motor
# Every function in this file should need a motor_id passed to it

# As of 2024, this should work for 4 of the 6 RMD motors that are being used. 
# The remaining motors are V2 motors and will have different controls

# The output of these functions should be a CAN message that can be sent

# This function will create a CAN message to set speed based on the joystick value
# As of writing, the joystick values range from -1 to 1, while speed ranges from 

import can
import can.message
import numpy

def neg_int(int_num,byte_length):
    speed_bytes = int.to_bytes(int_num,length=byte_length,byteorder='little',signed=True)
    return speed_bytes

def rmdv3_set_speed(motor_id,axis,max_speed,axis_start=-1,byte_length=4): #I'm start the axis_start value with a default of -1
    #Notice the default byte length is 4. The RMDV3 motors should always accept 4 bytes
    
    # This base data is defined in the RMD V3 communication protocol.
    # Data fields 0-3 should not change
    msg_data = [0xA2,0x00,0x00,0x00,0x00,0x00,0x00,0x00]

    # First, I want to make the speed value as a ratio of the max speed setting
    if axis_start < -0.5:
        speed = int(max_speed*(((axis+abs(axis_start))/(abs(axis_start)+1))))
    else:
        speed = int(max_speed*(axis))
    # Now that we have the speed, we want to convert that to a series of bytes that can be used

    # If the speed is negative, we have to find the twos complement
    if speed < 0:
        speed_bytes = neg_int(speed,byte_length)
    else:#If it isn't negative, we just have to split it up into bytes to use
        speed_bytes = int.to_bytes(speed,length=byte_length,byteorder='little',signed=True)
        #The byte order being 'little' sets the array so that the most significant bit is now at the end
    
    #At this point, we should be in a series of bytes that can be put into a CAN Message
    msg_data[4] = speed_bytes[0]
    msg_data[5] = speed_bytes[1]
    msg_data[6] = speed_bytes[2]
    msg_data[7] = speed_bytes[3]

    print(type(msg_data))
    
    speed_msg = can.Message(is_extended_id=False,arbitration_id=motor_id,data= msg_data)
    print(speed_msg)

    return speed_msg

def set_accelerate_RMDV3(motor_id):
    # this is the data to write the acceleration to 1 degrees per second
    
    accel_Data = [0x43,0x00,0x00,0x00,0x01,0x00,0x00,0x00]

    print(type(accel_Data))
    accel_CAN_Msg = can.Message(is_extended_id=False,arbitration_id=motor_id,data= accel_Data)
    return accel_CAN_Msg


def set_constant_RMDV3(motor_id):
    # Set KP = 85 and KI = 25
    constant_Data = [0x31,0x00,0x55,0x19,0x55,0x19,0x55,0x19]

    print(type(constant_Data))
    constant_CAN_Msg = can.Message(is_extended_id=False,arbitration_id=motor_id,data= constant_Data)
    return constant_CAN_Msg

def read_PID_RMDV3(motor_id):
    PID_Command = [0x30,0x00,0x00,0x00,0x00,0x00,0x00,0x00]
    print(type(PID_Command))
    PID_CAN_Msg = can.Message(is_extended_id=False,arbitration_id=motor_id,data= PID_Command)
    return PID_CAN_Msg
# this is the commmand we will use for the Demo of the rover
def increasing_speed_set(motor_id, axis_value, max_speed,bits_length=32):
    msg_data = [0xA2,0x00,0x00,0x00,0x00,0x00,0x00,0x00]

    motor_speed = int(axis_value * max_speed)

    #twocomp_speed = twos_comp(motor_speed,bits_length)
    #print(twocomp_speed)

    print(motor_speed)
    bytes = int(motor_speed).to_bytes(4, byteorder='little',signed=True)
    print(bytes)
    msg_data[4] = bytes[0]
    msg_data[5] = bytes[1]
    msg_data[6] = bytes[2]
    msg_data[7] = bytes[3]
    print(bytes)
    canMsg = can.Message(is_extended_id=False,arbitration_id=motor_id,data= msg_data)
    return canMsg



def twos_comp(val: int, bits: int) -> int:
    """compute the 2's complement of int value val
    """
    if (val & (1 << (bits - 1))) != 0: # if sign bit is set e.g., 8bit: 128-255
        val = val - (1 << bits)        # compute negative value
    return val

def twos_complement_binary(n, num_bits):
    mask = (1 << num_bits) - 1
    return (n & mask) if (n & (1 << (num_bits - 1))) == 0 else (n | ~mask)