
import time
import os
import can.interface
import pygame
import rmdv3
import can
from pygame.locals import *
import sys
import can

os.system('sudo ip link set can0 type can bitrate 1000000')
os.system('sudo ifconfig can0 up')
os.system("sudo ifconfig can0 txqueuelen 1000")

os.system('sudo ip link set can1 type can bitrate 1000000')
os.system('sudo ifconfig can1 up')
os.system("sudo ifconfig can1 txqueuelen 1000")

can0 = can.interface.Bus(channel= 'can0', bustype = 'socketcan')
can1 = can.interface.Bus(channel= 'can1', bustype = 'socketcan')


pygame.init()

joystickcount = pygame.joystick.get_count()
print(f"The number of joysticks detected is {joystickcount}")

joysticks = {}

# Below are the axes and buttons associated with the xbox series x controller
ljoy_hor_axis = 0
ljoy_ver_axis = 1
rjoy_hor_axis = 3
rjoy_ver_axis = 4
ltrigger_axis = 2
rtrigger_axis = 5

a_button = 0
b_button = 1
x_button = 2
y_button = 3
lb_button = 4
rb_button = 5
share_button = 6
options_button = 7
left_joy_push = 8
right_joy_push = 9
on_button = 10
center_button = 11

#The follow are the motor ids associated with each motor on the rover
#Note that these can be changed later on if need be
rfront_id = 0x141
rcen_id = 0x141
rback_id = 0x141
lfront_id = 0x141
lcen_id = 0x141
lback_id = 0x141

#For now, I am going to manually set the max speed.
#The goal is that later down the line, you should be able to use the d-pad to change the max speed anyways
max_speed = 16000 #This translates to 80dps

# I always to specify the starting values for these axes for future reference
trigger_axis_start = -1
button_start = 0

rtrigger_bool = 0
ltrigger_bool = 0
rb_bool = 0
lb_bool = 0
# makes a clock object so we can manipulate how fast our code runs
clock = pygame.time.Clock()


joysticks = [pygame.joystick.Joystick(i) for i in range(joystickcount)]

motion =[0, 0]
while True:
    for event in pygame.event.get():
        if event.type == JOYBUTTONDOWN:
            print(event)
            #This is the a button I believe
            if joysticks[0].get_button(0):
                can0.send(rmdv3.rmdv3_set_speed(rfront_id, 1, max_speed))
                print("You have pressed the a button")
            elif joysticks[0].get_button(1):
                can0.send(rmdv3.rmdv3_set_speed(rfront_id, 0, max_speed))
                print("This is B button")
                
        if event.type == JOYBUTTONUP:
            print(event)
        if event.type == JOYAXISMOTION:
            print(event)
            if event.type < 2:
                motion[event.axis] = event.value
        if event.type == JOYHATMOTION:
            print(event)
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    #This sets it to 60 frames per second
    clock.tick(60)
