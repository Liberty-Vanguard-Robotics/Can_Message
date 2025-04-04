import os
import sys
import pygame
#import rmdv3
#import can

#can0 = can.interface.Bus(channel= 'can0', bustype = 'socketcan')
#can1 = can.interface.Bus(channel= 'can1', bustype = 'socketcan')

pygame.init()


# This is a simple class that will help us print to the screen.
# It has nothing to do with the joysticks, just outputting the
# information.
class TextPrint:
    def __init__(self):
        self.reset()
        self.font = pygame.font.Font(None, 25)

    def tprint(self, screen, text):
        text_bitmap = self.font.render(text, True, (0, 0, 0))
        screen.blit(text_bitmap, (self.x, self.y))
        self.y += self.line_height

    def reset(self):
        self.x = 10
        self.y = 10
        self.line_height = 15

    def indent(self):
        self.x += 10

    def unindent(self):
        self.x -= 10


def main():
    # Set the width and height of the screen (width, height), and name the window.
    screen = pygame.display.set_mode((500, 700))
    pygame.display.set_caption("Joystick example")

    # Used to manage how fast the screen updates.
    clock = pygame.time.Clock()

    # Get ready to print.
    text_print = TextPrint()

    # This dict can be left as-is, since pygame will generate a
    # pygame.JOYDEVICEADDED event for every joystick connected
    # at the start of the program.
    joysticks = {}

    # Set of variables and lists used to print the proper names or gather important data and button states
    max_speed = 10
    autonomous_state = 0
    speed_left = 0
    speed_right = 0
    hats = 0
    buttons = 0
    axes = 0
    jid = 0
    name = "0"
    power_level = 0
    guid = 0
    joystick_count = 0
    #Arrays
    hat = (0,0)
    button = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    axis = [0,0,0,0,0,0]
    #Lists
    button_values_list = ["A","B","X","Y","LB","RB","Display Button","Three Lines Button","XBOX Symbol Button"," Left Joystick Trigger","Right Joystick Trigger","Inbox Button","0","0","0","0"]
    button_role_list = ["0","0","0","0","0","0","Shutdown","Autonomous","0","0","0","0","0","0","0","0"]
    axis_values_list = ["Left Joystick Horizontal","Left Joystick Vertical","Left Trigger","Right Joystick Horizontal","Right Joystick Vertical","Right Trigger"]
    axis_roles_list = ["Turning","Forward Motion","0","0","0","0"]
    #can motor ID's
 #   rfront_id = 0x141
 #   rcen_id = 0x141
 #   rback_id = 0x141
 #   lfront_id = 0x141
 #   lcen_id = 0x141
 #   lback_id = 0x141

    done = False
    while not done:
        # Event processing step.
        # Possible joystick events: JOYAXISMOTION, JOYBALLMOTION, JOYBUTTONDOWN,
        # JOYBUTTONUP, JOYHATMOTION, JOYDEVICEADDED, JOYDEVICEREMOVED

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True  # Flag that we are done so we exit this loop.
            if event.type == pygame.JOYBUTTONDOWN:
                print(f"Joystick button {button_values_list[event.button]} pressed.")
                if event.button == 0:
                    joystick = joysticks[event.instance_id]
                    if joystick.rumble(0, 0.7, 500):
                        print(f"Rumble effect played on joystick {event.instance_id}")

            if event.type == pygame.JOYBUTTONUP:
                print(f"Joystick button {button_values_list[event.button]}  released.")

            # Handle hotplugging
            if event.type == pygame.JOYDEVICEADDED:
                # This event will be generated when the program starts for every
                # joystick, filling up the list without needing to create them manually.
                joy = pygame.joystick.Joystick(event.device_index)
                joysticks[joy.get_instance_id()] = joy
                print(f"Joystick {joy.get_instance_id()} connencted")

            if event.type == pygame.JOYDEVICEREMOVED:
                del joysticks[event.instance_id]
                print(f"Joystick {event.instance_id} disconnected")

        # Drawing step
        # First, clear the screen to white. Don't put other drawing commands
        # above this, or they will be erased with this command.
        
        screen.fill((255, 255, 255))
        text_print.reset()

        # Get count of joysticks.
        joystick_count = pygame.joystick.get_count()

        text_print.tprint(screen, f"Number of joysticks: {joystick_count}")
        text_print.indent()

        # For each joystick:
        for joystick in joysticks.values():
            jid = joystick.get_instance_id()

            text_print.tprint(screen, f"Joystick {jid}")
            text_print.indent()

            # Get the name from the OS for the controller/joystick.
            name = joystick.get_name()
            text_print.tprint(screen, f"Joystick name: {name}")

            guid = joystick.get_guid()
            text_print.tprint(screen, f"GUID: {guid}")

            power_level = joystick.get_power_level()
            text_print.tprint(screen, f"Joystick's power level: {power_level}")

            # Usually axis run in pairs, up/down for one, and left/right for
            # the other. Triggers count as axes.
            axes = joystick.get_numaxes()
            text_print.tprint(screen, f"Number of axes: {axes}")
            text_print.indent()

            for i in range(axes):
                axis[i] = joystick.get_axis(i)
                text_print.tprint(screen, f"Axis {i} value: {axis[i]:>6.3f}")

            speed_left = (axis[1] + axis[0])*max_speed
            speed_right = (axis[1] - axis[0])*max_speed
            text_print.tprint(screen, f"Left Side Speed = {speed_left:>6.3f}")
            text_print.tprint(screen, f"Right Side Speed = {speed_right:>6.3f}")

            text_print.unindent()

            buttons = joystick.get_numbuttons()
            text_print.tprint(screen, f"Number of buttons: {buttons}")
            text_print.indent()

            for i in range(buttons):
                button[i] = joystick.get_button(i)
                if button[i] == 0:
                    text_print.tprint(screen, f"Button {button_values_list[i]} ({button_role_list[i]}) value: OFF")
                else:
                    text_print.tprint(screen, f"Button {button_values_list[i]} ({button_role_list[i]}) value: ON")

                if button[7] == 1:
                    autonomous_state = 1
                else:
                    autonomous_state = 0

                if button[6] == 1:
                    pygame.quit()
                    sys.exit()

            text_print.unindent()

            hats = joystick.get_numhats()
            text_print.tprint(screen, f"Number of hats: {hats}")
            text_print.indent()

            # Hat position. All or nothing for direction, not a float like
            # get_axis(). Position is a tuple of int values (x, y).

            for i in range(hats):
                hat = joystick.get_hat(i)
                text_print.tprint(screen, f"Hat {i} value: {str(hat)}")
                if hat == (0,1):
                    max_speed = max_speed + 1
                elif hat == (0,-1):
                    max_speed = max_speed - 1 
            text_print.unindent()

            text_print.unindent()

            # Misc. important data
            text_print.tprint(screen, f"Maximum speed: {max_speed}")
            
            if autonomous_state == 0:  
                text_print.tprint(screen, f"Autonomous State: OFF")
            else:
                text_print.tprint(screen, f"Autonomous State: ON")
#            can0.send(rmdv3.rmdv3_set_speed(rfront_id,1,speed_left,1))
#            can0.send(rmdv3.rmdv3_set_speed(rcen_id,1,speed_left,1))
#            can0.send(rmdv3.rmdv3_set_speed(rback_id,1,speed_left,1))
#            can1.send(rmdv3.rmdv3_set_speed(lfront_id,1,speed_right,1))
#            can1.send(rmdv3.rmdv3_set_speed(lcen_id,1,speed_right,1))
#            can1.send(rmdv3.rmdv3_set_speed(lback_id,1,speed_right,1))
        # Go ahead and update the screen with what we've drawn.
        pygame.display.flip()

        # Limit to 30 frames per second.
        clock.tick(30)


if __name__ == "__main__":
    main()
    # If you forget this line, the program will 'hang'
    # on exit if running from IDLE.
    pygame.quit()