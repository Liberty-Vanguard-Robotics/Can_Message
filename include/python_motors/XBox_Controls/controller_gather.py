import pygame
import controller_class
pygame.init()

def main():
    # Used to manage how fast the screen updates.
    clock = pygame.time.Clock()

    # This dict can be left as-is, since pygame will generate a
    # pygame.JOYDEVICEADDED event for every joystick connected
    # at the start of the program.
    joysticks = {}

    # Set of variables and lists used to print the proper names or gather important data and button states
    control = controller_class()

    done = False
    while not done:
        # Event processing step.
        # Possible joystick events: JOYAXISMOTION, JOYBALLMOTION, JOYBUTTONDOWN,
        # JOYBUTTONUP, JOYHATMOTION, JOYDEVICEADDED, JOYDEVICEREMOVED

        # This section connects the controller and verifies that something happens through the terminal. It will stay here in it's entirety
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True  # Flag that we are done so we exit this loop.
            if event.type == pygame.JOYBUTTONDOWN:
                print(f"Joystick button {control.__button_values_list[event.button]} pressed.")
                if event.button == 0:
                    joystick = joysticks[event.instance_id]
                    if joystick.rumble(0, 0.7, 500):
                        print(f"Rumble effect played on joystick {event.instance_id}")

            if event.type == pygame.JOYBUTTONUP:
                print(f"Joystick button {control.__button_values_list[event.button]}  released.")

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

        # Get count of joysticks.
        control.__joystick_count = pygame.joystick.get_count()

        # For each joystick:
        for joystick in joysticks.values():
            control.__jid = joystick.get_instance_id()
            control.__name = joystick.get_name()
            control.__guid = joystick.get_guid() 
            control.__power_level = joystick.get_power_level()
 
            # Usually axis run in pairs, up/down for one, and left/right for
            # the other. Triggers count as axes.
            axes = joystick.get_numaxes()

            for i in range(axes):
                control.__axis[i] = joystick.get_axis(i)
                
            control.__speed_left = (control.__axis[1] + control.__axis[0])*max_speed
            control.__speed_right = (control.__axis[1] - control.__axis[0])*max_speed
            
            buttons = joystick.get_numbuttons()
           
            for i in range(buttons):
                control.__button[i] = joystick.get_button(i)
                
                if control.__button[7] == 1:
                    control.__autonomous_state = 1
                else:
                    control.__autonomous_state = 0

                if control.__button[6] == 1:
                    pygame.quit()

            hats = joystick.get_numhats()
           
            # Hat position. All or nothing for direction, not a float like
            # get_axis(). Position is a tuple of int values (x, y).

            for i in range(hats):
                hat = joystick.get_hat(i)
                if hat == (0,1):
                    max_speed = max_speed + 1
                elif hat == (0,-1):
                    max_speed = max_speed - 1 

        clock.tick(30)

        return control

if __name__ == "__main__":
    main()
    # If you forget this line, the program will 'hang'
    # on exit if running from IDLE.
    pygame.quit()