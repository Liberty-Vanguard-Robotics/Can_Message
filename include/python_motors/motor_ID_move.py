import os
import can
import time

def setup_can_interface(channel, bitrate=1000000):
    """Set up the CAN interface with the specified bitrate."""
    os.system(f'sudo ip link set {channel} type can bitrate {bitrate}')
    os.system(f'sudo ifconfig {channel} up')
    return can.interface.Bus(channel=channel, bustype='socketcan')

def shutdown_can_interface(channel):
    """Shut down the CAN interface."""
    os.system(f'sudo ifconfig {channel} down')

def send_can_message(bus, arbitration_id, data):
    """Send a CAN message and receive the response."""
    message = can.Message(is_extended_id=False, arbitration_id=arbitration_id, data=data)
    try:
        bus.send(message)
        response = bus.recv(2.0)
        return response
    except can.CanError as e:
        print(f"CAN Error: {e}")
        return None

def turn_on_motor(bus, can_id):
    """Turn on the motor by sending a specific command."""
    # Assuming 'turn on' means setting a non-zero speed or torque.
    # You can replace the data array with the correct command for your specific motor.
    turn_on_data = [0xA2, 0x00, 0x00, 0x00, 0x27, 0x10, 0x00, 0x00]  # Example data to turn on the motor
    
    response = send_can_message(bus, can_id, turn_on_data)
    if response:
        print(f"Motor with CAN ID {can_id - 0x140} turned on. Response: {response}")
    else:
        print(f"Failed to turn on motor with CAN ID {can_id - 0x140}")

def main():
    # Setup CAN interface for can0
    can0 = setup_can_interface('can0')

    # Define the CAN ID of the motor you want to turn on
    motor_id = 0x05  # Replace this with the correct CAN ID of your motor
    can_id = 0x140 + motor_id  # Calculate the CAN ID with the base offset

    # Turn on the motor
    turn_on_motor(can0, can_id)

    # Optionally, you might want to keep the interface open or close it after the command
    # shutdown_can_interface('can0')

if __name__ == "__main__":
    main()
