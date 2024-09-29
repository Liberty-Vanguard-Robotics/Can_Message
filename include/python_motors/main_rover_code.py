import time
import os
import pygamimport rmdv3
import can

def setup_can_interface(channel, bitrate=1000000):
    """
    Sets up the CAN interface for communication.
    
    Parameters:
    - channel: The name of the CAN interface (e.g., 'can0', 'can1').
    - bitrate: The bitrate for the CAN interface, default is 1000000 bps.
    
    Returns:
    - bus: The CAN bus interface for sending/receiving messages.
    """
    os.system(f'sudo ip link set {channel} type can bitrate {bitrate}')
    os.system(f'sudo ifconfig {channel} up')
    os.system(f'sudo ifconfig {channel} txqueuelen 1000')
    return can.interface.Bus(channel=channel, bustype='socketcan')

def set_motor_speed(bus, motor_id, speed, max_speed):
    """
    Sends a CAN message to set the speed of a motor.

    Parameters:
    - bus: The CAN bus interface to use.
    - motor_id: The ID of the motor to control.
    - speed: The desired speed for the motor.
    - max_speed: The maximum allowable speed for the motor.
    """
    try:
        bus.send(rmdv3.rmdv3_set_speed(motor_id, speed, max_speed))
    except can.CanError as e:
        print(f"Failed to send CAN message to motor {motor_id}: {e}")

# Set up CAN interfaces for communication with the motors
can0 = setup_can_interface('can0')
can1 = setup_can_interface('can1')

# Initialize pygame to handle joystick input
pygame.init()
joystickcount = pygame.joystick.get_count()
print(f"The number of joysticks detected is {joystickcount}")

joysticks = {}

# Define joystick axes and button mappings for Xbox Series X controller
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

# Motor IDs for the rover's motors; these can be changed as needed
rfront_id = 0x141
rcen_id = 0x141
rback_id = 0x141
lfront_id = 0x141
lcen_id = 0x141
lback_id = 0x141

# Manually setting the maximum speed for the motors (in degrees per second)
max_speed = 16000 # This translates to 80 degrees per second (dps)

# Initial trigger and button states for reference
trigger_axis_start = -1
button_start = 0

# Boolean flags to track the state of triggers and bumpers
rtrigger_bool = 0
ltrigger_bool = 0
rb_bool = 0
lb_bool = 0

