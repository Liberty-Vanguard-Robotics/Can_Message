# THis represents the Jetson Nano. Will send information to the Rasberry PI
import zmq

# Set up the client (Linux computer)
context = zmq.Context()
socket = context.socket(zmq.REQ)  # REQ (request) socket type
socket.connect("tcp://192.168.1.100:5555")  # Connect to the Raspberry Pi's IP and port

# Send a message to the server
socket.send_string("Hello from the Linux computer!")

# Receive the response from the server
message = socket.recv_string()
print(f"Response from server: {message}")
