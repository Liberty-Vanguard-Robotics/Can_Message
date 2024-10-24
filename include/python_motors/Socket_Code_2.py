import socket

def execute_command(command):
	
	print(f"Exectuting Commands: {command}")

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('0.0.0.0', 65432))
server_socket.listen(1)

print("Server is listening for connections")

while True:
	client_socket, addr = server_socket.accept()
	#print(f"Conection from {addr}")
	data = client_socket.recv(1024).decode('utf-8')
	if data:
		execute_command(data)
	client_socket.close()