done = 1
while done:
    for event in pygame.event.get():
        if event.type == pygame.JOYDEVICEREMOVED:
            done = 0
        if event.type == pygame.JOYDEVICEADDED:
            joy = pygame.joystick.Joystick(event.device_index)
            joysticks[joy.get_instance_id()] = joy
            print(f"Joystick {joy.get_instance_id()} connected")
        if event.type == pygame.JOYDEVICEREMOVED:
            del joysticks[event.instance_id]
            print(f"Joystick {event.instance_id} disconnected")
        
    for joystick in joysticks.values():
        """
        The following logic is responsible for controlling the movement of the rover.
        It handles forward, backward, and spinning motions based on the input from the joystick.
        """
        axes = joystick.get_numaxes()
        if axes > 1: # Check to ensure it's a valid Xbox controller
            # Right trigger pressed: Move right motors forward
            if (joystick.get_axis(rtrigger_axis) > trigger_axis_start) & (rtrigger_bool == 0):
                rtrigger_bool = 1
                print("Right motors forward") # Debugging output
                rtrigger_axis_value = joystick.get_axis(rtrigger_axis)
                can0.send(rmdv3.rmdv3_set_speed(rfront_id, rtrigger_axis_value, max_speed))
                can0.send(rmdv3.rmdv3_set_speed(rcen_id, rtrigger_axis_value, max_speed))
                can0.send(rmdv3.rmdv3_set_speed(rback_id, rtrigger_axis_value, max_speed))
                # If the left bumper is pressed, move left motors in the opposite direction
                if joystick.get_button(lb_button):
                    can1.send(rmdv3.rmdv3_set_speed(lfront_id, -((rtrigger_axis_value + 1) / 2), max_speed, button_start))
                    can1.send(rmdv3.rmdv3_set_speed(lcen_id, -((rtrigger_axis_value + 1) / 2), max_speed, button_start))
                    can1.send(rmdv3.rmdv3_set_speed(lback_id, -((rtrigger_axis_value + 1) / 2), max_speed, button_start))
            # Right bumper pressed: Move right motors backward
            elif (joystick.get_button(rb_button)) & (rb_bool == 0):
                print("Right motors backward") # Debugging output
                rb_bool = 1
                if joystick.get_axis(ltrigger_axis) > trigger_axis_start:
                    print("Left motors forward")
                    ltrigger_axis_value = joystick.get_axis(ltrigger_axis)
                    can1.send(rmdv3.rmdv3_set_speed(lfront_id, ltrigger_axis_value, max_speed))
                    can1.send(rmdv3.rmdv3_set_speed(lcen_id, ltrigger_axis_value, max_speed))
                    can1.send(rmdv3.rmdv3_set_speed(lback_id, ltrigger_axis_value, max_speed))

                    can0.send(rmdv3.rmdv3_set_speed(rfront_id, -((ltrigger_axis_value + 1) / 2), max_speed, button_start))
                    can0.send(rmdv3.rmdv3_set_speed(rcen_id, -((ltrigger_axis_value + 1) / 2), max_speed, button_start))
                    can0.send(rmdv3.rmdv3_set_speed(rback_id, -((ltrigger_axis_value + 1) / 2), max_speed, button_start))
                else:
                    back_speed = -0.75 # Arbitrary speed value
                    can0.send(rmdv3.rmdv3_set_speed(rfront_id, back_speed, max_speed, button_start))
                    can0.send(rmdv3.rmdv3_set_speed(rcen_id, back_speed, max_speed, button_start))
                    can0.send(rmdv3.rmdv3_set_speed(rback_id, back_speed, max_speed, button_start))

            # Stop right motors when right trigger and bumper are released
            if (joystick.get_axis(rtrigger_axis) == trigger_axis_start) & ((rtrigger_bool == 1) | (rb_bool == 1)) & (joystick.get_button(rb_button) == 0):
                rtrigger_bool = 0
                rb_bool = 0
                print("Right motors stop") # Debugging output
                can0.send(rmdv3.rmdv3_set_speed(rfront_id, -1, max_speed))
                can0.send(rmdv3.rmdv3_set_speed(rcen_id, -1, max_speed))
                can0.send(rmdv3.rmdv3_set_speed(rback_id, -1, max_speed))

            # Stop left motors when left trigger and bumper are released
            if (joystick.get_axis(ltrigger_axis) == trigger_axis_start) & ((ltrigger_bool == 1) | (lb_bool == 1)) & (joystick.get_button(lb_button) == 0):
                ltrigger_bool = 0
                lb_bool = 0
                print("Left motors stop") # Debugging output
                can1.send(rmdv3.rmdv3_set_speed(lfront_id, -1, max_speed))
                can1.send(rmdv3.rmdv3_set_speed(lcen_id, -1, max_speed))
                can1.send(rmdv3.rmdv3_set_speed(lback_id, -1, max_speed))

            # Left trigger pressed: Move left motors forward
            if (joystick.get_axis(ltrigger_axis) > trigger_axis_start) & (ltrigger_bool == 0):
                print("Left motors forward") # Debugging output
                ltrigger_bool = 1
                ltrigger_axis_value = joystick.get_axis(ltrigger_axis)
                print(ltrigger_axis_value)
                can1.send(rmdv3.rmdv3_set_speed(lfront_id, ltrigger_axis_value, max_speed))
                can1.send(rmdv3.rmdv3_set_speed(lcen_id, ltrigger_axis_value, max_speed))
                can1.send(rmdv3.rmdv3_set_speed(lback_id, ltrigger_axis_value, max_speed))
                # If the right bumper is pressed, move right motors in the opposite direction
                if joystick.get_button(rb_button):
                    can0.send(rmdv3.rmdv3_set_speed(rfront_id, -((ltrigger_axis_value + 1) / 2), max_speed, button_start))
                    can0.send(rmdv3.rmdv3_set_speed(rcen_id, -((ltrigger_axis_value + 1) / 2), max_speed, button_start))
                    can0.send(rmdv3.rmdv3_set_speed(rback_id, -((ltrigger_axis_value + 1) / 2), max_speed, button_start))
            # Left bumper pressed: Move left motors backward
            elif (joystick.get_button(lb_button)) & (lb_bool == 0):
                print("Left motors backward") # Debugging output
                lb_bool = 1
                if joystick.get_axis(rtrigger_axis) > trigger_axis_start:
                    print("Right motors forward")
                    rtrigger_axis_value = joystick.get_axis(rtrigger_axis)
                    can0.send(rmdv3.rmdv3_set_speed(rfront_id, rtrigger_axis_value, max_speed))
                    can0.send(rmdv3.rmdv3_set_speed(rcen_id, rtrigger_axis_value, max_speed))
                    can0.send(rmdv3.rmdv3_set_speed(rback_id, rtrigger_axis_value, max_speed))

                    can1.send(rmdv3.rmdv3_set_speed(lfront_id, -((rtrigger_axis_value + 1) / 2), max_speed, button_start))
                    can1.send(rmdv3.rmdv3_set_speed(lcen_id, -((rtrigger_axis_value + 1) / 2), max_speed, button_start))
                    can1.send(rmdv3.rmdv3_set_speed(lback_id, -((rtrigger_axis_value + 1) / 2), max_speed, button_start))
                else:
                    back_speed = -0.75 # Arbitrary speed value
                    can1.send(rmdv3.rmdv3_set_speed(lfront_id, back_speed, max_speed, button_start))
                    can1.send(rmdv3.rmdv3_set_speed(lcen_id, back_speed, max_speed, button_start))
                    can1.send(rmdv3.rmdv3_set_speed(lback_id, back_speed, max_speed, button_start))

            time.sleep(0.5) # Add a short delay to prevent overwhelming the system with commands

# Clean up by shutting down the CAN interfaces
pygame.quit()
os.system('sudo ifconfig can0 down')
os.system('sudo ifconfig can1 down')
