import os
import can

os.system('sudo ip link set can0 type can bitrate 1000000')
os.system('sudo ifconfig can0 up')

os.system('sudo ip link set can1 type can bitrate 1000000')
os.system('sudo ifconfig can1 up')

can0 = can.interface.Bus(channel= 'can0', bustype = 'socketcan')
can1 = can.interface.Bus(channel= 'can1', bustype = 'socketcan')

msg = can.Message(is_extended_id=False,arbitration_id=0x028,data = [0,1,2,3,4,5,6,7])

can0.send(msg)

msg_recv = can1.recv(10.0)
print(msg_recv)

os.system('sudo ifconfig can0 down')
os.system('sudo ifconfig can1 down')