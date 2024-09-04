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
    bus.send(message)
    return bus.recv(2.0)

def set_motor_can_id(bus, current_id, new_id):
    """Set the CAN ID of the motor and save it permanently."""
    current_can_id = 0x140 + current_id
    new_can_id_data = [0x81, new_id, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
    
    # Set the new CAN ID
    response = send_can_message(bus, current_can_id, new_can_id_data)
    if response:
        print(f"CAN ID of motor {current_id} set to {new_id}. Response: {response}")
    else:
        print(f"Failed to set CAN ID for motor {current_id}")
        return

    # Small delay to ensure the motor has time to process the new ID
<<<<<<< HEAD
    time.sleep(1)
=======
    time.sleep(3)
>>>>>>> 02ce51b (hi)

    # Save the new CAN ID to NVM to make it permanent
    save_command = [0x78, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
    response = send_can_message(bus, 0x140 + new_id, save_command)
    if response:
        print(f"New CAN ID {new_id} saved to motor permanently. Response: {response}")
    else:
        print(f"Failed to save new CAN ID {new_id} permanently")
    
    # Power cycle the motor to ensure the new ID is saved
    print("Power cycling the motor to apply changes...")
    shutdown_can_interface('can0')
    time.sleep(2)  # Wait for the motor to fully power down
    setup_can_interface('can0')

def main():
    # Setup CAN interface for can0
    can0 = setup_can_interface('can0')

    # Define current CAN ID and desired new CAN ID
    current_id = 0x01  # Replace this with your current motor CAN ID
    new_id = 0x05      # New CAN ID that you want to set

    # Set the new CAN ID permanently
    set_motor_can_id(can0, current_id, new_id)

    # Shutdown CAN interface
    shutdown_can_interface('can0')

if __name__ == "__main__":
    main()
