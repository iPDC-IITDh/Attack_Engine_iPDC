import socket

# create UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# bind socket to port
sock.bind(('10.196.100.64', 5001))

# receive data
while True:
    data, address = sock.recvfrom(1024)
    print(f"Received data from {address}: {data}")
