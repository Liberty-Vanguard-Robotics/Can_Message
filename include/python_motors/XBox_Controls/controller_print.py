import pygame
import Socket_Code_2
import controller_class
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

    control = controller_class()
    control = Socket_Code_2.control

    done = False
    while not done:

        # Drawing step
        # First, clear the screen to white. Don't put other drawing commands
        # above this, or they will be erased with this command.
        
        # This section creates the screen. Put this into the separate code
        screen.fill((255, 255, 255))
        text_print.reset()

        text_print.tprint(screen, f"Number of joysticks: {control.__joystick_count}")
        text_print.indent()

        # For each joystick:
        for joystick in joysticks.values():
            text_print.tprint(screen, f"Joystick {control.__jid}")
            text_print.indent()
            text_print.tprint(screen, f"Joystick name: {control.__name}")
            text_print.tprint(screen, f"GUID: {control.__guid}")
            text_print.tprint(screen, f"Joystick's power level: {control.__power_level}")
            text_print.tprint(screen, f"Number of axes: {control.__axes}")
            text_print.indent()

            for i in range(control.__axes):
                text_print.tprint(screen, f"Axis {i} value: {control.__axis[i]:>6.3f}")

            text_print.tprint(screen, f"Left Side Speed = {control.__speed_left:>6.3f}")
            text_print.tprint(screen, f"Right Side Speed = {control.__speed_right:>6.3f}")

            text_print.unindent()
            text_print.tprint(screen, f"Number of buttons: {control.__buttons}")
            text_print.indent()

            # loop through each button and print to the screen
            for i in range(control.__buttons):
                if control.__button[i] == 0:
                    text_print.tprint(screen, f"Button {control.__button_values_list[i]} ({control.__button_role_list[i]}) value: OFF")
                else:
                    text_print.tprint(screen, f"Button {control.__button_values_list[i]} ({control.__button_role_list[i]}) value: ON")
                if control.__button[6] == 1:
                    pygame.quit() # The only "functionality" code in the print system, the shut down the code
                    # in both the computer and the pi simultaneously

            text_print.unindent()
            text_print.tprint(screen, f"Number of hats: {control.__hats}")
            text_print.indent()

            # Hat position. All or nothing for direction, not a float like
            # get_axis(). Position is a tuple of int values (x, y).

            for i in range(control.__hats):
                text_print.tprint(screen, f"Hat {i} value: {str(control.__hat)}")
            text_print.unindent()

            text_print.unindent()

            # Misc. important data
            text_print.tprint(screen, f"Maximum speed: {control.__max_speed}")
            
            if control.__autonomous_state == 0:  
                text_print.tprint(screen, f"Autonomous State: OFF")
            else:
                text_print.tprint(screen, f"Autonomous State: ON")

        # Go ahead and update the screen with what we've drawn.
        pygame.display.flip()

        # Limit to 30 frames per second.
        clock.tick(30)


if __name__ == "__main__":
    main()
    # If you forget this line, the program will 'hang'
    # on exit if running from IDLE.
    pygame.quit()