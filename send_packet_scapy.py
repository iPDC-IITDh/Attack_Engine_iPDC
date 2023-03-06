from scapy.all import *

# create IP header
ip = IP(src="192.168.0.1", dst="10.196.100.64")

# create UDP header
udp = UDP(sport=5000, dport=5001)

# create packet payload
payload = "Hello, UDP!"

# combine headers and payload into a packet
packet = ip/udp/payload

# send packet
send(packet, count=10)
