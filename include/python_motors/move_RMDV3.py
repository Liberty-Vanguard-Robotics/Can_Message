import os
import can
import time

#Set up the can interfaces
# Notice that the bitrate is set to 1Mbps. This is different between the V2 and V3 RMD motors
os.system('sudo ip link set can0 type can bitrate 1000000')
os.system('sudo ifconfig can0 up')

os.system('sudo ip link set can1 type can bitrate 1000000')
os.system('sudo ifconfig can1 up')

can0 = can.interface.Bus(channel= 'can0', bustype = 'socketcan')
can1 = can.interface.Bus(channel= 'can1', bustype = 'socketcan')

#Make message for moving motor

#Multi motor command sending
multi_id = 0x2fa
#Single motor command sending
single_id = 0x141


#System Reset
# reset_msg = can.Message(is_extended_id=False,arbitration_id=single_id,data= [0x76,0x00,0x00,0x00,0x00,0x00,0x00,0x00])
# can0.send(reset_msg)
# print(can0.recv(2.0))

#Read CAN ID
read_msg = can.Message(is_extended_id=False,arbitration_id=multi_id,data= [0x79,0x00,0x01,0x00,0x00,0x00,0x00,0x02])
can0.send(read_msg)
print(can0.recv(2.0))
response = can0.recv(2.0)

count = 100
while (~response & count > 0):
    multi_id = multi_id+1
    read_msg = can.Message(is_extended_id=False,arbitration_id=multi_id,data= [0x79,0x00,0x01,0x00,0x00,0x00,0x00,0x02])
    can0.send(read_msg)
    print(can0.recv(2.0))
    response = can0.recv(2.0)
    count = count-1

if count == 0:
    print("Received no response for write command")
elif response:
    print("Motor responded, please examine for ID change")

#Make send and receive messages
speed_write_msg_single = can.Message(is_extended_id=False,arbitration_id=single_id,data = [0xA2,0x00,0x00,0x00,0x27,0x27,0x00,0x00])

can0.send(speed_write_msg_single)

response = can0.recv(10.0)
print(response)

#time.sleep(2)

# motor_stop = can.Message(is_extended_id=False,arbitration_id=single_id,data = [0x81,0x00,0x00,0x00,0x00,0x00,0x00,0x00])

# can0.send(motor_stop)

# response = can0.recv(5.0)
# print(response)

time.sleep(2)

speed_write_msg_single = can.Message(is_extended_id=False,arbitration_id=single_id,data = [0xA2,0x00,0x00,0x00,0xFF,0x27,0x00,0xAA])

can0.send(speed_write_msg_single)

response = can0.recv(10.0)
print(response)
# if response:
#     print("Motor temperature is " + str(response[1]) + " C")
#     print("Torque current is " + str(((response[3] << 4) +response[2])*0.01) + " A")
#     print("Motor speed is " + str((response[5] << 4) +response[4]) + " dps")
#     print("Motor Angle is " + str((response[7] << 4) +response[6]) + " degrees")


# speed_write_msg_multi = can.Message(is_extended_id=False,arbitration_id=multi_id,data = [0xA2,0x00,0x00,0x00,0x00,0x27,0x00,0x00])

# can0.send(speed_write_msg_multi)

# response_multi = can0.recv(10.0)
# print(response_multi)

#Reset the speed to 0
time.sleep(2) #Delay 5 seconds before stopping the motor
speed_0_msg = can.Message(is_extended_id=False,arbitration_id=single_id,data = [0xA2,0x00,0x00,0x00,0x00,0x00,0x00,0x00])

can0.send(speed_0_msg)

response = can0.recv(10.0)
print(response)
# print("Motor temperature is " + str(response[1]) + " C")
# print("Torque current is " + str(((response[3] << 4) +response[2])*0.01) + " A")
# print("Motor speed is " + str((response[5] << 4) +response[4]) + " dps")
# print("Motor Angle is " + str((response[7] << 4) +response[6]) + " degrees")

#Shutdown CAN interfaces
os.system('sudo ifconfig can0 down')
os.system('sudo ifconfig can1 down')