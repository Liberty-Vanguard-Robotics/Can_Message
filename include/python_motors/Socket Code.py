import socket

def send_command(command):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('192.168.168.112', 65432))
    client_socket.sendall(command.encode('utf-8'))
    client_socket.close()
    print('Command Sent')

send_command('Say Hello!') 
send_command('This is working')