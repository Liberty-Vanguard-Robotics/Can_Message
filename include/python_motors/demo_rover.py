""" 
The purpose of this file is to provide three main things
1. Receive data from xbox controller
2. Broadcast data over radio to Raspberry pi on rover
3. Move rover forwards, backwards, and turning based on controller values

The idea is that this code will function to create a demo rover that can be shown off and
used for further code development
"""

import time
import os
import pygame
import rmdv3
import can

os.system('sudo ip link set can0 type can bitrate 1000000')
os.system('sudo ifconfig can0 up')

os.system('sudo ip link set can1 type can bitrate 1000000')
os.system('sudo ifconfig can1 up')

can0 = can.interface.Bus(channel= 'can0', bustype = 'socketcan')
can1 = can.interface.Bus(channel= 'can1', bustype = 'socketcan')

pygame.init()

joystickcount = pygame.joystick.get_count()
print(f"The number of joysticks detected is {joystickcount}")

joysticks = {}

# Below are the axes and buttons associated with the xbox series x controller
ljoy_hor_axis = 0
ljoy_ver_axis = 1
rjoy_hor_axis = 2
rjoy_ver_axis = 3
ltrigger_axis = 4
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
rcen_id = 0x142
rback_id = 0x143
lfront_id = 0x144
lcen_id = 0x145
lback_id = 0x146

#For now, I am going to manually set the max speed.
#The goal is that later down the line, you should be able to use the d-pad to change the max speed anyways
max_speed = 8000 #This translates to 80dps

# I always to specify the starting values for these axes for future reference
trigger_axis_start = -1

