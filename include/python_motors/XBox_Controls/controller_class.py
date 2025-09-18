# The controller class
# This class is created to store the information used in the controller

class controller_class:

# VARIABLES
# The many variables regarding the controller
# the double underscore (__) is used to help keep it separate from similarly named variables outside of the class

# since (at least for the time being) I want classes to not share variables, I declare them all in the __init__ function
# This may change depending on the needs of the program
  def __init__(self):
    self.__max_speed = 0
    self.__autonomous_state = 0
    self.__speed_left = 0
    self.__speed_right = 0
    self.__hats = 0
    self.__buttons = 0
    self.__axes = 0
    self.__jid = 0
    self.__name = "0"
    self.__power_level = 0
    self.__guid = 0
    self.__joystick_count = 0
    
    # Arrays (or tuples, in the hats case)
    self.__hat = (0,0)
    self.__button = [0,0,0,0,0,0,0,0,0,0,0,0]
    self.__axis = [0,0,0,0,0,0]

    # Also arrays, but these are focused on labeling the actual controller buttons. Notably, the names in
    # the values list are in the same position as their relative button in the __button array
    self.__button_values_list = ["A","B","X","Y","LB","RB","Display Button","Three Lines Button","XBOX Symbol Button"," Left Joystick Trigger","Right Joystick Trigger","Inbox Button"]
    self.__button_role_list = ["0","0","0","0","0","0","Shutdown","Autonomous","0","0","0","0",]
    self.__axis_values_list = ["Left Joystick Horizontal","Left Joystick Vertical","Left Trigger","Right Joystick Horizontal","Right Joystick Vertical","Right Trigger"]
    self.__axis_roles_list = ["Turning","Forward Motion","0","0","0","0"]
    self.__done = False

    # Dictionary. Used to match buttons with values. It might be a bit redundant, so depending on how code cleanup 
    # goes, I may get rid of it
    self.controller = {'A': self.__button[0], 'B': self.__button[1], 'X': self.__button[2], 'Y': self.__button[3], 'LB': self.__button[4], 'RB': 
                      self.__button[5], 'Display Button': self.__button[6], 'Menu Button': self.__button[7], 'XBOX Symbol': self.__button[8],
                      'Left Joystick Trigger': self.__button[9], 'Right Joystick Trigger': self.__button[10], 'Inbox Button': self.__button[11], 
                      'Left Joystick Horizontal': self.__axis[0], 'Left Joystick Vertical': self.__axis[1], 'Left Trigger': self.__axis[2],
                        'Right Joystick Horizontal': self.__axis[3],'Right Joystick Vertical': self.__axis[4],'Right Trigger': self.__axis[5] }
    
# FUNCTIONS
# some of these functions are only used once
# However, due to their bulkiness, they've been shifted here to help condense the code in the more complex sections

# print function
#  def controllerPrint(screen, controller):
    # Insert function here. I'm out of time for today