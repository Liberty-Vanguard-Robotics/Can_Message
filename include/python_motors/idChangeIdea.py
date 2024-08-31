import can

# Define the CAN bus interface (e.g., 'can0' on Linux)
bus = can.Bus(interface='can0', bustype='socketcan')

# Define the RMD motor's original CAN ID
original_id = 0x123  # Replace with the motor's current CAN ID

# Define the new CAN ID for the RMD motor
new_id = 0x456  # Replace with the desired new CAN ID

# Create a CAN message with the new ID
msg = can.Message(arbitration_id=new_id, data=b'')

# Send the CAN message to change the motor's ID
bus.send(msg)

# Wait for the motor to respond with an ACK (acknowledgment)
while True:
    msg = bus.recv(1)  # Wait for 1 second
    if msg.arbitration_id == original_id and msg.data == b'\x01':  # ACK received
        print("CAN ID changed successfully!")
        break

# Clean up
bus.shutdown()
