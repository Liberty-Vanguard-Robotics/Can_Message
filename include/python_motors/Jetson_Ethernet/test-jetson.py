# This code represents the Jetson Nano sending information to the Rasberry Pi
import socket
import pickle

# Set up the rasberry pi connection information 
HOST = '192.168.1.207'  # Raspberry Pi's IP address
PORT = 12345            # Port used by the server

# Create a socket object
jetson_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server (Raspberry Pi)
jetson_socket.connect((HOST, PORT))

# Send data to the server
message = 4.12345
data = {'y-axis': .5, 'x-axis': .23, 'max_speed': 160000}
jetson_socket.sendall(pickle.dumps(data))

# Receive response from the server
data = jetson_socket.recv(1024)
print(f"Received from server: {data.decode()}")

# Close the connection
jetson_socket.close()