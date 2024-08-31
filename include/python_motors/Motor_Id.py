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
    """Set the CAN ID of the motor."""
    current_can_id = 0x140 + current_id
    new_can_id_data = [0x81, new_id, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
    
    response = send_can_message(bus, current_can_id, new_can_id_data)
    if response:
        print(f"CAN ID of motor {current_id} set to {new_id}. Response: {response}")
    else:
        print(f"Failed to set CAN ID for motor {current_id}")

def stop_motor(bus, can_id):
    """Stop the motor by setting speed to 0."""
    stop_data = [0xA2, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
    response = send_can_message(bus, can_id, stop_data)
    if response:
        print(f"Motor with CAN ID {can_id - 0x140} stopped. Response:", response)
    else:
        print(f"Failed to stop motor with CAN ID {can_id - 0x140}")

def main():
    # Setup CAN interfaces
    can0 = setup_can_interface('can0')
    can1 = setup_can_interface('can1')

    # List of current and new CAN IDs for each motor
    motors = [
        {"current_id": 0x01, "new_id": 0x02},
        {"current_id": 0x03, "new_id": 0x04},
        # Add more motors as needed
    ]

    # Iterate over each motor and set the new CAN ID
    for motor in motors:
        set_motor_can_id(can0, motor["current_id"], motor["new_id"])
        time.sleep(1)  # Small delay between setting IDs for different motors

    # Optionally, stop all motors as a precaution
    for motor in motors:
        stop_motor(can0, 0x140 + motor["new_id"])

    # Shutdown CAN interfaces
    shutdown_can_interface('can0')
    shutdown_can_interface('can1')

if __name__ == "__main__":
    main()
