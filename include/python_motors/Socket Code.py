import socket
import pickle
import test2_gather #the file where the data we're sending comes from

def send_command(data):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('192.168.168.206', 65432))

    #serializes the array to be able to send
    serialized_data = pickle.dumps(data)


    client_socket.sendall(serialized_data)
    client_socket.close()
    print('Data Sent')

send_command(test2_gather.array_matrix_print) #Sending the entire array through in a single command
