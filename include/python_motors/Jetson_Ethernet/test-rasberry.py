import socket
import pickle
# Set up the server (Raspberry Pi)
HOST = '0.0.0.0'  # Listen on all available interfaces
PORT = 12345       # Port to listen on (use a port number > 1024)
BUFFER_SIZE = 1024 # Size of the buffer for receiving data

# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the IP and port PORT and HOST are grouped together
server_socket.bind((HOST,PORT))
# the main code that loops 
while True:

    # Listen for incoming connections (max 1 connection in this case)
    server_socket.listen(1)
    print(f"Listening for connections on {HOST}:{PORT}...")
    (HOST, PORT)
    # Accept an incoming connection
    conn, addr = server_socket.accept()
    print(f"Connected by {addr}")

    # Keep receiving data until connection is closed
    while True:
        data = conn.recv(BUFFER_SIZE)
        if not data:
            break
        print(f"Received data: {data.decode()}")
        
        # Send a response back
        conn.sendall(b"Data received!")

    # Close the connection
    conn.close()