done = 1
while done:
    for event in pygame.event.get():
        if event.type == pygame.JOYDEVICEREMOVED:
            done = 0
        if event.type == pygame.JOYDEVICEADDED:
            joy = pygame.joystick.Joystick(event.device_index)
            joysticks[joy.get_instance_id()] = joy
            print(f"Joystick {joy.get_instance_id()} connencted")
        if event.type == pygame.JOYDEVICEREMOVED:
            del joysticks[event.instance_id]
            print(f"Joystick {event.instance_id} disconnected")
        
    for joystick in joysticks.values():
        name = joystick.get_name()
        print(name)
        """
        At the present moment, I am only concerned with the forwards, backwards, and spinning motion
        The sequence of events should be as follows.
        1 - If right trigger is pressed, read speed value and set right motors to that speed.
            In this case, the right bumper should be ignored.
            If the left bumper is pressed, set the speed of the left motors to match the right motors but opposite direction
        2 - If right bumper is pressed, go backwards at some constant speed.
            Right trigger should be ignored.
            If left trigger is pressed, make left motors go forward
            reset right motors to match speed of left motors
        3 - copy right trigger sequence for left trigger
        4 - copy right bumper sequence for left bumper
        5 - No buttons pressed = no movement
        """
        axes = joystick.get_numaxes()
        if axes == 5: #Check to make sure it is the normal operation for xbox controller
            if joystick.get_axis(rtrigger_axis) > trigger_axis_start: #Check if right trigger has been pressed
                print("Right motors forward") #Debug line
                rtrigger_axis_value = joystick.get_axis(rtrigger_axis)
                can0.send(rmdv3.rmdv3_set_speed(rfront_id,rtrigger_axis_value,max_speed))
                can0.send(rmdv3.rmdv3_set_speed(rcen_id,rtrigger_axis_value,max_speed))
                can0.send(rmdv3.rmdv3_set_speed(rback_id,rtrigger_axis_value,max_speed))
                if joystick.get_button(lb_button):
                    can0.send(rmdv3.rmdv3_set_speed(lfront_id,-rtrigger_axis_value,max_speed))
                    can0.send(rmdv3.rmdv3_set_speed(lcen_id,-rtrigger_axis_value,max_speed))
                    can0.send(rmdv3.rmdv3_set_speed(lback_id,-rtrigger_axis_value,max_speed))
            elif joystick.get_button(rb_button):
                print("Right motors backward") #Debug line
                if joystick.get_axis(ltrigger_axis) > trigger_axis_start:
                    print("Left motors forward")
                    ltrigger_axis_value = joystick.get_axis(ltrigger_axis)
                    can0.send(rmdv3.rmdv3_set_speed(lfront_id,ltrigger_axis_value,max_speed))
                    can0.send(rmdv3.rmdv3_set_speed(lcen_id,ltrigger_axis_value,max_speed))
                    can0.send(rmdv3.rmdv3_set_speed(lback_id,ltrigger_axis_value,max_speed))

                    can0.send(rmdv3.rmdv3_set_speed(rfront_id,-ltrigger_axis_value,max_speed))
                    can0.send(rmdv3.rmdv3_set_speed(rcen_id,-ltrigger_axis_value,max_speed))
                    can0.send(rmdv3.rmdv3_set_speed(rback_id,-ltrigger_axis_value,max_speed))
                else:
                    back_speed = -0.25 #This is just arbitarily decided
                    can0.send(rmdv3.rmdv3_set_speed(rfront_id,back_speed,max_speed))
                    can0.send(rmdv3.rmdv3_set_speed(rcen_id,back_speed,max_speed))
                    can0.send(rmdv3.rmdv3_set_speed(rback_id,back_speed,max_speed))

            if joystick.get_axis(ltrigger_axis) > trigger_axis_start: #Check if right trigger has been pressed
                print("Right motors forward") #Debug line
                ltrigger_axis_value = joystick.get_axis(ltrigger_axis)
                can0.send(rmdv3.rmdv3_set_speed(lfront_id,ltrigger_axis_value,max_speed))
                can0.send(rmdv3.rmdv3_set_speed(lcen_id,ltrigger_axis_value,max_speed))
                can0.send(rmdv3.rmdv3_set_speed(lback_id,ltrigger_axis_value,max_speed))
                if joystick.get_button(rb_button):
                    can0.send(rmdv3.rmdv3_set_speed(rfront_id,-ltrigger_axis_value,max_speed))
                    can0.send(rmdv3.rmdv3_set_speed(rcen_id,-ltrigger_axis_value,max_speed))
                    can0.send(rmdv3.rmdv3_set_speed(rback_id,-ltrigger_axis_value,max_speed))
            elif joystick.get_button(lb_button):
                print("Right motors backward") #Debug line
                if joystick.get_axis(rtrigger_axis) > trigger_axis_start:
                    print("Left motors forward")
                    rtrigger_axis_value = joystick.get_axis(rtrigger_axis)
                    can0.send(rmdv3.rmdv3_set_speed(rfront_id,rtrigger_axis_value,max_speed))
                    can0.send(rmdv3.rmdv3_set_speed(rcen_id,rtrigger_axis_value,max_speed))
                    can0.send(rmdv3.rmdv3_set_speed(rback_id,rtrigger_axis_value,max_speed))

                    can0.send(rmdv3.rmdv3_set_speed(lfront_id,-rtrigger_axis_value,max_speed))
                    can0.send(rmdv3.rmdv3_set_speed(lcen_id,-rtrigger_axis_value,max_speed))
                    can0.send(rmdv3.rmdv3_set_speed(lback_id,-rtrigger_axis_value,max_speed))
                else:
                    back_speed = -0.25 #This is just arbitarily decided
                    can0.send(rmdv3.rmdv3_set_speed(lfront_id,back_speed,max_speed))
                    can0.send(rmdv3.rmdv3_set_speed(lcen_id,back_speed,max_speed))
                    can0.send(rmdv3.rmdv3_set_speed(lback_id,back_speed,max_speed))

            else:
                print("Error wrong number of joystick axes detected")

        


# for event in pygame.event.get():
#     if event.type == pygame.JOYDEVICEADDED:
#         joy = pygame.joystick.Joystick(event.device_index)
#         joysticks[joy.get_instance_id()] = joy
#         print(f"Joystick {joy.get_instance_id()} connencted")

# print(joysticks)
# for joystick in joysticks.values():
#     name = joystick.get_name()
#     print(name)

#     powerlevel = joystick.get_power_level()
#     print(powerlevel)
    
#     axes = joystick.get_numaxes()
    
#     for i in range(axes):
#         axis = joystick.get_axis(i)
#         print(f"axis {i} value: {axis:>6.3f}")

#     buttons = joystick.get_numbuttons()
#     print(f"Number of buttons: {buttons}")

#     for i in range(buttons):
#         button = joystick.get_button(i)
#         print(f"Button {i:>2} value: {button}")

#     hats = joystick.get_numhats()
#     print(f"Number of hats: {hats}")


# for joystick in joysticks.values:
#     name = joystick.get_name()
#     print(name)

pygame.quit()