# This code represents the Jetson Nano sending information to the Rasberry Pi
import socket

# Set up the client (Linux computer)
HOST = '192.168.1.100'  # Raspberry Pi's IP address
PORT = 12345            # Port used by the server

# Create a socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server (Raspberry Pi)
client_socket.connect((HOST, PORT))

# Send data to the server
message = "Hello from the Linux computer!"
client_socket.sendall(message.encode())

# Receive response from the server
data = client_socket.recv(1024)
print(f"Received from server: {data.decode()}")

# Close the connection
client_socket.close()
