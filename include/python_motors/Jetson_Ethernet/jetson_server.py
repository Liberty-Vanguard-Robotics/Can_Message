import paramiko

# Define Raspberry Pi credentials and IP address
hostname = 'raspberrypi.local'  # Or use the IP address, e.g., '192.168.1.100'
port = 22  # Default SSH port
username = 'pi'  # Default username
password = 'raspberry'  # Default password (or use SSH key for authentication)

# The Python code you want to execute on the Raspberry Pi
python_code = """
import time

# Simple code to print "Hello, World!" every second
for i in range(5):
    print(f'Hello, World! {i+1}')
    time.sleep(1)
"""

# Create a paramiko SSH client
client = paramiko.SSHClient()

# Automatically add the Raspberry Pi's SSH key if it's not known
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

try:
    # Connect to the Raspberry Pi
    client.connect(hostname, port=port, username=username, password=password)
    
    # Write the Python code to a temporary file on the Raspberry Pi
    with open("remote_script.py", "w") as f:
        f.write(python_code)
    
    # Execute the Python script on the Raspberry Pi
    stdin, stdout, stderr = client.exec_command("python3 remote_script.py")
    
    # Read the output of the executed command
    output = stdout.read().decode()
    error = stderr.read().decode()

    # Print the output and errors if any
    if output:
        print("Output:\n", output)
    if error:
        print("Error:\n", error)

finally:
    # Clean up: remove the temporary script
    client.exec_command("rm remote_script.py")
    
    # Close the SSH connection
    client.close()
