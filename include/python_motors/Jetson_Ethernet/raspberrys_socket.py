# This file represents the code for the Rasberry PI. 
# This would send information to the raspberry pi to execute
import socket
import time
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

can0 = can.interface.Bus(channel= 'can0', bustype = 'socketcan')
can1 = can.interface.Bus(channel= 'can1', bustype = 'socketcan')


#The follow are the motor ids associated with each motor on the rover
#Note that these can be changed later on if need be
rfront_id = 0x141
rback_id = 0x141
lfront_id = 0x141
lback_id = 0x141


# Set up the server (Raspberry Pi)
HOST = '0.0.0.0'  # Listen on all available interfaces
PORT = 12345       # Port to listen on (use a port number > 1024)
BUFFER_SIZE = 1024 # Size of the buffer for receiving data

# Create a socket object
rasberry_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the IP and port PORT and HOST are grouped together
rasberry_socket.bind((HOST,PORT))
# the main code that loops 
while True:

    # Listen for incoming connections (max 1 connection in this case)
    rasberry_socket.listen(1)
    print(f"Listening for connections on {HOST}:{PORT}...")
    (HOST, PORT)
    # Accept an incoming connection
    conn, addr = rasberry_socket.accept()
    print(f"Connected by {addr}")

    # Keep receiving data until connection is closed
    while True:
        serialize_data = conn.recv(BUFFER_SIZE)
        if not data:
            break

        data = pickle.loads(serialize_data)
        
        print(f"Received data: {data}")
        
        # Send a response back
        conn.sendall(b"Data received!")

    # Close the connection
    conn.close()
    break
