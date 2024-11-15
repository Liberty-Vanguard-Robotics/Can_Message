import socket  # This is now safe to use as we're not importing our own script named `socket`
import pickle
import test3_gather  # Import your module with the data

def send_command(data):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('192.168.168.206', 65432))

    # Serialize the array to send
    serialized_data = pickle.dumps(data)

    client_socket.sendall(serialized_data)
    client_socket.close()
    print('Data Sent')

# Ensure `array_matrix_print` is properly defined in `test3_gather.py`
data_to_send = test3_gather.main()  # If `main()` returns `array_matrix_print`
send_command(data_to_send)  # Sending the array through in a single command
