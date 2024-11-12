import os
import can
import time

def neg_int(int_num,byte_length):
    speed_bytes = int.to_bytes(int_num,length=byte_length,byteorder='little',signed=True)
    return speed_bytes


def set_accelerate_RMDV3(motor_id):
    # this is the data to write the acceleration to 5 degrees per second
    
    accel_Data = [0x43,0x00,0x00,0x00,0x05,0x00,0x00,0x00]

    print(type(accel_Data))
    accel_CAN_Msg = can.Message(is_extended_id=False,arbitration_id=motor_id,data= accel_Data)
    return accel_CAN_Msg