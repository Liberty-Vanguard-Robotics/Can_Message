import socket
import pickle

def send_command(data):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('192.168.168.206', 65432))

    #serializes the array to be able to send
    serialized_data = pickle.dumps(data)


    client_socket.sendall(serialized_data)
    client_socket.close()
    print('Data Sent')

array = [0,4,2,1]
send_command(array) 
