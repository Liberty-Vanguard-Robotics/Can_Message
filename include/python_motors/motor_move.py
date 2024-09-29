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
        print(f"Sent message: {message}")
        response = bus.recv(2.0)
        if response:
            print(f"Received response: {response}")
        return response
    except can.CanError as e:
        print(f"CAN Error: {e}")
        return None

def change_motor_id(bus, current_can_id, new_can_id):
    """Change the motor's CAN ID permanently."""
    # The command to change CAN ID is usually 0x79, followed by the new CAN ID in the data bytes
    # Adjust the data structure based on your motor's protocol documentation
    change_id_data = [0x80, 0x00, 0x00, 0x00, new_can_id & 0xFF, 0x00, 0x00, 0x00]

    response = send_can_message(bus, current_can_id, change_id_data)
    if response:
        print(f"Motor CAN ID changed from {current_can_id - 0x140} to {new_can_id - 0x140}. Response: {response}")
    else:
        print(f"Failed to change motor CAN ID from {current_can_id - 0x140} to {new_can_id - 0x140}")

def test_new_motor_id(bus, new_can_id):
    """Test if the motor responds to the new CAN ID."""
    # Send a simple velocity command or status request to verify the new CAN ID
    test_data = [0xA2, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]

    response = send_can_message(bus, new_can_id, test_data)
    if response:
        print(f"Motor with new CAN ID {new_can_id - 0x140} is responding. Response: {response}")
    else:
        print(f"Motor with new CAN ID {new_can_id - 0x140} is not responding.")

def main():
    # Setup CAN interface for can0
    can0 = setup_can_interface('can0')

    try:
        # Define the current CAN ID of the motor
        current_motor_id = 0x141  # Replace with the current CAN ID of your motor (e.g., 0x141 for CAN ID 1)
        current_can_id = 0x000 + current_motor_id

        # Define the new CAN ID you want to assign to the motor
        new_motor_id = 0x142  # Replace this with the new CAN ID you want (e.g., 0x142 for CAN ID 2)
        new_can_id = 0x000 + new_motor_id

        # Change the motor's CAN ID permanently
        change_motor_id(can0, current_can_id, new_can_id)

        # Shutdown the CAN interface to reinitialize it after power cycling the motor
        shutdown_can_interface('can0')

        # Prompt the user to manually power cycle the motor
        print("Please power cycle the motor now (turn it off and then on again).")
        input("After power cycling the motor, press Enter to continue...")

        # Reinitialize CAN interface for can0
        can0 = setup_can_interface('can0')

        # Test communication with the new CAN ID
        test_new_motor_id(can0, new_can_id)
        test_new_motor_id(can0, 0x141)


    finally:
        # Shutdown CAN interface after usage
        shutdown_can_interface('can0')

if __name__ == "__main__":
    main()
