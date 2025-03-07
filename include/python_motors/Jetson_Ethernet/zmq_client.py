#This represents the Rasberry Pi
# pip install pyzmq

import zmq

# Set up the server (Raspberry Pi)
context = zmq.Context()
socket = context.socket(zmq.REP)  # REP (reply) socket type
socket.bind("tcp://*:5555")  # Bind to a port (e.g., 5555)

while True:
    # Receive a message from the client
    message = socket.recv_string()
    print(f"Received: {message}")

    # Send a reply to the client
    socket.send_string("Data received!")
