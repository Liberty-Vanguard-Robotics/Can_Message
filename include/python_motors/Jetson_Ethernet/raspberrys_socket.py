# This file represents the code for the Rasberry PI. 
# This would send information to the raspberry pi to execute
import socket
import os
import can.interface
import pygame
import rmdv3
import can
from pygame.locals import *
import sys
import pickle




os.system('sudo ip link set can0 type can bitrate 1000000')
os.system('sudo ifconfig can0 up')
os.system("sudo ifconfig can0 txqueuelen 1000")

os.system('sudo ip link set can1 type can bitrate 1000000')
os.system('sudo ifconfig can1 up')
os.system("sudo ifconfig can1 txqueuelen 1000")
#CAN0 will be right side motors and CAN1 will be left side motors 
can0 = can.interface.Bus(channel= 'can0', bustype = 'socketcan')
can1 = can.interface.Bus(channel= 'can1', bustype = 'socketcan')


#The follow are the motor ids associated with each motor on the rover
#Note that these can be changed later on if need be
rfront_id = 0x141
rback_id = 0x141
lfront_id = 0x141
lback_id = 0x141
constMaxSpeed = 25000

# Set up the server (Raspberry Pi)
HOST = '0.0.0.0'  # Listen on all available interfaces
PORT = 12345       # Port to listen on (use a port number > 1024)
BUFFER_SIZE = 1024 # Size of the buffer for receiving data

# Create a socket object
rasberry_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#make clock to sync system
clock = pygame.time.Clock()
# Bind the socket to the IP and port PORT and HOST are grouped together
rasberry_socket.bind((HOST,PORT))
# the main code that loops 

# Listen for incoming connections (max 1 connection in this case)
rasberry_socket.listen(1)
print(f"Listening for connections on {HOST}:{PORT}...")
(HOST, PORT)
# Accept an incoming connection
conn, addr = rasberry_socket.accept()
print(f"Connected by {addr}")
while True:


    # Keep receiving data until connection is closed
    while True:
        serialize_data = conn.recv(BUFFER_SIZE)
        if serialize_data:
            data = pickle.loads(serialize_data)

            print(f"Received data: {data}")
            # send response back
            conn.sendall(pickle.dumps("Data received!"))
            break
            # buffer = ""
            # buffer += str(data)
            # try:
            #     command_dict = json.loads(buffer)
            #     print("Recieved dictionary:", command_dict)
            #     break
            # except json.JSONDecodeError:
            #     print("keep going")
            #     continue
        else:
           
            break
        
        # Send a response back
        #conn.sendall(b"Data received!")

    # data contains 3 parameters. y-axis and x-axis of joystick,
    # max_speed
    top_speed = data['max_speed']
    forward_vector = data['y-axis']
    turn_vector = data['x-axis']
    menu_button = data['Menu Button']
    #Postive means to the right of the joystick 
    if (turn_vector > .2 and forward_vector > .2):
        # This is just a linear transformation (inverted slope)
        # basically turns our turn_vector into a ratio between
        # 1 and -1. As turn_vector approaches 1 which allows it to turn
        #gradually.
        right_motor_ratio = -2 * turn_vector + 1
        # this makes it a reletive to the forward_vector. aka ratio
        right_motor_ratio = right_motor_ratio * forward_vector

        can1.send(rmdv3.increasing_speed_set(rfront_id, right_motor_ratio,constMaxSpeed))

        can0.send(rmdv3.increasing_speed_set(rfront_id, forward_vector, constMaxSpeed))
    elif (turn_vector < -.2 and forward_vector > .2):
        # Same thing as above but no negetive on the 2.
        left_motor_ratio = 2 * turn_vector + 1
        # this makes it a reletive to the forward_vector. aka ratio
        left_motor_ratio = left_motor_ratio * forward_vector

        #left motors
        can1.send(rmdv3.increasing_speed_set(rfront_id, forward_vector,constMaxSpeed))
        #right motors
        can0.send(rmdv3.increasing_speed_set(rfront_id, left_motor_ratio, constMaxSpeed))
    elif (turn_vector > .2):
        #left motors should go forward
        can1.send(rmdv3.increasing_speed_set(rfront_id,turn_vector,constMaxSpeed))
        turn_vector = -turn_vector
        #right motors go backwards
        can0.send(rmdv3.increasing_speed_set(rfront_id,turn_vector,constMaxSpeed))
    elif (turn_vector < -.2):
        turn_vector = abs(turn_vector)
        can0.send(rmdv3.increasing_speed_set(rfront_id,turn_vector,constMaxSpeed))
        turn_vector = -turn_vector
        can1.send(rmdv3.increasing_speed_set(rfront_id,turn_vector,constMaxSpeed))
    elif (forward_vector > .2):
        #make both left and right motors to go forward.
        can0.send(rmdv3.increasing_speed_set(rfront_id,forward_vector,constMaxSpeed))
        can1.send(rmdv3.increasing_speed_set(rfront_id,forward_vector,constMaxSpeed))
    elif (forward_vector < -.2):
        can0.send(rmdv3.increasing_speed_set(rfront_id,forward_vector,constMaxSpeed))
        can1.send(rmdv3.increasing_speed_set(rfront_id,forward_vector,constMaxSpeed))
    else:
        can0.send(rmdv3.increasing_speed_set(rfront_id,0,constMaxSpeed))
        can1.send(rmdv3.increasing_speed_set(rfront_id,0,constMaxSpeed))

    if (data['Menu Button'] == 1):
        break
    clock.tick(30)

conn.close()
os.system('sudo ifconfig can0 down')
os.system('sudo ifconfig can1 down')
    
