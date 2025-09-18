import socket
# GABRIEL MOCK: imported the controller class
import include.python_motors.XBox_Controls.controller_class as controller_class

# GABRIEL MOCK: Changed printing array (commented out below) to an object of the controller class
#printing_array = [] #Establishing the variable I'm importing
control = controller_class()
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
	# GABRIEL MOCK: Changed printing array (commented out below) to the object of the controller class that was created earlier
	#printing_array = data #Assigning the recieved value to the variable I'm going to import
	control = data
