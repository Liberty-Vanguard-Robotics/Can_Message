import pygame

pygame.init()

def main():
    # Used to manage how fast the screen updates.
    clock = pygame.time.Clock()

    # This dict can be left as-is, since pygame will generate a
    # pygame.JOYDEVICEADDED event for every joystick connected
    # at the start of the program.
    joysticks = {}

    # Set of variables and lists used to print the proper names or gather important data and button states
    max_speed = 0
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
    hat = (0, 0)
    button_values_list = ["A", "B", "X", "Y", "LB", "RB", "Display Button", "Three Lines Button",
                          "XBOX Symbol Button", "Left Joystick Trigger", "Right Joystick Trigger", "Inbox Button"]
    button_role_list = ["0", "0", "0", "0", "0", "0", "Shutdown", "Autonomous", "0", "0", "0", "0"]
    axis_values_list = ["Left Joystick Horizontal", "Left Joystick Vertical", "Left Trigger",
                        "Right Joystick Horizontal", "Right Joystick Vertical", "Right Trigger"]
    axis_roles_list = ["Turning", "Forward Motion", "0", "0", "0", "0"]
    array_matrix_print = []
    done = False

    while not done:
        # Event processing step.
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
                print(f"Joystick button {button_values_list[event.button]} released.")

            # Handle hotplugging
            if event.type == pygame.JOYDEVICEADDED:
                joy = pygame.joystick.Joystick(event.device_index)
                joysticks[joy.get_instance_id()] = joy
                print(f"Joystick {joy.get_instance_id()} connected")

            if event.type == pygame.JOYDEVICEREMOVED:
                del joysticks[event.instance_id]
                print(f"Joystick {event.instance_id} disconnected")

        # Get count of joysticks.
        joystick_count = pygame.joystick.get_count()

        # For each joystick:
        for joystick in joysticks.values():
            jid = joystick.get_instance_id()
            name = joystick.get_name()  # Get the name from the OS for the controller/joystick.
            guid = joystick.get_guid()
            power_level = joystick.get_power_level()

            # Get number of axes and initialize axis list
            axes = joystick.get_numaxes()
            axis = [0] * axes  # Initialize axis list dynamically

            for i in range(axes):
                axis[i] = joystick.get_axis(i)

            speed_left = (axis[1] + axis[0]) * max_speed
            speed_right = (axis[1] - axis[0]) * max_speed

            # Get number of buttons and initialize button list
            buttons = joystick.get_numbuttons()
            button = [0] * buttons  # Initialize button list dynamically

            for i in range(buttons):
                button[i] = joystick.get_button(i)

            # Check specific button conditions
            if buttons >= 8:
                if button[7] == 1:
                    autonomous_state = 1
                else:
                    autonomous_state = 0

                if button[6] == 1:
                    pygame.quit()
                    exit()  # Ensure the program exits

            # Get number of hats
            hats = joystick.get_numhats()

            for i in range(hats):
                hat = joystick.get_hat(i)
                if hat == (0, 1):
                    max_speed = max_speed + 1
                elif hat == (0, -1):
                    max_speed = max_speed - 1

        static_value_print = [hats, buttons, axes, jid, name, power_level, guid, joystick_count]
        variable_value_print = [max_speed, autonomous_state, speed_left, speed_right]
        array_matrix_print = [static_value_print, variable_value_print, hat, button, axis]
        return array_matrix_print
    
        # Limit to 30 frames per second.
        clock.tick(30)


if __name__ == "__main__":
    array_matrix_print = main()
    # If you forget this line, the program will 'hang'
    # on exit if running from IDLE.
    pygame.quit()
