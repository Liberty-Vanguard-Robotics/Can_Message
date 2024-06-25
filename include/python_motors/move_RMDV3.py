import os
import can

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
multi_id = 0x280

#Single motor command sending
single_id = 0x141

#Make send and receive messages
speed_write_msg_single = can.Message(is_extended_id=False,arbitration_id=single_id,data = [0xA2,0x00,0x00,0x00,0x10,0x27,0x00,0x00])

can0.send(speed_write_msg_single)

response = can0.recv(10.0)
print(response)

speed_write_msg_multi = can.Message(is_extended_id=False,arbitration_id=multi_id,data = [0xA2,0x00,0x00,0x00,0x10,0x27,0x00,0x00])

can0.send(speed_write_msg_multi)

response_multi = can0.recv(10.0)
print(response_multi)

#Shutdown CAN interfaces
os.system('sudo ifconfig can0 down')
os.system('sudo ifconfig can1 down')