# This file will accept joystick or button values from the main file.
# These will be converted into commands for the motor
# Every function in this file should need a motor_id passed to it

# As of 2024, this should work for 4 of the 6 RMD motors that are being used. 
# The remaining motors are V2 motors and will have different controls

# The output of these functions should be a CAN message that can be sent

# This function will create a CAN message to set speed based on the joystick value
# As of writing, the joystick values range from -1 to 1, while speed ranges from 

import can

def neg_int(int_num,byte_length):
    speed_bytes = int.to_bytes(int_num,length=byte_length,byteorder='little',signed=True)
    return speed_bytes

def rmdv2_set_speed(motor_id,axis,max_speed,axis_start=-1,byte_length=4): #I'm start the axis_start value with a default of -1
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
        #The big order being 'little' sets the array so that the most significant bit is now at the end
    
    #At this point, we should be in a series of bytes that can be put into a CAN Message
    msg_data[4] = speed_bytes[0]
    msg_data[5] = speed_bytes[1]
    msg_data[6] = speed_bytes[2]
    msg_data[7] = speed_bytes[3]

    speed_msg = can.Message(is_extended_id=False,arbitration_id=motor_id,data= msg_data)
    print(speed_msg)

    return speed_msg
    